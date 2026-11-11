"""Consumer tests: no arithmetic fallback, mixed attempts or stale receipts."""
from copy import deepcopy
from dataclasses import asdict
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts import dbt_shadow as shadow
from scripts import warehouse_candidate as consumer
from scripts.loan_review_sources import canonical
from test_dbt_shadow import rich_bundle, SHADOW_RUN_ID
from test_shadow_commentary import fake_commentary_rows


def saved_candidate(directory, *, mutate=None, mode='annual', valid_arithmetic=False):
    """Synthetic dbt artifacts for reader failures; live SQL is tested separately."""
    bundle = rich_bundle(mode)
    metadata, inputs, baseline, _ = shadow.prepare_run(bundle, run_id=SHADOW_RUN_ID)
    rows = [dict(f, fact_id=f['id'], run_id=SHADOW_RUN_ID,
                 source_hash=metadata['source_hash'], plan_hash=metadata['plan_hash'],
                 precision_version=metadata['precision_version'], publication_eligible=False)
            for f in baseline['facts'].values()]
    # Distinct SQL division value proves the reader does not replace with baseline.
    if not valid_arithmetic:
        next(r for r in rows if r['fact_id'] == 'interest_coverage:fy_t')['value'] = '5.83333333333333333333333333333333333333'
    if mutate:
        mutate(rows)
    commentary_baseline=deepcopy(baseline)
    for row in rows:
        if row['fact_id'] in commentary_baseline['facts']:
            commentary_baseline['facts'][row['fact_id']]['value']=row['value']
    payloads = {'source_bundle.json': bundle, 'shadow_inputs.json': inputs,
                'reconciliation_reviews.json': None, 'warehouse_facts.json': rows,
                'warehouse_reconciliations.json': [], 'kernel_results.json': [],
                'commentary_documents.json': [],
                'warehouse_commentary.json': fake_commentary_rows(commentary_baseline,metadata) if not mutate else [],
                'warehouse_acceptance.json': [dict({k:metadata[k] for k in
                    ('run_id','entity','scope','source_hash','plan_hash','precision_version')},
                    substantive_data_ready=False, acceptance_blockers=['Synthetic missing DSCR'],
                    precision_approved=False, final_report_accepted=False, publication_eligible=False)]}
    nodes = {'model.fixture.facts': {'resource_type': 'model', 'tags': ['formal_review_shadow']},
             'test.fixture.integrity': {'resource_type': 'test', 'tags': ['formal_review_shadow']}}
    for command, unique, status in (('run', 'model.fixture.facts', 'success'), ('test', 'test.fixture.integrity', 'pass')):
        payloads[f'dbt/run_results_{command}.json'] = dict(metadata=dict(invocation_id=command),
            args=dict(vars=dict(shadow_run_id=SHADOW_RUN_ID)), results=[dict(unique_id=unique, status=status)])
    payloads['dbt/target/manifest.json'] = dict(metadata=dict(invocation_id='test'), nodes=nodes)
    for name, payload in payloads.items():
        path = directory / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(canonical(payload))
    metadata.update(status='compared', publication_eligible=False, mismatches=0,
                    reconciliation_mismatches=0, acceptance_mismatches=0, numeric_differences=1,
                    commentary_mismatches=0,commentary_numeric_differences=0)
    metadata['dbt'] = dict(invocation_id='test', tested_resources=1,
        receipts={command: consumer.file_hash(directory / f'dbt/run_results_{command}.json') for command in ('run', 'test')},
        run_results_sha256=consumer.file_hash(directory / 'dbt/run_results_test.json'),
        manifest_sha256=consumer.file_hash(directory / 'dbt/target/manifest.json'))
    return metadata


