"""Generation-controlled candidate releases. Never selects production authority.

Immutable releases/events/run bindings plus one CAS pointer. Failed CAS events
remain auditable; rollback changes only the selection used by future runs.
"""
import argparse
import json
from pathlib import Path
import re

from .delivery_archive import ShadowDeliveryStorage,sha
from .loan_review_sources import canonical
from .warehouse_candidate import read_candidate,_require


def identifier(value):
    _require(isinstance(value,str) and re.fullmatch('[a-f0-9]{32}',value) is not None,'Invalid control identity')
    return value


def candidate_release(release_id,cases):
    identifier(release_id)
    _require(len(cases)>=2,'Annual and quarterly evidence required')
    evidence=[];versions=set()
    for directory,pin in cases:
        report,receipt=read_candidate(directory,expected_receipt_sha256=pin)
        bindings=receipt['bindings']
        versions.add(tuple(bindings[key] for key in ('code_hash','formula_version','policy_version','precision_version')))
        evidence.append(dict(mode=report.mode.value,run_id=bindings['run_id'],calculation_receipt_sha256=pin,
            source_hash=bindings['source_hash'],facts=len(report.facts),comparison=receipt['comparison']))
    _require({row['mode'] for row in evidence}=={'annual','quarterly'},'Annual and quarterly evidence required')
    _require(len({row['run_id'] for row in evidence})==len(evidence),'Duplicate release evidence run')
    _require(len(versions)==1,'Mixed release model/policy versions')
    code,formula,policy,precision=versions.pop()
    return dict(kind='candidate-release-v1',release_id=release_id,engine='dbt-bigquery-only',
        code_hash=code,formula_version=formula,policy_version=policy,precision_version=precision,
        evidence=sorted(evidence,key=lambda row:(row['mode'],row['run_id'])),precision_approved=False,publication_eligible=False)


class GCSCandidateControlStore:
    PREFIX='candidate-control/'
    def __init__(self,project,bucket,*,client=None):
        self.storage=ShadowDeliveryStorage(project,bucket,client=client)
    def ensure(self,*,create=False):self.storage.ensure_bucket(create=create)
    def create(self,key,body):return self.storage._put(self.PREFIX+key,canonical(body).encode())
    def load(self,record):return json.loads(self.storage._get(record))
    def read(self,key):
        from google.api_core.exceptions import NotFound
        blob=self.storage.bucket.blob(self.PREFIX+key)
        try:blob.reload(timeout=60)
        except NotFound:return None,None
        generation=int(blob.generation)
        data=self.storage.bucket.blob(blob.name,generation=generation).download_as_bytes(
            if_generation_match=generation,checksum='crc32c',timeout=60)
        return dict(name=blob.name,generation=str(generation),sha256=sha(data),size=len(data)),json.loads(data)
    def cas(self,key,body,generation):
        from google.api_core.exceptions import PreconditionFailed
        blob=self.storage.bucket.blob(self.PREFIX+key)
        data=canonical(body).encode()
        try:
            blob.upload_from_string(data,if_generation_match=int(generation),checksum='crc32c',timeout=60)
        except PreconditionFailed as exc:
            raise ValueError('Concurrent candidate selection changed; reload before retry') from exc
        return dict(name=blob.name,generation=str(blob.generation),sha256=sha(data),size=len(data))


