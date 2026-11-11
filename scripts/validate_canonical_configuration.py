"""Synthetic-only independent native checks for scale, basis and version claims."""
import argparse
from copy import deepcopy
from decimal import Decimal
import json
from pathlib import Path

from .dbt_shadow import prepare_run,ShadowWarehouse,digest,PRECISION_VERSION
from .loan_review_sources import load_json
from .warehouse_candidate import _require

CASES=('scale','basis','versions')


def mutate_configuration(records,case):
    _require(case in CASES,'Unknown configuration probe')
    records=deepcopy(records)
    metadata=next(row for kind,_,row in records if kind=='metadata')
    if case=='scale':
        metadata['scale']='1000'
        for kind,_,row in records:
            if kind=='slot' and row['unit']=='money':row['scale']='1000'
    elif case=='basis':
        metadata['standard_ebitda_basis']='PROBE-UNAPPROVED-ADJUSTED-EBITDA'
    else:
        metadata.update(formula_version='probe-formula',policy_version='probe-policy',
            precision_version='probe-approved-precision',precision_approved=True)
        for kind,_,row in records:
            if kind=='slot' and row['formula_id']:
                row['formula_version']='probe-policy' if row['formula_id']=='STANDARD-EBITDA-v1' else 'probe-formula'
    metadata['plan_hash']=digest([row for kind,_,row in records if kind=='slot'])
    return records


def validate(bundle,directory,*,project,kernels=(),case):
    _require(bundle['entity']=='SYNTHETIC-ONLY','Configuration probes require synthetic data')
    directory=Path(directory);directory.mkdir(parents=True,exist_ok=False)
    metadata,records,_,_=prepare_run(bundle,kernels=kernels,with_baseline=False)
    records=mutate_configuration(records,case)
    (directory/'corrupted_inputs.json').write_text(json.dumps(records,default=str,indent=2))
    warehouse=ShadowWarehouse(project,metadata['run_id'])
    try:
        warehouse.execute(records,directory)
    except RuntimeError as error:
        _require('dbt shadow/test failed' in str(error),'Unexpected failure; configuration contract rejection not proven')
        test_error=str(error)
    else:
        raise AssertionError('dbt accepted altered canonical configuration')
    from google.cloud import bigquery
    config=bigquery.QueryJobConfig(query_parameters=[bigquery.ScalarQueryParameter('run_id','STRING',metadata['run_id'])])
    rows=[dict(row) for row in warehouse.client.query(
        f'SELECT fact_id,formula_contract_valid,status,value,scale,standard_basis,precision_version '
        f'FROM `{project}.{warehouse.dataset}.fct_review_shadow_facts` WHERE run_id=@run_id',job_config=config).result()]
    _require(rows and all(row['formula_contract_valid'] is False for row in rows),'Altered configuration was accepted')
    revenue=next(row for row in rows if row['fact_id']=='revenue:fy_t')
    _require(revenue['value']=='120' and Decimal(str(revenue['scale']))==Decimal('1000000'),'Producer scale affected canonical source numbers')
    _require(all(row['precision_version']==PRECISION_VERSION for row in rows),
        'Producer metadata promoted precision policy')
    result=dict(status='passed',case=case,run_id=metadata['run_id'],dataset=warehouse.dataset,code_hash=metadata['code_hash'],
        rejected_contracts=len(rows),canonical_revenue=revenue,dbt_test_rejected=True,dbt_error=test_error,
        precision_approved=False,publication_eligible=False)
    (directory/'probe_manifest.json').write_text(json.dumps(result,default=str,indent=2))
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-bundle',required=True)
    parser.add_argument('--output-dir',required=True)
    parser.add_argument('--project',default='focus-heuristic-438521-v4')
    parser.add_argument('--kernel-cases',required=True)
    parser.add_argument('--case',choices=CASES,required=True)
    args=parser.parse_args()
    result=validate(load_json(args.source_bundle),args.output_dir,project=args.project,kernels=load_json(args.kernel_cases),case=args.case)
    print(json.dumps({k:v for k,v in result.items() if k!='dbt_error'},default=str,indent=2))


if __name__=='__main__':main()
