"""Immutable-by-contract candidate snapshots in isolated BigQuery namespaces.

One WRITE_EMPTY load atomically stores artifacts, analytical rows and a commit.
Fixed attempt/job identities plus content bindings reject conflicting retries.
This is not WORM storage or an IAM boundary; owners can still modify tables.
Every reader rechecks a caller-pinned receipt. No publication API is provided.
"""
from collections import Counter
from dataclasses import asdict
from datetime import datetime, timedelta, timezone
from decimal import Decimal
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import uuid

from .loan_review_sources import canonical
from .warehouse_candidate import ARTIFACTS,read_candidate, file_hash, _read, _require

VERSION = 'candidate-archive-v1'
KINDS = {'artifact','fact','evidence','reconciliation','acceptance','commentary','input_bridge','evidence_bridge','source_evidence_bridge'}
FIELDS = ('run_id','attempt_id','entity','scope','record_kind','record_id','payload','payload_sha256')


def sha(value):
    return hashlib.sha256(value.encode('utf-8')).hexdigest()


def content_hash(records):
    return sha('\n'.join(f"{row['record_kind']}:{row['record_id']}:{row['payload_sha256']}"
                         for row in sorted(records,key=lambda r:(r['record_kind'],r['record_id']))))


def archive_code_hash():
    root = Path(__file__).resolve().parents[1]
    paths = [Path(__file__),root/'scripts/review_cloud.py',root/'references/dbt/tests/review_candidate_integrity.sql']
    paths += sorted((root/'references/dbt/models/warehouse_candidate').glob('*'))
    return sha(canonical({str(path.relative_to(root)):file_hash(path) for path in paths if path.is_file()}))


def prepare_archive(directory, *, receipt_sha256, attempt_id):
    _require(isinstance(attempt_id,str) and re.fullmatch('[a-f0-9]{32}',attempt_id),'Invalid archive attempt ID')
    directory = Path(directory)
    report,receipt = read_candidate(directory,expected_receipt_sha256=receipt_sha256)
    bindings = receipt['bindings']
    records = []
    def add(kind,key,payload):
        text = payload if kind=='artifact' else canonical(payload)
        records.append(dict(run_id=bindings['run_id'],attempt_id=attempt_id,entity=bindings['entity'],scope=bindings['scope'],
            record_kind=kind,record_id=key,payload=text,payload_sha256=sha(text)))
    for name in sorted(set(receipt['artifacts'])|{'calculation_receipt.json'}):
        add('artifact',name,(directory/name).read_bytes().decode('utf-8'))
    for row in _read(directory/'warehouse_facts.json'):
        fid = row['fact_id']
        add('fact',fid,row)
        for position,iid in enumerate(row['input_ids']):
            add('input_bridge',canonical([fid,position]),dict(output_fact_id=fid,input_position=position,input_fact_id=iid))
        for kind,ids in (('evidence_bridge',row['evidence_ids']),('source_evidence_bridge',row.get('source_evidence_ids',[]))):
            for eid in ids:
                _require(eid in report.evidence,'Archive lineage references unknown evidence')
                add(kind,canonical([fid,eid]),dict(fact_id=fid,evidence_id=eid))
    for row in _read(directory/'warehouse_reconciliations.json'):
        add('reconciliation',row['kind']+':'+row['period_role'],row)
    for row in _read(directory/'warehouse_acceptance.json'):
        add('acceptance','financial',row)
    for eid,evidence in report.evidence.items():
        add('evidence',eid,asdict(evidence))
    if 'warehouse_commentary.json' in receipt['artifacts']:
        for row in _read(directory/'warehouse_commentary.json'):
            add('commentary',canonical([row['record_kind'],row['record_id']]),row)
    keys = [(r['record_kind'],r['record_id']) for r in records]
    _require(len(keys)==len(set(keys)),'Duplicate archive record identity')
    hashes = {r['record_id']:r['payload_sha256'] for r in records if r['record_kind']=='artifact'}
    _require(hashes.pop('calculation_receipt.json')==receipt_sha256 and hashes==receipt['artifacts'],'Archive artifact binding mismatch')
    commit = dict(format_version=VERSION,archive_code_hash=archive_code_hash(),bindings=bindings,run_id=bindings['run_id'],attempt_id=attempt_id,
        entity=bindings['entity'],scope=bindings['scope'],content_sha256=content_hash(records),
        calculation_receipt_sha256=receipt_sha256,record_counts=dict(Counter(r['record_kind'] for r in records)),
        artifact_hashes={r['record_id']:r['payload_sha256'] for r in records if r['record_kind']=='artifact'},
        precision_approved=False,publication_eligible=False)
    add('commit','calculation',commit)
    return commit,records


