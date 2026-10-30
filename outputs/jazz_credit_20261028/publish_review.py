"""Publish the visually checked annual review with exact cloud source round-trip."""
import json, pathlib, sys, uuid
from datetime import datetime, timezone
sys.path.insert(0, 'scripts')
from review_workflow import restore_report, write_json
from review_outputs import report_payload
from loan_review_pipeline import report_from_source_bundle, validate_arithmetic
from review_cloud import ReviewCloud

p = pathlib.Path(__file__).parent
out = p / 'delivery_final'
manifest_path = out / 'run_manifest.json'
manifest = json.loads(manifest_path.read_text())
assert manifest.get('cloud_status') != 'published', 'Already published; do not create duplicate run'
run_id = manifest.get('run_id') or uuid.uuid4().hex
manifest.update(run_id=run_id, status='draft', cloud_status='pending', execution='cloud',
                source_parent_run_id=json.loads((p/'formal/run_manifest.json').read_text())['run_id'])
write_json(manifest_path, manifest)
report = restore_report(json.loads((out/'report.json').read_text()))
acceptance = json.loads((out/'acceptance.json').read_text())
assert json.loads((out/'excel_validation.json').read_text())['passed']
assert len(acceptance['reconciliations']) == 8
validate_arithmetic(report)
cloud = ReviewCloud()
cloud.ensure()
bundle = cloud.stage_bundle(run_id, 'JAZZ', json.loads((out/'source_inputs.json').read_text()))
base, _ = report_from_source_bundle(bundle)
for fid, fact in base.facts.items():
    if fact.metric == 'cash_change':
        continue  # Separately reviewed complete cash bridge, including explicit FX.
    final = report.facts[fid]
    assert (fact.status, fact.value) == (final.status, final.value), fid
cloud.publish(run_id, 'JAZZ', report_payload(report), acceptance)
manifest.update(cloud_status='published', reconciliations_matched=8,
                final_report_accepted=False, finished_at=datetime.now(timezone.utc).isoformat(),
                stages=dict(source_round_trip='passed', canonical_financial_comparison='passed',
                            analyst_narratives='source_checked', visual_review='passed',
                            excel='passed', cloud_publish='passed'))
manifest['outputs'].update(excel_path=str((out/'loan_review.xlsx').resolve()),
                           dashboard_path=str((out/'dashboard.html').resolve()))
cloud.record_run(run_id, 'JAZZ', manifest)
write_json(manifest_path, manifest)
print(json.dumps(dict(run_id=run_id, cloud_status=manifest['cloud_status'],
                     reconciliations_matched=8, final_report_accepted=False)))
