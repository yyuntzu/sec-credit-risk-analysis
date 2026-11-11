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
    return _run_excel_exporter(directory)


def _run_excel_exporter(directory, *options):
    """Run the shared builder after its caller verifies the proper boundary."""
    dependencies = Path(os.environ.get('REVIEW_RUNTIME_ROOT', Path.home() / '.cache/codex-runtimes/codex-primary-runtime/dependencies'))
    node = os.environ.get('REVIEW_NODE', str(dependencies / 'node/bin/node'))
    packages = Path(os.environ.get('REVIEW_NODE_MODULES', dependencies / 'node/node_modules'))
    if not Path(node).is_file() or not (packages / '@oai/artifact-tool').exists():
        raise RuntimeError('Excel requires bundled Node and @oai/artifact-tool; configure REVIEW_NODE and REVIEW_NODE_MODULES')
    with tempfile.TemporaryDirectory(prefix='loan-review-excel-') as tmp:
        builder = Path(tmp) / 'export.mjs'
        shutil.copyfile(Path(__file__).with_name('export_loan_review_excel.mjs'), builder)
        (Path(tmp) / 'node_modules').symlink_to(packages, target_is_directory=True)
        result = subprocess.run([node, str(builder), str(Path(directory).resolve()), *options], capture_output=True, text=True, timeout=300)
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
               output_dir=None, html=True, excel=True, cloud=None, source_run_id=None,
               commentary=None, commentary_mode='auto', calculation_mode='python',
               shadow_reconciliations=None):
    """Execute once; an unaccepted review is an explicit draft, not a delivery success."""
    if execution not in ('local', 'cloud'): raise ValueError('execution must be local or cloud')
    if calculation_mode not in ('python', 'dbt-shadow'):
        raise ValueError('calculation_mode must be python or dbt-shadow')
    if calculation_mode == 'dbt-shadow' and (execution != 'cloud' or source == 'workbook'):
        raise ValueError('dbt-shadow requires cloud and SEC/snapshot/BigQuery sources; workbook is not supported')
    if shadow_reconciliations is not None and calculation_mode != 'dbt-shadow':
        raise ValueError('shadow_reconciliations requires calculation_mode=dbt-shadow')
    if commentary_mode not in ('auto','model','reviewed','off'): raise ValueError('Invalid commentary mode')
    if commentary_mode=='off' and commentary is not None: raise ValueError('commentary input conflicts with off mode')
    if commentary is not None and (not isinstance(commentary,dict) or set(commentary)-{'documents','claims'}):
        raise ValueError('Commentary input requires documents and optional claims')
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
        calculation_mode=calculation_mode, pipeline_version='formal-review-integration-v1', formula_version=FORMULA_VERSION,
        policy_version=APPROVED_POLICY_VERSION, source_run_id=source_run_id,
        cloud_status='pending' if execution == 'cloud' else 'not_requested', outputs={}, stages={})
    def save():
        write_json(directory / 'run_manifest.json', manifest)
    save()
    try:
        shadow_documents = []
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
        # Commentary has its own auditable stage. Failure keeps numeric drafts;
        # commentary availability is independent of financial acceptance.
        try:
            try:
                from .formal_commentary import collect_sec_documents, validate_documents, apply_commentary, commentary_gaps
                from .mda_commentary import generate_formal_commentary, MODEL
            except ImportError:
                from formal_commentary import collect_sec_documents, validate_documents, apply_commentary, commentary_gaps
                from mda_commentary import generate_formal_commentary, MODEL
            try:
                from .ratio_commentary_analysis import build_ratio_analysis
                from .filing_commentary_sources import document_observations
                from .loan_review_sources import balance_sheet_observations
            except ImportError:
                from ratio_commentary_analysis import build_ratio_analysis
                from filing_commentary_sources import document_observations
                from loan_review_sources import balance_sheet_observations
            generation_model = None
            commentary_input = commentary if commentary is not None else (snapshot or {}).get('commentary')
            if commentary_mode != 'off':
                if commentary_input is None and source!='sec' and commentary_mode in ('model','reviewed'):
                    raise ValueError('Explicit MD&A documents/claims required for this commentary mode')
                if commentary_input is None and source == 'sec' and commentary_mode in ('auto','model'):
                    commentary_input = {'documents':collect_sec_documents(runner.SECEdgarClient(), request)}
                if commentary_input is not None:
                    if request is None:
                        raise ValueError('MD&A requires a verified fiscal request/CIK; workbook provenance alone cannot establish SEC identity')
                    if not isinstance(commentary_input,dict) or set(commentary_input)-{'documents','claims'}:
                        raise ValueError('Invalid commentary input envelope')
                    documents = commentary_input.get('documents', [])
                    if not isinstance(documents,list): raise ValueError('Commentary documents must be a list')
                    validate_documents(report, request, documents)
                    shadow_documents = documents
                    analysis = build_ratio_analysis(report,
                        balance_sheet_observations(bundle) + document_observations(documents), documents)
                    write_json(directory / 'ratio_commentary_analysis.json', analysis)
                    manifest['outputs']['ratio_commentary_analysis_path'] = str(directory / 'ratio_commentary_analysis.json')
                    write_json(directory / 'commentary_inputs.json', dict(documents=documents, claims=commentary_input.get('claims')))
                    manifest['outputs']['commentary_inputs_path'] = str(directory / 'commentary_inputs.json')
                    claims = commentary_input.get('claims')
                    if claims is None and (commentary_mode=='model' or commentary_mode=='auto' and source=='sec'):
                        generation_model=os.environ.get('FORMAL_COMMENTARY_MODEL',os.environ.get('ANTHROPIC_MODEL',MODEL))
                        claims = generate_formal_commentary(report, documents, ratio_analysis=analysis)
                    if claims is None: claims=[]
                    if not isinstance(claims,list): raise ValueError('Commentary claims must be a list')
                    report = apply_commentary(report, request, documents, claims)
                    write_json(directory / 'commentary_inputs.json', dict(documents=documents,claims=claims))
                    manifest['outputs']['commentary_inputs_path']=str(directory/'commentary_inputs.json')
            gaps = commentary_gaps(report)
            manifest['stages']['commentary'] = 'not_requested' if commentary_mode=='off' else 'incomplete' if gaps else 'passed'
            write_json(directory/'commentary_validation.json',dict(complete=not gaps,incomplete_topics=gaps,
                mode=commentary_mode,model=generation_model,version='formal-commentary-balance-sheet-v3',
                semantic_review='Not required; display model summary and source excerpt'))
            manifest['outputs']['commentary_validation_path']=str(directory/'commentary_validation.json')
        except Exception as exc:
            manifest['stages']['commentary']='failed'
            report=replace(report,tables=tuple(replace(t,narratives=tuple(
                replace(n,reason='分析尚未取得：'+str(exc)) for n in t.narratives)) for t in report.tables))
            manifest.setdefault('warnings',{})['commentary']=str(exc)
            write_json(directory/'commentary_validation.json',dict(complete=False,error=str(exc),mode=commentary_mode,version='formal-commentary-balance-sheet-v3'))
            manifest['outputs']['commentary_validation_path']=str(directory/'commentary_validation.json')
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
        if calculation_mode == 'dbt-shadow':
            try:
                from importlib import import_module
                import sys
                package_root = str(Path(__file__).resolve().parents[1])
                if package_root not in sys.path:
                    sys.path.insert(0, package_root)
                run_shadow = import_module("scripts.dbt_shadow").run_shadow
                shadow = run_shadow(bundle, directory / 'dbt_shadow', project=cloud.project,
                                    reconciliations=shadow_reconciliations,commentary_documents=shadow_documents)
                manifest['stages']['dbt_shadow'] = shadow['status']
                manifest['outputs']['dbt_shadow_manifest_path'] = str(directory / 'dbt_shadow' / 'shadow_manifest.json')
                if shadow.get('calculation_receipt_sha256'):
                    manifest['shadow_calculation_receipt_sha256'] = shadow['calculation_receipt_sha256']
                manifest['shadow_comparison'] = {k: shadow[k] for k in ('equivalent', 'mismatches', 'numeric_differences')}
                manifest['shadow_comparison']['reconciliation_mismatches'] = shadow.get('reconciliation_mismatches',0)
                manifest['shadow_comparison']['acceptance_mismatches'] = shadow.get('acceptance_mismatches',0)
                manifest['shadow_comparison']['commentary_mismatches'] = shadow.get('commentary_mismatches',0)
                manifest['shadow_comparison']['commentary_numeric_differences'] = shadow.get('commentary_numeric_differences',0)
                if any(value for key,value in manifest['shadow_comparison'].items() if key!='equivalent'):
                    manifest.setdefault('warnings', {})['dbt_shadow'] = 'Shadow differences recorded; Python remains authoritative; no precision approval or cutover'
            except Exception as exc:
                manifest['stages']['dbt_shadow'] = 'failed'
                manifest.setdefault('errors', {})['dbt_shadow'] = str(exc)
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
    parser.add_argument('--calculation-mode', choices=('python', 'dbt-shadow'), default='python',
                        help='dbt-shadow compares in an isolated dataset; never replaces Python values')
    parser.add_argument('--shadow-reconciliations',
                        help='Structured reconciliation JSON for dbt-shadow only; does not alter report acceptance')
    parser.add_argument('--output-dir')
    parser.add_argument('--no-html', action='store_true')
    parser.add_argument('--no-excel', action='store_true')
    parser.add_argument('--commentary', help='JSON documents/claims bundle; offline unless model mode is selected')
    parser.add_argument('--commentary-mode', choices=('auto','model','reviewed','off'), default='auto')
    args = parser.parse_args(argv)
    try:
        result = run_review(args.ticker, load_json(args.request) if args.request else None,
            source=args.source or ('snapshot' if args.source_snapshot else 'workbook' if args.workbook else 'sec'),
            snapshot=load_json(args.source_snapshot) if args.source_snapshot else None,
            supplements=tuple(load_json(p) for p in args.supplement), workbook=args.workbook,
            review_date=args.review_date, mode=args.mode, quarter=args.quarter,
            execution=args.execution, calculation_mode=args.calculation_mode, output_dir=args.output_dir, html=not args.no_html, excel=not args.no_excel,
            source_run_id=args.source_run_id, commentary=load_json(args.commentary) if args.commentary else None,
            commentary_mode=args.commentary_mode,
            shadow_reconciliations=load_json(args.shadow_reconciliations) if args.shadow_reconciliations else None)
    except (ValueError, OSError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return exit_code(result)


if __name__ == '__main__':
    import sys
    sys.exit(cli(sys.argv[1:]))
