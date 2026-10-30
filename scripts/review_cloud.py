"""Run-scoped BigQuery storage and explicit dbt stages for formal reviews.

Payload strings preserve Decimal precision, original evidence and contract fields.
No credentials or cloud clients are needed by local mode.
"""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys


class ReviewCloud:
    TABLES = ('raw_review_sources', 'raw_review_results', 'raw_review_runs')

    def __init__(self, project=None, dataset=None, client=None):
        from google.cloud import bigquery
        self.project = project or os.environ.get('GCP_PROJECT_ID', 'focus-heuristic-438521-v4')
        self.dataset = dataset or os.environ.get('BQ_DATASET_ID', 'sec_raw')
        if not re.fullmatch(r'[a-zA-Z0-9_-]+', self.project) or not re.fullmatch(r'[a-zA-Z0-9_]+', self.dataset):
            raise ValueError('Invalid BigQuery project/dataset')
        self.client = client or bigquery.Client(project=self.project)
        self.bq = bigquery

    def ensure(self):
        dataset = self.bq.Dataset(f'{self.project}.{self.dataset}')
        dataset.location = os.environ.get('BQ_LOCATION', 'US')
        self.client.create_dataset(dataset, exists_ok=True)
        schema = [self.bq.SchemaField(k, 'STRING', mode='REQUIRED')
                  for k in ('run_id', 'entity', 'record_kind', 'record_id', 'payload')]
        schema.append(self.bq.SchemaField('created_at', 'TIMESTAMP', mode='REQUIRED'))
        for name in self.TABLES:
            table = self.bq.Table(f'{self.project}.{self.dataset}.{name}', schema=schema)
            table.clustering_fields = ['run_id', 'entity', 'record_kind']
            self.client.create_table(table, exists_ok=True)

    def write(self, table, run_id, entity, records):
        from google.api_core.exceptions import Conflict
        if table not in self.TABLES: raise ValueError('Unsupported review table')
        stamp = datetime.now(timezone.utc).isoformat()
        rows = [dict(run_id=run_id, entity=entity, record_kind=kind, record_id=key,
                     payload=json.dumps(value, default=str, ensure_ascii=False, sort_keys=True), created_at=stamp)
                for kind, key, value in records]
        if not rows: return
        fingerprint = hashlib.sha256(json.dumps([(r['record_kind'], r['record_id'], r['payload']) for r in rows]).encode()).hexdigest()[:24]
        job_id = f'loan_review_{run_id}_{table}_{fingerprint}'
        try:
            job = self.client.load_table_from_json(rows, f'{self.project}.{self.dataset}.{table}',
                job_id=job_id, job_config=self.bq.LoadJobConfig(write_disposition='WRITE_APPEND'))
        except Conflict:
            job = self.client.get_job(job_id, location=os.environ.get('BQ_LOCATION', 'US'))
        job.result()

    def stage_bundle(self, run_id, entity, bundle):
        metadata = {k: v for k, v in bundle.items() if k not in ('inputs', 'evidence')}
        records = [('metadata', 'bundle', metadata)]
        for kind in ('inputs', 'evidence'):
            records.extend((kind, key, value) for key, value in bundle[kind].items())
        self.write('raw_review_sources', run_id, entity, records)
        self.dbt('source')
        result = self.read_bundle(run_id, entity)
        expected = json.loads(json.dumps(bundle, default=str))
        if result != expected: raise ValueError('Cloud source round-trip mismatch')
        return result

    def read_bundle(self, run_id, entity):
        if not re.fullmatch('[a-f0-9]{32}', run_id): raise ValueError('source_run_id must be a 32-character run ID')
        config = self.bq.QueryJobConfig(query_parameters=[self.bq.ScalarQueryParameter('run_id', 'STRING', run_id),
                                                         self.bq.ScalarQueryParameter('entity', 'STRING', entity)])
        rows = self.client.query(f'SELECT record_kind, record_id, payload FROM `{self.project}.{self.dataset}.stg_loan_review_run_sources` WHERE run_id = @run_id AND entity = @entity', job_config=config).result()
        result = {'inputs': {}, 'evidence': {}}
        seen = set()
        for row in rows:
            kind, key = row['record_kind'], row['record_id']
            if (kind, key) in seen: raise ValueError('Duplicate staged source key')
            seen.add((kind, key))
            value = json.loads(row['payload'])
            if kind == 'metadata': result.update(value)
            elif kind in ('inputs', 'evidence'): result[kind][key] = value
            else: raise ValueError('Unknown staged source kind')
        if ('metadata', 'bundle') not in seen: raise ValueError('Cloud source round-trip missing metadata')
        return result

    def publish(self, run_id, entity, payload, acceptance):
        # Revalidate at this boundary as well; direct callers cannot forge PASS.
        try:
            from .review_workflow import restore_report
            from .loan_review_pipeline import acceptance_result
        except ImportError:
            from review_workflow import restore_report
            from loan_review_pipeline import acceptance_result
        report = restore_report(payload)
        verified = acceptance_result(report, acceptance.get('reconciliations', ()), acceptance.get('source_limitations', ()))
        if (entity != report.entity or not verified['substantive_data_ready']
                or acceptance.get('final_report_accepted') is not True
                or acceptance.get('technical_validation_passed') is not True
                or acceptance.get('rendered_validation_passed') is not True):
            raise ValueError('Cloud publication requires independently verified final acceptance')
        records = [('report', 'report', payload), ('acceptance', 'acceptance', acceptance)]
        for fid, fact in payload['facts'].items():
            records.append(('fact', fid, fact))
            for eid in fact['evidence_ids']:
                records.append(('fact_evidence', json.dumps([fid, eid]), {'fact_id': fid, 'evidence_id': eid}))
        records.extend(('evidence', eid, e) for eid, e in payload['evidence'].items())
        self.write('raw_review_results', run_id, entity, records)
        self.dbt('publish')

    def record_run(self, run_id, entity, manifest):
        self.write('raw_review_runs', run_id, entity, [('run', 'manifest', manifest)])

    def dbt(self, stage):
        project = Path(os.environ.get('DBT_PROJECT_DIR', Path(__file__).resolve().parents[1] / 'references/dbt')).resolve()
        selection = {'source': 'stg_loan_review_run_sources', 'legacy_source': 'stg_loan_review_sources', 'publish': 'tag:formal_review_marts'}[stage]
        common = ['--project-dir', str(project), '--profiles-dir', os.environ.get('DBT_PROFILES_DIR', str(project)),
                  '--target', os.environ.get('DBT_TARGET', 'prod')]
        env = {**os.environ, 'GCP_PROJECT_ID': self.project, 'BQ_DATASET_ID': self.dataset}
        executable = os.environ.get('DBT_EXECUTABLE', 'dbt')
        sibling = Path(sys.executable).with_name('dbt')
        if os.environ.get('DBT_PYTHON'):
            prefix = [os.environ['DBT_PYTHON'], executable]
        elif not os.environ.get('DBT_EXECUTABLE') and sibling.is_file():
            # Relocated virtualenv entry scripts can retain an obsolete shebang.
            with sibling.open('rb') as script: header = script.readline(256)
            prefix = [sys.executable, str(sibling)] if header.startswith(b'#!') and b'python' in header else [str(sibling)]
        else:
            prefix = [executable]
        for command in ('run', 'test'):
            completed = subprocess.run([*prefix, '--warn-error', command, '--select', selection, *common], capture_output=True,
                                       text=True, timeout=300, env=env)
            if completed.returncode:
                raise RuntimeError(f'dbt {stage}/{command} failed: {completed.stderr[-1500:]} {completed.stdout[-1500:]}')
