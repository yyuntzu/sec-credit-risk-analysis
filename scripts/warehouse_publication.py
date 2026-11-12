"""Validation-only publication registry. Production namespaces are not writable.

One atomic immutable batch owns facts, lineage and the final publication receipt.
Published views validate the batch independently; candidate flags stay unchanged.
"""
from collections import Counter
from datetime import datetime,timezone,timedelta
import json
from pathlib import Path
import re
import tempfile

from .loan_review_sources import canonical,digest
from .warehouse_candidate import _require,file_hash,read_candidate,read_acceptance
from .candidate_archive import prepare_archive,content_hash

VERSION='warehouse-publication-v1'
KINDS={'fact','evidence','input_bridge','evidence_bridge','source_evidence_bridge','reconciliation','acceptance',
    'source_receipt','delivery_receipt','release_policy','calculation_receipt'}
IDENTITY=('publication_id','run_id','attempt_id','entity','scope')


def validation_policy(release,package_sha256):
    return dict(kind='validation-publication-policy-v1',policy_id=digest(dict(release=release,package=package_sha256)),
        release_id=release['release_id'],package_sha256=package_sha256,
        **{key:release[key] for key in ('code_hash','formula_version','policy_version','precision_version')},
        deployment='validation',entity_allowlist=['SYNTHETIC-ONLY'],required_outputs=['report.md','report.json','dashboard.html','loan_review.xlsx'],
        authorization='User selected isolated A-J success/rejection/rollback validation, 2026-11-11')


