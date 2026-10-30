"""Equivalent observations collapse only at adoption; raw evidence stays intact."""
from copy import deepcopy
from decimal import Decimal
import json
from pathlib import Path
import re
import sqlite3
import tempfile
import unittest
from unittest.mock import MagicMock, patch

import sqlglot
from test_loan_review_sources import extract, entry, rows_of, request_fixture, supplement
from scripts import agent_runner as runner
from scripts.loan_review_sources import (
    SourceError, prepare_legacy_source_inputs, prepare_source_inputs, load_json,
)
from scripts.sec_client import financial_fact_id


def observations(financial):
    return [dict(r, statement_type=s) for s, rows in financial.items() for r in rows]


def repeated(value=1000000, second=None, start=None, tag='CashAndCashEquivalentsAtCarryingValue'):
    return observations(extract({tag: {'units': {'USD': [
        entry(value, start=start), entry(value if second is None else second, start=start,
                                       accn='0000000001-26-000002', filed='2026-03-01')]}}}))


class EquivalentSourceTests(unittest.TestCase):
    def prepare(self, rows):
        return prepare_legacy_source_inputs(rows, entity='SYNTHETIC-ONLY')

    def test_equal_versions_one_value_all_evidence_order_independent(self):
        rows = repeated()
        a = self.prepare(rows); b = self.prepare(list(reversed(rows)))
        self.assertEqual(a, b)
        self.assertTrue(a['collapsed'])
        self.assertEqual(len(a['statements']['balance_sheet']), 1)
        self.assertEqual(len(a['adoptions'][0]['evidence_ids']), 2)
        self.assertEqual(set(a['adoptions'][0]['evidence_ids']), set(a['evidence']))
        self.assertEqual(len(rows), 2)

    def test_physical_duplicate_is_adopted_once(self):
        row = repeated()[0]
        bundle = self.prepare([row, deepcopy(row)])
        self.assertEqual(len(bundle['statements']['balance_sheet']), 1)
        self.assertEqual(bundle['adoptions'][0]['evidence_ids'], [row['fact_id']])

    def test_precision_difference_not_hidden_by_float_or_display(self):
        with self.assertRaisesRegex(SourceError, 'conflict'):
            self.prepare(repeated(Decimal('1000000.00000000000001'), Decimal('1000000.00000000000002')))

    def test_unknown_identity_scope_currency_definition_block(self):
        for field, value in (('cik', '0000000002'), ('scope', 'subsidiary'), ('unit', 'EUR'),
                             ('xbrl_tag', 'UnapprovedAlternateCashDefinition'), ('source_locator', None)):
            rows = repeated(); rows[1][field] = value; rows[1]['fact_id'] = financial_fact_id(rows[1])
            with self.subTest(field=field), self.assertRaises(SourceError):
                self.prepare(rows)

    def test_different_borrower_never_merges(self):
        rows = repeated(); rows[1]['ticker'] = 'OTHER'; rows[1]['fact_id'] = financial_fact_id(rows[1])
        with self.assertRaises(SourceError): self.prepare(rows)

    def test_missing_and_zero_are_not_equivalent(self):
        rows = repeated(0); rows[1]['original_value'] = None; rows[1]['value'] = None
        rows[1]['fact_id'] = financial_fact_id(rows[1])
        with self.assertRaisesRegex(SourceError, 'conflict'): self.prepare(rows)
        zero = self.prepare(repeated(0))
        self.assertEqual(zero['adoptions'][0]['value'], '0')
        self.assertEqual(zero['adoptions'][0]['status'], 'sourced')

    def test_all_filing_forms_survive_equivalent_representative_selection(self):
        rows = repeated()
        rows[1]['filing_type'] = '10-Q/A'
        rows[1]['fact_id'] = financial_fact_id(rows[1])
        bundle = self.prepare(rows)
        adopted = bundle['statements']['balance_sheet'][0]
        self.assertEqual(adopted['source_forms'], ['10-K', '10-Q'])
        self.assertEqual(len(adopted['evidence_ids']), 2)

    def test_unaudited_rows_block_even_when_numeric_values_match(self):
        rows = repeated(); rows[1].pop('fact_id')
        with self.assertRaises(SourceError): self.prepare(rows)

    def test_numeric_text_format_does_not_change_adoption_with_order(self):
        rows = repeated(Decimal('1000000.0'), Decimal('1000000.00'))
        self.assertEqual(self.prepare(rows), self.prepare(list(reversed(rows))))

    def test_distinct_ytd_quarter_year_intervals_stay_separate(self):
        rows = observations(extract({'Revenues': {'units': {'USD': [
            entry(start=start) for start in ('2025-01-01', '2025-07-01', '2025-10-01')]}}}))
        bundle = self.prepare(rows)
        self.assertEqual(len(bundle['adoptions']), 3)
        self.assertFalse(bundle['collapsed'])

    def test_alternate_tags_are_not_assumed_equivalent(self):
        rows = observations(extract({tag: {'units': {'USD': [entry()]}} for tag in (
            'Revenues', 'RevenueFromContractWithCustomerExcludingAssessedTax')}))
        with self.assertRaisesRegex(SourceError, 'conflict'): self.prepare(rows)

    def test_source_stage_exact_scale_equivalence_and_basis_conflict(self):
        first = supplement(value='1'); second = deepcopy(first)
        second['records'][0].update(value='1000000', scale='1', version='v2')
        bundle = prepare_source_inputs(request_fixture(), [], [first, second])
        value = bundle['inputs']['ltm_ebitda:fy_t']
        self.assertEqual(value['status'], 'sourced'); self.assertEqual(value['value'], '1')
        self.assertEqual(len(value['evidence_ids']), 2)
        second['records'][0]['basis'] = 'Different basis'
        value = prepare_source_inputs(request_fixture(), [], [first, second])['inputs']['ltm_ebitda:fy_t']
        self.assertEqual(value['status'], 'conflict')


