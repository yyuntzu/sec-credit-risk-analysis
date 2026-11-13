"""Full offline report tests. Real workpaper fixtures are explicitly not SEC facts."""
from dataclasses import replace
from datetime import date
from decimal import Decimal as D
from io import StringIO
from contextlib import redirect_stdout
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts import agent_runner as runner
from scripts import loan_review_pipeline as pipeline
from scripts import nexstar_workbook_review as workbooks
from scripts.credit_memo_writer import render_loan_review
from scripts.loan_review_contract import Status
from scripts.loan_review_sources import prepare_source_inputs
from test_loan_review_sources import extract, entry, request_fixture, rows_of

FIXTURES = json.loads(Path(__file__).with_name('fixtures').joinpath('nexstar_workpaper_cells.json').read_text())


def fixture_book(name):
    source = FIXTURES[name]
    def get(cell): return source['cells'].get(cell, '')
    def locate(block, label):
        low, high = workbooks.BLOCKS[block]
        matches = [r for r in range(low, high+1) if get(f'A{r}') == label]
        if len(matches) != 1: raise ValueError('Ambiguous fixture original label')
        return matches[0]
    return {'path': Path(source['original_path']), 'hash': source['sha256'], 'get': get, 'locate': locate,
            'entity': 'NEXSTAR MEDIA GROUP, INC.', 'review_date': date(2026, 10, 24)}


def nexstar(name, mode, quarter=None):
    book = fixture_book(name)
    base, inputs, candidates = workbooks.build_inputs(book, mode, quarter)
    report, acceptance = pipeline.complete_report(base, inputs, candidates,
        checks=workbooks.reconciliation_checks(book), limitations=('Workpaper only; not SEC verified',))
    return report, acceptance, inputs, candidates


class NexstarGoldenTests(unittest.TestCase):
    def test_year_actual_values_ratios_and_exact_layout(self):
        report, acceptance, inputs, _ = nexstar('E-loan YYYY_Nexstar 2025.xls', 'annual')
        self.assertEqual(report.facts['revenue:fy_t'].value, D(4949))
        self.assertEqual(report.facts['current_ratio:fy_t'].value, D(1473000)/D(711000))
        self.assertEqual(report.facts['gross_margin:fy_t'].value, D(2714)/D(4949))
        self.assertEqual(report.facts['revenue_growth:fy_t'].value, (D(4949)-D(5407))/D(5407))
        text = render_loan_review(report, acceptance)
        self.assertTrue(pipeline.validate_rendered_report(report, text))
        self.assertEqual([len(t.spec.columns)+1 for t in report.tables], [7,5,5,5])
        self.assertFalse(acceptance['final_report_accepted'])
        self.assertIn("DEC-02", report.decisions)
        self.assertNotIn("DEC-03", report.decisions)
        self.assertEqual(report.facts['capitalized_interest:fy_t'].value if 'capitalized_interest:fy_t' in report.facts else report.facts['input:capitalized_interest:fy_t'].value, None)
        self.assertTrue(acceptance['missing_inputs'])

    def test_q2_is_comparable_ytd_not_quarter_or_annualized(self):
        report, acceptance, _, candidates = nexstar('E-Loan YQYQ-Nexstar Q2.xls', 'quarterly', 2)
        self.assertEqual(report.facts['revenue:current_interim'].value, D(3389))
        self.assertEqual(report.facts['revenue:prior_interim'].value, D(2462))
        self.assertEqual(report.facts['gross_margin:current_interim'].value, D(1848)/D(3389))
        self.assertEqual(report.facts['current_ratio:current_interim'].value, D(2005000)/D(1284000))
        self.assertEqual(report.periods[-1].start, date(2026,1,1))
        self.assertIsNone(report.periods[-1].ltm_start)
        self.assertEqual([len(t.spec.columns)+1 for t in report.tables], [5,5,5])
        self.assertFalse(acceptance['final_report_accepted'])
        self.assertIsNone(report.facts['ltm_ebitda:current_interim'].value)
        self.assertIsNone(report.facts['operating_expense:current_interim'].value)
        self.assertIn('1221000.0', {c['value'] for c in candidates.values()})
        self.assertEqual(report.facts['total_debt:current_interim'].status, Status.MISSING)

    def test_q1_negative_tax_benefit_remains_negative(self):
        report, _, _, _ = nexstar('E-Loan YQYQ-Nexstar Q1.xls', 'quarterly', 1)
        self.assertEqual(report.facts['income_tax:current_interim'].value, D(-7))
        self.assertEqual(report.facts['net_income:current_interim'].value, D(160))
        self.assertEqual(report.facts['pretax_profit:current_interim'].value, D(153))

    def test_cf_period_is_unverified_and_fx_is_never_zero_filled(self):
        report, acceptance, _, _ = nexstar('E-loan YYYY_Nexstar 2025.xls', 'annual')
        self.assertEqual(report.facts['cfo:fy_t'].status, Status.NOT_CALCULABLE)
        self.assertIsNone(report.facts['cfo:fy_t'].value)
        self.assertIsNone(report.facts['cash_flow_ratio:fy_t'].value)
        self.assertTrue(all(c['status']=='not_calculable' and c['difference'] is None
                            for c in acceptance['reconciliations'] if c['kind']=='cash_complete_bridge'))

    def test_real_cash_differences_not_patched_or_mislabelled_sec_errors(self):
        expected = {'E-loan YYYY_Nexstar 2025.xls': [D(32),D(3900),D(-12000)],
                    'E-Loan YQYQ-Nexstar Q1.xls': [D(-57000)],
                    'E-Loan YQYQ-Nexstar Q2.xls': [D(130000)]}
        for name, differences in expected.items():
            checks = workbooks.reconciliation_checks(fixture_book(name))
            actual = [c['difference'] for c in checks if c['status']=='unexplained_difference']
            self.assertEqual(actual, differences)
            self.assertTrue(all(c['scale']=='1000' for c in checks if c['unit']=='money'))

    def test_render_and_arithmetic_tampering_rejected(self):
        report, acceptance, _, _ = nexstar('E-loan YYYY_Nexstar 2025.xls', 'annual')
        text = render_loan_review(report, acceptance)
        with self.assertRaisesRegex(ValueError, 'Rendered value'):
            pipeline.validate_rendered_report(report, text.replace('4,949.00', '9,949,000.00', 1))
        with self.assertRaisesRegex(ValueError, 'headings'):
            pipeline.validate_rendered_report(report, '# Cover\n'+text)
        fid='current_ratio:fy_t'
        wrong=replace(report, facts={**report.facts, fid:replace(report.facts[fid],value=D(999))})
        with self.assertRaisesRegex(ValueError,'Arithmetic'):
            pipeline.validate_arithmetic(wrong)

    def test_diagnostic_pass_alone_is_not_substantive_acceptance(self):
        report, _, _, _ = nexstar('E-loan YYYY_Nexstar 2025.xls', 'annual')
        result = pipeline.acceptance_result(report, checks=[{'kind':'arbitrary_PASS','status':'matched'}])
        self.assertFalse(result['substantive_data_ready'])
        self.assertIn('Reconciliation is incomplete or contains unexplained differences', result['acceptance_blockers'])


