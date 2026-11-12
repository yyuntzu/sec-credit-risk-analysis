"""Loan Review skill: immutable sources -> pinned SQL -> delivery -> validated published views.

No Python financial engine, legacy fallback or production publication is invoked.
Exit 0 means isolated validation publication, 2 candidate draft, 1 execution failure.
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
from .candidate_archive import archive_calculation,ShadowCandidateArchive
from .delivery_archive import prepare_delivery,ShadowDeliveryStorage
from .publication_preflight import inspect_candidate
from .warehouse_source import BigQuerySourceStore,source_envelope
from .warehouse_workbook import workbook_bundle,reconciliation_slots
from .warehouse_publication import BigQueryPublicationStore,prepare_publication

ROOT=Path(__file__).resolve().parents[1]


def finalize_publication(directory,manifest):
    """Resume J from a pinned committed I; never recalculate or rewrite history."""
    directory=Path(directory)
    _require(file_hash(directory/'publication_receipt.json')==manifest['publication_receipt_sha256'],
        'Committed publication receipt pin mismatch')
    published=load_json(directory/'publication_receipt.json');config=manifest['runtime']
    _require(published['run_id']==manifest['calculation_run_id'] and published['publication_id']==manifest['publication_id']
        and published['calculation_receipt_sha256']==manifest['calculation_receipt_sha256'],'Resume publication identity differs')
    registry=BigQueryPublicationStore(config['project'],config['publication_dataset'],source_dataset=config['source_dataset']);registry.ensure()
    rows=registry.read(published['publication_id'])
    from .warehouse_publication import verify_publication
    commit=next(json.loads(row['payload']) for row in rows if row['record_kind']=='commit')
    verify_publication(rows,commit)
    _require(registry.receipt(commit)==published,'Stored publication receipt changed')
    manifest['publication_dbt']=registry.deploy_views(directory/('publication_dbt_'+uuid.uuid4().hex))
    identity={key:commit[key] for key in ('entity','scope','report_mode')}
    current=registry.current(**identity)
    manifest['publication_selection']=(current if current and current['publication_id']==published['publication_id']
        else registry.select(published['publication_id'],expected_version=current['version'] if current else 0))
    params=[registry.bq.ScalarQueryParameter('publication_id','STRING',published['publication_id'])]
    count=next(iter(registry.client.query(f'SELECT count(*) as n FROM `{registry.project}.{registry.dataset}.published_loan_review_facts` '
        'WHERE publication_id=@publication_id',job_config=registry.bq.QueryJobConfig(query_parameters=params),location='US').result()))['n']
    _require(count==commit['record_counts']['fact'],'Published view omitted committed facts')
    manifest.update(status='published_validation',validation_published=True,
        published_view=f'{config["project"]}.{config["publication_dataset"]}.published_loan_review_facts',
        validation_acceptance_blockers=[])
    manifest['stages']['published_views']='passed'
    return manifest


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
    for field,default in (('source_dataset','sec_review_shadow_skill_sources'),('publication_dataset','sec_review_shadow_skill_publications')):
        config.setdefault(field,default)
        _require(re.fullmatch('sec_review_shadow_[a-z0-9_]+',config[field]) is not None,'Isolated source/publication dataset required')
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
                     commentary_documents=None,output_dir=None,config=None,excel=True,workbook=None,quarter=None):
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
        if workbook is not None:
            _require(request is not None and bundle is None and snapshot is None and not supplements,'Workbook requires its fixed request without mixed sources')
            _require(ticker.strip().upper()==request['entity'],'Workbook ticker differs')
            source=workbook_bundle(workbook,request,quarter=quarter)
        else:
            _require(quarter is None,'Workbook quarter requires workbook source')
            source=reconciliation_slots(prepare_sources(ticker,request,snapshot=snapshot,bundle=bundle,supplements=supplements))
        source_path=directory/'source_bundle.json';source_path.write_text(json.dumps(source,default=str,ensure_ascii=False,indent=2))
        manifest.update(mode=source['request']['mode'],source_bundle_sha256=file_hash(source_path))
        manifest['stages']['sources']='passed';save()
        start('immutable_sources')
        source_store=BigQuerySourceStore(config['project'],config['source_dataset']);source_store.ensure()
        envelope=source_envelope(source,reconciliations=reconciliations,commentary_documents=commentary_documents)
        source_receipt=source_store.store(envelope)
        (directory/'source_receipt.json').write_text(json.dumps(source_receipt,indent=2))
        # D executes only the envelope read back from immutable C, not the caller's mutable object.
        restored=source_store.load(source_receipt);source=restored['bundle']
        source_path.write_text(json.dumps(source,default=str,ensure_ascii=False,indent=2))
        manifest['source_bundle_sha256']=file_hash(source_path)
        reconciliations=restored['reconciliations'];commentary_documents=restored['commentary_documents']
        manifest.update(source_id=source_receipt['source_id'],source_receipt_sha256=file_hash(directory/'source_receipt.json'))
        manifest['stages']['immutable_sources']='stored';save()
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
        if config.get('publication_policy_record') and preflight['financial_readiness']:
            start('publication')
            archive_receipt=load_json(archive_path)
            publication_id=uuid.uuid4().hex;manifest['publication_id']=publication_id;save()
            rows,commit=prepare_publication(calculation,calculation_pin=pin,archive_receipt=archive_receipt,
                archive_pin=file_hash(archive_path),storage_receipt=stored,source_receipt=source_receipt,selected=selected,
                control=CandidateReleaseControl(store),source_store=source_store,
                archive=ShadowCandidateArchive(config['project'],config['archive_dataset']),
                storage=storage,policy_record=config['publication_policy_record'],publication_id=publication_id)
            if rows is None:
                manifest['publication_blockers']=commit['reasons'];manifest['stages']['publication']='blocked'
            else:
                registry=BigQueryPublicationStore(config['project'],config['publication_dataset'],source_dataset=config['source_dataset']);registry.ensure()
                published=registry.store(rows,commit)
                (directory/'publication_receipt.json').write_text(json.dumps(published,indent=2))
                manifest['publication_receipt_sha256']=file_hash(directory/'publication_receipt.json')
                manifest['stages']['publication']='committed';save()
                start('published_views')
                finalize_publication(directory,manifest)
        else:
            manifest['stages']['publication']='blocked'
            manifest['publication_blockers']=(['Financial acceptance has not passed'] if not preflight['financial_readiness']
                else ['No isolated publication policy is registered'])
    except Exception as error:
        manifest.update(status='failed',error=str(error))
        manifest['stages'][manifest.get('current_stage','pipeline')]='failed'
    finally:
        for folder in (directory/'report',directory/'selected/execution/calculation/candidate_preview'):
            for filename in ('report.md','report.json','dashboard.html','loan_review.xlsx','excel_validation.json','preview_manifest.json'):
                if (folder/filename).is_file():manifest['outputs'].setdefault(filename,str(folder/filename))
        for filename in ('source_bundle.json','source_receipt.json','storage_receipt.json','publication_preflight.json','publication_receipt.json'):
            if (directory/filename).is_file():manifest['outputs'][filename]=str(directory/filename)
        for filename in ('selected/execution/calculation/calculation_receipt.json','selected/selected_execution_receipt.json',
                         'archive/archive_receipt.json'):
            if (directory/filename).is_file():manifest['outputs'][Path(filename).name]=str(directory/filename)
        manifest['finished_at']=datetime.now(timezone.utc).isoformat()
        manifest['manifest_path']=str(directory/'run_manifest.json');save()
    return manifest


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('ticker',nargs='?');parser.add_argument('--request');parser.add_argument('--source-snapshot')
    parser.add_argument('--resume-publication',help='Existing run directory with a pinned committed publication receipt')
    parser.add_argument('--source-bundle');parser.add_argument('--supplement',action='append',default=[])
    parser.add_argument('--reconciliations');parser.add_argument('--commentary-documents');parser.add_argument('--output-dir')
    parser.add_argument('--runtime-config');parser.add_argument('--project');parser.add_argument('--candidate-bucket')
    parser.add_argument('--archive-dataset');parser.add_argument('--delivery-bucket');parser.add_argument('--no-excel',action='store_true')
    parser.add_argument('--workbook');parser.add_argument('--quarter',type=int,choices=(1,2,3))
    args=parser.parse_args(argv)
    if args.resume_publication:
        _require(args.ticker is None and not any((args.request,args.output_dir,args.source_snapshot,args.source_bundle,
            args.supplement,args.reconciliations,args.commentary_documents,args.workbook,args.quarter,args.no_excel,
            args.runtime_config,args.project,args.candidate_bucket,args.archive_dataset,args.delivery_bucket)),
            'Resume cannot change inputs, configuration or requested delivery')
        directory=Path(args.resume_publication).resolve();manifest=load_json(directory/'run_manifest.json')
        try:
            finalize_publication(directory,manifest);manifest.pop('error',None)
        except Exception as error:
            manifest.update(status='failed',error=str(error));raise
        finally:
            manifest['finished_at']=datetime.now(timezone.utc).isoformat()
            temporary=directory/'.run_manifest.pending';temporary.write_text(json.dumps(manifest,ensure_ascii=False,indent=2));temporary.replace(directory/'run_manifest.json')
        print(json.dumps(manifest,ensure_ascii=False,indent=2));return 0
    if args.ticker is None:parser.error('ticker or --resume-publication is required')
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
        output_dir=args.output_dir,config=config,excel=not args.no_excel,workbook=args.workbook,quarter=args.quarter)
    print(json.dumps(result,default=str,ensure_ascii=False,indent=2))
    return 1 if result['status']=='failed' else 0 if result['status']=='published_validation' else 2


if __name__=='__main__':raise SystemExit(main())
