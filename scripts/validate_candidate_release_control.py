"""Native candidate selection/rollback proof; no financial run or cutover."""
import argparse
from copy import deepcopy
import json
from pathlib import Path

from .candidate_release_control import candidate_release,CandidateReleaseControl,GCSCandidateControlStore
from .warehouse_candidate import read_candidate,_require


def validate(project,bucket,output,cases_a,cases_b):
    for directory,pin in cases_a+cases_b:
        report,_=read_candidate(directory,expected_receipt_sha256=pin)
        _require(report.entity=='SYNTHETIC-ONLY','Release control probes require synthetic evidence')
    output=Path(output);output.mkdir(parents=True,exist_ok=False)
    store=GCSCandidateControlStore(project,bucket);store.ensure(create=True)
    control=CandidateReleaseControl(store)
    _require(control.current()==(None,None),'Control probe requires fresh bucket selection')
    a=candidate_release('1'*32,cases_a);b=candidate_release('2'*32,cases_b)
    _require(a['code_hash']!=b['code_hash'],'Use two actual calculation versions for rollback proof')
    ar=control.register(a);br=control.register(b)
    _require(control.register(a)==ar,'Release registration retry changed generation')
    actor='candidate-migration-validation'
    first,pa=control.select(a['release_id'],event_id='a'*32,reason='Candidate A',actor=actor,expected_generation='0')
    identity=dict(entity='SYNTHETIC-ONLY',scope='entity-wide',source_hash='1'*64,request_hash='2'*64)
    old_record,old=control.bind_run('4'*32,**identity)
    second,pb=control.select(b['release_id'],event_id='b'*32,reason='Candidate B',actor=actor,expected_generation=first['generation'])
    middle_record,middle=control.bind_run('5'*32,**identity)
    _require(control.select(b['release_id'],event_id='b'*32,reason='Candidate B',actor=actor,
        expected_generation=first['generation'])==(second,pb),'Selection retry was not idempotent')
    rejected=[]
    try:store.cas('current.json',pa,first['generation'])
    except ValueError as error:
        _require('Concurrent' in str(error),'Unexpected stale CAS error');rejected.append('stale_generation_cas')
    else:raise AssertionError('GCS accepted stale generation')
    _require(control.current()==(second,pb),'Stale CAS changed pointer')
    c=deepcopy(a);c['release_id']='3'*32;control.register(c)
    try:control.select(c['release_id'],event_id='c'*32,reason='Invalid rollback',actor=actor,
        expected_generation=second['generation'],rollback=True)
    except ValueError as error:
        _require('never selected' in str(error),'Unexpected rollback rejection');rejected.append('unselected_rollback')
    else:raise AssertionError('Rollback accepted unselected release')
    bad=deepcopy(a);bad['code_hash']='f'*64
    try:control.register(bad)
    except ValueError as error:
        _require('never overwrite' in str(error),'Unexpected release overwrite rejection');rejected.append('release_overwrite')
    else:raise AssertionError('Release overwritten')
    approved=deepcopy(a);approved.update(release_id='d'*32,precision_approved=True)
    try:control.register(approved)
    except ValueError as error:
        _require('cannot approve production' in str(error),'Unexpected candidate approval rejection');rejected.append('precision_promotion')
    else:raise AssertionError('Candidate control promoted precision')
    third,pc=control.select(a['release_id'],event_id='e'*32,reason='Rollback candidate to A',actor=actor,
        expected_generation=second['generation'],rollback=True)
    new_record,new=control.bind_run('6'*32,**identity)
    _require(control.bind_run('4'*32,**identity)==(old_record,old),'Existing A binding changed')
    _require(control.bind_run('5'*32,**identity)==(middle_record,middle),'Existing B binding changed')
    _require((old['release_id'],middle['release_id'],new['release_id'])==(a['release_id'],b['release_id'],a['release_id']),
        'Rollback did not affect only future bindings')
    result=dict(status='passed',project=project,bucket=bucket,releases=[dict(record=ar,body=a),dict(record=br,body=b)],
        selections=[dict(record=first,body=pa),dict(record=second,body=pb),dict(record=third,body=pc)],
        run_bindings=[dict(record=old_record,body=old),dict(record=middle_record,body=middle),dict(record=new_record,body=new)],
        rejected=rejected,existing_bindings_unchanged=True,precision_approved=False,publication_eligible=False)
    (output/'probe_manifest.json').write_text(json.dumps(result,indent=2))
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project',required=True);parser.add_argument('--bucket',required=True)
    parser.add_argument('--output-dir',required=True)
    for field in ('case-a','case-b'):parser.add_argument('--'+field,action='append',nargs=2,required=True)
    args=parser.parse_args();result=validate(args.project,args.bucket,args.output_dir,args.case_a,args.case_b)
    print(json.dumps({k:v for k,v in result.items() if k not in ('releases','selections','run_bindings')},indent=2))


if __name__=='__main__':main()
