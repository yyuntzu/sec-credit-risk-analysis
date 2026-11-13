"""Review regression cases: no cloud, calculations or narrative generation."""
from concurrent.futures import ThreadPoolExecutor
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
import json
import re
import sqlite3
import tempfile
import unittest
from unittest.mock import MagicMock, patch

from test_loan_review_sources import request_fixture, extract, entry, rows_of
from scripts import agent_runner as runner
from scripts import loan_review_sources as sources


class LegacyCompatibilityTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        patcher = patch.object(runner, 'OUTPUT_DIR', directory.name)
        patcher.start(); self.addCleanup(patcher.stop)

    def loader(self, rows):
        loader = MagicMock()
        loader.client.query.return_value.result.return_value = [
            dict(r, statement_type=statement) for statement, facts in rows.items() for r in facts]
        return loader

    def test_conflicting_versions_block_legacy_before_sum(self):
        financial = extract({'CashAndCashEquivalentsAtCarryingValue': {'units': {'USD': [
            entry(100, start=None), entry(101, start=None, accn='0000000001-26-000002')]}}})
        loader = self.loader(financial)
        for query in (runner.query_kpis_from_bq, runner.query_annual_financials, runner.query_quarterly_financials):
            with self.subTest(query=query.__name__), self.assertRaisesRegex(sources.SourceError, 'conflict'):
                query('SYNTHETIC-ONLY', loader, **({} if query is runner.query_kpis_from_bq else {'period_request': request_fixture('annual' if query is runner.query_annual_financials else 'quarterly')}))
        self.assertEqual(loader.client.query.call_count, 3)

    def test_distinct_durations_are_not_duplicates(self):
        financial = extract({'Revenues': {'units': {'USD': [entry(start='2025-01-01'), entry(start='2025-10-01')]}}})
        with tempfile.TemporaryDirectory() as tmp, patch.object(runner, 'OUTPUT_DIR', tmp):
            _, config, collapsed = runner.prepare_legacy_source_query('SYNTHETIC-ONLY', self.loader(financial))
        self.assertFalse(collapsed)
        self.assertEqual(len(config.query_parameters[0].values), 2)

    def test_readers_use_adopted_snapshot_not_stale_mart(self):
        for query in (runner.query_kpis_from_bq, runner.query_annual_financials, runner.query_quarterly_financials):
            annual = query is runner.query_annual_financials
            endpoint = '2025-12-31' if annual else '2025-06-30'
            loader = MagicMock()
            guard = MagicMock(); guard.result.return_value = []
            raw = MagicMock(); raw.result.return_value = [{'period_end': endpoint, 'revenue_m': 123}]
            loader.client.query.side_effect = [guard, raw]
            kwargs = {} if query is runner.query_kpis_from_bq else {'period_request': request_fixture('annual' if annual else 'quarterly')}
            result = query('SYNTHETIC-ONLY', loader, **kwargs)
            self.assertEqual(result[-1]['revenue_m'], 123)
            self.assertEqual(loader.client.query.call_count, 2)
            self.assertNotIn('.stg_', loader.client.query.call_args.args[0])
            self.assertNotIn('.fct_', loader.client.query.call_args.args[0])

    def test_guard_failure_never_falls_back(self):
        loader = MagicMock(); loader.client.query.side_effect = RuntimeError('BQ unavailable')
        with self.assertRaisesRegex(RuntimeError, 'BQ unavailable'):
            runner.query_kpis_from_bq('SYNTHETIC-ONLY', loader)
        self.assertEqual(loader.client.query.call_count, 1)

    def test_pipeline_returns_error_and_does_not_generate_report(self):
        with patch.object(runner, 'BigQueryLoader') as loader, patch.object(runner, 'ingest_ticker', return_value={}), \
             patch.object(runner, 'run_dbt'), patch.object(runner, 'verify_marts_in_bq'), \
             patch.object(runner, 'generate_credit_memo') as writer, patch.object(runner, 'generate_commentary') as llm:
            loader.return_value.client.query.side_effect = RuntimeError('validation unavailable')
            result = runner.analyze_ticker('SYNTHETIC-ONLY', period_request=request_fixture())
            self.assertEqual(result['status'], 'error')
            self.assertIn('validation unavailable', result['error'])
            writer.assert_not_called(); llm.assert_not_called()