class ExecutedLegacyQueryTests(unittest.TestCase):
    def execute(self, sql, config):
        """Execute actual reader SQL against its actual accepted parameter snapshot."""
        sqlglot.parse_one(sql, read='bigquery')
        db = sqlite3.connect(':memory:'); db.row_factory = sqlite3.Row
        try:
            for param in config.query_parameters:
                rows = [json.loads(v) for v in param.values]
                table = param.name
                columns = [f.name for f in runner.FINANCIAL_STATEMENT_SCHEMA] + ['source_forms', 'evidence_ids']
                db.execute(f'CREATE TABLE {table} (' + ','.join(f'"{c}"' for c in columns) + ')')
                for row in rows:
                    values = [row.get(c) for c in columns]
                    values[columns.index('value')] = float(row['value']) if row['value'] is not None else None
                    values = [json.dumps(v) if isinstance(v, list) else v for v in values]
                    db.execute(f'INSERT INTO {table} VALUES ('+','.join('?' for _ in values)+')', values)
            sql = re.sub(r"\(SELECT CAST\(JSON_VALUE\(record,.*?FROM UNNEST\(@(loan_review_\w+)\) AS record\)", r'\1', sql, flags=re.S)
            sql = sql.replace("EXISTS (SELECT 1 FROM UNNEST(source_forms) form WHERE form IN ('10-K','10-Q'))",
                              "(source_forms LIKE '%10-K%' OR source_forms LIKE '%10-Q%')")
            for form in ('10-K', '10-Q'):
                sql = sql.replace(f"'{form}' IN UNNEST(source_forms)", f"source_forms LIKE '%{form}%'")
            sql = re.sub(r'EXTRACT\((YEAR|MONTH)\s+FROM\s+([\w.]+)\)', lambda m: "CAST(STRFTIME('" + ('%Y' if m[1] == 'YEAR' else '%m') + "', " + m[2] + ") AS INTEGER)", sql)
            converted = sqlglot.transpile(sql, read='bigquery', write='sqlite')[0]
            return [dict(r) for r in db.execute(converted)]
        finally:
            db.close()

    def test_canonical_query_failure_never_returns_empty_success(self):
        loader = MagicMock()
        snapshot = MagicMock(); snapshot.result.return_value = repeated()
        loader.client.query.side_effect = [snapshot, RuntimeError('query rejected')]
        with tempfile.TemporaryDirectory() as tmp, patch.object(runner, 'OUTPUT_DIR', tmp):
            with self.assertRaisesRegex(SourceError, 'Canonical legacy source query failed'):
                runner.query_kpis_from_bq('SYNTHETIC-ONLY', loader)
        self.assertEqual(loader.client.query.call_count, 2)

    def test_all_three_readers_consume_once_and_save_all_evidence(self):
        for reader in (runner.query_kpis_from_bq, runner.query_annual_financials, runner.query_quarterly_financials):
            annual = reader is runner.query_annual_financials
            start, end, form = ('2025-01-01', '2025-12-31', '10-K') if annual else ('2025-04-01', '2025-06-30', '10-Q')
            if reader is runner.query_quarterly_financials:
                start = '2025-01-01'  # Comparable YTD, not the discrete third quarter.
            def pair(value, instant=False):
                return [entry(value, start=None if instant else start, end=end, form=form),
                        entry(value, start=None if instant else start, end=end, form=form,
                              accn='0000000001-26-000002', filed='2026-03-01')]
            financial = extract({
                'Revenues': {'units': {'USD': pair(1000000)}},
                'OperatingIncomeLoss': {'units': {'USD': pair(4000000)}},
                'CashAndCashEquivalentsAtCarryingValue': {'units': {'USD': pair(2000000, True)}},
                'NetCashProvidedByUsedInOperatingActivities': {'units': {'USD': pair(3000000)}},
            })
            rows = observations(financial)
            loader = MagicMock()
            def query(sql, job_config=None):
                job = MagicMock()
                if 'AS statement_type, *' in sql:
                    job.result.return_value = rows
                else:
                    self.assertNotIn('.raw_', sql)
                    self.assertNotIn('.stg_', sql)
                    self.assertNotIn('.fct_', sql)
                    job.result.return_value = self.execute(sql, job_config)
                return job
            loader.client.query.side_effect = query
            with self.subTest(reader=reader.__name__), tempfile.TemporaryDirectory() as tmp, patch.object(runner, 'OUTPUT_DIR', tmp):
                kwargs = {} if reader is runner.query_kpis_from_bq else {'period_request': request_fixture('annual' if annual else 'quarterly')}
                result = reader('SYNTHETIC-ONLY', loader, **kwargs)
                self.assertEqual(len(result), 1 if reader is runner.query_kpis_from_bq else 4 if annual else 2)
                result = [r for r in result if r.get('revenue_m') is not None]
                self.assertEqual(len(result), 1)
                self.assertEqual(result[0]['revenue_m'], 1)
                self.assertEqual(result[0]['cash_m'], 2)
                self.assertEqual(result[0]['cfo_m'], 3)
                if reader is runner.query_kpis_from_bq:
                    self.assertIsNone(result[0]['ebitda_m'])
                else:
                    self.assertEqual(result[0]['operating_income_m'], 4)
                self.assertEqual(loader.client.query.call_count, 2)
                saved = load_json(loader.loan_review_source_paths[0])
                self.assertEqual(len(saved['evidence']), 8)
                self.assertTrue(all(len(a['evidence_ids']) == 2 for a in saved['adoptions']))


if __name__ == '__main__':
    unittest.main()
