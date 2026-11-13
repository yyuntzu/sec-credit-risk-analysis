"""Independent numeric/period regressions. Synthetic only, no network or cloud."""
from dataclasses import replace
from datetime import date
from decimal import Decimal as D
from pathlib import Path
import re
import unittest
from unittest.mock import MagicMock, patch

from scripts import agent_runner as runner
from scripts import credit_memo_writer as writer
from scripts.loan_review_contract import (
    approved_formula_value, calculate_fact, calculate_identity, ContractError,
    Evidence, Fact, METRICS, Status,
)
from scripts.loan_review_sources import SourceError
from test_loan_review_contract import fixture, source_fact
from test_loan_review_sources import request_fixture, extract, entry
import test_loan_review_equivalence as equivalence
from test_loan_review_equivalence import observations


class ApprovedArithmeticTests(unittest.TestCase):
    def test_distinct_coverage_with_capitalized_interest(self):
        self.assertEqual(approved_formula_value('CF-04', (D(100), D(20), D(10))), D(4))
        self.assertEqual(approved_formula_value('CF-05', (D(100), D(20), D(30), D(10))), D(5))

    def test_zero_missing_negative_base_and_percentage_points(self):
        self.assertEqual(approved_formula_value('CF-01', (D(0), D(20))), D(0))
        self.assertIsNone(approved_formula_value('CF-01', (D(1), D(0))))
        self.assertIsNone(approved_formula_value('CF-05', (D(100), D(20), None, D(10))))
        self.assertEqual(approved_formula_value('CF-09', (D(-50), D(-100))), D('-.5'))
        self.assertEqual(approved_formula_value('CF-16', (D('.2'), D('.3'))), D('-.1'))

    def test_calculated_fact_retains_lineage_and_fraction_unit(self):
        r = fixture(); role = 'fy_t'
        for metric, value in (('current_assets', 0), ('current_liabilities', 20)):
            spec = METRICS[metric]; fid = metric + ':' + role
            f = Fact(fid, metric, role, Status.MISSING, None, 'money', spec.definition,
                     None, date(2025, 12, 31), r.entity, r.scope, currency='USD',
                     reason='No input yet', period_kind='instant')
            r = replace(r, facts={**r.facts, fid: f})
            r = source_fact(r, fid, D(value))
        r = calculate_fact(r, 'current_ratio:fy_t', input_ids=('current_assets:fy_t', 'current_liabilities:fy_t'), formula_version='1.0')
        f = r.facts['current_ratio:fy_t']
        self.assertEqual(f.value, D(0)); self.assertEqual(f.status, Status.CALCULATED)
        self.assertEqual(f.formula_id, 'CF-01'); self.assertEqual(f.formula_version, '1.0')
        self.assertEqual(f.input_ids, ('current_assets:fy_t', 'current_liabilities:fy_t'))

    def test_coverage_fact_uses_reviewed_inputs_and_preserves_formula_ids(self):
        r = fixture(); role = 'fy_t'
        approval = Evidence('approval', r.entity, r.scope, 'synthetic-only', 'v1', date(2026, 1, 1),
                            'reviewed interest definitions', 'definition', (role,), 'Synthetic reviewed gross interest/capitalized-interest basis')
        r = replace(r, evidence={**r.evidence, 'approval': approval}, decisions={'DEC-05': 'approval'})
        for metric, value in (('pretax_profit', 100), ('interest_expense', 20), ('da', 30), ('capitalized_interest', 10)):
            fid = metric + ':' + role
            if fid not in r.facts:
                f = Fact(fid, metric, role, Status.MISSING, None, 'money', METRICS[metric].definition,
                         date(2025, 1, 1), date(2025, 12, 31), r.entity, r.scope,
                         currency='USD', reason='No input', period_kind='duration')
                r = replace(r, facts={**r.facts, fid: f})
            r = source_fact(r, fid, D(value))
        r = calculate_fact(r, 'interest_coverage:fy_t', input_ids=('pretax_profit:fy_t', 'interest_expense:fy_t', 'capitalized_interest:fy_t'), formula_version='1.0')
        r = calculate_fact(r, 'ebitda_interest:fy_t', input_ids=('pretax_profit:fy_t', 'interest_expense:fy_t', 'da:fy_t', 'capitalized_interest:fy_t'), formula_version='1.0')
        self.assertEqual(r.facts['interest_coverage:fy_t'].value, D(4))
        self.assertEqual(r.facts['ebitda_interest:fy_t'].value, D(5))

    def test_pending_definition_or_missing_inputs_never_computed(self):
        r = calculate_fact(fixture(), 'quick_ratio:fy_t', input_ids=(), formula_version='1.0')
        self.assertEqual(r.facts['quick_ratio:fy_t'].status, Status.NOT_CALCULABLE)
        self.assertIn('DEC-01', r.facts['quick_ratio:fy_t'].reason)
        r = calculate_fact(fixture(), 'current_ratio:fy_t', input_ids=('absent',), formula_version='1.0')
        self.assertIsNone(r.facts['current_ratio:fy_t'].value)

    def test_signed_tax_requires_reviewed_identity_and_preserves_source(self):
        r = fixture(); r = source_fact(r, 'net_income:fy_t', D(80)); r = source_fact(r, 'income_tax:fy_t', D(-20))
        with self.assertRaisesRegex(ContractError, 'CALC-14'):
            calculate_identity(r, 'pretax_profit:fy_t', formula_id='DER-05', input_ids=('net_income:fy_t', 'income_tax:fy_t'), formula_version='1.0', definition_evidence_id='calendar')
        ev = Evidence('bridge', r.entity, r.scope, 'synthetic-reviewed-bridge', 'v1', date(2026, 1, 1),
                      'tax reconciliation', 'definition', ('fy_t',),
                      'Same consolidated net-income/tax basis; no discontinued, NCI or other unresolved bridge items.')
        r = replace(r, evidence={**r.evidence, 'bridge': ev})
        r = calculate_identity(r, 'pretax_profit:fy_t', formula_id='DER-05', input_ids=('net_income:fy_t', 'income_tax:fy_t'), formula_version='1.0', definition_evidence_id='bridge')
        self.assertEqual(r.facts['pretax_profit:fy_t'].value, D(60))
        self.assertEqual(r.facts['income_tax:fy_t'].value, D(-20))
        with self.assertRaisesRegex(ContractError, 'available source'):
            calculate_identity(r, 'pretax_profit:fy_t', formula_id='DER-05', input_ids=('net_income:fy_t', 'income_tax:fy_t'), formula_version='1.0', definition_evidence_id='bridge')