class WarehouseConsumerTests(unittest.TestCase):
    def test_legacy_v1_receipt_still_reads_its_original_snapshot(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)
            consumer.freeze_receipt(path,saved_candidate(path))
            receipt=json.loads((path/'calculation_receipt.json').read_text())
            receipt['consumer_version']='warehouse-candidate-v1'
            receipt['artifacts']={key:value for key,value in receipt['artifacts'].items() if key in consumer.V1_ARTIFACTS}
            receipt['bindings'].pop('commentary_documents_hash')
            for key in ('commentary_mismatches','commentary_numeric_differences'): receipt['comparison'].pop(key)
            (path/'calculation_receipt.json').write_text(canonical(receipt))
            (path/'warehouse_commentary.json').unlink()
            report,_=consumer.read_candidate(path,expected_receipt_sha256=consumer.file_hash(path/'calculation_receipt.json'))
            self.assertEqual(report.entity,'SYNTHETIC-ONLY')

    def test_reads_sql_decimal_without_baseline_or_python_financial_engine(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)
            metadata = saved_candidate(path)
            pinned = consumer.freeze_receipt(path, metadata)
            with (patch('scripts.loan_review_pipeline.report_from_source_bundle', side_effect=AssertionError('fallback')),
                  patch('scripts.loan_review_pipeline.validate_arithmetic', side_effect=AssertionError('recalculation'))):
                report, receipt = consumer.read_candidate(path, expected_receipt_sha256=pinned)
            self.assertEqual(str(report.facts['interest_coverage:fy_t'].value), '5.83333333333333333333333333333333333333')
            self.assertFalse(receipt['publication_eligible'])
            self.assertFalse((path / 'baseline.json').exists())

    def test_receipt_pin_and_every_saved_artifact_are_required(self):
        for artifact in consumer.ARTIFACTS + ('calculation_receipt.json',):
            with self.subTest(artifact=artifact), tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp)
                pinned = consumer.freeze_receipt(path, saved_candidate(path))
                (path / artifact).write_text('{}')
                with self.assertRaisesRegex(ValueError, 'hash mismatch'):
                    consumer.read_candidate(path, expected_receipt_sha256=pinned)
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, 'pinned'):
                consumer.read_candidate(tmp, expected_receipt_sha256=None)

    def test_structural_corruption_fails_even_with_a_fresh_content_receipt(self):
        def wrong_run(rows): rows[0]['run_id'] = 'b' * 32
        def wrong_plan(rows): rows[0]['period_role'] = 'foreign_period'
        def float_value(rows): next(r for r in rows if r['status'] == 'sourced' and r['unit'] != 'text')['value'] = 1.0
        def wrong_formula(rows): next(r for r in rows if r['status'] == 'calculated')['formula_id'] = 'UNKNOWN'
        def missing_source(rows): next(r for r in rows if r['status'] == 'sourced')['evidence_ids'] = ['unregistered']
        def publish(rows): rows[0]['publication_eligible'] = True
        for mutate in (wrong_run, wrong_plan, float_value, wrong_formula, missing_source, publish,
                       lambda rows: rows.append(deepcopy(rows[0])), lambda rows: rows.pop()):
            with self.subTest(mutate=mutate.__name__), tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp)
                pinned = consumer.freeze_receipt(path, saved_candidate(path, mutate=mutate))
                with self.assertRaises(ValueError):
                    consumer.read_candidate(path, expected_receipt_sha256=pinned)

    def test_skipped_or_incomplete_dbt_results_cannot_freeze(self):
        for defect in ('skipped', 'empty', 'run_mismatch'):
            with self.subTest(defect=defect), tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp)
                metadata = saved_candidate(path)
                result = json.loads((path / 'dbt/run_results_test.json').read_text())
                if defect == 'skipped': result['results'][0]['status'] = 'skipped'
                elif defect == 'empty': result['results'] = []
                else: result['args']['vars']['shadow_run_id'] = 'b' * 32
                (path / 'dbt/run_results_test.json').write_text(canonical(result))
                metadata['dbt']['receipts']['test'] = consumer.file_hash(path / 'dbt/run_results_test.json')
                with self.assertRaises(ValueError):
                    consumer.freeze_receipt(path, metadata)

    def test_mismatch_is_not_waived_by_a_receipt(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)
            metadata = saved_candidate(path)
            metadata['mismatches'] = 1
            pinned = consumer.freeze_receipt(path, metadata)
            with self.assertRaisesRegex(ValueError, 'unresolved mismatches'):
                consumer.read_candidate(path, expected_receipt_sha256=pinned)

    def test_preview_uses_sql_values_stays_draft_and_cannot_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'calculation'
            path.mkdir()
            pinned = consumer.freeze_receipt(path, saved_candidate(path))
            preview = Path(tmp) / 'preview'
            with (patch('scripts.loan_review_pipeline.validate_arithmetic',side_effect=AssertionError('Python arithmetic fallback')),
                  patch('scripts.loan_review_pipeline.build_narratives',side_effect=AssertionError('Python comparison fallback')),
                  patch('scripts.ratio_commentary_analysis.build_ratio_analysis',side_effect=AssertionError('Python ratio fallback'))):
                result = consumer.write_preview(path, preview, expected_receipt_sha256=pinned)
            self.assertFalse(result['final_report_accepted'])
            self.assertFalse(result['publication_eligible'])
            self.assertEqual(json.loads((preview / 'report.json').read_text())['facts']['interest_coverage:fy_t']['value'],
                             '5.83333333333333333333333333333333333333')
            self.assertIn('interest_coverage:fy_t', (preview / 'dashboard.html').read_text())
            with self.assertRaises(FileExistsError):
                consumer.write_preview(path, preview, expected_receipt_sha256=pinned)
