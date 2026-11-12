from collections import Counter
from copy import deepcopy
import json
import unittest
from unittest.mock import patch

from scripts.warehouse_publication import verify_publication,BigQueryPublicationStore,prepare_publication
from scripts.warehouse_source import BigQuerySourceStore,source_envelope
from scripts.loan_review_sources import canonical,digest
from scripts.candidate_archive import content_hash
from test_candidate_archive import FakeClient
from test_dbt_shadow import rich_bundle


class SnapshotClient(FakeClient):
    def get_table(self,key):return super().get_table(str(key))
    def load_table_from_json(self,rows,reference,**kwargs):
        assert kwargs['job_config'].schema and all(field.mode=='REQUIRED' for field in kwargs['job_config'].schema)
        return super().load_table_from_json(rows,str(reference),**kwargs)


def batch():
    identity=dict(publication_id='a'*32,run_id='b'*32,attempt_id='c'*32,entity='SYNTHETIC-ONLY',scope='entity-wide')
    bindings={k:identity[k] for k in ('run_id','entity','scope')}
    bindings.update({key:key+'-pin' for key in ('source_hash','request_hash','plan_hash','code_hash','formula_version','policy_version','precision_version')})
    policy=dict(deployment='validation',entity_allowlist=['SYNTHETIC-ONLY'],release_id='d'*32,package_sha256='1'*64,
        **{k:bindings[k] for k in ('code_hash','formula_version','policy_version','precision_version')})
    acceptance=dict(substantive_data_ready=True,acceptance_blockers=[],required_fact_ids=['revenue:fy_t'],
        **{k:bindings[k] for k in ('run_id','entity','scope','source_hash','plan_hash','precision_version')})
    values=[('fact','revenue:fy_t',dict(fact_id='revenue:fy_t',status='sourced',value='1',**bindings)),
        ('acceptance','financial',acceptance),('calculation_receipt','verified',dict(bindings=bindings)),
        ('release_policy','verified',policy),('source_receipt','verified',dict(source_id='2'*64,
            request_hash=bindings['request_hash'],entity=identity['entity'],scope=identity['scope'])),
        ('delivery_receipt','verified',dict(run_id=identity['run_id'],archive_attempt_id=identity['attempt_id']))]
    roles=['a','b','c','d']
    for role in roles:
        for kind in ('balance_sheet_equation','cash_bridge'):
            values.append(('reconciliation',kind+':'+role,dict(kind=kind,period_role=role,verified=True,status='matched')))
    rows=[dict(identity,record_kind=kind,record_id=key,payload=canonical(value),payload_sha256=digest(value)) for kind,key,value in values]
    commit=dict(identity,format_version='warehouse-publication-v1',deployment='validation',bindings=bindings,report_mode='quarterly',
        release_id=policy['release_id'],package_sha256=policy['package_sha256'],source_id='2'*64,period_roles=roles,
        required_fact_ids=acceptance['required_fact_ids'],calculation_receipt_sha256='3'*64,
        gates=dict(source_verified=True,dbt_tests_passed=True,financial_accepted=True,delivery_success=True,release_authorized=True))
    return seal(rows,commit)


def seal(rows,commit):
    rows=[deepcopy(row) for row in rows if row['record_kind']!='commit'];commit=deepcopy(commit)
    for row in rows:
        value=json.loads(row['payload']);row['payload']=canonical(value);row['payload_sha256']=digest(value)
    for kind,field in (('calculation_receipt','calculation_receipt_content_sha256'),('source_receipt','source_receipt_content_sha256'),
        ('delivery_receipt','delivery_receipt_content_sha256'),('release_policy','release_policy_content_sha256')):
        match=next((row for row in rows if row['record_kind']==kind),None)
        if match:commit[field]=match['payload_sha256']
    commit.update(content_sha256=content_hash(rows),record_counts=dict(Counter(row['record_kind'] for row in rows)))
    rows.append(dict({k:commit[k] for k in ('publication_id','run_id','attempt_id','entity','scope')},record_kind='commit',
        record_id='publication',payload=canonical(commit),payload_sha256=digest(commit)))
    return rows,commit


