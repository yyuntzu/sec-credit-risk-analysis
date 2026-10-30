"""Run-level integration boundaries; no live SEC, cloud writes or LLM calls."""
from contextlib import redirect_stdout
from io import StringIO
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, patch

from scripts import agent_runner as runner
from scripts import review_workflow as flow
from scripts.review_cloud import ReviewCloud
from scripts.review_outputs import report_payload
from test_loan_review_sources import request_fixture, extract
from test_loan_review_pipeline import fixture_book
from scripts.nexstar_workbook_review import build_inputs


def snapshot():
    return {'schema_version': 1, 'entity': 'SYNTHETIC-ONLY', 'cik': '0000000001', 'financial_facts': extract()}


class FormalIntegrationTests(unittest.TestCase):
    def run_local(self, root, **kwargs):
        return flow.run_review('SYNTHETIC-ONLY', request_fixture(), source='snapshot',
            snapshot=snapshot(), output_dir=root, excel=False, **kwargs)

    def test_default_requires_calendar_before_network_or_output(self):
        with patch.object(runner, 'SECEdgarClient') as sec:
            with self.assertRaisesRegex(ValueError, 'Review request required'):
                flow.run_review('AMZN')
            sec.assert_not_called()

    def test_draft_outputs_share_canonical_facts_and_acceptance(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self.run_local(tmp)
            self.assertEqual(result['status'], 'draft')
            self.assertEqual(flow.exit_code(result), 2)
            acceptance = json.loads(Path(tmp, 'acceptance.json').read_text())
            report = json.loads(Path(tmp, 'report.json').read_text())
            dashboard = Path(tmp, 'dashboard.html').read_text()
            self.assertFalse(acceptance['final_report_accepted'])
            self.assertIn('待驗收覆核稿', dashboard)
            for table in report['tables']:
                for row in table['cells']:
                    for fid in row:
                        self.assertIn('data-fact-id="' + fid + '"', dashboard)
                        self.assertIn('data-status="' + report['facts'][fid]['status'] + '"', dashboard)
            self.assertIn('formal-review-integration', report['decisions']['DEC-11'])
            self.assertEqual(json.loads(Path(result['manifest_path']).read_text())['run_id'], result['run_id'])

    def test_existing_run_cannot_be_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.run_local(tmp)
            with self.assertRaisesRegex(ValueError, 'must be empty'): self.run_local(tmp)

    def test_excel_failure_preserves_report_and_dashboard_but_fails_delivery(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(flow, 'export_excel', side_effect=RuntimeError('runtime missing')):
            result = flow.run_review('SYNTHETIC-ONLY', request_fixture(), source='snapshot', snapshot=snapshot(), output_dir=tmp)
            self.assertEqual(flow.exit_code(result), 1)
            self.assertEqual(result['stages']['dashboard'], 'passed')
            self.assertTrue(Path(result['outputs']['report_path']).exists())
            self.assertIn('runtime missing', result['errors']['excel'])

    def test_cloud_roundtrip_before_calculation_and_publication_of_same_report(self):
        cloud = MagicMock()
        cloud.stage_bundle.side_effect = lambda run_id, entity, bundle: bundle
        with tempfile.TemporaryDirectory() as tmp:
            result = self.run_local(tmp, execution='cloud', cloud=cloud)
            self.assertEqual(result['cloud_status'], 'published')
            cloud.ensure.assert_called_once()
            cloud.stage_bundle.assert_called_once()
            run_id, entity, payload, acceptance = cloud.publish.call_args.args
            self.assertEqual(run_id, result['run_id'])
            self.assertEqual(payload, json.loads(Path(tmp, 'report.json').read_text()))
            self.assertEqual(acceptance, json.loads(Path(tmp, 'acceptance.json').read_text()))
            cloud.record_run.assert_called_once()

    def test_cloud_failure_is_not_silently_local_success(self):
        cloud = MagicMock()
        cloud.stage_bundle.side_effect = RuntimeError('dbt unavailable')
        with tempfile.TemporaryDirectory() as tmp:
            result = self.run_local(tmp, execution='cloud', cloud=cloud)
            self.assertEqual(result['status'], 'failed')
            cloud.publish.assert_not_called()
            self.assertFalse(Path(tmp, 'report.json').exists())

    def test_publish_failure_preserves_local_outputs(self):
        cloud = MagicMock()
        cloud.stage_bundle.side_effect = lambda run_id, entity, bundle: bundle
        cloud.publish.side_effect = RuntimeError('dbt test failed')
        with tempfile.TemporaryDirectory() as tmp:
            result = self.run_local(tmp, execution='cloud', cloud=cloud)
            self.assertEqual(result['status'], 'failed')
            self.assertEqual(result['cloud_status'], 'failed')
            self.assertTrue(Path(tmp, 'dashboard.html').exists())

    def test_bigquery_backend_is_reachable(self):
        cloud = MagicMock(project='fixture', dataset='raw')
        from scripts.loan_review_sources import prepare_source_inputs
        bundle = prepare_source_inputs(request_fixture(), [])
        with tempfile.TemporaryDirectory() as tmp, patch.object(runner, 'prepare_loan_review_source_stage', return_value=bundle) as prepare:
            result = flow.run_review('SYNTHETIC-ONLY', request_fixture(), source='bigquery', cloud=cloud, output_dir=tmp, excel=False)
            cloud.dbt.assert_called_once_with('legacy_source')
            self.assertIn('bq_loader', prepare.call_args.kwargs)
            self.assertEqual(result['status'], 'draft')

    def test_workbook_contract_roundtrip(self):
        report, _, _ = build_inputs(fixture_book('E-loan YYYY_Nexstar 2025.xls'), 'annual')
        self.assertEqual(report_payload(flow.restore_report(report_payload(report))), report_payload(report))

    def test_reuse_run_sources_does_not_reextract_or_change_request(self):
        from scripts.loan_review_sources import prepare_source_inputs
        cloud = MagicMock()
        cloud.read_bundle.return_value = prepare_source_inputs(request_fixture(), [])
        with tempfile.TemporaryDirectory() as tmp, patch.object(runner, 'prepare_loan_review_source_stage') as prepare:
            result = flow.run_review('SYNTHETIC-ONLY', request_fixture(), source='bigquery',
                source_run_id='a'*32, cloud=cloud, output_dir=tmp, excel=False)
            self.assertEqual(result['status'], 'draft')
            cloud.read_bundle.assert_called_once_with('a'*32, 'SYNTHETIC-ONLY')
            prepare.assert_not_called()
        changed = request_fixture(); changed['as_of'] = '2026-10-21'
        with tempfile.TemporaryDirectory() as tmp:
            result = flow.run_review('SYNTHETIC-ONLY', changed, source='bigquery', source_run_id='a'*32,
                cloud=cloud, output_dir=tmp, excel=False)
            self.assertEqual(result['status'], 'failed')
            self.assertIn('Stored source request differs', result['errors']['pipeline'])

    def test_workbook_uses_same_output_pipeline(self):
        from scripts import nexstar_workbook_review as workbooks
        book = fixture_book('E-loan YYYY_Nexstar 2025.xls')
        book['observations'] = []
        with tempfile.TemporaryDirectory() as tmp, patch.object(workbooks, 'read_workbook', return_value=book):
            result = flow.run_review('NXST', source='workbook', workbook='fixture.xls', review_date='2026-10-24',
                mode='annual', output_dir=tmp, excel=False)
            self.assertEqual(result['status'], 'draft')
            self.assertTrue(Path(tmp, 'original_cells.json').exists())
            self.assertTrue(Path(tmp, 'dashboard.html').exists())

    def test_ambiguous_options_rejected(self):
        for options in [dict(source='sec', snapshot={}), dict(source='snapshot'),
                        dict(source='sec', workbook='x.xls'), dict(execution='unknown')]:
            with self.subTest(options=options), self.assertRaises(ValueError):
                flow.run_review('SYNTHETIC-ONLY', request_fixture(), **options)

    def test_cli_shell_and_default_agent_entrypoint(self):
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            (tmp/'request.json').write_text(json.dumps(request_fixture()))
            (tmp/'snapshot.json').write_text(json.dumps(snapshot()))
            common = ['SYNTHETIC-ONLY', '--request', str(tmp/'request.json'), '--source-snapshot', str(tmp/'snapshot.json'), '--no-excel']
            env = {**os.environ, 'PYTHON': sys.executable}
            for name, command in [('cli', [sys.executable, str(root/'scripts/agent_runner.py')]),
                                  ('shell', ['bash', str(root/'scripts/run_analysis.sh')])]:
                run = subprocess.run(command + common + ['--output-dir', str(tmp/name)], env=env,
                    capture_output=True, text=True, timeout=30, cwd=tmp)
                self.assertEqual(run.returncode, 2, run.stderr)
                receipt = json.loads(run.stdout)
                self.assertEqual(receipt['status'], 'draft')
                self.assertTrue((tmp/name/'dashboard.html').exists())

    def test_http_formal_and_batch_inputs(self):
        if runner.app is None: self.skipTest('Flask not installed')
        with runner.app.test_client() as client, tempfile.TemporaryDirectory() as tmp, patch.dict(os.environ, {'OUTPUT_DIR': tmp}):
            self.assertEqual(client.post('/analyze/AMZN', json={}).status_code, 400)
            self.assertEqual(client.post('/run', json={'tickers': ['AMZN']}).status_code, 400)
            body = {'review_request': request_fixture(), 'source_snapshot': snapshot(), 'excel': False}
            response = client.post('/analyze/SYNTHETIC-ONLY', json=body)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json()['status'], 'draft')
            response = client.post('/run', json={'reviews': [{'ticker': 'SYNTHETIC-ONLY', **body}]})
            self.assertEqual(response.status_code, 200)
            self.assertFalse(response.get_json()['success'])
            self.assertEqual(client.post('/analyze/SYNTHETIC-ONLY', json={**body, 'excel': 'false'}).status_code, 400)


class CloudStorageTests(unittest.TestCase):
    def test_relocated_virtualenv_dbt_uses_active_interpreter(self):
        cloud = ReviewCloud(project='fixture-project', dataset='raw', client=MagicMock())
        with tempfile.TemporaryDirectory() as tmp:
            executable = str(Path(tmp, 'python'))
            script = Path(tmp, 'dbt'); script.write_text('#!/obsolete/venv/bin/python\n')
            with patch.dict(os.environ), patch('scripts.review_cloud.sys.executable', executable), \
                 patch('scripts.review_cloud.subprocess.run', return_value=MagicMock(returncode=0)) as run:
                os.environ.pop('DBT_EXECUTABLE', None); os.environ.pop('DBT_PYTHON', None)
                cloud.dbt('source')
                self.assertEqual(run.call_args.args[0][:3], [executable, str(script), 'test'])

    def test_run_scoped_source_roundtrip_rejects_partial_reads(self):
        cloud = ReviewCloud(project='fixture-project', dataset='raw', client=MagicMock())
        bundle = {'request': {'entity': 'SYNTHETIC-ONLY'}, 'inputs': {'x': {'value': '1.000000000000000001'}}, 'evidence': {}}
        rows = []
        def capture(table, run_id, entity, records):
            rows.extend(dict(record_kind=kind, record_id=key, payload=json.dumps(value)) for kind, key, value in records)
        cloud.write = capture
        cloud.dbt = MagicMock()
        cloud.client.query.return_value.result.side_effect = lambda: rows
        self.assertEqual(cloud.stage_bundle('a'*32, 'SYNTHETIC-ONLY', bundle), bundle)
        cloud.dbt.assert_called_once_with('source')
        self.assertEqual(cloud.client.query.call_args.kwargs['job_config'].query_parameters[0].value, 'a'*32)
        rows.clear()
        cloud.write = MagicMock()
        with self.assertRaisesRegex(ValueError, 'round-trip'): cloud.stage_bundle('a'*32, 'SYNTHETIC-ONLY', bundle)

    def test_load_job_is_idempotent_for_same_run_payload(self):
        client = MagicMock()
        cloud = ReviewCloud(project='fixture-project', dataset='raw', client=client)
        records = [('fact', 'x', {'value': '1.000000000000000000001'})]
        cloud.write('raw_review_results', 'a'*32, 'X', records)
        first = client.load_table_from_json.call_args.kwargs['job_id']
        cloud.write('raw_review_results', 'a'*32, 'X', records)
        self.assertEqual(client.load_table_from_json.call_args.kwargs['job_id'], first)
        self.assertIn('1.000000000000000000001', client.load_table_from_json.call_args.args[0][0]['payload'])

    def test_dbt_builds_and_tests_explicit_stages(self):
        cloud = ReviewCloud(project='fixture-project', dataset='raw', client=MagicMock())
        with patch.dict(os.environ, {'DBT_EXECUTABLE': 'dbt'}), patch('scripts.review_cloud.subprocess.run', return_value=MagicMock(returncode=0)) as run:
            cloud.dbt('source')
            self.assertEqual(run.call_args_list[0].args[0][1], 'run')
            self.assertEqual(run.call_args_list[1].args[0][1], 'test')
            self.assertIn('stg_loan_review_run_sources', run.call_args.args[0])
            self.assertEqual(run.call_args.kwargs['env']['BQ_DATASET_ID'], 'raw')
        with patch('scripts.review_cloud.subprocess.run', return_value=MagicMock(returncode=1, stderr='failure', stdout='')):
            with self.assertRaisesRegex(RuntimeError, 'failed'): cloud.dbt('publish')


if __name__ == '__main__': unittest.main()