def verify_snapshot(rows, *, expected):
    """Verify all physical table rows, including foreign/duplicate attempts."""
    rows = [dict(row) for row in rows]
    keys = [(r['record_kind'],r['record_id']) for r in rows]
    _require(len(keys)==len(set(keys)),'Duplicate archive record')
    _require(all(all(row.get(k)==expected[k] for k in ('run_id','attempt_id','entity','scope')) for row in rows),
             'Archive attempt identity mismatch')
    _require(all(row.get('payload_sha256')==sha(row['payload']) for row in rows),'Archive payload hash mismatch')
    commits = [row for row in rows if row['record_kind']=='commit']
    _require(len(commits)==1 and commits[0]['record_id']=='calculation','Missing or duplicate archive commit')
    commit = json.loads(commits[0]['payload'])
    _require(sha(commits[0]['payload'])==(expected.get('commit_sha256') or sha(canonical(expected))),
             'Archive commit checksum mismatch')
    _require(commit.get('format_version')==VERSION,'Unsupported archive format')
    _require(all(commit.get(k)==expected[k] for k in ('run_id','attempt_id','entity','scope','content_sha256','calculation_receipt_sha256','archive_code_hash')),
             'Archive commit binding mismatch')
    _require(commit.get('publication_eligible') is False and commit.get('precision_approved') is False,
             'Candidate archive cannot grant publication')
    data = [row for row in rows if row['record_kind']!='commit']
    _require(all(row['record_kind'] in KINDS for row in data),'Unknown archive record kind')
    _require(content_hash(data)==expected['content_sha256'],'Archive content checksum mismatch')
    _require(dict(Counter(row['record_kind'] for row in data))==commit['record_counts'],'Archive record coverage mismatch')
    artifacts = {row['record_id']:row['payload'] for row in data if row['record_kind']=='artifact'}
    _require({key:sha(value) for key,value in artifacts.items()}==commit['artifact_hashes'],'Archive artifact coverage mismatch')
    receipt = json.loads(artifacts['calculation_receipt.json'])
    _require(sha(artifacts['calculation_receipt.json'])==expected['calculation_receipt_sha256'] and
             receipt['bindings']==commit['bindings'],'Archived calculation receipt mismatch')
    _require(set(artifacts)==set(receipt['artifacts'])|{'calculation_receipt.json'} and
             all(sha(artifacts[name])==fingerprint for name,fingerprint in receipt['artifacts'].items()),
             'Archived calculation artifacts changed')
    # Analytical records must be exactly the same projections as the frozen files.
    def projection(kind,filename,key):
        expected_rows = {key(row):canonical(row) for row in json.loads(artifacts[filename])}
        found = {row['record_id']:row['payload'] for row in data if row['record_kind']==kind}
        _require(found==expected_rows,'Archive analytical projection mismatch: '+kind)
    projection('fact','warehouse_facts.json',lambda r:r['fact_id'])
    projection('reconciliation','warehouse_reconciliations.json',lambda r:r['kind']+':'+r['period_role'])
    projection('acceptance','warehouse_acceptance.json',lambda r:'financial')
    if 'warehouse_commentary.json' in artifacts:
        projection('commentary','warehouse_commentary.json',lambda r:canonical([r['record_kind'],r['record_id']]))
    return commit,artifacts