class BoundaryTests(unittest.TestCase):
    def test_malformed_nested_calendar_inputs(self):
        for key in ('periods', 'evidence'):
            for bad in (None, [], 'text', 4):
                request = request_fixture(); request[key][0] = bad
                with self.subTest(key=key, bad=bad), self.assertRaisesRegex(sources.SourceError, key + r'\[0\]'):
                    sources.parse_request(request)
        for key, field in (('periods', 'evidence_ids'), ('evidence', 'period_roles')):
            request = request_fixture(); request[key][0][field] = [None]
            with self.assertRaisesRegex(sources.SourceError, field):
                sources.parse_request(request)

    def test_snapshot_statement_requires_list(self):
        snapshot = {'schema_version': 1, 'entity': 'SYNTHETIC-ONLY', 'cik': '0000000001',
                    'financial_facts': dict(income_statement=None, balance_sheet=[], cash_flow=[])}
        with self.assertRaisesRegex(sources.SourceError, 'must be lists'):
            runner.prepare_loan_review_source_stage('SYNTHETIC-ONLY', request_fixture(), snapshot=snapshot)

    def test_cli_space_and_equals_stay_in_source_branch(self):
        snapshot = {'schema_version': 1, 'entity': 'SYNTHETIC-ONLY', 'cik': '0000000001', 'financial_facts': extract()}
        with tempfile.TemporaryDirectory() as tmp, patch.object(runner, 'OUTPUT_DIR', tmp), \
             patch.object(runner, 'run_dbt') as dbt, patch.object(runner, 'generate_credit_memo') as writer, \
             patch.object(runner, 'generate_commentary') as llm, patch.object(runner, 'SECEdgarClient') as sec:
            req = Path(tmp) / 'request.json'; req.write_text(json.dumps(request_fixture()))
            snap = Path(tmp) / 'snapshot.json'; snap.write_text(json.dumps(snapshot))
            paths = []
            for equals in (False, True):
                argv = ['SYNTHETIC-ONLY']
                for option, value in (('--source-request', req), ('--source-snapshot', snap)):
                    argv += [f'{option}={value}'] if equals else [option, str(value)]
                stdout = StringIO()
                with redirect_stdout(stdout):
                    self.assertEqual(runner.run_source_cli(argv), 0)
                result = json.loads(stdout.getvalue())
                self.assertEqual(result['status'], 'source_inputs_prepared')
                paths.append(result['source_inputs_path'])
            self.assertNotEqual(*paths)
            for mock in (dbt, writer, llm, sec): mock.assert_not_called()

    def test_cli_orphan_options_rejected_and_legacy_arguments_preserved(self):
        for option in ('--source-snapshot=x', '--supplement=x'):
            with redirect_stderr(StringIO()), self.assertRaises(SystemExit) as error:
                runner.run_source_cli(['SYNTHETIC-ONLY', option])
            self.assertEqual(error.exception.code, 2)
        self.assertIsNone(runner.run_source_cli(['WMT', 'META', '--periods', 'FY2025', '--no-html']))

    def test_cli_input_and_io_errors_are_explicit(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'request.json'
            for contents in (None, '{', json.dumps({**request_fixture(), 'periods': [None]})):
                if contents is not None: path.write_text(contents)
                stderr = StringIO()
                with redirect_stderr(stderr):
                    self.assertEqual(runner.run_source_cli(['SYNTHETIC-ONLY', f'--source-request={path}']), 1)
                self.assertEqual(json.loads(stderr.getvalue())['status'], 'error')
                self.assertNotIn('Traceback', stderr.getvalue())


class SnapshotTests(unittest.TestCase):
    def test_parallel_runs_preserve_all_snapshots(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'borrower.json'
            with ThreadPoolExecutor(max_workers=4) as pool:
                paths = list(pool.map(lambda n: sources.write_source_bundle({'run': n}, path), range(8)))
            self.assertEqual(len(set(paths)), 8)
            self.assertEqual([sources.load_json(p)['run'] for p in paths], list(range(8)))
            self.assertFalse(path.exists())

    def test_write_failures_preserve_previous_snapshot_and_cleanup(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'borrower.json'
            saved = sources.write_source_bundle({'mode': 'annual'}, path)
            for operation in ('fsync', 'replace'):
                with patch.object(sources.os, operation, side_effect=OSError('disk failure')):
                    with self.assertRaisesRegex(OSError, 'disk failure'):
                        sources.write_source_bundle({'mode': 'quarterly'}, path)
                self.assertEqual(sources.load_json(saved), {'mode': 'annual'})
                self.assertEqual(list(Path(tmp).iterdir()), [saved.parent])


if __name__ == '__main__':
    unittest.main()
