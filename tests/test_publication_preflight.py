import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from types import SimpleNamespace

from scripts.publication_preflight import inspect_candidate, main


class PublicationPreflightTests(unittest.TestCase):
    def inspect(self, *, ready=False, precision=False, comparisons=None,policy='unapproved'):
        receipt = dict(bindings=dict(precision_version=policy), precision_approved=precision,
                       comparison=comparisons or {})
        with patch('scripts.publication_preflight.read_candidate', return_value=(SimpleNamespace(facts={}), receipt)), \
             patch('scripts.publication_preflight._read', return_value=[dict(
                 substantive_data_ready=ready, acceptance_blockers=[] if ready else ['missing'])]):
            return inspect_candidate('/unused', receipt_sha256='pinned')

    def test_shadow_always_blocked(self):
        for ready in (True, False):
            for precision in (True, False):
                result = self.inspect(ready=ready, precision=precision)
                self.assertFalse(result['publication_eligible'])
                self.assertFalse(result['publication_receipt'])
                self.assertEqual(result['status'], 'blocked')
                self.assertIn('release_authorization_missing', [b['code'] for b in result['blockers']])

    def test_each_difference_is_recorded(self):
        result = self.inspect(comparisons=dict(mismatches=1, reconciliation_mismatches=2,
            acceptance_mismatches=3, commentary_mismatches=4, numeric_differences=5,
            commentary_numeric_differences=6))
        self.assertEqual(sum(b['code']=='comparison_mismatch' for b in result['blockers']), 4)
        self.assertEqual(sum(b['code']=='unapproved_precision_differences' for b in result['blockers']), 2)

    def test_untrusted_receipt_failure_propagates(self):
        with patch('scripts.publication_preflight.read_candidate', side_effect=ValueError('pin mismatch')):
            with self.assertRaisesRegex(ValueError, 'pin mismatch'):
                inspect_candidate('/unused', receipt_sha256='wrong')

    def test_approved_math_and_verified_policy_changes_do_not_approve_release(self):
        result=self.inspect(policy='bignumeric-q18-half-even-v1',comparisons=dict(
            canonical_precision_mismatches=0,numeric_differences=26))
        codes=[row['code'] for row in result['blockers']]
        self.assertTrue(result['canonical_precision_verified'])
        self.assertNotIn('precision_unapproved',codes)
        self.assertNotIn('unapproved_precision_differences',codes)
        self.assertIn('precision_release_not_activated',codes)
        self.assertFalse(result['publication_eligible'])
        self.assertEqual(result['legacy_precision_changes']['numeric_differences'],26)
        missing=self.inspect(policy='bignumeric-q18-half-even-v1')
        self.assertIn('canonical_precision_validation_missing',[row['code'] for row in missing['blockers']])

    def test_cli_nonzero_and_never_overwrites(self):
        with tempfile.TemporaryDirectory() as root, \
             patch('scripts.publication_preflight.inspect_candidate', return_value={'status':'blocked'}), \
             patch('builtins.print'):
            output = str(Path(root)/'new')
            args = ['--candidate-dir', root, '--receipt-sha256', 'pin', '--output-dir', output]
            self.assertEqual(main(args), 2)
            self.assertTrue((Path(output)/'publication_preflight.json').is_file())
            with self.assertRaisesRegex(ValueError, 'already exists'):
                main(args)
