"""Loan Review skill: sources -> pinned SQL runtime -> draft delivery and storage.

No Python financial engine, legacy fallback or production publication is invoked.
Exit 2 means the candidate was generated successfully; exit 1 means execution failed.
"""
import argparse
from datetime import datetime,timezone
import json
import os
from pathlib import Path
import re
import uuid

from .candidate_release_control import CandidateReleaseControl,GCSCandidateControlStore
from .selected_runtime import execute_selected
from .warehouse_candidate import file_hash,_require,write_preview
from .loan_review_sources import load_json,parse_request,canonical
from .candidate_archive import archive_calculation
from .delivery_archive import prepare_delivery,ShadowDeliveryStorage
from .publication_preflight import inspect_candidate

ROOT=Path(__file__).resolve().parents[1]


def runtime_configuration(path=None,**overrides):
    config=load_json(path or ROOT/'references/loan-review-runtime.json')
    for field,value in overrides.items():
        if value is not None:config[field]=value
    _require(config.get('schema_version')==1 and config.get('execution')=='candidate','Candidate runtime configuration required')
    _require(config['precision_version']=='bignumeric-q18-half-even-v1','Unsupported skill precision policy')
    _require(re.fullmatch('[a-z][a-z0-9-]+',config['project']) is not None,'Invalid project')
    for field in ('candidate_bucket','delivery_bucket'):
        _require(re.fullmatch('sec-review-shadow-[a-z0-9-]+',config[field]) is not None,'Isolated candidate bucket required')
    _require(re.fullmatch('sec_review_shadow_[a-z0-9_]+',config['archive_dataset']) is not None,'Isolated archive dataset required')
    return config


def prepare_sources(ticker,request,*,snapshot=None,bundle=None,supplements=()):
    _require(not (bundle is not None and (snapshot is not None or supplements)),'Source bundle cannot be mixed with snapshot/supplements')
    if bundle is not None:
        _require(request is None or canonical(request)==canonical(bundle['request']),'Source bundle request differs')
        request=bundle['request']
    _require(request is not None,'Provide borrower and verified Annual/Quarterly fiscal request before generation')
    report,_,_=parse_request(request)
    _require(report.entity==ticker.strip().upper(),'Ticker differs from requested borrower')
    if bundle is not None:
        _require(bundle.get('entity')==report.entity and bundle.get('scope')==report.scope,'Source bundle borrower/scope differs')
        return bundle
    if snapshot is None:
        agent=os.environ.get('SEC_USER_AGENT','')
        _require(agent.strip() and 'example.com' not in agent,'Configure SEC_USER_AGENT with a real SEC contact before fetching')
    from .agent_runner import prepare_loan_review_source_stage
    return prepare_loan_review_source_stage(ticker,request,supplements,snapshot=snapshot)