class PublicationTests(unittest.TestCase):
    def test_complete_batch_is_atomic_idempotent_and_readable_without_jobs(self):
        rows,commit=batch();client=SnapshotClient();store=BigQueryPublicationStore('test-project','sec_review_shadow_publication',client=client)
        result=store.store(rows,commit);client.jobs.clear()
        self.assertEqual(store.store(rows,commit),result);self.assertEqual(client.loads,1)
        self.assertTrue(result['published']);self.assertEqual(result['deployment'],'validation')
        altered=deepcopy(rows);altered[0]['payload']='{}'
        client.rows[f'test-project.sec_review_shadow_publication.{result["table"]}']=altered
        with self.assertRaises(ValueError):store.store(rows,commit)

    def test_hashes_do_not_waive_bad_financial_or_delivery_gates(self):
        rows,commit=batch()
        for gate in commit['gates']:
            altered=deepcopy(commit);altered['gates'][gate]=False
            bad_rows,bad=seal(rows,altered)
            with self.assertRaises(ValueError):verify_publication(bad_rows,bad)
        for kind,field,value in (('acceptance','substantive_data_ready',False),('fact','value',None),
            ('fact','entity','FOREIGN'),('fact','input_ids',['missing-parent']),('fact','evidence_ids',['missing-source']),
            ('release_policy','package_sha256','wrong'),('delivery_receipt','run_id','f'*32)):
            changed=deepcopy(rows);row=next(r for r in changed if r['record_kind']==kind)
            body=json.loads(row['payload']);body[field]=value;row['payload']=canonical(body)
            bad_rows,bad=seal(changed,commit)
            with self.assertRaises(ValueError):verify_publication(bad_rows,bad)

    def test_missing_duplicate_or_cross_batch_records_never_publish(self):
        rows,commit=batch()
        for changed in (rows[:-1],rows+[rows[0]],rows[1:],[dict(rows[0],attempt_id='f'*32)]+rows[1:]):
            with self.assertRaises(ValueError):verify_publication(changed,commit)
        without=[r for r in rows if r['record_kind']!='fact'];bad_rows,bad=seal(without,commit)
        with self.assertRaises(ValueError):verify_publication(bad_rows,bad)

    def test_draft_stops_before_external_publication_policy_or_storage(self):
        with patch('scripts.warehouse_publication.read_candidate',return_value=(object(),{})), \
             patch('scripts.warehouse_publication.read_acceptance',return_value=dict(substantive_data_ready=False,acceptance_blockers=['missing'])):
            records,state=prepare_publication('/unused',calculation_pin='pin',archive_receipt={},archive_pin='pin',storage_receipt={},
                source_receipt={},selected={},control=None,source_store=None,archive=None,storage=None,policy_record={},publication_id='a'*32)
        self.assertIsNone(records);self.assertEqual(state['status'],'blocked')

    def test_source_store_fixed_content_retries_without_overwriting(self):
        client=SnapshotClient();store=BigQuerySourceStore('test-project','sec_review_shadow_sources',client=client)
        envelope=source_envelope(rich_bundle());receipt=store.store(envelope);client.jobs.clear()
        self.assertEqual(store.store(envelope),receipt);self.assertEqual(client.loads,1)
        other=deepcopy(envelope);other['bundle']['request']['as_of']='2026-10-21'
        second=store.store(other);self.assertNotEqual(second['source_id'],receipt['source_id'])
        self.assertEqual(store.load(receipt),envelope)

    def test_production_namespace_and_foreign_deployment_are_rejected(self):
        with self.assertRaises(ValueError):BigQueryPublicationStore('test-project','production',client=object())
        rows,commit=batch();commit['deployment']='production';rows,commit=seal(rows,commit)
        with self.assertRaises(ValueError):verify_publication(rows,commit)
