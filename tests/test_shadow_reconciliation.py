"""Reviewed bridges must agree independently with source lineage and SQL facts."""
from copy import deepcopy
from dataclasses import asdict
from decimal import Decimal, localcontext
import json
from pathlib import Path
import tempfile
import unittest

from scripts import dbt_shadow as shadow
from scripts.shadow_reconciliation import compare_reconciliations, compare_acceptance
from scripts.loan_review_sources import canonical
from test_dbt_shadow import rich_bundle, SHADOW_RUN_ID


def review_envelope(bundle, *, forged=False):
    _,_,report,_=shadow.prepare_run(bundle)
    facts=report['facts']
    checks=[];evidence={}
    for i,period in enumerate(report['periods']):
        role=period['role']
        for kind,reported,terms in (
            ('balance_sheet_equation','total_assets',['total_liabilities','net_worth']),
            ('cash_bridge','ending_cash',['beginning_cash','cfo','cfi','cff','cash_fx','cash_other'])):
            def fid(metric):
                key=metric+':'+role
                return key if key in facts else 'input:'+key
            term_ids=[fid(m) for m in terms];reported_id=fid(reported)
            if any(key not in facts for key in term_ids+[reported_id]):
                continue  # Quarterly snapshots need not contain FY cash-flow slots.
            calculated=sum((Decimal(facts[key]['value']) for key in term_ids),Decimal(0))
            amount=Decimal(facts[reported_id]['value']);delta=calculated-amount
            tolerance=abs(delta)
            check=dict(kind=kind,period_role=role,
                status='matched' if delta==0 else 'within_precision',
                terms=[dict(fact_id=key,coefficient='1') for key in term_ids],
                reported_fact_id=reported_id,tolerance=str(tolerance),
                calculated_value=str(calculated),reported_value=str(amount),difference=str(delta))
            eids=set(eid for key in term_ids+[reported_id] for eid in facts[key]['evidence_ids'])
            eid=f'review:{kind}:{role}'
            check['evidence_ids']=sorted(eids)+[eid]
            binding={k:check[k] for k in ('kind','period_role','terms','reported_fact_id','tolerance')}
            binding.update(currency=report['currency'],scale=report['scale'])
            ev=dict(id=eid,entity=report['entity'],scope=report['scope'],source_id='SYNTHETIC-BRIDGE',
                version='v1',document_date='2026-09-02',locator=kind+':'+role,kind='definition',
                period_roles=[role],content=canonical(binding),purpose='borrower')
            if forged:
                if i==0 and kind=='balance_sheet_equation':
                    ev['content']=canonical(dict(binding,scope='unapproved-extra-field'))
                elif i==0:
                    check['evidence_ids'].remove(facts[fid('cash_fx')]['evidence_ids'][0])
                elif i==1 and kind=='balance_sheet_equation':
                    check['tolerance']='100'
                    binding['tolerance']='100';ev['content']=canonical(binding)
                elif i==1:
                    check['terms'][-1]=deepcopy(check['terms'][1])
                    binding['terms']=check['terms'];ev['content']=canonical(binding)
                elif i==2 and kind=='balance_sheet_equation':
                    check['calculated_value']='999'
                elif i==2:
                    check['terms'][0]['coefficient']='-1'
                    binding['terms']=check['terms'];ev['content']=canonical(binding)
                elif i==3 and kind=='balance_sheet_equation':
                    check['terms'][0]['ignored']='not-authorized'
                    binding['terms']=check['terms'];ev['content']=canonical(binding)
                else:
                    check['reported_fact_id']=fid('beginning_cash')
                    binding['reported_fact_id']=check['reported_fact_id'];ev['content']=canonical(binding)
            checks.append(check);evidence[eid]=ev
    return dict(schema_version=1,checks=checks,evidence=evidence)


