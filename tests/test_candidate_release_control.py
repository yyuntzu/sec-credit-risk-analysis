from copy import deepcopy
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts.candidate_release_control import CandidateReleaseControl
from scripts import candidate_release_control as control_module
from scripts.delivery_archive import sha
from scripts.loan_review_sources import canonical


class MemoryStore:
    def __init__(self):self.live={};self.versions={};self.counter=0;self.fail_cas=False
    def ensure(self,*,create=False):pass
    def save(self,key,body):
        self.counter+=1;data=canonical(body).encode()
        record=dict(name=key,generation=str(self.counter),sha256=sha(data),size=len(data))
        self.live[key]=record;self.versions[key,str(self.counter)]=deepcopy(body)
        return deepcopy(record)
    def load(self,record):
        body=deepcopy(self.versions[record['name'],record['generation']])
        assert sha(canonical(body).encode())==record['sha256']
        return body
    def read(self,key):
        if key not in self.live:return None,None
        record=deepcopy(self.live[key]);return record,self.load(record)
    def create(self,key,body):
        record,existing=self.read(key)
        if existing is not None:
            if existing!=body:raise ValueError('never overwrite')
            return record
        return self.save(key,body)
    def cas(self,key,body,generation):
        current=self.live.get(key,{}).get('generation','0')
        if str(generation)!=current or self.fail_cas:
            self.fail_cas=False;raise ValueError('Concurrent candidate selection changed')
        return self.save(key,body)


def release(rid,code='a'*64):
    return dict(kind='candidate-release-v1',release_id=rid,engine='dbt-bigquery-only',code_hash=code,
        evidence=[dict(mode='annual'),dict(mode='quarterly')],precision_approved=False,publication_eligible=False)


class CandidateReleaseControlTests(unittest.TestCase):
    def setUp(self):
        self.store=MemoryStore();self.control=CandidateReleaseControl(self.store)
        self.a='a'*32;self.b='b'*32;self.c='c'*32
        for rid in (self.a,self.b,self.c):self.control.register(release(rid))
    def select(self,rid,event,generation,rollback=False):
        return self.control.select(rid,event_id=event,reason='synthetic test',actor='test',
            expected_generation=generation,rollback=rollback)
    def bind(self,rid,**changes):
        return self.control.bind_run(rid,**dict(dict(entity='SYNTHETIC-ONLY',scope='entity-wide',
            source_hash='1'*64,request_hash='2'*64),**changes))

    def test_rollback_only_changes_future_runs_and_history_is_fixed(self):
        first,_=self.select(self.a,'1'*32,'0')
        old_record,old=self.bind('4'*32)
        second,_=self.select(self.b,'2'*32,first['generation'])
        _,middle=self.bind('5'*32);self.assertEqual(middle['release_id'],self.b)
        self.select(self.a,'3'*32,second['generation'],rollback=True)
        self.assertEqual(self.bind('4'*32),(old_record,old))
        self.assertEqual(self.bind('5'*32)[1],middle)
        self.assertEqual(self.bind('6'*32)[1]['release_id'],self.a)
        self.assertEqual(self.store.load(old_record),old)

    def test_stale_selection_is_rejected_without_history_mutation(self):
        record,pointer=self.select(self.a,'1'*32,'0')
        with self.assertRaisesRegex(ValueError,'Stale'):
            self.select(self.b,'2'*32,'0')
        self.assertEqual(self.control.current(),(record,pointer))

    def test_captured_selection_survives_pointer_change_but_cannot_rebind_run(self):
        snapshot=self.select(self.a,'1'*32,'0')
        self.select(self.b,'2'*32,snapshot[0]['generation'])
        _,binding=self.bind('4'*32,selection_snapshot=snapshot)
        self.assertEqual(binding['release_id'],self.a)
        with self.assertRaisesRegex(ValueError,'Run selection changed'):
            self.bind('4'*32,selection_snapshot=self.control.current())

    def test_orphan_snapshot_cannot_authorize_execution(self):
        first,_=self.select(self.a,'1'*32,'0');self.store.fail_cas=True
        with self.assertRaises(ValueError):self.select(self.c,'2'*32,first['generation'])
        event_record,event=self.store.read('events/'+'2'*32+'.json')
        fake=dict(kind='candidate-selection-v1',event_id=event['event_id'],release_id=self.c,
            event=event_record,release=event['release'],precision_approved=False,publication_eligible=False)
        with self.assertRaisesRegex(ValueError,'never successfully selected'):
            self.bind('4'*32,selection_snapshot=(first,fake))

    def test_cas_race_leaves_orphan_but_cannot_rollback_to_it(self):
        record,_=self.select(self.a,'1'*32,'0')
        self.store.fail_cas=True
        with self.assertRaisesRegex(ValueError,'Concurrent'):
            self.select(self.c,'2'*32,record['generation'])
        self.assertIsNotNone(self.store.read('events/'+'2'*32+'.json')[0])
        current,_=self.select(self.b,'3'*32,record['generation'])
        with self.assertRaisesRegex(ValueError,'never selected'):
            self.select(self.c,'4'*32,current['generation'],rollback=True)

    def test_idempotent_retry_and_conflicting_event_are_distinct(self):
        original=self.select(self.a,'1'*32,'0')
        self.assertEqual(self.select(self.a,'1'*32,'0'),original)
        with self.assertRaisesRegex(ValueError,'Conflicting'):
            self.select(self.b,'1'*32,'0')

    def test_run_source_identity_cannot_change(self):
        self.select(self.a,'1'*32,'0');self.bind('4'*32)
        with self.assertRaisesRegex(ValueError,'Run identity changed'):
            self.bind('4'*32,source_hash='3'*64)

    def test_release_and_candidate_flags_cannot_be_overwritten(self):
        with self.assertRaisesRegex(ValueError,'never overwrite'):
            self.control.register(release(self.a,code='b'*64))
        bad=release('d'*32);bad['precision_approved']=True
        with self.assertRaisesRegex(ValueError,'cannot approve production'):
            self.control.register(bad)

    def test_current_cli_does_not_change_selection(self):
        original=self.select(self.a,'1'*32,'0');counter=self.store.counter
        with tempfile.TemporaryDirectory() as root,patch.object(control_module,'GCSCandidateControlStore',return_value=self.store), \
             patch('sys.argv',['control','--project','test-project','--bucket','sec-review-shadow-fixture',
                 '--output-dir',str(Path(root)/'status'),'current']),patch('builtins.print'):
            control_module.main()
            self.assertTrue((Path(root)/'status'/'control_receipt.json').is_file())
        self.assertEqual(self.control.current(),original);self.assertEqual(self.store.counter,counter)