class FullRunnerTests(unittest.TestCase):
    def test_source_bundle_calculates_renders_and_keeps_mode_even_with_missing_data(self):
        for mode in ('annual','quarterly'):
            request = request_fixture(mode)
            report, acceptance = pipeline.report_from_source_bundle(prepare_source_inputs(request, []))
            text=render_loan_review(report,acceptance)
            self.assertTrue(pipeline.validate_rendered_report(report,text))
            self.assertFalse(acceptance['final_report_accepted'])
            self.assertNotIn('[refer to MD&A]',text)
            self.assertEqual(report.mode.value,mode)

    def test_runner_full_branch_never_calls_legacy_dbt_cloud_or_llm(self):
        payload = request_fixture()
        snapshot={'schema_version':1,'entity':'SYNTHETIC-ONLY','cik':'0000000001','financial_facts':extract()}
        with tempfile.TemporaryDirectory() as tmp, patch.object(runner,'OUTPUT_DIR',tmp), \
             patch.object(runner,'run_dbt') as dbt,patch.object(runner,'_enrich_rows') as enrich, \
             patch.object(runner,'generate_credit_memo') as legacy, patch.object(runner,'generate_commentary') as llm, \
             patch.object(runner,'SECEdgarClient') as sec:
            result=runner.analyze_ticker('SYNTHETIC-ONLY',source_request=payload,source_snapshot=snapshot,
                                        formal_report=True,report_output_dir=str(Path(tmp)/'review'))
            self.assertTrue(result['technical_validation_passed']);self.assertTrue(result['rendered_validation_passed'])
            self.assertFalse(result['final_report_accepted'])
            self.assertTrue(Path(result['report_path']).is_file())
            for mock in (dbt,enrich,legacy,llm,sec):mock.assert_not_called()

    def test_cli_full_roundtrip_and_saved_acceptance(self):
        with tempfile.TemporaryDirectory() as tmp,patch.object(runner,'OUTPUT_DIR',tmp):
            root=Path(tmp); req=root/'request.json'; snap=root/'snapshot.json'
            req.write_text(json.dumps(request_fixture('quarterly')))
            snap.write_text(json.dumps({'schema_version':1,'entity':'SYNTHETIC-ONLY','cik':'0000000001','financial_facts':extract()}))
            stdout=StringIO()
            with redirect_stdout(stdout):
                code=runner.run_report_cli(['SYNTHETIC-ONLY','--report-request',str(req),'--source-snapshot',str(snap),'--output-dir',str(root/'report')])
            self.assertEqual(code,2)  # Technically valid draft is not an accepted delivery.
            receipt=json.loads(stdout.getvalue()); audit=json.loads(Path(receipt['acceptance_path']).read_text())
            self.assertFalse(audit['final_report_accepted']); self.assertTrue(audit['rendered_validation_passed'])

    def test_source_conflict_same_document_different_tags_is_preserved(self):
        payload=request_fixture()
        facts=extract({tag:{'units':{'USD':[entry(1000000)]}} for tag in (
            'Revenues','RevenueFromContractWithCustomerExcludingAssessedTax')})
        bundle=prepare_source_inputs(payload,rows_of(facts))
        report, acceptance=pipeline.report_from_source_bundle(bundle)
        self.assertEqual(report.facts['revenue:fy_t'].status,Status.CONFLICT)
        self.assertIsNone(report.facts['revenue:fy_t'].value)
        self.assertFalse(acceptance['final_report_accepted'])