class ComparisonClassificationTests(unittest.TestCase):
    def setUp(self):
        _,_,self.baseline,_=shadow.prepare_run(rich_bundle())
        self.rows=[dict(deepcopy(f),fact_id=f['id'],run_id=SHADOW_RUN_ID) for f in self.baseline['facts'].values()]

    def compare(self):
        return shadow.compare_facts(self.baseline,self.rows,expected_run_id=SHADOW_RUN_ID)

    def test_source_and_exact_sum_defects_are_errors_not_precision(self):
        for fid in ('revenue:fy_t','ltm_ebitda:fy_t','operating_margin_change:fy_t'):
            with self.subTest(fid=fid):
                rows=deepcopy(self.rows)
                next(r for r in rows if r['fact_id']==fid)['value']='999'
                result=shadow.compare_facts(self.baseline,rows,expected_run_id=SHADOW_RUN_ID)
                self.assertEqual(next(r for r in result['details'] if r['fact_id']==fid)['classification'],'mismatch')
                self.assertGreater(result['mismatches'],0)

    def test_exact_subtraction_may_only_carry_a_verified_input_difference(self):
        index={r['fact_id']:r for r in self.rows}
        index['operating_margin:fy_t']['value']='0.50000000000000000000000000000000000001'
        index['operating_margin_change:fy_t']['value']='0.00000000000000000000000000000000000001'
        result=self.compare()
        self.assertEqual(result['mismatches'],0)
        self.assertEqual(result['numeric_differences'],2)
        index['operating_margin_change:fy_t']['value']='0.00000000000000000000000000000000000002'
        self.assertEqual(self.compare()['mismatches'],1)


class ReconciliationTests(unittest.TestCase):
    def test_matched_and_source_precision_checks_are_verified_by_baseline(self):
        bundle=rich_bundle(values_override={'ending_cash':'20.5'})
        reviews=review_envelope(bundle)
        metadata,records,_,acceptance=shadow.prepare_run(bundle,reconciliations=reviews)
        self.assertEqual(len(acceptance['reconciliations']),8)
        self.assertTrue(all(c['verified'] for c in acceptance['reconciliations']))
        self.assertEqual({c['status'] for c in acceptance['reconciliations']},{'matched','within_precision'})
        self.assertFalse(acceptance['final_report_accepted'])
        self.assertEqual(len([r for r in records if r[0]=='reconciliation_review']),8)
        obs=next(v for k,_,v in records if k=='observation' and v.get('metric')=='ending_cash')
        self.assertEqual(obs['source_quantum'],'0.1')
        self.assertIsNotNone(metadata['reconciliations_hash'])

    def test_forged_review_amount_tolerance_sources_and_terms_are_rejected(self):
        bundle=rich_bundle(values_override={'ending_cash':'20.5'})
        _,_,_,acceptance=shadow.prepare_run(bundle,reconciliations=review_envelope(bundle,forged=True))
        self.assertTrue(all(not c['verified'] for c in acceptance['reconciliations']))
        self.assertEqual({c['status'] for c in acceptance['reconciliations']},{'not_calculable'})

    def test_duplicate_reviews_and_foreign_evidence_are_rejected(self):
        bundle=rich_bundle();reviews=review_envelope(bundle)
        reviews['checks'].append(deepcopy(reviews['checks'][0]))
        with self.assertRaisesRegex(ValueError,'Duplicate reconciliation'):
            shadow.prepare_run(bundle,reconciliations=reviews)
        reviews=review_envelope(bundle)
        next(iter(reviews['evidence'].values()))['entity']='OTHER'
        with self.assertRaises(ValueError):shadow.prepare_run(bundle,reconciliations=reviews)

    def test_comparison_rejects_foreign_missing_and_publishing_rows(self):
        bundle=rich_bundle();_,_,baseline,acceptance=shadow.prepare_run(bundle,reconciliations=review_envelope(bundle))
        rows=[dict(c,run_id=SHADOW_RUN_ID,entity=baseline['entity'],publication_eligible=False) for c in acceptance['reconciliations']]
        self.assertEqual(compare_reconciliations(acceptance,rows,run_id=SHADOW_RUN_ID,entity=baseline['entity'])['mismatches'],0)
        self.assertEqual(compare_reconciliations(acceptance,rows[:-1],run_id=SHADOW_RUN_ID,entity=baseline['entity'])['mismatches'],1)
        rows[0]['publication_eligible']=True
        with self.assertRaisesRegex(ValueError,'cannot grant publication'):
            compare_reconciliations(acceptance,rows,run_id=SHADOW_RUN_ID,entity=baseline['entity'])


