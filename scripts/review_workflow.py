"""Unified formal Loan Review orchestration. Local artifacts and cloud publication share one Report."""
from datetime import date, datetime, timezone
from decimal import Decimal
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import uuid

try:
    from . import loan_review_contract as contract
    from .loan_review_sources import load_json, parse_request
    from .loan_review_pipeline import complete_report, report_from_source_bundle, write_report_artifacts, FORMULA_VERSION, APPROVED_POLICY_VERSION
    from .review_outputs import report_payload, write_dashboard
except ImportError:
    import loan_review_contract as contract
    from loan_review_sources import load_json, parse_request
    from loan_review_pipeline import complete_report, report_from_source_bundle, write_report_artifacts, FORMULA_VERSION, APPROVED_POLICY_VERSION
    from review_outputs import report_payload, write_dashboard


def restore_report(data):
    """Rehydrate the existing typed contract, used for workbook source staging."""
    def day(value): return date.fromisoformat(value) if value else None
    periods = tuple(contract.Period(**{**p, 'start': day(p['start']), 'end': day(p['end']),
        'ltm_start': day(p['ltm_start']), 'evidence_ids': tuple(p['evidence_ids'])}) for p in data['periods'])
    evidence = {key: contract.Evidence(**{**e, 'document_date': day(e['document_date']),
        'period_roles': tuple(e['period_roles'])}) for key, e in data['evidence'].items()}
    facts = {}
    for key, f in data['facts'].items():
        f = dict(f)
        f.update(status=contract.Status(f['status']), start=day(f['start']), end=day(f['end']),
                 evidence_ids=tuple(f['evidence_ids']), input_ids=tuple(f['input_ids']))
        for field in ('value', 'original_value', 'original_scale'):
            if f[field] is not None and (field == 'original_scale' or f['unit'] != 'text'):
                f[field] = Decimal(f[field])
        facts[key] = contract.Fact(**f)
    def narrative(n):
        return contract.Narrative(**{**n, **{k: tuple(n[k]) for k in ('fact_ids', 'evidence_ids', 'period_roles')}})
    tables = []
    for table in data['tables']:
        spec = table['spec']
        spec = contract.TableSpec(**{**spec, **{k: tuple(spec[k]) for k in ('columns', 'rows', 'topics')}})
        tables.append(contract.Table(spec, tuple(tuple(r) for r in table['cells']),
            tuple(narrative(n) for n in table['narratives']), tuple(narrative(n) for n in table['notes'])))
    return contract.Report(contract.Mode(data['mode']), data['entity'], data['scope'], data['currency'],
        Decimal(data['scale']), periods, tuple(tuple(h) for h in data['headings']), tuple(tables), facts, evidence, data['decisions'])


def export_excel(directory):
    """Use the bundled runtime; dependencies are never installed into the repository."""
    try:
        from .loan_review_pipeline import validate_saved_artifacts
    except ImportError:
        from loan_review_pipeline import validate_saved_artifacts
    validate_saved_artifacts(directory)
    dependencies = Path(os.environ.get('REVIEW_RUNTIME_ROOT', Path.home() / '.cache/codex-runtimes/codex-primary-runtime/dependencies'))
    node = os.environ.get('REVIEW_NODE', str(dependencies / 'node/bin/node'))
    packages = Path(os.environ.get('REVIEW_NODE_MODULES', dependencies / 'node/node_modules'))
    if not Path(node).is_file() or not (packages / '@oai/artifact-tool').exists():
        raise RuntimeError('Excel requires bundled Node and @oai/artifact-tool; configure REVIEW_NODE and REVIEW_NODE_MODULES')
    with tempfile.TemporaryDirectory(prefix='loan-review-excel-') as tmp:
        builder = Path(tmp) / 'export.mjs'
        shutil.copyfile(Path(__file__).with_name('export_loan_review_excel.mjs'), builder)
        (Path(tmp) / 'node_modules').symlink_to(packages, target_is_directory=True)
        result = subprocess.run([node, str(builder), str(Path(directory).resolve())], capture_output=True, text=True, timeout=300)
        if result.returncode: raise RuntimeError('Excel export failed: ' + result.stderr[-2000:])
    target = Path(directory) / 'loan_review.xlsx'
    if not target.is_file(): raise RuntimeError('Excel exporter did not produce loan_review.xlsx')
    return str(target.resolve())


