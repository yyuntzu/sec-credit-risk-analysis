"""Synthetic-only native proof that SQL rejects valid-looking wrong plans."""
import argparse
from copy import deepcopy
import json
from pathlib import Path

from .dbt_shadow import prepare_run, ShadowWarehouse, digest
from .loan_review_sources import load_json
from .warehouse_candidate import _require


def corrupt_plan(records):
    records = deepcopy(records)
    slots = {key:payload for kind,key,payload in records if kind=='slot'}
    targets = ('current_ratio:fy_t','quick_ratio:fy_t','interest_coverage:fy_t','operating_margin:fy_t','dscr:fy_t')
    _require(all(fid in slots for fid in targets),'Formula probes require annual slots')
    slots[targets[0]]['input_ids'].reverse()
    slots[targets[1]]['formula_id']='CF-01'
    slots[targets[2]]['input_ids']=slots[targets[2]]['input_ids'][:-1]
    slots[targets[3]]['input_ids'][1]='revenue:fy_t_minus_1'
    slots[targets[4]]['pending']=[]
    observation = deepcopy(next(payload for kind,_,payload in records if kind=='observation'))
    target = slots[targets[4]]
    observation.update(metric='dscr',start=target['start'],end=target['end'],unit='multiple',
        scale='1',value='2',source_quantum='1',status='sourced',definition=target['definition'],
        source_id='SYNTHETIC-UNAPPROVED-DSCR',locator='Synthetic pending definition probe')
    records.append(('observation','probe:unapproved-dscr',observation))
    metadata = next(payload for kind,_,payload in records if kind=='metadata')
    # Keep the supplied plan hash internally consistent: rejection must come
    # from the independent SQL business contract, not a stale Python checksum.
    metadata['plan_hash']=digest([payload for kind,_,payload in records if kind=='slot'])
    return records,targets


def validate(bundle,directory,*,project,kernels=()):
    _require(bundle['entity']=='SYNTHETIC-ONLY','Formula probes require synthetic data')
    directory = Path(directory);directory.mkdir(parents=True,exist_ok=False)
    metadata,records,_,_ = prepare_run(bundle,kernels=kernels,with_baseline=False)
    records,targets=corrupt_plan(records)
    (directory/'corrupted_inputs.json').write_text(json.dumps(records,default=str,indent=2))
    warehouse=ShadowWarehouse(project,metadata['run_id'])
    try:
        warehouse.execute(records,directory)
    except RuntimeError as error:
        _require('dbt shadow/test failed' in str(error),'Unexpected failure; SQL contract rejection not proven')
        test_error=str(error)
    else:
        raise AssertionError('dbt accepted a corrupt formula plan')
    from google.cloud import bigquery
    config=bigquery.QueryJobConfig(query_parameters=[bigquery.ScalarQueryParameter('run_id','STRING',metadata['run_id'])])
    rows=[dict(row) for row in warehouse.client.query(
        f'SELECT c.fact_id,c.formula_contract_valid,f.status,f.value FROM `{project}.{warehouse.dataset}.int_review_shadow_formula_contracts` c '
        f'JOIN `{project}.{warehouse.dataset}.fct_review_shadow_facts` f USING(run_id,entity,fact_id) WHERE c.run_id=@run_id',
        job_config=config).result()]
    index={row['fact_id']:row for row in rows}
    _require(all(index[fid]['formula_contract_valid'] is False and index[fid]['status']=='not_calculable'
        and index[fid]['value'] is None for fid in targets),'Invalid plan still produced a numeric result')
    result=dict(status='passed',run_id=metadata['run_id'],dataset=warehouse.dataset,project=project,
        code_hash=metadata['code_hash'],rejected_targets=[index[fid] for fid in targets],dbt_test_rejected=True,
        dbt_error=test_error,precision_approved=False,publication_eligible=False)
    (directory/'probe_manifest.json').write_text(json.dumps(result,indent=2))
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-bundle',required=True)
    parser.add_argument('--output-dir',required=True)
    parser.add_argument('--project',default='focus-heuristic-438521-v4')
    parser.add_argument('--kernel-cases',required=True)
    args=parser.parse_args()
    result=validate(load_json(args.source_bundle),args.output_dir,project=args.project,kernels=load_json(args.kernel_cases))
    print(json.dumps({k:v for k,v in result.items() if k!='dbt_error'},indent=2))


if __name__=='__main__':main()
