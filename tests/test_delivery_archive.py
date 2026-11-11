from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest

from google.api_core.exceptions import PreconditionFailed,NotFound
from scripts import delivery_archive as delivery
from scripts.warehouse_candidate import file_hash
from test_warehouse_excel import preview_fixture


class Blob:
    def __init__(self,bucket,name,generation=None):
        self.bucket,self.name,self.generation = bucket,name,generation
    def upload_from_string(self,data,**kwargs):
        assert kwargs['if_generation_match']==0 and kwargs['checksum']=='crc32c'
        if self.name in self.bucket.current:raise PreconditionFailed('already exists')
        self.generation = self.bucket.counter;self.bucket.counter+=1
        self.bucket.current[self.name]=self.generation
        self.bucket.data[self.name,self.generation]=data
    def reload(self,**kwargs):
        self.generation=self.bucket.current[self.name]
    def download_as_bytes(self,**kwargs):
        assert kwargs['if_generation_match']==self.generation and kwargs['checksum']=='crc32c'
        try:return self.bucket.data[self.name,self.generation]
        except KeyError:raise NotFound('generation gone')


class Bucket:
    def __init__(self):self.current={};self.data={};self.counter=1
    def blob(self,name,generation=None):return Blob(self,name,generation)


class Client:
    def __init__(self):self.value=Bucket()
    def bucket(self,name):return self.value


class DeliveryArchiveTests(unittest.TestCase):
    def fixture(self,root):
        calculation,preview,pin = preview_fixture(root)
        receipt = json.loads((calculation/'calculation_receipt.json').read_text())
        archive = dict(format_version='candidate-archive-v1',attempt_id='b'*32,table='review_candidate_'+'b'*32,
            dataset='sec_review_shadow_fixture',calculation_receipt_sha256=pin,
            **{k:receipt['bindings'][k] for k in ('run_id','entity','scope')},
            precision_approved=False,publication_eligible=False)
        path = root/'archive_receipt.json';path.write_text(json.dumps(archive))
        kwargs = dict(calculation_pin=pin,preview_pin=file_hash(preview/'preview_manifest.json'),
            archive_receipt=path,archive_pin=file_hash(path),delivery_id='c'*32,require_excel=False)
        return calculation,preview,kwargs

    def test_verified_roundtrip_retry_and_generation_pin(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);calc,preview,kwargs=self.fixture(root)
            body,files=delivery.prepare_delivery(calc,preview,**kwargs)
            client=Client();storage=delivery.ShadowDeliveryStorage('test-project','sec-review-shadow-fixture',client=client)
            receipt=storage.store(body,files)
            self.assertEqual(storage.store(body,files),receipt)
            commit=storage.restore(receipt,root/'restored')
            self.assertFalse(commit['publication_eligible'])
            self.assertEqual({p.name:p.read_bytes() for p in (root/'restored').iterdir()},files)
            # A newer current object must never be substituted for the pinned generation.
            name=commit['objects']['report.json']['name']
            client.value.current[name]=999
            client.value.data[name,999]=b'new live version'
            storage.restore(receipt,root/'second-restored')
            self.assertEqual((root/'second-restored'/'report.json').read_bytes(),files['report.json'])

    def test_tampering_with_fresh_preview_hash_still_fails_semantics(self):
        for filename in ('dashboard.html','report.md','report.json'):
            with self.subTest(filename=filename),tempfile.TemporaryDirectory() as tmp:
                calc,preview,kwargs=self.fixture(Path(tmp))
                (preview/filename).write_text('foreign content')
                manifest=json.loads((preview/'preview_manifest.json').read_text())
                manifest['artifacts'][filename]=file_hash(preview/filename)
                (preview/'preview_manifest.json').write_text(json.dumps(manifest))
                kwargs['preview_pin']=file_hash(preview/'preview_manifest.json')
                with self.assertRaisesRegex(ValueError,'receipt-bound rendering'):
                    delivery.prepare_delivery(calc,preview,**kwargs)

    def test_required_excel_and_mixed_archive_are_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            calc,preview,kwargs=self.fixture(Path(tmp))
            with self.assertRaisesRegex(ValueError,'Required Excel'):
                delivery.prepare_delivery(calc,preview,**dict(kwargs,require_excel=True))
            archive=json.loads(kwargs['archive_receipt'].read_text());archive['run_id']='d'*32
            kwargs['archive_receipt'].write_text(json.dumps(archive));kwargs['archive_pin']=file_hash(kwargs['archive_receipt'])
            with self.assertRaisesRegex(ValueError,'archive binding mismatch'):
                delivery.prepare_delivery(calc,preview,**kwargs)

    def test_partial_retry_different_content_and_corrupt_generation_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);calc,preview,kwargs=self.fixture(root)
            body,files=delivery.prepare_delivery(calc,preview,**kwargs)
            client=Client();storage=delivery.ShadowDeliveryStorage('test-project','sec-review-shadow-fixture',client=client)
            prefix=storage._prefix(body)
            storage._put(prefix+'dashboard.html',files['dashboard.html'])
            receipt=storage.store(body,files)
            with self.assertRaisesRegex(ValueError,'never overwrite'):
                storage._put(prefix+'dashboard.html',b'changed')
            commit=json.loads(storage._get(receipt['commit']))
            obj=commit['objects']['report.json'];client.value.data[obj['name'],int(obj['generation'])]=b'corrupt'
            with self.assertRaisesRegex(ValueError,'checksum mismatch'):
                storage.restore(receipt,root/'bad-restore')
            self.assertFalse((root/'bad-restore').exists())

    def test_invalid_namespace_pin_and_path_are_rejected(self):
        with self.assertRaisesRegex(ValueError,'shadow bucket'):
            delivery.ShadowDeliveryStorage('test-project','production',client=Client())
        with tempfile.TemporaryDirectory() as tmp:
            calc,preview,kwargs=self.fixture(Path(tmp))
            with self.assertRaisesRegex(ValueError,'manifest pin mismatch'):
                delivery.prepare_delivery(calc,preview,**dict(kwargs,preview_pin='0'*64))
            body,files=delivery.prepare_delivery(calc,preview,**kwargs)
            body['delivery_id']='../escape'
            with self.assertRaisesRegex(ValueError,'delivery identity'):
                delivery.ShadowDeliveryStorage('test-project','sec-review-shadow-fixture',client=Client()).store(body,files)
