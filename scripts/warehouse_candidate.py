"""Receipt-bound, read-only dbt candidate consumer; no financial recalculation.

Hashes bind saved artifacts to a receipt supplied by the caller. They are content
integrity checks, not signatures or a substitute for warehouse IAM. This consumer
can render a draft preview only; it has no publication interface.
"""
from dataclasses import asdict, replace
from datetime import date
from decimal import Decimal, localcontext
import argparse
import hashlib
import json
from pathlib import Path
import re

from .loan_review_contract import Evidence, Fact, Status, validate_report
from .loan_review_sources import canonical, parse_request

VERSION = 'warehouse-candidate-v2'
EXECUTION_VERSION = 'warehouse-execution-v1'
V1_ARTIFACTS = ('source_bundle.json', 'shadow_inputs.json', 'reconciliation_reviews.json',
             'warehouse_facts.json', 'warehouse_reconciliations.json', 'warehouse_acceptance.json', 'kernel_results.json',
             'dbt/run_results_run.json', 'dbt/run_results_test.json', 'dbt/target/manifest.json')
ARTIFACTS = V1_ARTIFACTS + ('warehouse_commentary.json','commentary_documents.json')


def file_hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def _read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _verify_dbt(directory, metadata):
    """Check complete selected-resource coverage, not merely exit code or PASS."""
    receipt = metadata['dbt']
    manifest = _read(directory / 'dbt/target/manifest.json')
    _require(file_hash(directory / 'dbt/target/manifest.json') == receipt['manifest_sha256'],
             'dbt manifest hash mismatch')
    for command, resource_type, good_status in (('run', 'model', 'success'), ('test', 'test', 'pass')):
        path = directory / f'dbt/run_results_{command}.json'
        _require(file_hash(path) == receipt['receipts'][command], 'dbt result hash mismatch')
        result = _read(path)
        expected = {key for key, node in manifest['nodes'].items()
                    if node['resource_type'] == resource_type
                    and 'formal_review_shadow' in node.get('tags', [])
                    and node.get('config', {}).get('enabled', True)}
        actual = [row['unique_id'] for row in result['results']]
        _require(bool(expected) and set(actual) == expected and len(actual) == len(expected),
                 'Incomplete or duplicate dbt resource coverage')
        _require(all(row['status'] == good_status for row in result['results']), 'dbt resources did not all pass')
        _require(result['args']['vars'].get('shadow_run_id') == metadata['run_id'], 'dbt invocation run mismatch')
        if command == 'test':
            _require(result['metadata']['invocation_id'] == receipt['invocation_id'], 'dbt invocation identity mismatch')
            _require(manifest['metadata']['invocation_id'] == receipt['invocation_id'], 'dbt manifest invocation mismatch')
            _require(len(actual) == receipt['tested_resources'], 'dbt test count mismatch')
            _require(file_hash(path) == receipt['run_results_sha256'], 'dbt final result hash mismatch')


def freeze_receipt(directory, metadata):
    """Freeze a completed isolated calculation; never certifies publishability."""
    directory = Path(directory)
    _require(metadata['status'] == 'compared' and metadata['publication_eligible'] is False
             and metadata['precision_approved'] is False, 'Expected an unapproved shadow calculation')
    _verify_dbt(directory, metadata)
    bindings = {key: metadata[key] for key in ('run_id', 'entity', 'scope', 'source_hash', 'plan_hash',
                'code_hash', 'formula_version', 'policy_version', 'precision_version', 'reconciliations_hash', 'commentary_documents_hash')}
    receipt = dict(schema_version=1, consumer_version=VERSION, bindings=bindings,
                   comparison={key: metadata[key] for key in ('mismatches', 'reconciliation_mismatches', 'acceptance_mismatches',
                        'numeric_differences','commentary_mismatches','commentary_numeric_differences')},
                   dbt=metadata['dbt'], artifacts={name: file_hash(directory / name) for name in ARTIFACTS},
                   precision_approved=False, publication_eligible=False)
    if 'canonical_precision_mismatches' in metadata:
        receipt['comparison']['canonical_precision_mismatches']=metadata['canonical_precision_mismatches']
    path = directory / 'calculation_receipt.json'
    with path.open('x', encoding='utf-8') as stream:
        stream.write(json.dumps(receipt, ensure_ascii=False, indent=2))
    return file_hash(path)