class LegacySafetyTests(unittest.TestCase):
    def test_no_zero_or_proxy_for_unknown_inputs(self):
        r = runner._enrich_rows([{'net_income_m': 80, 'income_tax_m': -20, 'operating_income_m': 100,
                                 'current_ratio': 2, 'cash_m': 500, 'total_debt_m': 300,
                                 'revenue_m': 200, 'cost_of_revenue_m': 50}])[0]
        for key in ('income_before_tax_m', 'ebitda_m', 'quick_ratio_pct', 'debt_ratio_pct',
                    'debt_service_m', 'debt_service_coverage_x', 'interest_coverage_x',
                    'beginning_cash_m', 'net_cash_change_m', 'gross_profit_m', 'total_debt_m'):
            self.assertIsNone(r[key], key)
        r = runner._enrich_rows([{'current_assets_m': 0, 'current_liabilities_m': 20}])[0]
        self.assertEqual(r['current_ratio_pct'], 0)

    def test_incomplete_stale_or_zero_ltm_not_replaced(self):
        for rows in ([{'period_end': '2025-03-31', 'ebitda_m': 100}],
                     [{'period_end': '2024-12-31', 'ttm_ebitda_m': 400}],
                     [{'period_end': '2025-03-31', 'ttm_ebitda_m': 0}]):
            self.assertIsNone(writer._compute_ltm_ebitda(rows, date(2025, 3, 31)))

    def test_unknown_revenue_is_not_one_hundred_percent(self):
        for rev in (None, 0):
            col = writer.PeriodColumn('Reviewed YTD', 'quarterly', {'revenue_m': rev})
            self.assertNotIn('100%', writer._q1_income_table([col]))
        self.assertEqual(writer._pct_change(-50, -100), -.5)
        self.assertEqual(writer._dir(1, 1), 'unchanged')
        self.assertEqual(writer._dir(None, 1), 'not comparable')


