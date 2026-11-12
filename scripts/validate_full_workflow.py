"""Isolated A-J bootstrap and native publication success/rejection/rollback audit."""
import argparse
from copy import deepcopy
import json
from pathlib import Path
import uuid

from .candidate_release_control import CandidateReleaseControl,GCSCandidateControlStore,candidate_release
from .selected_runtime import RuntimeStorage,register_runtime_release
from .warehouse_publication import validation_policy,BigQueryPublicationStore,verify_publication,IDENTITY
from .candidate_archive import content_hash
from .loan_review_sources import canonical,digest,load_json
from .warehouse_candidate import file_hash,_require,read_candidate
from .warehouse_source import BigQuerySourceStore


def bootstrap(args):
    root=Path(args.output_dir);root.mkdir(parents=True,exist_ok=False)
    for directory,pin in (args.annual_case,args.quarterly_case):
        report,_=read_candidate(directory,expected_receipt_sha256=pin)
        _require(report.entity=='SYNTHETIC-ONLY','Synthetic qualification required')
    store=GCSCandidateControlStore(args.project,args.bucket);store.ensure()
    control=CandidateReleaseControl(store)
    runtime=RuntimeStorage(store.storage).store(args.package,args.package_sha256)
    release=candidate_release('a'*32,[args.annual_case,args.quarterly_case])
    release_record=register_runtime_release(control,release,runtime)
    current,_=control.current()
    selection=control.select(release['release_id'],event_id='5'*32,reason='Isolated A-J validation runtime',
        actor='full-workflow-validation',expected_generation=current['generation'] if current else '0')
    policy=validation_policy(release,args.package_sha256)
    policy_record=store.create('publication-policies/'+policy['policy_id']+'.json',policy)
    config=load_json(Path(__file__).resolve().parents[1]/'references/loan-review-runtime.json')
    config.update(project=args.project,candidate_bucket=args.bucket,delivery_bucket=args.bucket,
        source_dataset='sec_review_shadow_source_aj_20261111',archive_dataset='sec_review_shadow_archive_aj_20261111',
        publication_dataset='sec_review_shadow_published_aj_20261111',publication_policy_record=policy_record)
    (root/'runtime_config.json').write_text(json.dumps(config,indent=2))
    result=dict(status='ready',release=dict(record=release_record,body=release),runtime=runtime,
        selection=selection,policy=dict(record=policy_record,body=policy),production_deployment=False)
    (root/'bootstrap_receipt.json').write_text(json.dumps(result,indent=2));return result


