"""Synthetic review claims; never interpreted as project financial approvals."""
from copy import deepcopy
import json
import unittest

from scripts.dbt_shadow import prepare_plan, prepare_run, digest
from scripts.shadow_identity import RULES
from scripts.loan_review_sources import canonical
from test_dbt_shadow import rich_bundle


def identity_bundle(formula='DER-01',mode='annual'):
    bundle = json.loads(canonical(rich_bundle(mode)))
    metric, inputs = RULES[formula]
    role = 'fy_t' if mode=='annual' else 'current_interim'
    fid = metric+':'+role
    item = bundle['inputs'][fid]
    removed = set(item['candidate_ids'])
    bundle['evidence'] = {k:v for k,v in bundle['evidence'].items() if k not in removed}
    item.update(candidate_ids=[],evidence_ids=[],value=None,status='missing',reason='Synthetic missing source')
    plan = next(p for p in prepare_plan(bundle) if p['fact_id']==fid)
    ids = [m+':'+role for m in inputs]
    claim = dict(source_hash=digest(bundle),entity=bundle['entity'],scope=bundle['scope'],
        fact_id=fid,formula_id=formula,formula_version='synthetic-reviewed-v1',input_ids=ids,
        period_role=role,start=str(plan['start']),end=str(plan['end']),
        currency=plan['currency'],unit=plan['unit'],complete=True)
    evidence = dict(id='identity:'+fid,entity=bundle['entity'],scope=bundle['scope'],
        source_id='synthetic-reviewed-identity',version='v1',document_date='2026-09-01',
        locator='Synthetic complete identity review',kind='definition',period_roles=[role],
        content=canonical(claim))
    bundle['identity_reviews'] = dict(schema_version=1,source_hash=digest(bundle),reviews=[
        dict(fact_id=fid,formula_id=formula,formula_version='synthetic-reviewed-v1',input_ids=ids,evidence=evidence)])
    return bundle


class IdentityShadowTests(unittest.TestCase):
    def test_all_six_formulas_are_planned_and_baseline_recomputed(self):
        expected = {'DER-01':'80','DER-02':'40','DER-03':'20','DER-04':'60','DER-05':'50','DER-06':'55'}
        for formula in RULES:
            with self.subTest(formula=formula):
                bundle = identity_bundle(formula)
                _,records,baseline,_ = prepare_run(bundle)
                review = bundle['identity_reviews']['reviews'][0]
                fact = baseline['facts'][review['fact_id']]
                self.assertEqual(fact['value'],expected[formula])
                self.assertEqual(fact['evidence_ids'],[review['evidence']['id']])
                plan = next(p for k,_,p in records if k=='slot' and p['fact_id']==review['fact_id'])
                self.assertEqual(plan['formula_id'],formula)
                self.assertEqual(plan['input_ids'],review['input_ids'])
                self.assertNotIn('value',plan)
                self.assertGreater(plan['depth'],0)

    def test_source_claim_and_evidence_changes_are_rejected(self):
        for change in ('source','content','date','scope','order','duplicate','version','reserved','boolean'):
            with self.subTest(change=change):
                bundle = identity_bundle()
                review = bundle['identity_reviews']['reviews'][0]
                if change=='source':bundle['cik']='9999999999'
                if change=='content':review['evidence']['content']='{}'
                if change=='date':review['evidence']['document_date']='2099-01-01'
                if change=='scope':review['evidence']['scope']='other'
                if change=='order':review['input_ids'].reverse()
                if change=='duplicate':bundle['identity_reviews']['reviews'].append(deepcopy(review))
                if change=='version':review['formula_version']=' '
                if change=='reserved':review['evidence']['id']='calendar'
                if change=='boolean':
                    claim = json.loads(review['evidence']['content']);claim['complete']=1
                    review['evidence']['content']=canonical(claim)
                with self.assertRaises(ValueError):prepare_plan(bundle)

    def test_no_review_does_not_enable_identity(self):
        bundle = identity_bundle()
        bundle.pop('identity_reviews')
        _,_,baseline,_ = prepare_run(bundle)
        self.assertEqual(baseline['facts']['gross_profit:fy_t']['status'],'missing')

    def test_quarterly_review_stays_on_ytd_period(self):
        bundle = identity_bundle(mode='quarterly')
        _,_,baseline,_ = prepare_run(bundle)
        fact = baseline['facts']['gross_profit:current_interim']
        self.assertEqual(fact['value'],'80')
        self.assertEqual(fact['formula_id'],'DER-01')
        self.assertEqual(fact['start'],bundle['request']['periods'][-1]['start'])

    def combined(self,second_formula):
        bundle = identity_bundle()
        old = bundle.pop('identity_reviews')['reviews'][0]
        other = identity_bundle(second_formula)['identity_reviews']['reviews'][0]
        fid = other['fact_id']
        removed = set(bundle['inputs'][fid]['candidate_ids'])
        bundle['evidence'] = {k:v for k,v in bundle['evidence'].items() if k not in removed}
        bundle['inputs'][fid].update(candidate_ids=[],evidence_ids=[],value=None,
            status='missing',reason='Synthetic chained missing source')
        source_hash = digest(bundle)
        for review in (old,other):
            claim = json.loads(review['evidence']['content'])
            claim['source_hash'] = source_hash
            review['evidence']['content'] = canonical(claim)
        bundle['identity_reviews'] = dict(schema_version=1,source_hash=source_hash,reviews=[other,old])
        return bundle

    def test_chain_is_ordered_before_downstream_ratios(self):
        bundle = self.combined('DER-04')
        _,records,baseline,_ = prepare_run(bundle)
        plans = {p['fact_id']:p for k,_,p in records if k=='slot'}
        self.assertEqual(baseline['facts']['operating_income:fy_t']['value'],'60')
        self.assertGreater(plans['operating_income:fy_t']['depth'],plans['gross_profit:fy_t']['depth'])
        self.assertGreater(plans['operating_margin:fy_t']['depth'],plans['operating_income:fy_t']['depth'])
        self.assertEqual(baseline['facts']['operating_margin:fy_t']['value'],'0.5')

    def test_mutually_reversing_reviews_are_rejected_before_execution(self):
        with self.assertRaisesRegex(ValueError,'dependency cycle'):
            prepare_plan(self.combined('DER-02'))
