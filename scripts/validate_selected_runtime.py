"""Synthetic native selector -> GCS runtime -> BigQuery -> rollback proof."""
import argparse
from copy import deepcopy
import json
from pathlib import Path
import tempfile

from .candidate_release_control import CandidateReleaseControl,GCSCandidateControlStore
from .selected_runtime import RuntimeStorage,register_runtime_release,execute_selected
from .warehouse_candidate import _require,file_hash
from .loan_review_sources import load_json


def validate(args):
    _require(file_hash(args.control_manifest)==args.control_manifest_pin,'Historical control evidence pin mismatch')
    historical=load_json(args.control_manifest)
    _require(historical['status']=='passed' and historical['precision_approved'] is False,'Invalid historical evidence')
    source=load_json(args.source_bundle)
    _require(source['request']['entity']=='SYNTHETIC-ONLY','Synthetic-only validation required')
    output=Path(args.output_dir);output.mkdir(parents=True,exist_ok=False)
    store=GCSCandidateControlStore(args.project,args.bucket);store.ensure(create=True)
    control=CandidateReleaseControl(store);_require(control.current()==(None,None),'Fresh selector required')
    storage=RuntimeStorage(store.storage)
    state=dict(status='preparing',project=args.project,bucket=args.bucket,runs=[],releases=[],
        rejected=[],precision_approved=False,publication_eligible=False)
    def checkpoint(): (output/'probe_manifest.json').write_text(json.dumps(state,indent=2))
    try:
        for index,(path,pin) in enumerate(((args.package_a,args.package_a_pin),(args.package_b,args.package_b_pin))):
            reference=storage.store(path,pin)
            _require(storage.store(path,pin)==reference,'Runtime store retry changed generation')
            release=deepcopy(historical['releases'][index]['body']);release['release_id']=('7' if index==0 else '8')*32
            record=register_runtime_release(control,release,reference)
            state['releases'].append(dict(record=record,body=dict(release,runtime=reference)))
            checkpoint()
        _require(state['releases'][0]['body']['code_hash']!=state['releases'][1]['body']['code_hash'],'Two versions required')
        generation='0'
        for index,target in enumerate((0,1,0)):
            release=state['releases'][target]['body']
            pointer,_=control.select(release['release_id'],event_id=str(index+1)*32,
                reason='Synthetic selected execution '+str(index),actor='candidate-runtime-validation',
                expected_generation=generation,rollback=index==2)
            generation=pointer['generation'];checkpoint()
            run=execute_selected(control,args.source_bundle,output/('run_'+str(index)),project=args.project,
                reconciliations=args.reconciliations)
            _require(run['execution']['financial_code_hash']==release['code_hash'],'Wrong executed version')
            state['runs'].append(run);checkpoint()
            # Earlier calculation receipts remain byte-for-byte fixed after selection changes.
            for old_index,old in enumerate(state['runs']):
                receipt=output/('run_'+str(old_index))/'execution/calculation/calculation_receipt.json'
                _require(file_hash(receipt)==old['execution']['calculation_receipt_sha256'],'Historical result changed')
        reference=state['releases'][0]['body']['runtime']
        from google.api_core.exceptions import NotFound
        with tempfile.TemporaryDirectory() as temporary:
            bad=deepcopy(reference);bad['object']['sha256']='0'*64
            # Keep name/package pin consistent; corrupt downloaded content checksum expectation instead.
            try:storage.storage._get(bad['object'])
            except ValueError:state['rejected'].append('gcs_content_checksum')
            else:raise AssertionError('Bad checksum accepted')
            missing=deepcopy(reference);missing['object']['generation']='1'
            try:storage.fetch(missing,Path(temporary)/'missing.zip')
            except NotFound:state['rejected'].append('missing_generation')
            else:raise AssertionError('Missing generation accepted')
        state.update(status='passed',old_receipts_unchanged=True)
    except Exception as error:
        state.update(status='failed',error=str(error));raise
    finally:checkpoint()
    return state


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for field in ('project','bucket','output-dir','control-manifest','control-manifest-pin','package-a',
                  'package-a-pin','package-b','package-b-pin','source-bundle','reconciliations'):
        parser.add_argument('--'+field,required=True)
    result=validate(parser.parse_args())
    print(json.dumps(dict(status=result['status'],runs=[run['execution'] for run in result['runs']],
        rejected=result['rejected']),indent=2))


if __name__=='__main__':main()
