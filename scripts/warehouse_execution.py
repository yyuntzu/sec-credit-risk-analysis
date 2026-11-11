"""SQL-only candidate execution. Isolated namespace, no Python financial baseline.

This prepares the eventual cloud engine; it does not authorize M4 or publishing.
Migration comparisons remain a distinct, explicitly recorded shadow operation.
"""
import argparse
import json
from pathlib import Path

from .dbt_shadow import prepare_run, ShadowWarehouse, code_hash
from .loan_review_sources import load_json
from .warehouse_candidate import (ARTIFACTS, EXECUTION_VERSION, file_hash,
    _verify_dbt, _require, read_candidate, write_preview)


def freeze_execution(directory,metadata):
    directory = Path(directory)
    _require(metadata['status']=='executed' and metadata['calculation_mode']=='dbt-only-candidate'
        and metadata['baseline_comparison']=='not_run','Expected SQL-only execution')
    _require(metadata['precision_approved'] is False and metadata['publication_eligible'] is False,
        'Candidate execution cannot approve publication')
    _verify_dbt(directory,metadata)
    bindings = {key:metadata[key] for key in ('run_id','entity','scope','request_hash','source_hash','plan_hash',
        'code_hash','formula_version','policy_version','precision_version','reconciliations_hash','commentary_documents_hash')}
    receipt = dict(schema_version=1,consumer_version=EXECUTION_VERSION,engine='dbt-bigquery-only',
        bindings=bindings,comparison=dict(status='not_run',mode='dbt-only'),dbt=metadata['dbt'],
        artifacts={name:file_hash(directory/name) for name in ARTIFACTS},
        precision_approved=False,publication_eligible=False)
    path = directory/'calculation_receipt.json'
    with path.open('x',encoding='utf-8') as handle:
        handle.write(json.dumps(receipt,ensure_ascii=False,indent=2))
    return file_hash(path)


def execute_candidate(bundle,directory,*,project,warehouse=None,kernels=(),reconciliations=None,
                      commentary_documents=None,candidate_preview=False):
    directory = Path(directory)
    directory.mkdir(parents=True,exist_ok=False)
    metadata = dict(status='preparing',engine='dbt-bigquery-only',publication_eligible=False,precision_approved=False)
    try:
        prepared,records,baseline,acceptance = prepare_run(bundle,kernels=kernels,reconciliations=reconciliations,
            commentary_documents=commentary_documents,with_baseline=False)
        _require(baseline is None and acceptance is None,'SQL-only execution unexpectedly created a Python baseline')
        metadata.update(prepared,status='prepared')
        payloads = dict(source_bundle=bundle,reconciliation_reviews=reconciliations,
            commentary_documents=[] if commentary_documents is None else commentary_documents,shadow_inputs=records)
        for name,payload in payloads.items():
            (directory/(name+'.json')).write_text(json.dumps(payload,default=str,ensure_ascii=False,indent=2),encoding='utf-8')
        warehouse = warehouse or ShadowWarehouse(project,metadata['run_id'])
        metadata.update(project=project,dataset=getattr(warehouse,'dataset',None))
        facts,kernel_rows,receipt = warehouse.execute(records,directory)
        _require(metadata['code_hash']==code_hash(),'Source code changed during SQL-only execution')
        outputs = dict(warehouse_facts=facts,kernel_results=kernel_rows,
            warehouse_reconciliations=receipt.pop('reconciliation_rows'),
            warehouse_acceptance=receipt.pop('acceptance_rows'),warehouse_commentary=receipt.pop('commentary_rows'))
        for name,payload in outputs.items():
            (directory/(name+'.json')).write_text(json.dumps(payload,default=str,ensure_ascii=False,indent=2),encoding='utf-8')
        metadata.update(status='executed',dbt=receipt)
        pin = freeze_execution(directory,metadata)
        # Structure, complete coverage, evidence, SQL resource receipts and hashes;
        # no arithmetic or financial acceptance is repeated in Python.
        report,_ = read_candidate(directory,expected_receipt_sha256=pin)
        metadata.update(calculation_receipt_sha256=pin,facts=len(report.facts))
        if candidate_preview:
            preview = write_preview(directory,directory/'candidate_preview',expected_receipt_sha256=pin)
            metadata['candidate_preview_path'] = preview['dashboard_path']
    except Exception as error:
        metadata.update(status='failed',error=str(error),publication_eligible=False)
        raise
    finally:
        (directory/'execution_manifest.json').write_text(json.dumps(metadata,ensure_ascii=False,default=str,indent=2),encoding='utf-8')
    return metadata


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-bundle',required=True)
    parser.add_argument('--output-dir',required=True)
    parser.add_argument('--project',default='focus-heuristic-438521-v4')
    parser.add_argument('--kernel-cases')
    parser.add_argument('--reconciliations')
    parser.add_argument('--commentary-documents')
    parser.add_argument('--candidate-preview',action='store_true')
    args = parser.parse_args(argv)
    result = execute_candidate(load_json(args.source_bundle),args.output_dir,project=args.project,
        kernels=load_json(args.kernel_cases) if args.kernel_cases else (),
        reconciliations=load_json(args.reconciliations) if args.reconciliations else None,
        commentary_documents=load_json(args.commentary_documents) if args.commentary_documents else None,
        candidate_preview=args.candidate_preview)
    print(json.dumps(result,ensure_ascii=False,default=str,indent=2))


if __name__=='__main__':main()