class PartialReviewTests(unittest.TestCase):
    def test_missing_reviews_remain_explicit_and_unverified(self):
        bundle=rich_bundle();envelope=review_envelope(bundle)
        envelope['checks']=envelope['checks'][:1]
        _,_,_,acceptance=shadow.prepare_run(bundle,reconciliations=envelope)
        self.assertEqual(len(acceptance['reconciliations']),8)
        self.assertEqual(sum(c['verified'] for c in acceptance['reconciliations']),1)
        self.assertFalse(acceptance['substantive_data_ready'])

    def test_source_and_plan_bindings_are_mandatory_when_provided(self):
        _,_,baseline,_=shadow.prepare_run(rich_bundle())
        rows=[dict(deepcopy(f),fact_id=f['id'],run_id=SHADOW_RUN_ID) for f in baseline['facts'].values()]
        with self.assertRaisesRegex(ValueError,'identity mismatch: source_hash'):
            shadow.compare_facts(baseline,rows,expected_run_id=SHADOW_RUN_ID,expected_bindings={'source_hash':'fixed'})

    def test_duplicate_evidence_ids_cannot_be_hidden_by_set_comparison(self):
        _,_,baseline,_=shadow.prepare_run(rich_bundle())
        rows=[dict(deepcopy(f),fact_id=f['id'],run_id=SHADOW_RUN_ID) for f in baseline['facts'].values()]
        row=next(r for r in rows if r['fact_id']=='revenue:fy_t')
        row['evidence_ids']*=2
        result=shadow.compare_facts(baseline,rows,expected_run_id=SHADOW_RUN_ID)
        self.assertEqual(result['mismatches'],1)


class AcceptanceComparisonTests(unittest.TestCase):
    def setUp(self):
        self.metadata, _, _, self.baseline = shadow.prepare_run(rich_bundle(), run_id=SHADOW_RUN_ID)
        self.bindings = {key:self.metadata[key] for key in
                         ('run_id','entity','scope','source_hash','plan_hash','precision_version')}
        self.row = dict(self.bindings, substantive_data_ready=self.baseline['substantive_data_ready'],
            unavailable_fact_ids=[item['fact_id'] for item in self.baseline['missing_or_pending']],
            acceptance_blockers=list(self.baseline['acceptance_blockers']),
            precision_approved=False, final_report_accepted=False, publication_eligible=False)

    def test_readiness_and_unavailable_coverage_match_without_authorizing_publication(self):
        result = compare_acceptance(self.baseline, [self.row], bindings=self.bindings)
        self.assertEqual(result['mismatches'], 0)
        self.assertFalse(result['publication_eligible'])
        self.row['unavailable_fact_ids'].pop()
        self.assertEqual(compare_acceptance(self.baseline, [self.row], bindings=self.bindings)['differing_fields'],
                         ['unavailable_fact_ids'])

    def test_foreign_duplicate_or_published_acceptance_is_rejected(self):
        for rows in ([], [self.row,self.row], [dict(self.row,run_id='b'*32)],
                     [dict(self.row,publication_eligible=True)], [dict(self.row,final_report_accepted=True)]):
            with self.subTest(rows=rows), self.assertRaises(ValueError):
                compare_acceptance(self.baseline, rows, bindings=self.bindings)


if __name__=='__main__':unittest.main()