class ShadowCandidateArchive:
    """Only isolated datasets are writable until the release is approved."""
    def __init__(self,project,dataset,*,client=None):
        _require(re.fullmatch('[A-Za-z0-9_-]+',project) is not None,'Invalid archive project')
        _require(re.fullmatch('sec_review_shadow_[a-z0-9_]+',dataset) is not None,'Archive currently requires an isolated shadow dataset')
        from google.cloud import bigquery
        self.project,self.dataset,self.bq = project,dataset,bigquery
        self.client = client or bigquery.Client(project=project)
        self.location = os.environ.get('BQ_LOCATION','US')

    def ensure_dataset(self):
        target = self.bq.Dataset(f'{self.project}.{self.dataset}')
        target.location = self.location
        target.default_table_expiration_ms = 7*24*60*60*1000
        self.client.create_dataset(target,exists_ok=True)
        actual = self.client.get_dataset(target.reference)
        _require(actual.location.upper()==self.location.upper(),'Archive dataset location mismatch')

    def _read(self,table):
        _require(re.fullmatch('review_candidate_[a-f0-9]{32}',table) is not None,'Invalid archive table')
        return [dict(row) for row in self.client.query(
            f'SELECT * FROM `{self.project}.{self.dataset}.{table}`',location=self.location).result()]

    def _claim_run(self,commit):
        """Atomically reserve the run's source/policy identity before any attempt."""
        from google.api_core.exceptions import Conflict
        payload = canonical(commit['bindings'])
        fingerprint = sha(payload)
        reference = f"{self.project}.{self.dataset}.review_run_binding_{commit['run_id']}"
        table = self.bq.Table(reference,schema=[self.bq.SchemaField('reserved','STRING')])
        table.labels = dict(binding_hi=fingerprint[:32],binding_lo=fingerprint[32:])
        table.description = payload
        try:
            self.client.create_table(table,exists_ok=False)
        except Conflict:
            current = self.client.get_table(reference)
            _require(current.description==payload and all((current.labels or {}).get(k)==v for k,v in table.labels.items()),
                     'Run is already bound to different source, review or calculation versions; use a new run')

    def store(self,commit,records):
        from google.api_core.exceptions import Conflict,NotFound
        verify_snapshot(records,expected=commit)
        self._claim_run(commit)
        table_id = 'review_candidate_'+commit['attempt_id']
        reference = f'{self.project}.{self.dataset}.{table_id}'
        receipt = dict(format_version=VERSION,project=self.project,dataset=self.dataset,table=table_id,
            **{key:commit[key] for key in ('run_id','attempt_id','entity','scope','content_sha256','calculation_receipt_sha256')},
            commit_sha256=sha(canonical(commit)),archive_code_hash=commit['archive_code_hash'],
            load_job_id='review_archive_'+commit['run_id']+'_'+commit['attempt_id'],precision_approved=False,publication_eligible=False)
        labels = dict(archive_format='v1',content_hi=commit['content_sha256'][:32],content_lo=commit['content_sha256'][32:],
            commit_hi=receipt['commit_sha256'][:32],commit_lo=receipt['commit_sha256'][32:])
        schema = [self.bq.SchemaField(name,'STRING',mode='REQUIRED') for name in FIELDS]
        schema.append(self.bq.SchemaField('created_at','TIMESTAMP',mode='REQUIRED'))
        table = self.bq.Table(reference,schema=schema)
        table.labels = labels
        table.expires = datetime.now(timezone.utc)+timedelta(days=7)
        try:
            self.client.create_table(table,exists_ok=False)
        except Conflict:
            existing = self.client.get_table(reference)
            _require(all((existing.labels or {}).get(k)==v for k,v in labels.items()),'Immutable archive attempt has different content')
            _require([(f.name,f.field_type,f.mode) for f in existing.schema]==[(f.name,f.field_type,f.mode) for f in schema],
                     'Archive table schema mismatch')
            if existing.num_rows:
                # Historical retry must not depend on retained BigQuery job metadata.
                verify_snapshot(self._read(table_id),expected=commit)
                return receipt
        job_id = 'review_archive_'+commit['run_id']+'_'+commit['attempt_id']
        try:
            job = self.client.get_job(job_id,location=self.location)
        except NotFound:
            rows = [dict(row,created_at=datetime.now(timezone.utc).isoformat()) for row in records]
            try:
                job = self.client.load_table_from_json(rows,reference,job_id=job_id,location=self.location,
                    job_config=self.bq.LoadJobConfig(schema=schema,write_disposition='WRITE_EMPTY',create_disposition='CREATE_NEVER',labels=labels))
            except Conflict:
                job = self.client.get_job(job_id,location=self.location)
        _require(job.destination.project==self.project and job.destination.dataset_id==self.dataset and
                 job.destination.table_id==table_id and job.write_disposition=='WRITE_EMPTY' and
                 all((job.labels or {}).get(k)==v for k,v in labels.items()),'Archive job identity/content mismatch')
        job.result()
        verify_snapshot(self._read(table_id),expected=commit)
        return receipt

    def _receipt_context(self,receipt):
        _require(receipt['project']==self.project and receipt['dataset']==self.dataset,'Archive target mismatch')
        _require(receipt['format_version']==VERSION and receipt['publication_eligible'] is False and receipt['precision_approved'] is False,
                 'Unsupported or ineligible candidate archive receipt')
        _require(receipt['table']=='review_candidate_'+receipt['attempt_id'],'Archive table/attempt mismatch')

    def read_facts(self,receipt):
        """Read typed warehouse projections only when every field matches the pin."""
        self._receipt_context(receipt)
        commit,artifacts = verify_snapshot(self._read(receipt['table']),expected=receipt)
        expected = {row['fact_id']:row for row in json.loads(artifacts['warehouse_facts.json'])}
        config = self.bq.QueryJobConfig(query_parameters=[self.bq.ScalarQueryParameter(key,'STRING',receipt[key])
            for key in ('run_id','attempt_id','entity','scope')])
        rows = [dict(row) for row in self.client.query(
            f'SELECT * FROM `{self.project}.{self.dataset}.fct_review_candidate_facts` '
            'WHERE run_id=@run_id AND attempt_id=@attempt_id AND entity=@entity AND scope=@scope',
            location=self.location,job_config=config).result()]
        _require(len(rows)==len(expected) and {r['fact_id'] for r in rows}==set(expected),'Typed archive Fact coverage mismatch')
        for row in rows:
            _require(all(row.get(key)==receipt[key] for key in ('run_id','attempt_id','entity','scope','content_sha256','calculation_receipt_sha256')),
                     'Typed archive Fact identity mismatch')
            _require(row.get('archive_integrity_passed') is True and row.get('publication_eligible') is False,
                     'Typed archive Fact is unverified or publication-enabled')
            _require(all(row.get(key)==commit['bindings'][key] for key in ('source_hash','plan_hash','precision_version')),
                     'Typed archive Fact source/version mismatch')
            fact = expected[row['fact_id']]
            _require(row.get('frozen_fact_payload')==canonical(fact),'Typed archive frozen payload mismatch')
            for key in ('metric','period_role','status','unit','currency','value','original_value','original_scale',
                        'definition','basis','start','end','period_kind','formula_id','formula_version','input_ids','evidence_ids','source_evidence_ids'):
                _require(row.get(key)==fact.get(key),'Typed archive projection changed: '+key)
            if fact['unit']!='text' and fact['value'] is not None:
                _require(isinstance(row['value_numeric'],Decimal) and row['value_numeric']==Decimal(fact['value']),
                         'Typed archive decimal changed')
            else:
                _require(row['value_numeric'] is None,'Unavailable/text archive Fact became numeric')
        return rows

    def restore(self,receipt,directory):
        self._receipt_context(receipt)
        rows = self._read(receipt['table'])
        _,artifacts = verify_snapshot(rows,expected=receipt)
        # Receipt was created by read_candidate; still reject traversal explicitly.
        allowed = set(ARTIFACTS)|{'calculation_receipt.json'}
        _require(set(artifacts)<=allowed,'Unsafe archived artifact name')
        directory = Path(directory);directory.mkdir(parents=True,exist_ok=False)
        for name,content in artifacts.items():
            path = directory/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(content.encode('utf-8'))
        report,_ = read_candidate(directory,expected_receipt_sha256=receipt['calculation_receipt_sha256'])
        actual_evidence = {row['record_id']:row['payload'] for row in rows if row['record_kind']=='evidence'}
        _require(actual_evidence=={eid:canonical(asdict(item)) for eid,item in report.evidence.items()},'Archive evidence registry mismatch')
        return report


