import unittest
from scripts.dbt_shadow import prepare_run,digest
from scripts.validate_canonical_configuration import mutate_configuration,CASES
from test_dbt_shadow import rich_bundle


class CanonicalConfigurationProbeTests(unittest.TestCase):
    def test_rebound_claims_preserve_raw_numbers_and_request(self):
        _,records,_,_=prepare_run(rich_bundle(),with_baseline=False)
        original=digest(records)
        raw=[row for kind,_,row in records if kind=='observation']
        for case in CASES:
            with self.subTest(case=case):
                changed=mutate_configuration(records,case)
                metadata=next(row for kind,_,row in changed if kind=='metadata')
                self.assertEqual(metadata['plan_hash'],digest([row for kind,_,row in changed if kind=='slot']))
                self.assertEqual(raw,[row for kind,_,row in changed if kind=='observation'])
                self.assertEqual(digest(records),original)
                if case=='scale':self.assertEqual(metadata['scale'],'1000')
                if case=='basis':self.assertEqual(metadata['standard_ebitda_basis'],'PROBE-UNAPPROVED-ADJUSTED-EBITDA')
                if case=='versions':self.assertTrue(metadata['precision_approved'])