def read_candidate(directory, *, expected_receipt_sha256):
    """Rehydrate SQL facts using only request/evidence metadata and pinned receipt.

    No baseline.json, Python calculation/adoption or acceptance engine is read.
    Missing/corrupt evidence is a hard failure; there is no Python value fallback.
    """
    directory = Path(directory)
    _require(isinstance(expected_receipt_sha256, str) and re.fullmatch('[a-f0-9]{64}', expected_receipt_sha256),
             'A pinned calculation receipt hash is required')
    _require(file_hash(directory / 'calculation_receipt.json') == expected_receipt_sha256, 'Calculation receipt hash mismatch')
    receipt = _read(directory / 'calculation_receipt.json')
    _require(receipt['schema_version'] == 1 and receipt['consumer_version'] in ('warehouse-candidate-v1',VERSION,EXECUTION_VERSION),
             'Unsupported calculation receipt')
    _require(receipt['precision_approved'] is False and receipt['publication_eligible'] is False,
             'Candidate reader cannot grant publication')
    if receipt['consumer_version']==EXECUTION_VERSION:
        _require(receipt.get('engine')=='dbt-bigquery-only' and receipt['comparison']=={'status':'not_run','mode':'dbt-only'},
            'Invalid execution-only receipt; comparison was not performed')
    else:
        mismatch_keys = ('mismatches','reconciliation_mismatches','acceptance_mismatches') + (('commentary_mismatches',) if receipt['consumer_version']==VERSION else ())
        _require(all(receipt['comparison'][key] == 0 for key in mismatch_keys),
                 'Candidate comparison contains unresolved mismatches')
        _require(receipt['comparison'].get('canonical_precision_mismatches',0)==0,
                 'Candidate canonical precision comparison failed')
    artifacts = V1_ARTIFACTS if receipt['consumer_version']=='warehouse-candidate-v1' else ARTIFACTS
    _require(set(receipt['artifacts']) == set(artifacts), 'Incomplete candidate artifact coverage')
    for name in artifacts:
        _require(file_hash(directory / name) == receipt['artifacts'][name], 'Candidate artifact hash mismatch: ' + name)
    bindings = receipt['bindings']
    _require(re.fullmatch('[a-f0-9]{32}', bindings['run_id']) is not None, 'Invalid candidate run identity')
    _verify_dbt(directory, dict(bindings, dbt=receipt['dbt']))
    bundle = _read(directory / 'source_bundle.json')
    _require(_digest(bundle) == bindings['source_hash'], 'Candidate source binding mismatch')
    if receipt['consumer_version']==EXECUTION_VERSION:
        _require(_digest(bundle['request'])==bindings['request_hash'],'Execution request binding mismatch')
    reviews = _read(directory / 'reconciliation_reviews.json')
    _require(_digest(reviews) == bindings['reconciliations_hash'], 'Candidate reconciliation binding mismatch')
    if receipt['consumer_version']!='warehouse-candidate-v1':
        _require(_digest(_read(directory/'commentary_documents.json'))==bindings['commentary_documents_hash'],
                 'Candidate commentary documents binding mismatch')
    inputs = _read(directory / 'shadow_inputs.json')
    keys = [(kind, key) for kind, key, _ in inputs]
    _require(len(keys) == len(set(keys)), 'Duplicate candidate input')
    metadatas = [row for kind, key, row in inputs if kind == 'metadata' and key == 'run']
    _require(len(metadatas) == 1, 'Missing candidate metadata')
    metadata = metadatas[0]
    if receipt['consumer_version']==EXECUTION_VERSION:
        _require(metadata.get('calculation_mode')=='dbt-only-candidate' and metadata.get('baseline_comparison')=='not_run',
            'Execution metadata cannot impersonate a shadow comparison')
    _require(all(metadata.get(key) == value for key, value in bindings.items()), 'Candidate metadata binding mismatch')
    _require(metadata['request'] == bundle['request'], 'Candidate request mismatch')
    plans = [row for kind, _, row in inputs if kind == 'slot']
    _require(_digest(plans) == bindings['plan_hash'], 'Candidate plan binding mismatch')
    report, _, _ = parse_request(bundle['request'])
    required = sorted({fid for table in report.tables for row in table.cells for fid in row})
    _require(metadata['required_fact_ids'] == required, 'Candidate required-cell contract mismatch')
    _require((report.entity, report.scope) == (bindings['entity'], bindings['scope']), 'Candidate entity/scope mismatch')
    # Reuse policy *metadata* construction with empty inputs; never adopt/calculate.
    from .loan_review_pipeline import apply_approved_policy, APPROVED_DEFINITIONS, APPROVED_POLICY_VERSION, FORMULA_VERSION
    _require(metadata['approved_definitions'] == APPROVED_DEFINITIONS
             and metadata['policy_version'] == APPROVED_POLICY_VERSION
             and metadata['formula_version'] == FORMULA_VERSION, 'Unsupported candidate policy/formula version')
    report, _ = apply_approved_policy(report, {}, {})
    _require(metadata['formula_version'] == bindings['formula_version']
             and metadata['policy_version'] == bindings['policy_version'], 'Candidate version mismatch')
    evidence = dict(report.evidence)
    for key,value in (reviews or {}).get('evidence',{}).items():
        row = dict(value)
        row['document_date'] = date.fromisoformat(row['document_date'])
        row['period_roles'] = tuple(row['period_roles'])
        item = Evidence(**row)
        _require(item.id==key and key not in evidence,'Candidate reconciliation evidence collision')
        evidence[key] = item
    from .shadow_identity import parse_identity_reviews
    _, identity_evidence = parse_identity_reviews(bundle,plans)
    _require(not set(evidence)&set(identity_evidence),'Candidate identity evidence collision')
    evidence.update(identity_evidence)
    rows = _read(directory / 'warehouse_facts.json')
    index = {}
    plan_index = {p['fact_id']: p for p in plans}
    roles = {}
    for row in rows:
        fid = row['fact_id']
        _require(fid not in index and fid in plan_index, 'Unexpected or duplicate candidate Fact')
        _require(all(row.get(k) == bindings[k] for k in ('run_id', 'entity', 'scope', 'source_hash', 'plan_hash', 'precision_version')),
                 'Candidate Fact binding mismatch')
        _require(row.get('publication_eligible') is False, 'Candidate Fact cannot grant publication')
        plan = plan_index[fid]
        for key in ('metric', 'period_role', 'start', 'end', 'unit', 'currency', 'period_kind'):
            _require(row[key] == plan[key], 'Candidate Fact plan mismatch: ' + key)
        if row['status'] == 'calculated':
            _require(row['formula_id'] == plan['formula_id'] and row['formula_version'] == plan['formula_version']
                     and row['input_ids'] == plan['input_ids'], 'Candidate calculation plan mismatch')
        for eid in set(row.get('candidate_ids', [])) | set(row['evidence_ids']):
            roles.setdefault(eid, set()).add(row['period_role'])
        index[fid] = row
    _require(set(index) == set(plan_index), 'Incomplete candidate Fact coverage')
    for eid, used_roles in roles.items():
        if eid in bundle['evidence']:
            item = bundle['evidence'][eid]
            _require(eid not in evidence, 'Candidate evidence identity collision')
            evidence[eid] = Evidence(eid, item['entity'], item['scope'], item['source_id'], item['version'],
                date.fromisoformat(item['document_date']), item['locator'],
                'fact' if item['status'] == 'sourced' else 'review', tuple(sorted(used_roles)),
                json.dumps({k: item.get(k) for k in ('value', 'unit', 'scale', 'definition', 'basis', 'excerpt', 'source_url', 'reason')}, ensure_ascii=False))
        elif eid.startswith('policy-basis:'):
            role = eid.removeprefix('policy-basis:')
            _require(used_roles == {role}, 'Candidate basis evidence period mismatch')
            approval = evidence[report.decisions['DEC-06']]
            evidence[eid] = replace(approval, id=eid, kind='fact', period_roles=(role,),
                content='User-selected calculation basis; not a company-reported EBITDA amount: ' + metadata['standard_ebitda_basis'])
        else:
            _require(eid in evidence, 'Missing candidate source evidence: ' + eid)
    def number(value):
        if value is None:
            return None
        _require(isinstance(value, str), 'Candidate decimals must be strings, never floats')
        result = Decimal(value)
        _require(result.is_finite(), 'Nonfinite candidate decimal')
        return result
    facts = {}
    for fid, row in index.items():
        textual = row['unit'] == 'text'
        facts[fid] = Fact(fid, row['metric'], row['period_role'], Status(row['status']),
            row['value'] if textual else number(row['value']), row['unit'], row['definition'],
            date.fromisoformat(row['start']) if row['start'] else None,
            date.fromisoformat(row['end']) if row['end'] else None, report.entity, report.scope,
            tuple(row['evidence_ids']), row['original_value'] if textual else number(row['original_value']),
            number(row['original_scale']), row['currency'], row['formula_id'], row['formula_version'],
            tuple(row['input_ids']), '' if row['status'] in ('sourced', 'calculated') else
            'Warehouse candidate: ' + row['status'] + '; inspect source selection and calculation artifacts',
            row['basis'], row['period_kind'])
    report = replace(report, scale=Decimal(metadata['scale']), facts=facts, evidence=evidence)
    # Structure/evidence/lineage checks only. Ample context makes source identity
    # multiplication lossless; division is never recomputed by this consumer.
    with localcontext() as ctx:
        ctx.prec = 256
        validate_report(report, expected_mode=report.mode)
    read_acceptance(directory,receipt)
    return report, receipt


