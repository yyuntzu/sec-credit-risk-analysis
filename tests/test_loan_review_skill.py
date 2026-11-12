from copy import deepcopy
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch,MagicMock

from scripts import loan_review_skill as skill
from test_dbt_shadow import rich_bundle


class LoanReviewSkillTests(unittest.TestCase):
    def setUp(self):
        from scripts.warehouse_source import source_envelope
        class SourceStore:
            def __init__(self,*args,**kwargs):pass
            def ensure(self):pass
            def store(self,envelope):
                self.envelope=deepcopy(envelope)
                return dict(source_id='1'*64)
            def load(self,receipt):return deepcopy(self.envelope)
        self.source_patch=patch.object(skill,'BigQuerySourceStore',SourceStore)
        self.source_patch.start();self.addCleanup(self.source_patch.stop)
    def test_missing_request_and_mismatched_borrower_stop_before_cloud(self):
        with tempfile.TemporaryDirectory() as tmp,patch.object(skill,'GCSCandidateControlStore') as cloud:
            missing=skill.run_skill_review('AMZN',output_dir=Path(tmp)/'missing')
            wrong=skill.run_skill_review('AMZN',bundle=rich_bundle(),output_dir=Path(tmp)/'wrong')
            self.assertEqual(missing['status'],'failed');self.assertEqual(wrong['status'],'failed')
            self.assertIn('verified',missing['error']);self.assertIn('Ticker',wrong['error'])
            cloud.assert_not_called()

    def test_bundle_cannot_ignore_other_sources_or_override_request(self):
        bundle=rich_bundle();changed=deepcopy(bundle['request']);changed['as_of']='2026-10-21'
        for kwargs in (dict(snapshot={}),dict(supplements=({},)),dict(request=changed)):
            with self.assertRaises(ValueError):
                skill.prepare_sources('SYNTHETIC-ONLY',kwargs.pop('request',None),bundle=bundle,**kwargs)

    def test_snapshot_source_uses_only_existing_source_adapter(self):
        bundle=rich_bundle();snapshot={'schema_version':1}
        with patch('scripts.agent_runner.prepare_loan_review_source_stage',return_value=bundle) as adapter:
            self.assertEqual(skill.prepare_sources('SYNTHETIC-ONLY',bundle['request'],snapshot=snapshot),bundle)
            adapter.assert_called_once_with('SYNTHETIC-ONLY',bundle['request'],(),snapshot=snapshot)

    def test_invalid_runtime_cannot_promote_production(self):
        for changes in (dict(execution='production'),dict(candidate_bucket='production-bucket'),
                        dict(archive_dataset='sec_raw'),dict(precision_version='unapproved')):
            with self.assertRaises(ValueError):skill.runtime_configuration(**changes)

    def test_sec_source_requires_real_contact_before_network(self):
        bundle=rich_bundle()
        with patch.dict(os.environ,{'SEC_USER_AGENT':'contact@example.com'}), \
             patch('scripts.agent_runner.prepare_loan_review_source_stage') as fetch:
            with self.assertRaisesRegex(ValueError,'SEC_USER_AGENT'):
                skill.prepare_sources('SYNTHETIC-ONLY',bundle['request'])
            fetch.assert_not_called()

    def test_selected_runtime_failure_preserves_inputs_without_fallback(self):
        with tempfile.TemporaryDirectory() as tmp,patch.object(skill,'GCSCandidateControlStore'), \
             patch.object(skill,'execute_selected',side_effect=ValueError('Missing pinned runtime')) as execute, \
             patch.object(skill,'write_preview') as preview:
            result=skill.run_skill_review('SYNTHETIC-ONLY',bundle=rich_bundle(),output_dir=Path(tmp)/'run')
            self.assertEqual(result['status'],'failed');self.assertIn('Missing pinned',result['error'])
            self.assertTrue(Path(result['manifest_path']).is_file());preview.assert_not_called()
            self.assertEqual(execute.call_args.kwargs['expected_precision_version'],'bignumeric-q18-half-even-v1')

    def test_default_flow_delivers_and_archives_same_pinned_calculation(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory=Path(tmp)/'run';order=[];bundle=rich_bundle()
            def selected(control,source,output,**kwargs):
                order.append('sql');self.assertEqual(json.loads(Path(source).read_text()),json.loads(json.dumps(skill.reconciliation_slots(bundle),default=str)))
                Path(output).mkdir();(Path(output)/'selected_execution_receipt.json').write_text('{}')
                return dict(execution=dict(calculation_receipt_sha256='a'*64,run_id='1'*32),release_id='9'*32,package_sha256='b'*64)
            def preview(calculation,output,**kwargs):
                order.append('report');self.assertTrue(kwargs['excel']);self.assertEqual(kwargs['expected_receipt_sha256'],'a'*64)
                Path(output).mkdir()
                for filename in ('report.md','report.json','dashboard.html','loan_review.xlsx','preview_manifest.json'):
                    (Path(output)/filename).write_text('{}')
            def archive(calculation,output,**kwargs):
                order.append('archive');self.assertEqual(kwargs['receipt_sha256'],'a'*64)
                Path(output).mkdir();(Path(output)/'archive_receipt.json').write_text('{}');return dict(status='stored')
            storage=MagicMock();storage.store.return_value={'generation':'1'}
            with patch.object(skill,'GCSCandidateControlStore'),patch.object(skill,'execute_selected',side_effect=selected), \
                 patch.object(skill,'write_preview',side_effect=preview),patch.object(skill,'archive_calculation',side_effect=archive), \
                 patch.object(skill,'prepare_delivery',return_value=({},{})) as prepare, \
                 patch.object(skill,'ShadowDeliveryStorage',return_value=storage), \
                 patch.object(skill,'inspect_candidate',return_value=dict(financial_readiness=False,blockers=['incomplete'])):
                result=skill.run_skill_review('SYNTHETIC-ONLY',bundle=bundle,output_dir=directory)
            self.assertEqual(result['status'],'draft',result.get('error'));self.assertEqual(order,['sql','report','archive'])
            self.assertFalse(result['final_report_accepted']);self.assertFalse(result['publication_eligible'])
            self.assertTrue(Path(result['outputs']['loan_review.xlsx']).is_file())
            self.assertEqual(prepare.call_args.kwargs['calculation_pin'],'a'*64)
            self.assertTrue(prepare.call_args.kwargs['require_excel']);storage.store.assert_called_once()

    def test_export_failure_retains_numeric_outputs_and_blocks_storage(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory=Path(tmp)/'run'
            def selected(control,source,output,**kwargs):
                Path(output).mkdir();(Path(output)/'selected_execution_receipt.json').write_text('{}')
                return dict(execution=dict(calculation_receipt_sha256='a'*64,run_id='1'*32),release_id='9'*32,package_sha256='b'*64)
            def preview(calculation,output,**kwargs):
                Path(output).mkdir();(Path(output)/'report.md').write_text('numeric draft')
                raise RuntimeError('Excel runtime unavailable')
            with patch.object(skill,'GCSCandidateControlStore'),patch.object(skill,'execute_selected',side_effect=selected), \
                 patch.object(skill,'write_preview',side_effect=preview),patch.object(skill,'archive_calculation') as archive:
                result=skill.run_skill_review('SYNTHETIC-ONLY',bundle=rich_bundle(),output_dir=directory)
            self.assertEqual(result['status'],'failed');self.assertIn('Excel',result['error'])
            self.assertEqual(result['stages']['report'],'failed')
            self.assertTrue(Path(result['outputs']['report.md']).exists());archive.assert_not_called()

    def test_cli_successful_candidate_is_exit_two(self):
        with patch.object(skill,'run_skill_review',return_value=dict(status='draft')) as run,patch('builtins.print'):
            self.assertEqual(skill.main(['SYNTHETIC-ONLY','--no-excel']),2)
            self.assertFalse(run.call_args.kwargs['excel'])

    def test_resume_cannot_silently_ignore_new_source_inputs(self):
        with self.assertRaisesRegex(ValueError,'Resume cannot change'):
            skill.main(['--resume-publication','/not-read','--source-bundle','/other-source'])
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'publication_receipt.json').write_text('{}')
            with patch.object(skill,'BigQueryPublicationStore') as store,self.assertRaisesRegex(ValueError,'pin mismatch'):
                skill.finalize_publication(root,dict(publication_receipt_sha256='0'*64))
            store.assert_not_called()