class FiscalPeriodTests(unittest.TestCase):
    def test_missing_calendar_fails_before_cloud_and_labels_do_not_prove_dates(self):
        for reader in (runner.query_annual_financials, runner.query_quarterly_financials):
            loader = MagicMock()
            with self.assertRaisesRegex(SourceError, 'Verified fiscal calendar'):
                reader('SYNTHETIC-ONLY', loader)
            loader.client.query.assert_not_called()

    def test_actual_quarter_sql_joins_ytd_not_same_end_qtd(self):
        request = request_fixture('quarterly')
        facts = extract({
            'Revenues': {'units': {'USD': [entry(6000000, '2025-01-01', '2025-06-30', form='10-Q'), entry(2000000, '2025-04-01', '2025-06-30', form='10-Q')]}},
            'NetCashProvidedByUsedInOperatingActivities': {'units': {'USD': [entry(9000000, '2025-01-01', '2025-06-30', form='10-Q'), entry(3000000, '2025-04-01', '2025-06-30', form='10-Q')]}}})
        loader = MagicMock()
        def query(sql, job_config=None):
            job = MagicMock()
            job.result.return_value = (observations(facts) if 'AS statement_type, *' in sql else
                                       equivalence.ExecutedLegacyQueryTests().execute(sql, job_config))
            return job
        loader.client.query.side_effect = query
        import tempfile
        with tempfile.TemporaryDirectory() as tmp, patch.object(runner, 'OUTPUT_DIR', tmp):
            rows = runner.query_quarterly_financials('SYNTHETIC-ONLY', loader, period_request=request)
        self.assertEqual(len(rows), 2); self.assertIsNone(rows[0].get('revenue_m'))
        self.assertEqual(rows[1]['revenue_m'], 6); self.assertEqual(rows[1]['cfo_m'], 9)
        self.assertEqual(rows[1]['period_start'], date(2025, 1, 1))

    def test_noncalendar_dates_and_labels_are_preserved(self):
        request = request_fixture('quarterly')
        updates = [('2022-10-01', '2023-09-30', '2022-10-01'),
                   ('2023-10-01', '2024-03-30', '2023-04-01'),
                   ('2023-10-01', '2024-09-28', '2023-10-01'),
                   ('2024-09-29', '2025-03-29', '2024-03-31')]
        for p, (start, end, ltm) in zip(request['periods'], updates):
            p.update(start=start, end=end, ltm_start=ltm)
        periods, _ = runner._requested_financial_periods(request, 'SYNTHETIC-ONLY', 'quarterly')
        sql = runner._period_sql(periods)
        self.assertIn("DATE '2024-09-29'", sql); self.assertIn("DATE '2025-03-29'", sql)
        self.assertNotIn('EXTRACT', sql); self.assertNotIn('BETWEEN', sql)
        rows = runner._attach_periods([], periods)
        self.assertEqual(rows[-1]['fiscal_year'], 2025)
        self.assertEqual(rows[-1]['period_end'], date(2025, 3, 29))

    def test_dbt_join_keeps_flow_start_and_end(self):
        sql = Path('references/dbt/models/model/intermediate/int_financials_combined.sql').read_text()
        self.assertIn('and inc.period_start = cf.period_start', sql)
        self.assertIn('partition by ticker, period_start, period_end, period_days', sql)


class DbtSyntaxTests(unittest.TestCase):
    def test_models_parse_as_bigquery_after_jinja_rendering(self):
        import sqlglot
        for path in Path('references/dbt/models/model').rglob('*.sql'):
            sql = re.sub(r"\{\{\s*config\(.*?\)\s*\}\}", '', path.read_text(), flags=re.S)
            sql = re.sub(r"\{\{\s*ref\('([^']+)'\)\s*\}\}", r'\1', sql)
            sql = re.sub(r"\{\{\s*source\('([^']+)',\s*'([^']+)'\)\s*\}\}", r'\1.\2', sql)
            if '{%' in sql: continue  # Models with loops are outside this simple renderer.
            with self.subTest(path=path):
                sqlglot.parse_one(sql, read='bigquery')


