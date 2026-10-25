"""Approved business policies do not substitute for source verification."""
from dataclasses import replace
from decimal import Decimal as D
import unittest
from scripts import loan_review_pipeline as p
from scripts.loan_review_contract import Fact, METRICS, Status, calculate_fact, approved_formula_value
from scripts.credit_memo_writer import render_loan_review
from test_loan_review_contract import fixture, source_fact
from test_loan_review_pipeline import nexstar, fixture_book

class ApprovedPolicyTests(unittest.TestCase):
    def test_millions_preserve_original_tax_and_ratios(self):
        report, acceptance, _, _ = nexstar('E-Loan YQYQ-Nexstar Q1.xls', 'quarterly', 1)
        tax = report.facts['income_tax:current_interim']
        self.assertEqual((tax.value, tax.original_value, tax.original_scale), (D(-7), D(-7000), D(1000)))
        text = render_loan_review(report, acceptance)
        self.assertIn('(7.00)', text)
        self.assertTrue(p.validate_rendered_report(report, text))
        self.assertEqual(report.scale, D(1000000))
        self.assertFalse(acceptance['final_report_accepted'])

    def test_approval_does_not_validate_raw_interest_equity_or_dscr(self):
        report, _, _, _ = nexstar('E-loan YYYY_Nexstar 2025.xls', 'annual')
        self.assertIn('DEC-02', report.decisions)
        self.assertNotIn('DEC-03', report.decisions)
        for key in ('interest_expense:fy_t', 'input:net_worth:fy_t', 'debt_service:fy_t', 'dscr:fy_t'):
            self.assertIsNone(report.facts[key].value)
        self.assertIn('company-specific', report.facts['interest_expense:fy_t'].reason)

    def test_standard_ebitda_signed_tax_and_missing(self):
        self.assertEqual(approved_formula_value('STANDARD-EBITDA-v1', (D(160), D(20), D(-7), D(30))), D(203))
        self.assertIsNone(approved_formula_value('STANDARD-EBITDA-v1', (D(160), D(20), D(-7), None)))

    def ebitda_inputs(self, mode='annual'):
        r, _ = p.apply_approved_policy(fixture(mode), {}, {})
        role = 'fy_t' if mode == 'annual' else 'current_interim'
        period = next(q for q in r.periods if q.role == role)
        for metric, value in [('net_income',160), ('interest_expense',20), ('income_tax',-7), ('da',30)]:
            fid = metric + ':' + role
            if fid not in r.facts:
                f = Fact(fid, metric, role, Status.MISSING, None, 'money', METRICS[metric].definition,
                    period.start, period.end, r.entity, r.scope, currency=r.currency, reason='No source', period_kind='duration')
                r = replace(r, facts={**r.facts, fid:f})
            r = source_fact(r, fid, D(value))
        r = source_fact(r, 'ebitda_basis:'+role, p.STANDARD_EBITDA_BASIS)
        r = replace(r, facts={**r.facts, 'ebitda_basis:'+role:replace(r.facts['ebitda_basis:'+role], basis=p.STANDARD_EBITDA_BASIS)})
        return r, role

    def test_annual_standard_calculation_and_lineage(self):
        r, role = self.ebitda_inputs()
        ids = tuple(m+':'+role for m in ('net_income','interest_expense','income_tax','da'))
        r = calculate_fact(r, 'ltm_ebitda:'+role, input_ids=ids, formula_version=p.APPROVED_POLICY_VERSION)
        self.assertEqual(r.facts['ltm_ebitda:'+role].value, D(203))
        self.assertEqual(r.facts['ltm_ebitda:'+role].input_ids, ids)
        p.validate_arithmetic(r)

    def test_ytd_cannot_be_annualized_as_ltm(self):
        r, role = self.ebitda_inputs('quarterly')
        r = calculate_fact(r, 'ltm_ebitda:'+role,
            input_ids=tuple(m+':'+role for m in ('net_income','interest_expense','income_tax','da')),
            formula_version=p.APPROVED_POLICY_VERSION)
        self.assertIsNone(r.facts['ltm_ebitda:'+role].value)
        self.assertIn('exact LTM', r.facts['ltm_ebitda:'+role].reason)

    def test_leverage_retains_verified_denominator_basis(self):
        r, role = self.ebitda_inputs()
        ids = tuple(m+':'+role for m in ('net_income','interest_expense','income_tax','da'))
        r = calculate_fact(r, 'ltm_ebitda:'+role, input_ids=ids,
                           formula_version=p.APPROVED_POLICY_VERSION)
        r = source_fact(r, 'total_debt:'+role, D(406))
        r = calculate_fact(r, 'total_leverage:'+role,
                           input_ids=('total_debt:'+role, 'ltm_ebitda:'+role),
                           formula_version=p.FORMULA_VERSION)
        self.assertEqual(r.facts['total_leverage:'+role].value, D(2))
        self.assertEqual(r.facts['total_leverage:'+role].basis, p.STANDARD_EBITDA_BASIS)

    def test_debt_definition_excludes_operating_leases(self):
        self.assertIn('exclude operating lease', METRICS['total_debt'].definition)
        self.assertIn('including current portions once', METRICS['total_debt'].definition)


class SourcePolicyAdoptionTests(unittest.TestCase):
    def test_only_verified_gross_interest_adopted(self):
        from scripts.nexstar_workbook_review import build_inputs
        base, inputs, candidates = build_inputs(fixture_book('E-loan YYYY_Nexstar 2025.xls'), 'annual')
        fid='interest_expense:fy_t'
        eid=inputs[fid]['evidence_ids'][0]
        candidates[eid]['definition']=METRICS['interest_expense'].definition
        r, converted=p.apply_approved_policy(base,inputs,candidates)
        r=p.adopt_inputs(r,converted,candidates)
        self.assertEqual(r.facts[fid].status,Status.SOURCED)
        self.assertEqual(r.facts[fid].value*D(1000000),r.facts[fid].original_value*D(1000))
        self.assertIsNone(r.facts['input:capitalized_interest:fy_t'].value)

    def test_reject_debt_candidate_including_operating_leases(self):
        from scripts.nexstar_workbook_review import build_inputs
        base, inputs, candidates = build_inputs(fixture_book('E-loan YYYY_Nexstar 2025.xls'), 'annual')
        fid='total_debt:fy_t'; source=inputs['interest_expense:fy_t']['evidence_ids'][0]
        inputs[fid].update(status='sourced',value=candidates[source]['value'],evidence_ids=[source])
        candidates[source]['definition']='Total debt including operating leases'
        r, converted=p.apply_approved_policy(base,inputs,candidates)
        self.assertEqual(converted[fid]['status'],'not_calculable')
        self.assertIsNone(converted[fid]['value'])

    def test_pipeline_creates_basis_from_approval_only_with_complete_components(self):
        helper=ApprovedPolicyTests()
        r,role=helper.ebitda_inputs()
        fid='ebitda_basis:'+role
        f=r.facts[fid]
        r=replace(r,facts={**r.facts,fid:replace(f,status=Status.MISSING,value=None,original_value=None,reason='No company EBITDA')})
        r=p.calculate_report(r)
        self.assertEqual(r.facts['ltm_ebitda:'+role].value,D(203))
        self.assertEqual(r.facts[fid].value,p.STANDARD_EBITDA_BASIS)

if __name__ == '__main__': unittest.main()