def read_acceptance(directory, receipt):
    rows = _read(Path(directory) / 'warehouse_acceptance.json')
    _require(len(rows) == 1, 'Expected one warehouse acceptance row')
    row = rows[0]
    _require(all(row.get(key) == receipt['bindings'][key] for key in
                 ('run_id', 'entity', 'scope', 'source_hash', 'plan_hash', 'precision_version')),
             'Warehouse acceptance identity mismatch')
    _require(all(row.get(key) is False for key in ('precision_approved', 'final_report_accepted', 'publication_eligible')),
             'Shadow acceptance cannot grant publication')
    _require(row['substantive_data_ready'] == (len(row['acceptance_blockers']) == 0), 'Invalid warehouse acceptance status')
    return row


def read_preview_data(directory, *, expected_receipt_sha256):
    report, receipt = read_candidate(directory, expected_receipt_sha256=expected_receipt_sha256)
    ratio_analysis = None
    if receipt['consumer_version']!='warehouse-candidate-v1':
        from .warehouse_commentary import assemble_analysis, build_narratives
        ratio_analysis,comparisons = assemble_analysis(report,_read(Path(directory)/'warehouse_commentary.json'),
            bindings=receipt['bindings'],documents=_read(Path(directory)/'commentary_documents.json'))
        report = build_narratives(report,comparisons)
    return report, receipt, ratio_analysis