def verify(args):
    from google.cloud import bigquery
    config=load_json(args.runtime_config);root=Path(args.output_dir);root.mkdir(parents=True,exist_ok=False)
    runs=[load_json(Path(directory)/'run_manifest.json') for directory in (args.first,args.second)]
    _require(all(run['status']=='published_validation' and run['entity']=='SYNTHETIC-ONLY' for run in runs),'Two successful isolated publications required')
    registry=BigQueryPublicationStore(config['project'],config['publication_dataset'],source_dataset=config['source_dataset'])
    registry.deploy_views(root/'dbt_before_faults')
    publications=[load_json(Path(directory)/'publication_receipt.json') for directory in (args.first,args.second)]
    original_rows=[registry.read(row['publication_id']) for row in publications]
    commits=[next(json.loads(row['payload']) for row in rows if row['record_kind']=='commit') for rows in original_rows]
    for rows,commit,receipt in zip(original_rows,commits,publications):
        _require(registry.store(rows,commit)==receipt,'Publication retry changed receipt')
    source=BigQuerySourceStore(config['project'],config['source_dataset'])
    receipts=[load_json(Path(directory)/'source_receipt.json') for directory in (args.first,args.second)]
    _require(receipts[0]==receipts[1],'Same fixed inputs did not reuse immutable source C')
    envelope=source.load(receipts[0]);_require(source.store(envelope)==receipts[0],'Source retry changed receipt')
    def visible(view):
        return [dict(row) for row in registry.client.query(f'SELECT publication_id,count(*) as facts FROM '
            f'`{registry.project}.{registry.dataset}.{view}` GROUP BY publication_id',location='US').result()]
    before=visible('published_loan_review_facts')
    _require(before==[dict(publication_id=publications[1]['publication_id'],facts=commits[1]['record_counts']['fact'])],
        'Current view does not select the second publication')
    rejected=[]
    if args.blocked:
        blocked=load_json(Path(args.blocked)/'run_manifest.json')
        _require(blocked['status']=='draft' and blocked['financial_readiness'] is False
            and not (Path(args.blocked)/'publication_receipt.json').exists(),'Incomplete finance batch was not blocked')
        params=[bigquery.ScalarQueryParameter('run_id','STRING',blocked['calculation_run_id'])]
        n=next(iter(registry.client.query(f'SELECT count(*) as n FROM `{registry.project}.{registry.dataset}.published_history_facts` '
            'WHERE run_id=@run_id',job_config=bigquery.QueryJobConfig(query_parameters=params),location='US').result()))['n']
        _require(n==0,'Financially rejected run leaked to published history')
        rejected.append(dict(case='financial_acceptance_failed',run_id=blocked['calculation_run_id'],published_rows=n))
    for kind in ('missing_commit','foreign_fact_with_valid_hashes'):
        pid=uuid.uuid4().hex;rows=deepcopy(original_rows[0])
        for row in rows:row['publication_id']=pid
        commit=deepcopy(commits[0]);commit['publication_id']=pid
        if kind=='missing_commit':rows=[row for row in rows if row['record_kind']!='commit']
        else:
            fact=next(row for row in rows if row['record_kind']=='fact')
            value=json.loads(fact['payload']);value['source_hash']='0'*64
            fact.update(payload=canonical(value),payload_sha256=digest(value))
            commit['content_sha256']=content_hash([row for row in rows if row['record_kind']!='commit'])
            row=next(row for row in rows if row['record_kind']=='commit');row.update(payload=canonical(commit),payload_sha256=digest(commit))
        table=f'{registry.project}.{registry.dataset}.published_batch_{pid}'
        fields=IDENTITY+('record_kind','record_id','payload','payload_sha256')
        registry.client.create_table(bigquery.Table(table,schema=[bigquery.SchemaField(key,'STRING',mode='REQUIRED') for key in fields]))
        try:
            registry.client.load_table_from_json(rows,table,job_config=bigquery.LoadJobConfig(
                schema=[bigquery.SchemaField(key,'STRING',mode='REQUIRED') for key in fields],write_disposition='WRITE_EMPTY')).result()
            checks=list(registry.client.query(f'SELECT publication_valid FROM `{registry.project}.{registry.dataset}.int_publication_checks` '
                f'WHERE table_publication_id="{pid}"',location='US').result())
            _require(len(checks)==1 and checks[0]['publication_valid'] is False,'SQL published gate accepted '+kind)
            _require(not any(row['publication_id']==pid for row in visible('published_history_facts')),'Invalid batch leaked into history')
            _require(visible('published_loan_review_facts')==before,'Invalid batch affected current published facts')
            rejected.append(dict(case=kind,publication_id=pid,sql_rejected=True))
        finally:
            # Only the newly created, named fault-injection table is removed.
            registry.client.delete_table(table)
    fake_source_id=uuid.uuid4().hex+uuid.uuid4().hex
    fake_source=f'{source.project}.{source.dataset}.source_bundle_{fake_source_id}'
    source_schema=[bigquery.SchemaField(key,'STRING',mode='REQUIRED') for key in source.fields]
    registry.client.create_table(bigquery.Table(fake_source,schema=source_schema))
    try:
        # A physically foreign source with otherwise identical declared source ID
        # must fail the J-to-C join, even though publication record hashes are intact.
        physical=source._read(receipts[0]['table'])
        registry.client.load_table_from_json(physical,fake_source,
            job_config=bigquery.LoadJobConfig(schema=source_schema,write_disposition='WRITE_EMPTY')).result()
        _require(visible('published_loan_review_facts')==[],'Ambiguous/foreign physical C source was accepted')
        rejected.append(dict(case='foreign_physical_source',sql_rejected=True))
    finally:registry.client.delete_table(fake_source)
    _require(visible('published_loan_review_facts')==before,'Source recovery did not restore unchanged publications')
    identity={key:commits[0][key] for key in ('entity','scope','report_mode')}
    current=registry.current(**identity)
    rolled=registry.select(publications[0]['publication_id'],expected_version=current['version'],rollback=True,
        reason='Validate rollback to first accepted result')
    after=visible('published_loan_review_facts')
    _require(after==[dict(publication_id=publications[0]['publication_id'],facts=commits[0]['record_counts']['fact'])],'Rollback did not restore first result')
    for rows,receipt in zip(original_rows,publications):_require(registry.read(receipt['publication_id'])==rows,'Historical publication changed')
    history=visible('published_history_facts');_require(len(history)==2,'Rollback lost history')
    try:registry.select(publications[1]['publication_id'],expected_version=0)
    except ValueError:rejected.append(dict(case='stale_selection',rejected=True))
    else:raise AssertionError('Stale selection accepted')
    dbt=registry.deploy_views(root/'dbt')
    result=dict(status='passed',deployment='validation',publications=publications,source_receipt=receipts[0],
        before=before,after=after,history=history,rollback=rolled,rejected=rejected,dbt=dbt,
        production_deployment=False,source_idempotent=True,publication_idempotent=True,historical_rows_unchanged=True)
    (root/'verification_receipt.json').write_text(json.dumps(result,indent=2));return result


def main():
    parser=argparse.ArgumentParser(description=__doc__);commands=parser.add_subparsers(dest='command',required=True)
    init=commands.add_parser('bootstrap')
    for field in ('project','bucket','package','package-sha256'):init.add_argument('--'+field,required=True)
    init.add_argument('--annual-case',nargs=2,required=True);init.add_argument('--quarterly-case',nargs=2,required=True)
    check=commands.add_parser('verify')
    for field in ('runtime-config','first','second'):check.add_argument('--'+field,required=True)
    check.add_argument('--blocked')
    for command in (init,check):command.add_argument('--output-dir',required=True)
    args=parser.parse_args();result=bootstrap(args) if args.command=='bootstrap' else verify(args)
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
