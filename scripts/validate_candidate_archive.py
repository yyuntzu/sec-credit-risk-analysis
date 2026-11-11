"""Live negative probes confined to a fresh synthetic-only archive dataset.

Never mutates a valid snapshot. Intentionally invalid tables are written only in
sec_review_shadow_archive_probe_* to exercise SQL and reader rejection paths.
"""
from copy import deepcopy
from datetime import datetime,timezone
import argparse
import json
from pathlib import Path
import re
import uuid
from unittest.mock import patch

from .candidate_archive import ShadowCandidateArchive,VERSION,FIELDS,prepare_archive,sha
from .loan_review_sources import canonical
from .warehouse_candidate import _require
from .review_cloud import ReviewCloud


def validate_archive_rejections(directory,output_dir,*,project,dataset,receipt_sha256):
    _require(re.fullmatch('sec_review_shadow_archive_probe_[a-z0-9_]+',dataset) is not None,
             'Probe requires a fresh dedicated synthetic namespace')
    output = Path(output_dir);output.mkdir(parents=True,exist_ok=False)
    archive = ShadowCandidateArchive(project,dataset)
    probe = dict(status='preparing',project=project,dataset=dataset,cases=[],precision_approved=False,publication_eligible=False)
    try:
        # Reject a real borrower and bad source pin before creating a cloud dataset.
        first,_ = prepare_archive(directory,receipt_sha256=receipt_sha256,attempt_id=uuid.uuid4().hex)
        _require(first['entity']=='SYNTHETIC-ONLY','Archive corruption probes require synthetic data')
        target = archive.bq.Dataset(f'{project}.{dataset}')
        target.location = archive.location;target.default_table_expiration_ms=7*24*60*60*1000
        archive.client.create_dataset(target,exists_ok=False)
        for defect in ('payload_hash','content_hash','missing_commit','foreign_identity'):
            attempt = uuid.uuid4().hex
            commit,records = prepare_archive(directory,receipt_sha256=receipt_sha256,attempt_id=attempt)
            rows = deepcopy(records)
            fact = next(r for r in rows if r['record_kind']=='fact' and json.loads(r['payload'])['metric']=='revenue')
            if defect in ('payload_hash','content_hash'):
                fact['payload']=canonical(dict(json.loads(fact['payload']),value='999'))
                if defect=='content_hash':fact['payload_sha256']=sha(fact['payload'])
            elif defect=='missing_commit':rows=[r for r in rows if r['record_kind']!='commit']
            else:fact['entity']='FOREIGN-SYNTHETIC'
            table_name='review_candidate_'+attempt
            reference=f'{project}.{dataset}.{table_name}'
            schema=[archive.bq.SchemaField(k,'STRING',mode='REQUIRED') for k in FIELDS]+[archive.bq.SchemaField('created_at','TIMESTAMP',mode='REQUIRED')]
            table=archive.bq.Table(reference,schema=schema)
            table.labels={'synthetic_failure_probe':defect}
            archive.client.create_table(table,exists_ok=False)
            job=archive.client.load_table_from_json([dict(r,created_at=datetime.now(timezone.utc).isoformat()) for r in rows],
                reference,job_id='archive_negative_probe_'+uuid.uuid4().hex,location=archive.location,
                job_config=archive.bq.LoadJobConfig(schema=schema,write_disposition='WRITE_EMPTY',create_disposition='CREATE_NEVER'))
            job.result()
            expected=dict(format_version=VERSION,project=project,dataset=dataset,table=table_name,
                **{k:commit[k] for k in ('run_id','attempt_id','entity','scope','content_sha256','calculation_receipt_sha256','archive_code_hash')},
                commit_sha256=sha(canonical(commit)),precision_approved=False,publication_eligible=False)
            try:
                with (patch('scripts.loan_review_pipeline.report_from_source_bundle',side_effect=AssertionError('Python fallback')),
                      patch('scripts.loan_review_contract.approved_formula_value',side_effect=AssertionError('Python fallback'))):
                    archive.restore(expected,output/(defect+'_restore'))
            except ValueError as error:
                probe['cases'].append(dict(defect=defect,attempt_id=attempt,load_job_id=job.job_id,reader_rejected=True,error=str(error)))
            else:raise AssertionError('Corrupt archive was accepted: '+defect)
            _require(not (output/(defect+'_restore')).exists(),'Corrupt source was extracted before verification')
        try:
            ReviewCloud(project,dataset,client=archive.client).dbt('archive',artifact_dir=output/'dbt')
        except RuntimeError as error:
            _require(str(error).startswith('dbt archive/test failed:'),'Probe failed before the intended integrity test: '+str(error))
            probe['dbt_test_rejected']=True;probe['dbt_error']=str(error)
        else:raise AssertionError('dbt accepted corrupt archive tables')
        diagnostics=[dict(r) for r in archive.client.query(f'SELECT * FROM `{project}.{dataset}.int_review_candidate_checks`',location=archive.location).result()]
        _require({r['table_attempt_id'] for r in diagnostics}=={r['attempt_id'] for r in probe['cases']},'Incomplete SQL probe coverage')
        _require(all(r['archive_integrity_passed'] is False and r['publication_eligible'] is False for r in diagnostics),
                 'Corrupt snapshot passed SQL archive integrity')
        probe.update(status='passed',diagnostics=diagnostics)
    except Exception as error:
        probe.update(status='failed',error=str(error));raise
    finally:
        (output/'probe_manifest.json').write_text(json.dumps(probe,ensure_ascii=False,default=str,indent=2),encoding='utf-8')
    return probe


def main(argv=None):
    parser=argparse.ArgumentParser(description='Synthetic-only BigQuery archive rejection matrix')
    parser.add_argument('--shadow-dir',required=True);parser.add_argument('--receipt-sha256',required=True)
    parser.add_argument('--project',required=True);parser.add_argument('--dataset',required=True);parser.add_argument('--output-dir',required=True)
    args=parser.parse_args(argv)
    print(json.dumps(validate_archive_rejections(args.shadow_dir,args.output_dir,project=args.project,dataset=args.dataset,
        receipt_sha256=args.receipt_sha256),ensure_ascii=False,default=str,indent=2))


if __name__=='__main__':main()
