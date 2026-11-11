from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts import selected_runtime as selected
from scripts import selected_runtime_worker as worker
from scripts.candidate_release_control import CandidateReleaseControl
from scripts.delivery_archive import sha
from tests.test_candidate_release_control import MemoryStore,release
from tests import test_runtime_package as package_tests


class BinaryStorage:
    name='sec-review-shadow-fixture'
    def __init__(self):self.objects={}
    def _put(self,name,data):
        if name in self.objects and self.objects[name]!=data:raise ValueError('never overwrite')
        self.objects[name]=data
        return dict(name=name,generation='1',sha256=sha(data),size=len(data))
    def _get(self,record):
        data=self.objects[record['name']]
        if sha(data)!=record['sha256'] or len(data)!=record['size']:raise ValueError('checksum mismatch')
        return data


class SelectedRuntimeTests(unittest.TestCase):
    def test_runtime_storage_uses_generation_pins_and_rejects_tampering(self):
        package_tests.RuntimePackageTests.setUpClass()
        try:
            storage=BinaryStorage();runtime=selected.RuntimeStorage(storage)
            reference=runtime.store(package_tests.RuntimePackageTests.archive,package_tests.RuntimePackageTests.receipt['package_sha256'])
            self.assertEqual(runtime.store(package_tests.RuntimePackageTests.archive,reference['package_sha256']),reference)
            with tempfile.TemporaryDirectory() as tmp:
                runtime.fetch(reference,Path(tmp)/'valid.zip')
                bad=deepcopy(reference);bad['code_hash']='f'*64
                with self.assertRaisesRegex(ValueError,'reference contract'):
                    runtime.fetch(bad,Path(tmp)/'mixed.zip')
                storage.objects[reference['object']['name']]=b'tampered'
                with self.assertRaisesRegex(ValueError,'checksum'):
                    runtime.fetch(reference,Path(tmp)/'bad.zip')
                self.assertFalse((Path(tmp)/'bad.zip').exists())
        finally:package_tests.RuntimePackageTests.tearDownClass()

    def test_worker_binds_before_client_creation_and_sql(self):
        store=MemoryStore();control=CandidateReleaseControl(store)
        body=release('a'*32);body.update(runtime={'package_sha256':'1'*64},
            formula_version='formula',policy_version='policy',precision_version='pending')
        control.register(body)
        snapshot=control.select('a'*32,event_id='1'*32,actor='test',reason='test',expected_generation='0')
        metadata=dict(run_id='4'*32,entity='SYNTHETIC-ONLY',scope='entity-wide',source_hash='2'*64,
            request_hash='3'*64,**{key:body[key] for key in ('code_hash','formula_version','policy_version','precision_version')})
        order=[]
        class Warehouse:
            def __init__(self,project,run_id):
                assert store.read('runs/'+run_id+'.json')[1] is not None
                order.append('client')
            def execute(self,records,directory):order.append('sql');return 'done'
        with tempfile.TemporaryDirectory() as tmp,patch.object(worker,'GCSCandidateControlStore',return_value=store), \
             patch.object(worker.warehouse_execution,'ShadowWarehouse',Warehouse):
            config=dict(project='test-project',bucket='sec-review-shadow-fixture',snapshot=snapshot,
                runtime=body['runtime'],binding_output=str(Path(tmp)/'binding.json'))
            worker.install_binding(config)
            engine=worker.warehouse_execution.ShadowWarehouse('test-project',metadata['run_id'])
            self.assertEqual(order,[])
            self.assertEqual(engine.execute([('metadata','run',metadata)],tmp),'done')
            self.assertEqual(order,['client','sql'])
            binding=json.loads(Path(config['binding_output']).read_text())['body']
            self.assertEqual(binding['source_hash'],metadata['source_hash'])

    def test_worker_rejects_contract_mismatch_before_warehouse(self):
        store=MemoryStore();control=CandidateReleaseControl(store)
        body=release('a'*32);body.update(runtime={},formula_version='f',policy_version='p',precision_version='pending')
        control.register(body);snapshot=control.select('a'*32,event_id='1'*32,actor='test',reason='test',expected_generation='0')
        with tempfile.TemporaryDirectory() as tmp,patch.object(worker,'GCSCandidateControlStore',return_value=store), \
             patch.object(worker.warehouse_execution,'ShadowWarehouse') as original:
            worker.install_binding(dict(project='test-project',bucket='sec-review-shadow-fixture',snapshot=snapshot,
                runtime={},binding_output=str(Path(tmp)/'binding.json')))
            engine=worker.warehouse_execution.ShadowWarehouse('test-project','4'*32)
            with self.assertRaisesRegex(ValueError,'contract differs'):
                engine.execute([('metadata','run',dict(code_hash='b'*64))],tmp)
            original.assert_not_called();self.assertIsNone(store.read('runs/'+'4'*32+'.json')[1])

    def test_missing_package_stops_before_execution_and_preserves_failure(self):
        store=MemoryStore();store.storage=BinaryStorage();control=CandidateReleaseControl(store)
        body=release('a'*32);body['runtime']=dict(kind='candidate-runtime-reference-v1',
            object=dict(name='candidate-runtime/'+'1'*64+'.zip',sha256='1'*64,generation='1',size=3),
            package_sha256='1'*64,precision_approved=False,publication_eligible=False)
        control.register(body);control.select('a'*32,event_id='1'*32,actor='test',reason='test',expected_generation='0')
        with tempfile.TemporaryDirectory() as tmp,patch.object(selected,'run_package') as run:
            output=Path(tmp)/'execution'
            with self.assertRaises(KeyError):selected.execute_selected(control,'source.json',output,project='test-project')
            run.assert_not_called();self.assertFalse((output/'selected_execution_receipt.json').exists())
            self.assertEqual(json.loads((output/'selected_execution_manifest.json').read_text())['status'],'failed')

    def test_skill_policy_mismatch_stops_before_package_fetch(self):
        store=MemoryStore();control=CandidateReleaseControl(store)
        body=release('a'*32);body['precision_version']='old-policy'
        control.register(body);control.select('a'*32,event_id='1'*32,actor='test',reason='test',expected_generation='0')
        with tempfile.TemporaryDirectory() as tmp,patch.object(selected,'RuntimeStorage') as storage:
            with self.assertRaisesRegex(ValueError,'precision policy differs'):
                selected.execute_selected(control,'source.json',Path(tmp)/'run',project='test-project',
                    expected_precision_version='bignumeric-q18-half-even-v1')
            storage.assert_not_called()