class EntryAndAsOfTests(unittest.TestCase):
    def test_preflight_missing_calendar_never_ingests(self):
        with patch.object(runner, 'ingest_ticker') as ingest, patch.object(runner, 'BigQueryLoader') as bq:
            result = runner.analyze_ticker('SYNTHETIC-ONLY')
        self.assertEqual(result['status'], 'error')
        self.assertIn('Verified fiscal calendar', result['error'])
        ingest.assert_not_called(); bq.assert_not_called()

    def test_period_cli_reuses_request_schema_without_changing_source_only_cli(self):
        import json, tempfile
        from contextlib import redirect_stdout
        from io import StringIO
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'request.json'; payload = request_fixture('quarterly')
            path.write_text(json.dumps(payload))
            with patch.object(runner, 'analyze_ticker', return_value={'status': 'success', 'final_report_accepted': False}) as analyze, redirect_stdout(StringIO()):
                self.assertEqual(runner.run_period_cli(['SYNTHETIC-ONLY', '--period-request', str(path), '--no-html']), 0)
            self.assertEqual(analyze.call_args.kwargs['period_request'], payload)
            self.assertFalse(analyze.call_args.kwargs['generate_html'])

    def test_future_version_is_excluded_before_adoption_and_audited(self):
        import tempfile
        facts = extract({'Revenues': {'units': {'USD': [
            entry(1000000), entry(9000000, filed='2026-12-01', accn='0000000001-26-000002')]}}})
        loader = MagicMock(); loader.client.query.return_value.result.return_value = observations(facts)
        with tempfile.TemporaryDirectory() as tmp, patch.object(runner, 'OUTPUT_DIR', tmp):
            _, config, _ = runner.prepare_legacy_source_query('SYNTHETIC-ONLY', loader, as_of=date(2026, 10, 20))
            import json
            adopted = [json.loads(v) for v in config.query_parameters[0].values]
            self.assertEqual(len(adopted), 1); self.assertEqual(D(adopted[0]['value']), D(1000000))
            bundle = json.loads(Path(loader.loan_review_source_paths[0]).read_text())
            self.assertEqual(len(bundle['excluded']), 1); self.assertEqual(len(bundle['evidence']), 2)

    def test_cash_flow_survives_missing_income(self):
        import tempfile
        request = request_fixture('quarterly')
        facts = extract({'NetCashProvidedByUsedInOperatingActivities': {'units': {'USD': [entry(9000000, '2025-01-01', '2025-06-30', form='10-Q')]}}})
        loader = MagicMock()
        def query(sql, job_config=None):
            job = MagicMock()
            job.result.return_value = (observations(facts) if 'AS statement_type, *' in sql else
                                       equivalence.ExecutedLegacyQueryTests().execute(sql, job_config))
            return job
        loader.client.query.side_effect = query
        with tempfile.TemporaryDirectory() as tmp, patch.object(runner, 'OUTPUT_DIR', tmp):
            rows = runner.query_quarterly_financials('SYNTHETIC-ONLY', loader, period_request=request)
        self.assertEqual(rows[-1]['cfo_m'], 9); self.assertIsNone(rows[-1]['revenue_m'])


class RequestIdentityTests(unittest.TestCase):
    def test_cik_mismatch_rejected_before_query_adoption(self):
        import tempfile
        facts = extract({'Revenues': {'units': {'USD': [entry()]}}})
        loader = MagicMock(); loader.client.query.return_value.result.return_value = observations(facts)
        with tempfile.TemporaryDirectory() as tmp, patch.object(runner, 'OUTPUT_DIR', tmp):
            with self.assertRaisesRegex(SourceError, 'CIK'):
                runner.prepare_legacy_source_query('SYNTHETIC-ONLY', loader, expected_cik='0000000002')
        self.assertEqual(loader.client.query.call_count, 1)

    def test_conflicting_year_labels_do_not_override_request(self):
        loader = MagicMock()
        with self.assertRaisesRegex(SourceError, 'FY labels conflict'):
            runner.query_annual_financials('SYNTHETIC-ONLY', loader, periods=['FY2025'], period_request=request_fixture())
        loader.client.query.assert_not_called()