def verify_publication(rows,commit):
    keys=[(row['record_kind'],row['record_id']) for row in rows]
    _require(len(keys)==len(set(keys)),'Duplicate publication records')
    _require(all(all(row[key]==commit[key] for key in IDENTITY) for row in rows),'Publication batch identity differs')
    _require(all(row['payload_sha256']==digest(json.loads(row['payload'])) and canonical(json.loads(row['payload']))==row['payload']
        for row in rows),'Publication payload/hash changed')
    commits=[row for row in rows if row['record_kind']=='commit']
    _require(len(commits)==1 and commits[0]['record_id']=='publication' and json.loads(commits[0]['payload'])==commit,
        'Missing or mixed publication receipt')
    data=[row for row in rows if row['record_kind']!='commit']
    _require(all(row['record_kind'] in KINDS for row in data),'Unknown publication record kind')
    _require(content_hash(data)==commit['content_sha256'] and dict(Counter(row['record_kind'] for row in data))==commit['record_counts'],
        'Publication coverage/content changed')
    _require(commit['format_version']==VERSION and commit['deployment']=='validation' and commit['entity']=='SYNTHETIC-ONLY',
        'Only isolated synthetic publication is authorized')
    _require(set(commit['gates'])=={'source_verified','dbt_tests_passed','financial_accepted','delivery_success','release_authorized'}
        and all(value is True for value in commit['gates'].values()),'Publication gate failed')
    grouped={kind:[json.loads(row['payload']) for row in data if row['record_kind']==kind] for kind in KINDS}
    _require(all(len(grouped[kind])==1 for kind in ('acceptance','source_receipt','delivery_receipt','release_policy','calculation_receipt')),
        'Publication singleton coverage differs')
    receipt=grouped['calculation_receipt'][0]
    _require(receipt['bindings']==commit['bindings'] and digest(receipt)==commit['calculation_receipt_content_sha256'],
        'Publication calculation binding differs')
    acceptance=grouped['acceptance'][0]
    _require(acceptance['substantive_data_ready'] is True and not acceptance['acceptance_blockers']
        and all(acceptance[k]==commit['bindings'][k] for k in ('run_id','entity','scope','source_hash','plan_hash','precision_version')),
        'Publication financial acceptance differs')
    facts={row['fact_id']:row for row in grouped['fact']}
    _require(len(facts)==commit['record_counts'].get('fact',0) and len(facts)>0,'Missing published facts')
    _require(set(acceptance['required_fact_ids'])==set(commit['required_fact_ids'])
        and all(fid in facts and facts[fid]['status'] in ('sourced','calculated') and facts[fid]['value'] is not None
            for fid in commit['required_fact_ids']),'Required published fact unavailable')
    _require(all(all(row[k]==commit['bindings'][k] for k in ('run_id','entity','scope','source_hash','plan_hash','precision_version'))
        for row in grouped['fact']),'Foreign published fact')
    evidence={row['id']:row for row in grouped['evidence']}
    _require(all(row['entity']==commit['entity'] and row['scope']==commit['scope'] for row in evidence.values()),'Foreign published evidence')
    expected_inputs={(fid,pos,parent) for fid,row in facts.items() for pos,parent in enumerate(row.get('input_ids',[]))}
    actual_inputs={(row['output_fact_id'],row['input_position'],row['input_fact_id']) for row in grouped['input_bridge']}
    _require(expected_inputs==actual_inputs and len(actual_inputs)==len(grouped['input_bridge'])
        and all(parent in facts for _,_,parent in expected_inputs),'Published input lineage incomplete')
    for kind,key in (('evidence_bridge','evidence_ids'),('source_evidence_bridge','source_evidence_ids')):
        expected={(fid,eid) for fid,row in facts.items() for eid in row.get(key,[])}
        actual={(row['fact_id'],row['evidence_id']) for row in grouped[kind]}
        _require(expected==actual and len(actual)==len(grouped[kind]) and all(eid in evidence for _,eid in expected),
            'Published evidence lineage incomplete')
    policy=grouped['release_policy'][0]
    for kind,field in (('source_receipt','source_receipt_content_sha256'),('delivery_receipt','delivery_receipt_content_sha256'),
                       ('release_policy','release_policy_content_sha256')):
        _require(digest(grouped[kind][0])==commit[field],'Publication supporting receipt changed')
    _require(policy['deployment']=='validation' and policy['entity_allowlist']==['SYNTHETIC-ONLY']
        and policy['release_id']==commit['release_id'] and policy['package_sha256']==commit['package_sha256']
        and all(policy[k]==commit['bindings'][k] for k in ('code_hash','formula_version','policy_version','precision_version')),
        'Publication release policy differs')
    source=grouped['source_receipt'][0]
    _require((source['source_id'],source['request_hash'],source['entity'],source['scope'])==
        (commit['source_id'],commit['bindings']['request_hash'],commit['entity'],commit['scope']),'Published source differs')
    delivery=grouped['delivery_receipt'][0]
    _require(delivery['run_id']==commit['run_id'] and delivery['archive_attempt_id']==commit['attempt_id'],
        'Published delivery belongs to another calculation')
    recs=grouped['reconciliation']
    expected={(kind,role) for kind in ('balance_sheet_equation','cash_bridge') for role in commit['period_roles']}
    _require({(row['kind'],row['period_role']) for row in recs}==expected and len(recs)==len(expected)
        and all(row['verified'] is True and row['status'] in ('matched','within_precision') for row in recs),
        'Published reconciliation incomplete')