def write_json(path, value):
    """Atomic replacement inside an already isolated run directory."""
    path = Path(path)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=path.parent, delete=False) as handle:
            temporary = Path(handle.name)
            json.dump(value, handle, ensure_ascii=False, default=str, indent=2)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None: temporary.unlink(missing_ok=True)


def run_review(ticker, request=None, *, source='sec', snapshot=None, supplements=(),
               workbook=None, review_date=None, mode=None, quarter=None, execution='local',
               output_dir=None, html=True, excel=True, cloud=None, source_run_id=None):
    """Execute once; an unaccepted review is an explicit draft, not a delivery success."""
    if execution not in ('local', 'cloud'): raise ValueError('execution must be local or cloud')
    if source not in ('sec', 'snapshot', 'bigquery', 'workbook'): raise ValueError('Unknown source backend')
    if snapshot is not None and source != 'snapshot': raise ValueError('snapshot requires source=snapshot')
    if source == 'snapshot' and snapshot is None: raise ValueError('snapshot source requires a snapshot')
    if source_run_id is not None and source != 'bigquery': raise ValueError('source_run_id requires source=bigquery')
    if source_run_id is not None and supplements: raise ValueError('Stored source bundles are immutable; add supplements using a new source snapshot')
    if source != 'workbook' and (workbook or review_date or quarter is not None or mode is not None): raise ValueError('Workbook options require source=workbook')
    if source == 'workbook' and (request is not None or supplements): raise ValueError('Workbook uses its verified calendar; request/supplements cannot be silently ignored')
    if source != 'workbook':
        if request is None: raise ValueError('Review request required: provide --request with verified fiscal dates, CIK and as_of')
        base, _, _ = parse_request(request)
        if base.entity != ticker.strip().upper(): raise ValueError('Ticker differs from review request')
        entity = base.entity
    else:
        if not workbook or not review_date or mode not in ('annual', 'quarterly'):
            raise ValueError('Workbook requires path, review_date and annual/quarterly mode')
        if (mode == 'quarterly' and quarter not in (1, 2, 3)) or (mode == 'annual' and quarter is not None):
            raise ValueError('quarter 1/2/3 is required only for a quarterly workbook')
        entity = ticker.strip().upper()
    run_id = uuid.uuid4().hex
    directory = Path(output_dir or Path(os.environ.get('OUTPUT_DIR', '/tmp/sec_reports')) / f'review_{run_id}').resolve()
    if directory.exists() and any(directory.iterdir()): raise ValueError('Output directory must be empty; each run has independent artifacts')
    directory.mkdir(parents=True, exist_ok=True)
    manifest = dict(run_id=run_id, entity=entity, execution=execution, source=source, status='running',
        started_at=datetime.now(timezone.utc).isoformat(), final_report_accepted=False,
        pipeline_version='formal-review-integration-v1', formula_version=FORMULA_VERSION,
        policy_version=APPROVED_POLICY_VERSION, source_run_id=source_run_id,
        cloud_status='pending' if execution == 'cloud' else 'not_requested', outputs={}, stages={})
    def save():
        write_json(directory / 'run_manifest.json', manifest)
    save()
    try:
        try:
            from . import agent_runner as runner
        except ImportError:
            import agent_runner as runner
        if execution == 'cloud' or source == 'bigquery':
            if cloud is None:
                try:
                    from .review_cloud import ReviewCloud
                except ImportError:
                    from review_cloud import ReviewCloud
                cloud = ReviewCloud()
        if execution == 'cloud': cloud.ensure()
        if source == 'workbook':
            try:
                from .nexstar_workbook_review import read_workbook, build_inputs, reconciliation_checks
            except ImportError:
                from nexstar_workbook_review import read_workbook, build_inputs, reconciliation_checks
            book = read_workbook(workbook, date.fromisoformat(str(review_date)))
            base, inputs, evidence = build_inputs(book, mode, quarter)
            if entity not in ('NXST', base.entity): raise ValueError('Workbook adapter only supports NXST / its full borrower name')
            entity = base.entity
            manifest['entity'] = entity
            bundle = dict(base_report=report_payload(base), inputs=inputs, evidence=evidence,
                checks=reconciliation_checks(book), limitations=[
                    'User e-loan workpaper; SEC source and CIK not independently verified',
                    'Source publication date unknown; review date does not prove historical as-of availability',
                    'Cash flow periods/bridge and company-specific definitions remain subject to review'])
            write_json(directory / 'original_cells.json', book['observations'])
        elif source == 'bigquery' and source_run_id:
            cloud.dbt('source')
            bundle = cloud.read_bundle(source_run_id, entity)
            if bundle.get('request') != json.loads(json.dumps(request, default=str)):
                raise ValueError('Stored source request differs; select a snapshot to change periods/as_of')
        elif source == 'bigquery':
            # Explicitly build the lossless existing source view before using its reader.
            from types import SimpleNamespace
            cloud.dbt('legacy_source')
            loader = SimpleNamespace(dataset_ref=f'{cloud.project}.{cloud.dataset}', client=cloud.client)
            bundle = runner.prepare_loan_review_source_stage(entity, request, supplements, bq_loader=loader)
        else:
            bundle = runner.prepare_loan_review_source_stage(entity, request, supplements, snapshot=snapshot)
        manifest['stages']['sources'] = 'passed'
        write_json(directory / 'source_inputs.json', bundle)
        if execution == 'cloud':
            bundle = cloud.stage_bundle(run_id, entity, bundle)
            manifest['stages']['cloud_sources'] = 'passed'
        if 'base_report' in bundle:
            report, acceptance = complete_report(restore_report(json.loads(json.dumps(bundle['base_report'], default=str))),
                bundle['inputs'], bundle['evidence'], checks=bundle['checks'], limitations=bundle['limitations'])
        else:
            report, acceptance = report_from_source_bundle(bundle)
        # Latest user authorization includes Dashboard; supersede the historical exclusion.
        from dataclasses import replace
        evidence = dict(report.evidence)
        eid = 'approval:formal-review-integration:DEC-11'
        evidence[eid] = contract.Evidence(eid, report.entity, report.scope, 'user-approved-integration',
            'formal-review-integration-v1', date(2026, 10, 27), 'references/loan-review-integration.md',
            'definition', tuple(p.role for p in report.periods), 'Dashboard authorized; display canonical formal facts and acceptance state')
        report = replace(report, evidence=evidence, decisions={**report.decisions, 'DEC-11': eid})
        outputs = write_report_artifacts(report, acceptance, directory, source_bundle=bundle)
        acceptance = load_json(directory / 'acceptance.json')
        manifest.update(final_report_accepted=acceptance['final_report_accepted'], acceptance_blockers=acceptance['acceptance_blockers'])
        manifest['outputs'].update({k: v for k, v in outputs.items() if k.endswith('_path')})
        for filename in ('source_inputs.json', 'missing_data.csv', 'reconciliations.csv'):
            manifest['outputs'][Path(filename).stem + '_path'] = str(directory / filename)
        manifest.update(mode=report.mode.value, currency=report.currency, scale=str(report.scale))
        manifest['stages']['report'] = 'passed'
        # Each requested output is independent; one failed export must not hide the others.
        for name, enabled, writer in [('dashboard', html, lambda: write_dashboard(report, acceptance, directory)),
                                      ('excel', excel, lambda: export_excel(directory))]:
            if not enabled:
                manifest['stages'][name] = 'not_requested'
                continue
            try:
                manifest['outputs'][name + '_path'] = writer()
                manifest['stages'][name] = 'passed'
            except Exception as exc:
                manifest['stages'][name] = 'failed'
                manifest.setdefault('errors', {})[name] = str(exc)
        if execution == 'cloud':
            if not manifest['final_report_accepted'] or manifest.get('errors'):
                manifest['cloud_status'] = 'blocked_acceptance' if not manifest['final_report_accepted'] else 'blocked_delivery'
                manifest['stages']['cloud_publish'] = 'blocked'
            else:
                try:
                    cloud.publish(run_id, entity, report_payload(report), acceptance)
                    manifest['cloud_status'] = 'published'
                    manifest['stages']['cloud_publish'] = 'passed'
                except Exception as exc:
                    manifest['cloud_status'] = 'failed'
                    manifest['stages']['cloud_publish'] = 'failed'
                    manifest.setdefault('errors', {})['cloud_publish'] = str(exc)
        manifest['status'] = ('failed' if manifest.get('errors') else 'accepted' if manifest['final_report_accepted'] else 'draft')
    except Exception as exc:
        manifest['status'] = 'failed'
        manifest.setdefault('errors', {})['pipeline'] = str(exc)
        if execution == 'cloud': manifest['cloud_status'] = 'failed'
    manifest['finished_at'] = datetime.now(timezone.utc).isoformat()
    manifest['manifest_path'] = str(directory / 'run_manifest.json')
    if execution == 'cloud' and cloud is not None:
        try: cloud.record_run(run_id, entity, manifest)
        except Exception as exc:
            manifest['status'] = 'failed'
            manifest['cloud_status'] = 'failed'
            manifest.setdefault('errors', {})['cloud_manifest'] = str(exc)
    save()
    return manifest


