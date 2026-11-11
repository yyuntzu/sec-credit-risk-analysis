import unittest

from scripts.dbt_shadow import prepare_run,digest
from scripts.validate_formula_contracts import corrupt_plan
from test_dbt_shadow import rich_bundle


class FormulaContractProbeTests(unittest.TestCase):
    def test_mutations_preserve_identity_and_rebind_hash_without_numeric_overrides(self):
        _,records,_,_=prepare_run(rich_bundle(),with_baseline=False)
        old=digest(records)
        bad,targets=corrupt_plan(records)
        self.assertEqual(digest(records),old)
        slots={key:row for kind,key,row in bad if kind=='slot'}
        metadata=next(row for kind,_,row in bad if kind=='metadata')
        self.assertEqual(metadata['plan_hash'],digest([row for kind,_,row in bad if kind=='slot']))
        self.assertEqual(slots[targets[0]]['input_ids'],['input:current_liabilities:fy_t','input:current_assets:fy_t'])
        self.assertEqual(slots[targets[1]]['formula_id'],'CF-01')
        self.assertEqual(len(slots[targets[2]]['input_ids']),2)
        self.assertEqual(slots[targets[3]]['input_ids'][1],'revenue:fy_t_minus_1')
        self.assertEqual(slots[targets[4]]['pending'],[])
        self.assertEqual(next(row for kind,key,row in bad if key=='probe:unapproved-dscr')['value'],'2')
        self.assertTrue(all('value' not in row for row in slots.values()))
