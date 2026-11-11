"""Reviewed cash adoption is conditional; synthetic claims only."""
import unittest

from scripts.dbt_shadow import prepare_run
from test_dbt_shadow import rich_bundle
from test_shadow_reconciliation import review_envelope


class ShadowCashTests(unittest.TestCase):
    def cash(self,bundle,checks=None):
        _,_,report,acceptance = prepare_run(bundle,reconciliations=checks)
        return [f for f in report['facts'].values() if f['metric']=='cash_change'],acceptance

    def test_complete_review_computes_annual_and_does_not_invent_quarterly_rows(self):
        for mode in ('annual','quarterly'):
            bundle = rich_bundle(mode)
            facts,acceptance = self.cash(bundle,review_envelope(bundle))
            self.assertEqual(len(facts),4 if mode=='annual' else 0)
            for f in facts:
                self.assertEqual(f['value'],'10')
                self.assertEqual(f['formula_id'],'CASH-CHANGE-v1')
                self.assertEqual(f['input_ids'],['ending_cash:'+f['period_role'],'beginning_cash:'+f['period_role']])
                self.assertEqual(f['evidence_ids'],['review:cash_bridge:'+f['period_role']])
            self.assertEqual(sum(c.get('verified',False) for c in acceptance['reconciliations']),8 if mode=='annual' else 4)

    def test_missing_or_forged_review_does_not_fill_cash(self):
        bundle = rich_bundle()
        for envelope in (None,review_envelope(bundle,forged=True)):
            facts,_ = self.cash(bundle,envelope)
            self.assertTrue(all(f['value'] is None and f['formula_id'] is None for f in facts))

    def test_review_kind_without_definition_does_not_authorize_cash_identity(self):
        bundle = rich_bundle();envelope = review_envelope(bundle)
        for e in envelope['evidence'].values():e['kind']='review'
        facts,acceptance = self.cash(bundle,envelope)
        self.assertTrue(all(f['value'] is None for f in facts))
        self.assertEqual(sum(c.get('verified',False) for c in acceptance['reconciliations']),8)

    def test_source_lineage_or_fx_omission_blocks_adoption(self):
        bundle = rich_bundle();envelope = review_envelope(bundle)
        for check in envelope['checks']:
            if check['kind']=='cash_bridge':check['terms']=check['terms'][:-1]
        facts,_ = self.cash(bundle,envelope)
        self.assertTrue(all(f['value'] is None for f in facts))

    def test_future_review_is_rejected(self):
        bundle = rich_bundle();envelope = review_envelope(bundle)
        next(iter(envelope['evidence'].values()))['document_date']='2099-01-01'
        with self.assertRaisesRegex(ValueError,'later than analysis as_of'):
            self.cash(bundle,envelope)