def exit_code(result):
    return 1 if result['status'] == 'failed' else 0 if result['final_report_accepted'] else 2


def cli(argv):
    parser = argparse.ArgumentParser(description='Formal Loan Review: exit 0 accepted, 2 draft, 1 execution failure')
    parser.add_argument('ticker')
    parser.add_argument('--request', '--report-request', '--period-request', dest='request')
    parser.add_argument('--source', choices=('sec', 'snapshot', 'bigquery', 'workbook'))
    parser.add_argument('--source-snapshot')
    parser.add_argument('--source-run-id')
    parser.add_argument('--supplement', action='append', default=[])
    parser.add_argument('--workbook')
    parser.add_argument('--review-date')
    parser.add_argument('--mode', choices=('annual', 'quarterly'))
    parser.add_argument('--quarter', type=int, choices=(1, 2, 3))
    parser.add_argument('--execution', choices=('local', 'cloud'), default='local')
    parser.add_argument('--output-dir')
    parser.add_argument('--no-html', action='store_true')
    parser.add_argument('--no-excel', action='store_true')
    args = parser.parse_args(argv)
    try:
        result = run_review(args.ticker, load_json(args.request) if args.request else None,
            source=args.source or ('snapshot' if args.source_snapshot else 'workbook' if args.workbook else 'sec'),
            snapshot=load_json(args.source_snapshot) if args.source_snapshot else None,
            supplements=tuple(load_json(p) for p in args.supplement), workbook=args.workbook,
            review_date=args.review_date, mode=args.mode, quarter=args.quarter,
            execution=args.execution, output_dir=args.output_dir, html=not args.no_html, excel=not args.no_excel,
            source_run_id=args.source_run_id)
    except (ValueError, OSError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return exit_code(result)


if __name__ == '__main__':
    import sys
    sys.exit(cli(sys.argv[1:]))
