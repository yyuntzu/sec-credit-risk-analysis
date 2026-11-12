"""Delivery behavior only: no live Looker, SEC or warehouse calls."""
import copy
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import MagicMock, patch
from urllib.parse import parse_qs, urlsplit

from scripts.review_delivery import delivery_receipt, validate_looker_config
from scripts import review_workflow as flow
from scripts import agent_runner as runner
from test_loan_review_sources import request_fixture, extract


def config():
    return {'schema_version': 1,
            'report_url': 'https://lookerstudio.google.com/reporting/synthetic-report/page/p1?hl=zh-TW',
            'url_parameter_names': {'entity': 'company', 'run_id': 'review_run', 'mode': 'review_mode'}}


def accepted_manifest():
    return dict(run_id='a'*32, entity='SYNTHETIC & 測試', mode='quarterly', status='accepted',
                final_report_accepted=True, execution='cloud', cloud_status='published', outputs={})


def snapshot():
    return {'schema_version': 1, 'entity': 'SYNTHETIC-ONLY', 'cik': '0000000001', 'financial_facts': extract()}


class DeliveryTests(unittest.TestCase):
    def test_url_preserves_query_and_encodes_exact_entity_run_and_mode(self):
        manifest = accepted_manifest()
        result = delivery_receipt(manifest, config())['looker_studio']
        query = parse_qs(urlsplit(result['url']).query)
        self.assertEqual(query['hl'], ['zh-TW'])
        self.assertEqual(json.loads(query['params'][0]), {
            'company': manifest['entity'], 'review_run': manifest['run_id'], 'review_mode': 'quarterly'})
        self.assertEqual(result['status'], 'link_ready')
        self.assertFalse(result['render_verified'])

    def test_configuration_is_optional_and_no_unfiltered_fallback_is_returned(self):
        result = delivery_receipt(accepted_manifest())
        self.assertEqual(result['looker_studio']['status'], 'not_configured')
        self.assertIsNone(result['looker_studio']['url'])

    def test_draft_failed_local_and_unpublished_runs_have_no_url(self):
        cases = [dict(status='draft', final_report_accepted=False), dict(status='failed'),
                 dict(execution='local', cloud_status='not_requested'),
                 dict(cloud_status='failed'), dict(cloud_status='blocked_delivery')]
        for changes in cases:
            with self.subTest(changes=changes):
                result = delivery_receipt({**accepted_manifest(), **changes}, config())['looker_studio']
                self.assertEqual(result['status'], 'blocked')
                self.assertIsNone(result['url'])

    def test_repeated_runs_produce_different_urls(self):
        original = accepted_manifest()
        first = delivery_receipt(original, config())['looker_studio']['url']
        second = delivery_receipt({**original, 'run_id': 'b'*32}, config())['looker_studio']['url']
        self.assertNotEqual(first, second)

    def test_rejects_ambiguous_or_invalid_configuration(self):
        cases = [dict(schema_version=True), dict(report_url='https://example.com/reporting/x'),
                 dict(report_url='https://lookerstudio.google.com/reporting/x?params=%7B%7D'),
                 dict(url_parameter_names={'entity': 'same', 'run_id': 'same'}),
                 dict(url_parameter_names={'entity': 'company'}),
                 dict(url_parameter_names={'entity': 'company', 'run_id': 'run', 'unknown': 'x'})]
        for changes in cases:
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                validate_looker_config({**config(), **changes})

    def test_draft_run_writes_matching_receipt_and_preserves_local_dashboard(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = flow.run_review('SYNTHETIC-ONLY', request_fixture(), source='snapshot',
                snapshot=snapshot(), output_dir=tmp, excel=False, looker_config=config())
            receipt = json.loads(Path(tmp, 'delivery.json').read_text())
            self.assertEqual(result['delivery'], receipt)
            self.assertEqual(receipt['status'], 'draft')
            self.assertEqual(receipt['periods'][-1]['end'], request_fixture()['periods'][-1]['end'])
            self.assertEqual(receipt['currency'], 'USD')
            self.assertTrue(Path(receipt['local']['dashboard_path']).is_file())
            self.assertIsNone(receipt['looker_studio']['url'])
            self.assertEqual(flow.exit_code(result), 2)

    def test_invalid_configuration_fails_before_creating_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp, 'new')
            with self.assertRaises(ValueError):
                flow.run_review('SYNTHETIC-ONLY', request_fixture(), source='snapshot', snapshot=snapshot(),
                    output_dir=target, excel=False, looker_config={})
            self.assertFalse(target.exists())

    def test_http_forwards_structured_configuration(self):
        with patch('scripts.review_workflow.run_review', return_value={}) as run:
            runner.formal_http_review('SYNTHETIC-ONLY', {'review_request': request_fixture(), 'looker_config': config()})
            self.assertEqual(run.call_args.kwargs['looker_config'], config())

    def test_environment_configuration_is_used(self):
        with tempfile.TemporaryDirectory() as tmp:
            settings = Path(tmp, 'looker.json'); settings.write_text(json.dumps(config()))
            with patch.dict(os.environ, {'LOOKER_STUDIO_CONFIG': str(settings)}):
                result = flow.run_review('SYNTHETIC-ONLY', request_fixture(), source='snapshot', snapshot=snapshot(),
                    output_dir=Path(tmp, 'run'), excel=False)
            self.assertEqual(result['delivery']['looker_studio']['status'], 'blocked')

    def test_final_manifest_failure_retracts_link(self):
        # Stub only the financial acceptance boundary: this test exercises delivery
        # ordering, not whether synthetic financial evidence is actually accepted.
        writer = flow.write_report_artifacts
        def accepted_boundary(*args, **kwargs):
            outputs = writer(*args, **kwargs)
            path = Path(outputs['acceptance_path'])
            acceptance = json.loads(path.read_text())
            acceptance.update(final_report_accepted=True, acceptance_blockers=[])
            path.write_text(json.dumps(acceptance))
            return outputs
        for fails in (False, True):
            with self.subTest(manifest_fails=fails), tempfile.TemporaryDirectory() as tmp:
                cloud = MagicMock()
                cloud.stage_bundle.side_effect = lambda run, entity, bundle: bundle
                recorded = []
                def record(run, entity, manifest):
                    recorded.append(copy.deepcopy(manifest))
                    if fails: raise RuntimeError('manifest unavailable')
                cloud.record_run.side_effect = record
                with patch.object(flow, 'write_report_artifacts', side_effect=accepted_boundary):
                    result = flow.run_review('SYNTHETIC-ONLY', request_fixture(), source='snapshot', snapshot=snapshot(),
                        output_dir=tmp, excel=False, execution='cloud', cloud=cloud, looker_config=config())
                cloud.publish.assert_called_once()
                self.assertEqual(recorded[0]['delivery']['looker_studio']['status'], 'link_ready')
                receipt = json.loads(Path(tmp, 'delivery.json').read_text())
                self.assertEqual(receipt, result['delivery'])
                if fails:
                    self.assertEqual(result['status'], 'failed')
                    self.assertIsNone(receipt['looker_studio']['url'])
                else:
                    self.assertEqual(receipt['looker_studio']['status'], 'link_ready')


if __name__ == '__main__':
    unittest.main()