class CandidateReleaseControl:
    def __init__(self,store):self.store=store
    @staticmethod
    def candidate(body,kind):
        _require(body.get('kind')==kind and body.get('precision_approved') is False
            and body.get('publication_eligible') is False,'Candidate control cannot approve production')
    def register(self,release):
        self.candidate(release,'candidate-release-v1');identifier(release['release_id'])
        _require(release['engine']=='dbt-bigquery-only','Unsupported candidate engine')
        _require({e['mode'] for e in release['evidence']}=={'annual','quarterly'},'Incomplete release evidence')
        return self.store.create('releases/'+release['release_id']+'.json',release)
    def current(self):
        record,pointer=self.store.read('current.json')
        if pointer is None:return None,None
        self.candidate(pointer,'candidate-selection-v1')
        event=self.store.load(pointer['event'])
        self.candidate(event,'candidate-selection-event-v1')
        _require(event['event_id']==pointer['event_id'] and event['release']==pointer['release'],
            'Mixed selection event')
        release=self.store.load(pointer['release']);self.candidate(release,'candidate-release-v1')
        _require(release['release_id']==pointer['release_id'],'Mixed selection release')
        return record,pointer
    def select(self,release_id,*,event_id,reason,actor,rollback=False,expected_generation):
        identifier(release_id);identifier(event_id)
        _require(isinstance(reason,str) and reason.strip() and isinstance(actor,str) and actor.strip(),
            'Selection reason and actor required')
        current_record,current=self.current()
        action='rollback' if rollback else 'select'
        if current and current['event_id']==event_id:
            old=self.store.load(current['event'])
            _require((old['action'],old['reason'],old['actor'],current['release_id'])==(action,reason,actor,release_id),
                'Conflicting operation retry')
            return current_record,current
        actual=current_record['generation'] if current_record else '0'
        _require(str(expected_generation)==str(actual),'Stale candidate selection generation')
        release_record,release=self.store.read('releases/'+release_id+'.json')
        _require(release is not None,'Candidate release not registered')
        self.candidate(release,'candidate-release-v1')
        if rollback:
            _require(current is not None and current['release_id']!=release_id,'Rollback must change selected release')
            seen=set();event_record=current['event'];visited=set()
            while event_record:
                _require(event_record['sha256'] not in visited,'Selection history cycle')
                visited.add(event_record['sha256'])
                event=self.store.load(event_record);self.candidate(event,'candidate-selection-event-v1')
                seen.add(self.store.load(event['release'])['release_id'])
                event_record=event['parent']
            _require(release_id in seen,'Rollback release was never selected')
        event=dict(kind='candidate-selection-event-v1',event_id=event_id,action=action,actor=actor,reason=reason,
            release=release_record,parent=current['event'] if current else None,
            precision_approved=False,publication_eligible=False)
        event_record=self.store.create('events/'+event_id+'.json',event)
        pointer=dict(kind='candidate-selection-v1',event_id=event_id,release_id=release_id,event=event_record,
            release=release_record,precision_approved=False,publication_eligible=False)
        pointer_record=self.store.cas('current.json',pointer,actual)
        return pointer_record,pointer
    def validate_snapshot(self,snapshot):
        """Accept only an event reachable from the successfully selected history."""
        selected_record,selected=snapshot
        self.candidate(selected,'candidate-selection-v1')
        _,current=self.current();_require(current is not None,'No candidate release selected')
        cursor=current['event'];visited=set()
        while cursor:
            _require(cursor['sha256'] not in visited,'Selection history cycle')
            visited.add(cursor['sha256']);event=self.store.load(cursor)
            self.candidate(event,'candidate-selection-event-v1')
            if cursor==selected['event']:
                _require(event['event_id']==selected['event_id'] and event['release']==selected['release'],
                    'Mixed captured selection')
                release=self.store.load(event['release']);self.candidate(release,'candidate-release-v1')
                _require(release['release_id']==selected['release_id'],'Mixed captured release')
                _require(str(selected_record['generation']).isdigit(),'Invalid captured generation')
                return release
            cursor=event['parent']
        raise ValueError('Captured selection was never successfully selected')

    def bind_run(self,run_id,*,entity,scope,source_hash,request_hash,selection_snapshot=None):
        identifier(run_id)
        _require(all(isinstance(v,str) and re.fullmatch('[a-f0-9]{64}',v) for v in (source_hash,request_hash)),
            'Run source/request pins required')
        identity=dict(run_id=run_id,entity=entity,scope=scope,source_hash=source_hash,request_hash=request_hash)
        if selection_snapshot is not None:
            release=self.validate_snapshot(selection_snapshot)
            current_record,current=selection_snapshot
        record,existing=self.store.read('runs/'+run_id+'.json')
        if existing is not None:
            self.candidate(existing,'candidate-run-binding-v1')
            _require(all(existing[k]==v for k,v in identity.items()),'Run identity changed')
            if selection_snapshot is not None:
                _require(existing['release']==current['release'] and existing['event']==current['event'],
                    'Run selection changed')
            return record,existing
        if selection_snapshot is None:
            current_record,current=self.current();_require(current is not None,'No candidate release selected')
            release=self.store.load(current['release'])
        binding=dict(identity,kind='candidate-run-binding-v1',engine=release['engine'],code_hash=release['code_hash'],
            release_id=release['release_id'],release=current['release'],event=current['event'],
            selection_generation=current_record['generation'],precision_approved=False,publication_eligible=False)
        record=self.store.create('runs/'+run_id+'.json',binding)
        return record,binding


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project',required=True);parser.add_argument('--bucket',required=True)
    parser.add_argument('--output-dir',required=True);parser.add_argument('--create-bucket',action='store_true')
    commands=parser.add_subparsers(dest='command',required=True)
    commands.add_parser('current')
    register=commands.add_parser('register');register.add_argument('--release-id',required=True)
    register.add_argument('--case',action='append',nargs=2,required=True,metavar=('DIRECTORY','RECEIPT_SHA256'))
    for name in ('select','rollback'):
        command=commands.add_parser(name)
        for field in ('release-id','event-id','reason','actor','expected-generation'):command.add_argument('--'+field,required=True)
    bind=commands.add_parser('bind')
    for field in ('run-id','entity','scope','source-hash','request-hash'):bind.add_argument('--'+field,required=True)
    args=parser.parse_args();output=Path(args.output_dir);_require(not output.exists(),'Control output already exists')
    store=GCSCandidateControlStore(args.project,args.bucket);store.ensure(create=args.create_bucket)
    control=CandidateReleaseControl(store)
    if args.command=='register':
        body=candidate_release(args.release_id,args.case);record=control.register(body)
    elif args.command in ('select','rollback'):
        record,body=control.select(args.release_id,event_id=args.event_id,reason=args.reason,actor=args.actor,
            rollback=args.command=='rollback',expected_generation=args.expected_generation)
    elif args.command=='current':
        record,body=control.current();_require(body is not None,'No candidate release selected')
    else:
        record,body=control.bind_run(args.run_id,entity=args.entity,scope=args.scope,source_hash=args.source_hash,request_hash=args.request_hash)
    output.mkdir(parents=True)
    (output/'control_receipt.json').write_text(json.dumps(dict(record=record,body=body),indent=2))
    print(json.dumps(dict(record=record,body=body),indent=2))


if __name__=='__main__':main()