def consumer_code_hash():
    return _digest({name:file_hash(Path(__file__).with_name(name)) for name in (
        'warehouse_candidate.py','warehouse_commentary.py','warehouse_excel.py','export_loan_review_excel.mjs',
        'review_outputs.py','credit_memo_writer.py','review_workflow.py',
        'loan_review_contract.py','loan_review_pipeline.py','formal_commentary.py')})


def write_preview(directory, output_dir, *, expected_receipt_sha256, excel=False):
    report, receipt, ratio_analysis = read_preview_data(directory,expected_receipt_sha256=expected_receipt_sha256)
    target = Path(output_dir)
    target.mkdir(parents=True, exist_ok=False)
    from .review_outputs import write_dashboard
    warehouse_acceptance = read_acceptance(directory, receipt)
    blockers = list(warehouse_acceptance['acceptance_blockers']) + [
                '此頁為影子比對預覽，精度驗證與正式切換尚未放行。',
                '尚未完成全部發布與交付檢查，請勿作為正式授信結論。']
    acceptance = dict(final_report_accepted=False, acceptance_blockers=blockers)
    acceptance['source_limitations'] = ['影子預覽；尚未取得完整精度驗證與正式切換放行，不可作為正式發布結果。']
    acceptance['reconciliations'] = _read(Path(directory) / 'warehouse_reconciliations.json')
    payload = json.dumps(asdict(report), ensure_ascii=False, indent=2, default=str)
    (target / 'report.json').write_text(payload, encoding='utf-8')
    from .formal_commentary import commentary_payload
    (target/'commentary.json').write_text(json.dumps(commentary_payload(report),ensure_ascii=False,indent=2),encoding='utf-8')
    if ratio_analysis is not None:
        (target/'ratio_commentary_analysis.json').write_text(json.dumps(ratio_analysis,ensure_ascii=False,indent=2),encoding='utf-8')
    from .credit_memo_writer import _render_validated_loan_review
    from .loan_review_pipeline import validate_rendered_report
    markdown = _render_validated_loan_review(report, acceptance)
    validate_rendered_report(report, markdown)
    (target / 'report.md').write_text(markdown, encoding='utf-8')
    dashboard = write_dashboard(report, acceptance, target)
    manifest = dict(engine='dbt-bigquery-candidate', consumer_version=VERSION,
        consumer_code_hash=consumer_code_hash(),
        calculation_receipt_sha256=expected_receipt_sha256, bindings=receipt['bindings'],
        precision_approved=False, publication_eligible=False, final_report_accepted=False,
        excel_status='pending' if excel else 'not_requested',
        artifacts={name: file_hash(target / name) for name in ('report.json', 'report.md', 'dashboard.html','commentary.json') +
                   (('ratio_commentary_analysis.json',) if ratio_analysis is not None else ())})
    (target / 'preview_manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    if excel:
        from .warehouse_excel import export_candidate_excel
        export_candidate_excel(directory,target,expected_receipt_sha256=expected_receipt_sha256)
        manifest = _read(target/'preview_manifest.json')
    return dict(manifest, dashboard_path=dashboard)


def main(argv=None):
    parser = argparse.ArgumentParser(description='Read a receipt-bound warehouse candidate; draft preview only')
    parser.add_argument('--shadow-dir', required=True)
    parser.add_argument('--receipt-sha256', required=True, help='Pinned receipt hash supplied by the calculation run')
    parser.add_argument('--output-dir', required=True, help='New preview directory')
    parser.add_argument('--excel',action='store_true',help='Also produce a receipt-bound Excel snapshot with separate local trial')
    args = parser.parse_args(argv)
    print(json.dumps(write_preview(args.shadow_dir, args.output_dir,
        expected_receipt_sha256=args.receipt_sha256,excel=args.excel), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