class BoundaryRegressionTests(unittest.TestCase):
    def test_incompatible_unit_is_unavailable_not_zero_or_conversion(self):
        payload=request_fixture()
        financial=extract({'Revenues':{'units':{'EUR':[entry(1000000)]}}})
        report,acceptance=pipeline.report_from_source_bundle(prepare_source_inputs(payload,rows_of(financial)))
        f=report.facts['revenue:fy_t']
        self.assertIsNone(f.value);self.assertEqual(f.status,Status.NOT_CALCULABLE)
        self.assertIn('compatibility',f.reason)
        self.assertFalse(acceptance['final_report_accepted'])

    def test_actual_zero_remains_available_and_zero_revenue_has_no_common_size(self):
        payload=request_fixture()
        financial=extract({'Revenues':{'units':{'USD':[entry(0)]}}})
        report,acceptance=pipeline.report_from_source_bundle(prepare_source_inputs(payload,rows_of(financial)))
        self.assertEqual(report.facts['revenue:fy_t'].value,D(0))
        self.assertEqual(report.facts['revenue:fy_t'].status,Status.SOURCED)
        self.assertIsNone(report.facts['revenue:pct:fy_t'].value)
        text=render_loan_review(report,acceptance)
        self.assertNotIn('100.00%',text)
        self.assertTrue(acceptance['reconciliations'])

    def test_reviewed_cash_change_can_calculate_without_proxy_bridge(self):
        from test_loan_review_contract import fixture,source_fact
        from scripts.loan_review_contract import Evidence,calculate_fact
        r=source_fact(source_fact(fixture(),'beginning_cash:fy_t',D(50)), 'ending_cash:fy_t',D(70))
        no_review=calculate_fact(r,'cash_change:fy_t',input_ids=('ending_cash:fy_t','beginning_cash:fy_t'),formula_version='1.0')
        self.assertIsNone(no_review.facts['cash_change:fy_t'].value)
        e=Evidence('cash-review',r.entity,r.scope,'synthetic-reviewed-cash-bridge','v1',date(2026,1,1),'complete cash note',
                   'definition',('fy_t',),'Synthetic explicit review of same-basis cash and complete FX/restricted-cash/other adjustments; test only')
        f=replace(r.facts['cash_change:fy_t'],evidence_ids=(e.id,))
        r=replace(r,evidence={**r.evidence,e.id:e},facts={**r.facts,f.id:f})
        r=calculate_fact(r,'cash_change:fy_t',input_ids=('ending_cash:fy_t','beginning_cash:fy_t'),formula_version='1.0')
        self.assertEqual(r.facts['cash_change:fy_t'].value,D(20))
        self.assertIn('cash_change:fy_t',pipeline.validate_arithmetic(r))

    def test_caller_cannot_force_acceptance_of_missing_report(self):
        report,acceptance=pipeline.report_from_source_bundle(prepare_source_inputs(request_fixture(),[]))
        forged={**acceptance,'substantive_data_ready':True,'final_report_accepted':True,'acceptance_blockers':[]}
        with tempfile.TemporaryDirectory() as tmp:
            result=pipeline.write_report_artifacts(report,forged,tmp)
            self.assertFalse(result['final_report_accepted'])
            saved=json.loads(Path(tmp,'acceptance.json').read_text())
            self.assertTrue(saved['acceptance_blockers'])


    def test_renderer_cannot_relabel_metrics_or_periods_even_when_values_unchanged(self):
        report,acceptance,_,_=nexstar('E-loan YYYY_Nexstar 2025.xls','annual')
        text=render_loan_review(report,acceptance)
        with self.assertRaisesRegex(ValueError,'metric label'):
            pipeline.validate_rendered_report(report,text.replace('Revenues／營業收入','Net income／營業收入',1))
        with self.assertRaisesRegex(ValueError,'period binding'):
            pipeline.validate_rendered_report(report,text.replace('2022-01-01～2022-12-31','2021-01-01～2021-12-31',1))
