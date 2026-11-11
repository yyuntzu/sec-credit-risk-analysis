from copy import deepcopy
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
from zipfile import ZipFile,ZipInfo

from scripts import runtime_package as runtime
from scripts.dbt_shadow import code_hash
from scripts.warehouse_candidate import file_hash
from scripts.loan_review_sources import canonical

ROOT=Path(__file__).resolve().parents[1]
LOCK=dict(python=[3,13,1],platform='fixture',machine='fixture',distributions={
    'dbt-core':dict(version='1.12.0',content_sha256='a'*64)})


class RuntimePackageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary=tempfile.TemporaryDirectory();cls.root=Path(cls.temporary.name)
        cls.hash=code_hash()
        with patch.object(runtime,'runtime_lock',return_value=deepcopy(LOCK)):
            cls.receipt=runtime.build_package(ROOT,cls.root/'built',expected_code_hash=cls.hash)
        cls.archive=cls.root/'built'/'runtime.zip'
    @classmethod
    def tearDownClass(cls):cls.temporary.cleanup()
    def forge(self,path,*,change=None,extra=None):
        with ZipFile(self.archive) as archive:files={name:archive.read(name) for name in archive.namelist()}
        if change:change(files)
        with ZipFile(path,'x') as archive:
            for name,data in files.items():archive.writestr(name,data)
            if extra:archive.writestr(*extra)
        return file_hash(path)

    def test_build_is_deterministic_and_contains_no_inputs_or_credentials(self):
        with tempfile.TemporaryDirectory() as tmp,patch.object(runtime,'runtime_lock',return_value=deepcopy(LOCK)):
            receipt=runtime.build_package(ROOT,Path(tmp)/'second',expected_code_hash=self.hash)
            self.assertEqual(receipt,self.receipt)
            manifest,files=runtime.inspect_package(self.archive,self.receipt['package_sha256'])
            self.assertEqual(manifest['financial_code_hash'],self.hash)
            self.assertIn('scripts/__init__.py',files)
            self.assertFalse(any(name.endswith(('.env','source_bundle.json','report.json')) for name in files))
            self.assertNotIn('keyfile',files['references/dbt/profiles.yml'].decode())

    def test_bad_pin_path_and_symlink_are_rejected_before_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            with self.assertRaisesRegex(ValueError,'pin mismatch'):
                runtime.extract_package(self.archive,'0'*64,root/'bad',check_environment=False)
            self.assertFalse((root/'bad').exists())
            link=ZipInfo('scripts/link');link.create_system=3;link.external_attr=0o120777<<16
            for name,extra in (('path',('../escape',b'bad')),('link',(link,b'/private/secret'))):
                path=root/(name+'.zip');pin=self.forge(path,extra=extra)
                with self.assertRaisesRegex(ValueError,'Unsafe runtime'):
                    runtime.extract_package(path,pin,root/name,check_environment=False)
                self.assertFalse((root/name).exists())

    def test_updated_file_hash_cannot_hide_financial_code_change(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            def change(files):
                files['scripts/review_outputs.py']+=b'\n# altered runtime\n'
                manifest=json.loads(files['runtime_manifest.json'])
                import hashlib
                manifest['files']['scripts/review_outputs.py']=hashlib.sha256(files['scripts/review_outputs.py']).hexdigest()
                files['runtime_manifest.json']=canonical(manifest).encode()
            path=root/'forged.zip';pin=self.forge(path,change=change)
            with self.assertRaisesRegex(ValueError,'fingerprint mismatch'):
                runtime.extract_package(path,pin,root/'unpacked',check_environment=False)
            self.assertFalse((root/'unpacked').exists())

    def test_same_dependency_version_with_different_content_is_blocked(self):
        bad=deepcopy(LOCK);bad['distributions']['dbt-core']['content_sha256']='b'*64
        with tempfile.TemporaryDirectory() as tmp,patch.object(runtime,'runtime_lock',return_value=bad):
            with self.assertRaisesRegex(ValueError,'dependency content'):
                runtime.extract_package(self.archive,self.receipt['package_sha256'],Path(tmp)/'runtime')
            self.assertFalse((Path(tmp)/'runtime').exists())

    def test_failed_process_preserves_failure_and_never_falls_back(self):
        with tempfile.TemporaryDirectory() as tmp, \
             patch.object(runtime,'extract_package',return_value=dict(financial_code_hash=self.hash)), \
             patch.object(runtime.subprocess,'run',return_value=SimpleNamespace(returncode=1,stderr='SQL failure')) as runner:
            output=Path(tmp)/'attempt'
            with self.assertRaisesRegex(ValueError,'no current-code fallback'):
                runtime.run_package(self.archive,self.receipt['package_sha256'],'source.json',output,project='test-project')
            state=json.loads((output/'package_execution_manifest.json').read_text())
            self.assertEqual(state['status'],'failed');self.assertFalse(state['publication_eligible'])
            self.assertFalse((output/'package_execution_receipt.json').exists());runner.assert_called_once()
            self.assertIn('-I',runner.call_args.args[0])

    def test_dependency_lock_follows_extras_and_hashes_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            for name in ('root','plugin','leaf'):(root/(name+'.py')).write_text(name)
            def distribution(name):
                return SimpleNamespace(version='1.0',files=[Path(name+'.py')],locate_file=lambda entry:root/entry,
                    requires={'root':['plugin[feature]'],'plugin':['leaf; extra == "feature"'],'leaf':[]}[name])
            with patch.object(runtime,'ROOTS',('root',)),patch.object(runtime.metadata,'distribution',side_effect=distribution):
                first=runtime.runtime_lock();self.assertEqual(set(first['distributions']),{'root','plugin','leaf'})
                (root/'leaf.py').write_text('changed content')
                second=runtime.runtime_lock()
                self.assertEqual(first['distributions']['leaf']['version'],second['distributions']['leaf']['version'])
                self.assertNotEqual(first['distributions']['leaf']['content_sha256'],second['distributions']['leaf']['content_sha256'])

    def test_unreconstructable_source_or_wrong_manifest_cannot_be_packaged(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            with self.assertRaisesRegex(ValueError,'Exact financial source unavailable'):
                runtime.build_package(ROOT,root/'bad',expected_code_hash='0'*64)
            self.assertFalse((root/'bad').exists())
            manifest=root/'manifest.json';manifest.write_text('{"nodes":{}}')
            with self.assertRaisesRegex(ValueError,'manifest pin mismatch'):
                runtime.build_package(ROOT,root/'wrong-manifest',expected_code_hash=self.hash,
                    dbt_manifest=manifest,manifest_pin='0'*64)
            self.assertFalse((root/'wrong-manifest').exists())