def archive_calculation(directory,output_dir,*,project,dataset,receipt_sha256,attempt_id=None,archive=None,build_models=False):
    from .review_workflow import write_json
    output = Path(output_dir);output.mkdir(parents=True,exist_ok=False)
    attempt_id = attempt_id or uuid.uuid4().hex
    metadata = dict(status='preparing',attempt_id=attempt_id,project=project,dataset=dataset,
        calculation_receipt_sha256=receipt_sha256,precision_approved=False,publication_eligible=False)
    write_json(output/'archive_manifest.json',metadata)
    try:
        commit,records = prepare_archive(directory,receipt_sha256=receipt_sha256,attempt_id=attempt_id)
        metadata.update(commit,status='prepared',project=project,dataset=dataset)
        (output/'archive_records.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
        write_json(output/'archive_manifest.json',metadata)
        archive = archive or ShadowCandidateArchive(project,dataset)
        archive.ensure_dataset()
        receipt = archive.store(commit,records)
        write_json(output/'archive_receipt.json',receipt)
        metadata.update(status='stored',archive_receipt_sha256=file_hash(output/'archive_receipt.json'))
        write_json(output/'archive_manifest.json',metadata)
        if build_models:
            from .review_cloud import ReviewCloud
            metadata['archive_dbt'] = ReviewCloud(project,dataset,client=archive.client).dbt('archive',artifact_dir=output/'dbt')
            metadata['status'] = 'verified'
        _require(archive_code_hash()==commit['archive_code_hash'],
                 'Archive code changed during storage/validation; use a new attempt')
    except Exception as error:
        metadata.update(status='failed',error=str(error))
        raise
    finally:
        write_json(output/'archive_manifest.json',metadata)
    return metadata


def main(argv=None):
    parser = argparse.ArgumentParser(description='Isolated candidate archive; never publishes')
    commands = parser.add_subparsers(dest='command',required=True)
    store = commands.add_parser('store')
    store.add_argument('--shadow-dir',required=True);store.add_argument('--receipt-sha256',required=True)
    store.add_argument('--project',required=True);store.add_argument('--dataset',required=True)
    store.add_argument('--attempt-id');store.add_argument('--output-dir',required=True)
    store.add_argument('--build-models',action='store_true',help='Build/test read-only candidate projections in the isolated archive dataset')
    for command in ('restore','facts'):
        reader = commands.add_parser(command)
        reader.add_argument('--archive-receipt',required=True);reader.add_argument('--archive-receipt-sha256',required=True)
        reader.add_argument('--output-dir',required=True)
    args = parser.parse_args(argv)
    if args.command=='store':
        result = archive_calculation(args.shadow_dir,args.output_dir,project=args.project,dataset=args.dataset,
            receipt_sha256=args.receipt_sha256,attempt_id=args.attempt_id,build_models=args.build_models)
    else:
        _require(file_hash(args.archive_receipt)==args.archive_receipt_sha256,'Pinned archive receipt hash mismatch')
        receipt = _read(args.archive_receipt)
        archive = ShadowCandidateArchive(receipt['project'],receipt['dataset'])
        if args.command=='restore':
            report = archive.restore(receipt,args.output_dir)
            result = dict(status='restored',entity=report.entity,facts=len(report.facts),precision_approved=False,publication_eligible=False)
        else:
            rows = archive.read_facts(receipt)
            output = Path(args.output_dir);output.mkdir(parents=True,exist_ok=False)
            (output/'candidate_facts.json').write_text(json.dumps(rows,ensure_ascii=False,default=str,indent=2),encoding='utf-8')
            result = dict(status='read_verified',archive_receipt_sha256=args.archive_receipt_sha256,
                reader_code_hash=file_hash(__file__),facts=len(rows),precision_approved=False,publication_eligible=False)
            (output/'fact_reader_manifest.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