def prepare_publication(calculation,*,calculation_pin,archive_receipt,archive_pin,storage_receipt,source_receipt,selected,
                        control,source_store,archive,storage,policy_record,publication_id):
    _require(re.fullmatch('[a-f0-9]{32}',publication_id) is not None,'Invalid publication identity')
    report,receipt=read_candidate(calculation,expected_receipt_sha256=calculation_pin)
    acceptance=read_acceptance(calculation,receipt)
    if not acceptance['substantive_data_ready']:
        return None,dict(status='blocked',reasons=acceptance['acceptance_blockers'],publication_eligible=False)
    policy=control.store.load(policy_record)
    _require(policy_record['name'].endswith('publication-policies/'+policy['policy_id']+'.json')
        and policy['kind']=='validation-publication-policy-v1','Invalid publication authorization record')
    _require(policy['deployment']=='validation','Production publication is not authorized')
    if report.entity!='SYNTHETIC-ONLY':
        return None,dict(status='blocked',reasons=['Isolated publication policy permits SYNTHETIC-ONLY, not production borrower publication'],publication_eligible=False)
    bound=control.store.load(selected['run_binding']['record'])
    release=control.store.load(bound['release'])
    _require(bound==selected['run_binding']['body'] and bound['run_id']==receipt['bindings']['run_id']
        and selected['execution']['calculation_receipt_sha256']==calculation_pin,'Selected publication run differs')
    _require(selected['package_sha256']==policy['package_sha256']==release['runtime']['package_sha256']
        and release['release_id']==policy['release_id'] and all(policy[k]==receipt['bindings'][k]==release[k]
            for k in ('code_hash','formula_version','policy_version','precision_version')),'Publication release/code differs')
    envelope=source_store.load(source_receipt)
    _require(digest(envelope['bundle'])==receipt['bindings']['source_hash'] and
        digest(envelope['bundle']['request'])==receipt['bindings']['request_hash'],'Published source does not match calculation')
    _require(not envelope['bundle'].get('source_limitations'),'Unresolved source provenance cannot be published')
    for filename,value in (('source_bundle.json',envelope['bundle']),('reconciliation_reviews.json',envelope['reconciliations']),
                           ('commentary_documents.json',envelope['commentary_documents'])):
        _require(json.loads((Path(calculation)/filename).read_text())==value,'C-to-D source envelope changed: '+filename)
    required={fid for table in report.tables for cell in table.cells for fid in cell}
    _require(set(acceptance['required_fact_ids'])==required,'Financial gate omitted required report cells')
    with tempfile.TemporaryDirectory() as temporary:
        archived=Path(temporary)/'calculation';archive.restore(archive_receipt,archived)
        _require(file_hash(archived/'calculation_receipt.json')==calculation_pin,'Archived calculation differs')
        _,records=prepare_archive(archived,receipt_sha256=calculation_pin,attempt_id=archive_receipt['attempt_id'])
        delivery=storage.restore(storage_receipt,Path(temporary)/'delivery')
        _require(delivery['calculation_receipt_sha256']==calculation_pin and delivery['candidate_archive_receipt_sha256']==
            archive_pin and file_hash(Path(temporary)/'delivery/candidate_archive_receipt.json')==archive_pin
            and json.loads((Path(temporary)/'delivery/candidate_archive_receipt.json').read_text())==archive_receipt,
            'Delivery archive/calculation differs')
        _require(set(policy['required_outputs'])<=set(delivery['artifacts']) and delivery['excel_included'] is True,
            'Required publication deliveries incomplete')
    identity=dict(publication_id=publication_id,**{k:receipt['bindings'][k] for k in ('run_id','entity','scope')},attempt_id=archive_receipt['attempt_id'])
    published=[]
    def add(kind,key,value):
        text=canonical(value);published.append(dict(identity,record_kind=kind,record_id=key,payload=text,payload_sha256=digest(value)))
    for row in records:
        if row['record_kind'] in KINDS:add(row['record_kind'],row['record_id'],json.loads(row['payload']))
    for kind,value in (('source_receipt',source_receipt),('delivery_receipt',storage_receipt),('release_policy',policy),('calculation_receipt',receipt)):
        add(kind,'verified',value)
    commit=dict(identity,format_version=VERSION,deployment='validation',bindings=receipt['bindings'],
        report_mode=report.mode.value,
        release_id=policy['release_id'],package_sha256=policy['package_sha256'],source_id=source_receipt['source_id'],
        required_fact_ids=sorted(required),period_roles=[period.role for period in report.periods],
        calculation_receipt_sha256=calculation_pin,calculation_receipt_content_sha256=digest(receipt),
        source_receipt_content_sha256=digest(source_receipt),delivery_receipt_content_sha256=digest(storage_receipt),
        release_policy_content_sha256=digest(policy),content_sha256=content_hash(published),
        record_counts=dict(Counter(row['record_kind'] for row in published)),
        gates=dict(source_verified=True,dbt_tests_passed=True,financial_accepted=True,delivery_success=True,release_authorized=True))
    add('commit','publication',commit);verify_publication(published,commit)
    return published,commit


