"""Content-addressed, create-only BigQuery source envelopes, before calculation."""
from datetime import datetime,timezone,timedelta
import json
import re

from .loan_review_sources import canonical,digest,parse_request
from .warehouse_candidate import _require


def source_envelope(bundle,*,reconciliations=None,commentary_documents=None):
    report,_,_=parse_request(bundle['request'])
    _require((bundle['entity'],bundle['scope'])==(report.entity,report.scope),'Source envelope borrower mismatch')
    return json.loads(canonical(dict(format_version='warehouse-source-v1',bundle=bundle,
        reconciliations=reconciliations,commentary_documents=commentary_documents or [])))


class BigQuerySourceStore:
    def __init__(self,project,dataset,*,client=None):
        from google.cloud import bigquery
        _require(re.fullmatch('[a-z][a-z0-9-]+',project) is not None,'Invalid source project')
        _require(re.fullmatch('sec_review_shadow_[a-z0-9_]+',dataset) is not None,'Isolated source dataset required')
        self.project,self.dataset,self.bq=project,dataset,bigquery
        self.client=client or bigquery.Client(project=project)
        self.fields=('source_id','entity','scope','request_hash','payload_sha256','payload')
    def ensure(self):
        dataset=self.bq.Dataset(f'{self.project}.{self.dataset}');dataset.location='US'
        dataset.default_table_expiration_ms=7*24*60*60*1000
        self.client.create_dataset(dataset,exists_ok=True)
        _require(self.client.get_dataset(dataset.reference).location.upper()=='US','Source location mismatch')
    def _read(self,table):
        _require(re.fullmatch('source_bundle_[a-f0-9]{64}',table) is not None,'Invalid source table')
        return [dict(row) for row in self.client.query(f'SELECT * FROM `{self.project}.{self.dataset}.{table}`',location='US').result()]
    def load(self,receipt):
        _require(receipt['format_version']=='warehouse-source-receipt-v1'
            and (receipt['project'],receipt['dataset'])==(self.project,self.dataset),'Source receipt storage mismatch')
        _require(receipt['table']=='source_bundle_'+receipt['source_id'],'Source table binding mismatch')
        rows=self._read(receipt['table']);_require(len(rows)==1,'Source envelope must have exactly one row')
        row=rows[0]
        _require(all(row[key]==receipt[key] for key in self.fields if key!='payload'),'Source identity/hash mismatch')
        envelope=json.loads(row['payload']);_require(digest(envelope)==row['source_id']==row['payload_sha256'],'Source payload changed')
        _require(canonical(envelope)==row['payload'],'Noncanonical source payload')
        validated=source_envelope(envelope['bundle'],reconciliations=envelope['reconciliations'],
            commentary_documents=envelope['commentary_documents'])
        _require(validated==envelope and digest(envelope['bundle']['request'])==row['request_hash'],'Source request/envelope contract mismatch')
        _require((envelope['bundle']['entity'],envelope['bundle']['scope'])==(row['entity'],row['scope']),'Source borrower changed')
        return envelope
    def store(self,envelope):
        from google.api_core.exceptions import Conflict,NotFound
        source_id=digest(envelope);bundle=envelope['bundle']
        receipt=dict(format_version='warehouse-source-receipt-v1',project=self.project,dataset=self.dataset,
            table='source_bundle_'+source_id,source_id=source_id,entity=bundle['entity'],scope=bundle['scope'],
            request_hash=digest(bundle['request']),payload_sha256=source_id)
        row={key:receipt[key] for key in self.fields if key!='payload'};row['payload']=canonical(envelope)
        schema=[self.bq.SchemaField(key,'STRING',mode='REQUIRED') for key in self.fields]
        table=self.bq.Table(f'{self.project}.{self.dataset}.{receipt["table"]}',schema=schema)
        table.labels=dict(source_hi=source_id[:32],source_lo=source_id[32:])
        table.expires=datetime.now(timezone.utc)+timedelta(days=7)
        try:self.client.create_table(table,exists_ok=False)
        except Conflict:
            old=self.client.get_table(table.reference)
            _require(old.labels==table.labels and [(f.name,f.field_type,f.mode) for f in old.schema]==
                [(f.name,f.field_type,f.mode) for f in schema],'Source table identity/schema changed')
            if old.num_rows:
                _require(self.load(receipt)==envelope,'Existing source content changed');return receipt
        job_id='source_'+digest(dict(dataset=self.dataset,source_id=source_id,load_contract='explicit-schema-v1'))
        try:job=self.client.get_job(job_id,location='US')
        except NotFound:
            try:
                job=self.client.load_table_from_json([row],table.reference,job_id=job_id,location='US',
                    job_config=self.bq.LoadJobConfig(schema=schema,write_disposition='WRITE_EMPTY',create_disposition='CREATE_NEVER'))
            except Conflict:job=self.client.get_job(job_id,location='US')
        _require((job.destination.project,job.destination.dataset_id,job.destination.table_id)==
            (self.project,self.dataset,receipt['table']) and job.write_disposition=='WRITE_EMPTY','Source load job mismatch')
        job.result();_require(self.load(receipt)==envelope,'Source round-trip changed')
        return receipt