def run_skill_review(ticker,request=None,*,snapshot=None,bundle=None,supplements=(),reconciliations=None,
                     commentary_documents=None,output_dir=None,config=None,excel=True):
    config=runtime_configuration() if config is None else runtime_configuration(**config)
    directory=Path(output_dir or Path(os.environ.get('OUTPUT_DIR','/tmp/sec_reports'))/('loan_review_'+uuid.uuid4().hex)).resolve()
    _require(not directory.exists(),'Skill output directory already exists; choose a new run directory')
    directory.mkdir(parents=True)
    manifest=dict(status='running',engine='dbt-bigquery-only',execution='candidate',entity=ticker.strip().upper(),
        started_at=datetime.now(timezone.utc).isoformat(),final_report_accepted=False,publication_eligible=False,
        precision_policy_implementation_approved=True,runtime=config,stages={},outputs={})
    def save():
        temporary=directory/'.run_manifest.pending'
        temporary.write_text(json.dumps(manifest,default=str,ensure_ascii=False,indent=2))
        temporary.replace(directory/'run_manifest.json')
    def start(stage):
        manifest['current_stage']=stage;manifest['stages'][stage]='running';save()
    save()
    try:
        start('sources')
        source=prepare_sources(ticker,request,snapshot=snapshot,bundle=bundle,supplements=supplements)
        source_path=directory/'source_bundle.json';source_path.write_text(json.dumps(source,default=str,ensure_ascii=False,indent=2))
        manifest.update(mode=source['request']['mode'],source_bundle_sha256=file_hash(source_path))
        manifest['stages']['sources']='passed';save()
        arguments={}
        for name,value in (('reconciliations',reconciliations),('commentary_documents',commentary_documents)):
            if value is not None:
                path=directory/(name+'.json');path.write_text(json.dumps(value,default=str,ensure_ascii=False,indent=2))
                arguments[name]=str(path)
        start('calculation')
        store=GCSCandidateControlStore(config['project'],config['candidate_bucket']);store.ensure()
        selected=execute_selected(CandidateReleaseControl(store),source_path,directory/'selected',project=config['project'],
            expected_precision_version=config['precision_version'],**arguments)
        pin=selected['execution']['calculation_receipt_sha256']
        calculation=directory/'selected/execution/calculation'
        manifest.update(calculation_run_id=selected['execution']['run_id'],release_id=selected['release_id'],
            package_sha256=selected['package_sha256'],calculation_receipt_sha256=pin,
            selected_execution_receipt_sha256=file_hash(directory/'selected/selected_execution_receipt.json'))
        manifest['stages']['calculation']='passed';save()
        start('report')
        write_preview(calculation,directory/'report',expected_receipt_sha256=pin,excel=excel)
        manifest['stages']['report']='passed';save()
        start('warehouse_archive')
        archived=archive_calculation(calculation,directory/'archive',project=config['project'],
            dataset=config['archive_dataset'],receipt_sha256=pin)
        manifest['stages']['warehouse_archive']=archived['status'];save()
        archive_path=directory/'archive/archive_receipt.json'
        start('delivery_storage')
        body,files=prepare_delivery(calculation,directory/'report',calculation_pin=pin,
            preview_pin=file_hash(directory/'report/preview_manifest.json'),archive_receipt=archive_path,
            archive_pin=file_hash(archive_path),delivery_id=uuid.uuid4().hex,require_excel=excel)
        storage=ShadowDeliveryStorage(config['project'],config['delivery_bucket']);storage.ensure_bucket()
        stored=storage.store(body,files)
        (directory/'storage_receipt.json').write_text(json.dumps(stored,indent=2))
        manifest['stages']['delivery_storage']='stored'
        start('publication_preflight')
        preflight=inspect_candidate(calculation,receipt_sha256=pin)
        (directory/'publication_preflight.json').write_text(json.dumps(preflight,indent=2))
        manifest.update(status='draft',financial_readiness=preflight['financial_readiness'],
            acceptance_blockers=preflight['blockers'],storage_receipt_sha256=file_hash(directory/'storage_receipt.json'))
        manifest['stages']['publication_preflight']='passed'
    except Exception as error:
        manifest.update(status='failed',error=str(error))
        manifest['stages'][manifest.get('current_stage','pipeline')]='failed'
    finally:
        for folder in (directory/'report',directory/'selected/execution/calculation/candidate_preview'):
            for filename in ('report.md','report.json','dashboard.html','loan_review.xlsx','excel_validation.json','preview_manifest.json'):
                if (folder/filename).is_file():manifest['outputs'].setdefault(filename,str(folder/filename))
        for filename in ('source_bundle.json','storage_receipt.json','publication_preflight.json'):
            if (directory/filename).is_file():manifest['outputs'][filename]=str(directory/filename)
        for filename in ('selected/execution/calculation/calculation_receipt.json','selected/selected_execution_receipt.json',
                         'archive/archive_receipt.json'):
            if (directory/filename).is_file():manifest['outputs'][Path(filename).name]=str(directory/filename)
        manifest['finished_at']=datetime.now(timezone.utc).isoformat()
        manifest['manifest_path']=str(directory/'run_manifest.json');save()
    return manifest


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('ticker');parser.add_argument('--request');parser.add_argument('--source-snapshot')
    parser.add_argument('--source-bundle');parser.add_argument('--supplement',action='append',default=[])
    parser.add_argument('--reconciliations');parser.add_argument('--commentary-documents');parser.add_argument('--output-dir')
    parser.add_argument('--runtime-config');parser.add_argument('--project');parser.add_argument('--candidate-bucket')
    parser.add_argument('--archive-dataset');parser.add_argument('--delivery-bucket');parser.add_argument('--no-excel',action='store_true')
    args=parser.parse_args(argv)
    config=runtime_configuration(args.runtime_config,project=args.project or os.environ.get('GCP_PROJECT_ID'),
        candidate_bucket=args.candidate_bucket or os.environ.get('LOAN_REVIEW_CANDIDATE_BUCKET'),
        archive_dataset=args.archive_dataset or os.environ.get('LOAN_REVIEW_ARCHIVE_DATASET'),
        delivery_bucket=args.delivery_bucket or os.environ.get('LOAN_REVIEW_DELIVERY_BUCKET'))
    result=run_skill_review(args.ticker,load_json(args.request) if args.request else None,
        snapshot=load_json(args.source_snapshot) if args.source_snapshot else None,
        bundle=load_json(args.source_bundle) if args.source_bundle else None,
        supplements=tuple(load_json(path) for path in args.supplement),
        reconciliations=load_json(args.reconciliations) if args.reconciliations else None,
        commentary_documents=load_json(args.commentary_documents) if args.commentary_documents else None,
        output_dir=args.output_dir,config=config,excel=not args.no_excel)
    print(json.dumps(result,default=str,ensure_ascii=False,indent=2))
    return 1 if result['status']=='failed' else 2


if __name__=='__main__':raise SystemExit(main())
