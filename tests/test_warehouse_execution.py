from contextlib import ExitStack
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch,MagicMock

from scripts import dbt_shadow
from scripts import warehouse_candidate as candidate
from scripts.warehouse_execution import freeze_execution,execute_candidate
from scripts.validate_sql_only import DISABLED
from scripts.loan_review_sources import canonical
from test_dbt_shadow import rich_bundle
from test_shadow_reconciliation import review_envelope
import test_shadow_identity as identity_fixture
from test_warehouse_candidate import saved_candidate


class WarehouseExecutionTests(unittest.TestCase):
    def disabled(self):
        stack=ExitStack()
        for name in DISABLED:stack.enter_context(patch(name,side_effect=AssertionError(name)))
        return stack

    def test_preparation_with_reviews_and_identity_never_calls_python_finance(self):
        for bundle in (rich_bundle(),identity_fixture.IdentityShadowTests().combined('DER-04')):
            reviews=review_envelope(bundle)
            # Poison Python-selected values/statuses; SQL must receive raw candidates.
            for item in bundle['inputs'].values():
                item.update(value='FORBIDDEN-PYTHON-VALUE',status='FORBIDDEN-PYTHON-STATUS')
            if 'identity_reviews' in bundle:
                # Bind the test review to the amended metadata, not the old envelope.
                original={k:v for k,v in bundle.items() if k!='identity_reviews'}
                source_hash=dbt_shadow.digest(original);bundle['identity_reviews']['source_hash']=source_hash
                for review in bundle['identity_reviews']['reviews']:
                    claim=json.loads(review['evidence']['content']);claim['source_hash']=source_hash
                    review['evidence']['content']=canonical(claim)
            with self.disabled():
                metadata,records,baseline,acceptance=dbt_shadow.prepare_run(bundle,reconciliations=reviews,with_baseline=False)
            self.assertIsNone(baseline);self.assertIsNone(acceptance)
            self.assertNotIn('baseline_context',metadata)
            self.assertEqual(metadata['baseline_comparison'],'not_run')
            self.assertEqual(metadata['request_hash'],dbt_shadow.digest(bundle['request']))
            self.assertNotIn('FORBIDDEN-PYTHON',canonical(records))

    def test_execution_receipt_does_not_claim_comparison_and_reader_does_not_recalculate(self):
        with tempfile.TemporaryDirectory() as root:
            directory=Path(root);old=saved_candidate(directory)
            bundle=json.loads((directory/'source_bundle.json').read_text())
            metadata,records,_,_=dbt_shadow.prepare_run(bundle,run_id=old['run_id'],with_baseline=False)
            (directory/'shadow_inputs.json').write_text(canonical(records))
            metadata.update(status='executed',publication_eligible=False,dbt=old['dbt'])
            with self.disabled():
                pin=freeze_execution(directory,metadata)
                report,receipt=candidate.read_candidate(directory,expected_receipt_sha256=pin)
                candidate.write_preview(directory,directory/'preview',expected_receipt_sha256=pin)
            self.assertEqual(receipt['comparison'],dict(status='not_run',mode='dbt-only'))
            self.assertEqual(str(report.facts['interest_coverage:fy_t'].value),'5.83333333333333333333333333333333333333')
            self.assertFalse((directory/'baseline.json').exists())

    def test_cloud_failure_is_preserved_without_python_fallback(self):
        with tempfile.TemporaryDirectory() as root:
            directory=Path(root)/'execution';warehouse=MagicMock()
            warehouse.dataset='sec_review_shadow_failure';warehouse.execute.side_effect=RuntimeError('SQL failed')
            bundle=rich_bundle()
            with self.disabled(),self.assertRaisesRegex(RuntimeError,'SQL failed'):
                execute_candidate(bundle,directory,project='test-project',warehouse=warehouse)
            manifest=json.loads((directory/'execution_manifest.json').read_text())
            self.assertEqual(manifest['status'],'failed')
            self.assertFalse(manifest['publication_eligible'])
            self.assertFalse((directory/'baseline.json').exists())
            self.assertFalse((directory/'calculation_receipt.json').exists())
            warehouse.execute.assert_called_once()