class BigQueryPublicationStore:
    def __init__(self,project,dataset,*,client=None,source_dataset='sec_review_shadow_source_aj_20261111'):
        from google.cloud import bigquery
        _require(re.fullmatch('[a-z][a-z0-9-]+',project) is not None,'Invalid publication project')
        _require(re.fullmatch('sec_review_shadow_[a-z0-9_]+',dataset) is not None,'Isolated publication dataset required')
        _require(re.fullmatch('sec_review_shadow_[a-z0-9_]+',source_dataset) is not None,'Isolated source dataset required')
        self.source_dataset=source_dataset
        self.project,self.dataset,self.bq=project,dataset,bigquery;self.client=client or bigquery.Client(project=project)
    def ensure(self):
        target=self.bq.Dataset(f'{self.project}.{self.dataset}');target.location='US';target.default_table_expiration_ms=7*86400000
        self.client.create_dataset(target,exists_ok=True)
        _require(self.client.get_dataset(target.reference).location.upper()=='US','Publication location mismatch')
        schema=[self.bq.SchemaField(key,'STRING',mode='REQUIRED') for key in ('entity','scope','report_mode','publication_id')]
        schema.append(self.bq.SchemaField('version','INTEGER',mode='REQUIRED'))
        self.client.create_table(self.bq.Table(f'{self.project}.{self.dataset}.publication_selection',schema=schema),exists_ok=True)
        event_schema=schema+[self.bq.SchemaField(key,'STRING',mode='REQUIRED') for key in ('action','reason','actor')]
        self.client.create_table(self.bq.Table(f'{self.project}.{self.dataset}.publication_selection_events',schema=event_schema),exists_ok=True)
        fields=IDENTITY+('record_kind','record_id','payload','payload_sha256')
        schema=[self.bq.SchemaField(key,'STRING',mode='REQUIRED') for key in fields]
        self.client.create_table(self.bq.Table(f'{self.project}.{self.dataset}.published_batch_'+('0'*32),schema=schema),exists_ok=True)
    def read(self,publication_id):
        _require(re.fullmatch('[a-f0-9]{32}',publication_id) is not None,'Invalid publication ID')
        return [dict(row) for row in self.client.query(
            f'SELECT * FROM `{self.project}.{self.dataset}.published_batch_{publication_id}` ORDER BY record_kind,record_id',location='US').result()]
    def store(self,rows,commit):
        from google.api_core.exceptions import Conflict,NotFound
        verify_publication(rows,commit)
        fields=IDENTITY+('record_kind','record_id','payload','payload_sha256')
        schema=[self.bq.SchemaField(key,'STRING',mode='REQUIRED') for key in fields]
        table=self.bq.Table(f'{self.project}.{self.dataset}.published_batch_{commit["publication_id"]}',schema=schema)
        pin=digest(commit);table.labels=dict(commit_hi=pin[:32],commit_lo=pin[32:]);table.expires=datetime.now(timezone.utc)+timedelta(days=7)
        try:self.client.create_table(table,exists_ok=False)
        except Conflict:
            old=self.client.get_table(table.reference)
            _require(old.labels==table.labels and [(f.name,f.field_type,f.mode) for f in old.schema]==
                [(f.name,f.field_type,f.mode) for f in schema],'Publication ID cannot be overwritten')
            if old.num_rows:verify_publication(self.read(commit['publication_id']),commit);return self.receipt(commit)
        job_id='publish_'+digest(dict(dataset=self.dataset,id=commit['publication_id']))
        try:job=self.client.get_job(job_id,location='US')
        except NotFound:
            try:job=self.client.load_table_from_json(rows,table.reference,job_id=job_id,location='US',
                job_config=self.bq.LoadJobConfig(schema=schema,write_disposition='WRITE_EMPTY',create_disposition='CREATE_NEVER'))
            except Conflict:job=self.client.get_job(job_id,location='US')
        _require((job.destination.project,job.destination.dataset_id,job.destination.table_id)==
            (self.project,self.dataset,table.table_id) and job.write_disposition=='WRITE_EMPTY','Publication job binding differs')
        job.result();verify_publication(self.read(commit['publication_id']),commit);return self.receipt(commit)
    def receipt(self,commit):
        return dict(format_version=VERSION,project=self.project,dataset=self.dataset,table='published_batch_'+commit['publication_id'],
            **{key:commit[key] for key in IDENTITY},commit_sha256=digest(commit),result_sha256=commit['content_sha256'],
            calculation_receipt_sha256=commit['calculation_receipt_sha256'],deployment='validation',published=True)

    def deploy_views(self,output):
        from .review_cloud import ReviewCloud
        return ReviewCloud(self.project,self.dataset,client=self.client).dbt('published_validation',artifact_dir=output,
            variables={'publication_source_dataset':self.source_dataset})

    def current(self,*,entity,scope,report_mode):
        params=[self.bq.ScalarQueryParameter(key,'STRING',value) for key,value in
            (('entity',entity),('scope',scope),('report_mode',report_mode))]
        rows=list(self.client.query(f'SELECT * FROM `{self.project}.{self.dataset}.publication_selection` '
            'WHERE entity=@entity AND scope=@scope AND report_mode=@report_mode',
            job_config=self.bq.QueryJobConfig(query_parameters=params),location='US').result())
        _require(len(rows)<=1,'Duplicate current publication selection')
        return dict(rows[0]) if rows else None

    def select(self,publication_id,*,expected_version,rollback=False,reason='Verified publication commit',actor='workflow-validation'):
        _require(isinstance(reason,str) and reason.strip() and isinstance(actor,str) and actor.strip(),'Selection reason/actor required')
        rows=self.read(publication_id);commits=[json.loads(row['payload']) for row in rows if row['record_kind']=='commit']
        _require(len(commits)==1,'Target publication commit unavailable');commit=commits[0];verify_publication(rows,commit)
        identity={key:commit[key] for key in ('entity','scope','report_mode')}
        current=self.current(**identity)
        if current and current['publication_id']==publication_id and current['version']==int(expected_version)+1:return current
        _require((current['version'] if current else 0)==int(expected_version),'Stale publication selection')
        params=[self.bq.ScalarQueryParameter(key,'STRING',value) for key,value in dict(identity,publication_id=publication_id).items()]
        params.append(self.bq.ScalarQueryParameter('expected','INT64',int(expected_version)))
        params.extend([self.bq.ScalarQueryParameter('rollback','BOOL',rollback),
            self.bq.ScalarQueryParameter('reason','STRING',reason),self.bq.ScalarQueryParameter('actor','STRING',actor)])
        table=f'`{self.project}.{self.dataset}.publication_selection`'
        events=f'`{self.project}.{self.dataset}.publication_selection_events`'
        sql=f'''begin transaction;
        assert (select count(*) from {table} where entity=@entity and scope=@scope and report_mode=@report_mode)<=1 as 'duplicate selection';
        assert coalesce((select version from {table} where entity=@entity and scope=@scope and report_mode=@report_mode),0)=@expected as 'stale selection';
        assert not @rollback or exists(select 1 from {events} where entity=@entity and scope=@scope
            and report_mode=@report_mode and publication_id=@publication_id and version<=@expected) as 'rollback target never selected';
        merge {table} t using (select @entity entity,@scope scope,@report_mode report_mode) s
        on t.entity=s.entity and t.scope=s.scope and t.report_mode=s.report_mode
        when matched then update set publication_id=@publication_id,version=@expected+1
        when not matched then insert(entity,scope,report_mode,publication_id,version)
        values(@entity,@scope,@report_mode,@publication_id,@expected+1);
        insert into {events}(entity,scope,report_mode,publication_id,version,action,reason,actor)
        values(@entity,@scope,@report_mode,@publication_id,@expected+1,if(@rollback,'rollback','select'),@reason,@actor);
        commit transaction;'''
        self.client.query(sql,job_config=self.bq.QueryJobConfig(query_parameters=params),location='US').result()
        selected=self.current(**identity)
        _require(selected['publication_id']==publication_id and selected['version']==int(expected_version)+1,'Publication selection changed concurrently')
        return selected
