"""Explicit source-backed cash/equity reconciliation; retain unresolved debt-service definitions."""
import json,pathlib,re,sys,uuid,subprocess
from dataclasses import replace
from datetime import date,datetime,timezone
from decimal import Decimal as D
sys.path.insert(0,'scripts')
from review_workflow import restore_report,write_json
from review_outputs import report_payload,write_dashboard
from loan_review_contract import Evidence,Narrative,calculate_fact,validate_report
from loan_review_pipeline import acceptance_result,write_report_artifacts
from review_cloud import ReviewCloud
p=pathlib.Path(__file__).parent;old=p/'reviewed';out=p/'delivery';out.mkdir(exist_ok=True)
assert not any(out.iterdir())
r=restore_report(json.loads((old/'report.json').read_text()));bundle=json.loads((old/'source_inputs.json').read_text());initial=json.loads((old/'run_manifest.json').read_text())
f=json.loads((p/'companyfacts.json').read_text())['facts']['us-gaap'];checks=[]
def val(tag,start,end):
 rows=[x for x in f[tag]['units']['USD'] if x.get('start')==start and x['end']==end and x['form']=='10-K']
 vs={D(x['val'])/1000000 for x in rows};assert len(vs)==1,(tag,vs)
 return vs.pop(),rows
for period in r.periods:
 role=period.role;end=period.end.isoformat();start=period.start.isoformat();raw=re.sub(r'\s+',' ',(p/(end+'.txt')).read_text())
 cal=r.evidence[period.evidence_ids[0]];e=dict(r.evidence)
 assets,ar=val('Assets',None,end);liab,lr=val('Liabilities',None,end);equity,er=val('StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest',None,end)
 assert assets==liab+equity
 cfo=r.facts['cfo:'+role].value;cfi=r.facts['cfi:'+role].value;cff=r.facts['cff:'+role].value;begin=r.facts['beginning_cash:'+role].value;ending=r.facts['ending_cash:'+role].value
 assert cfo+cfi+cff==ending-begin
 # Retain the complete source statement, including the published cash movement and its cash-equivalent basis.
 loc=raw.rindex('CONSOLIDATED STATEMENTS OF CASH FLOWS');content=raw[loc:loc+14000]
 assert 'Cash and cash equivalents' in content or 'cash and cash equivalents' in content
 cashid='review:cash-basis:'+role;factid='review:statement:'+role;bsid='review:equity-basis:'+role
 e[cashid]=Evidence(cashid,r.entity,r.scope,cal.source_id,cal.version,cal.document_date,cal.locator+'; consolidated cash flow statement','definition',(role,), 'Reviewed complete published cash-flow statement: opening/closing cash and equivalents use the same basis; published three flows reconcile exactly to the stated net movement. No separate FX/restricted cash movement is presented; none has been backsolved or imputed. '+content)
 e[factid]=Evidence(factid,r.entity,r.scope,cal.source_id,cal.version,cal.document_date,cal.locator+'; balance sheet and cash flow facts','fact',(role,),json.dumps(dict(assets=ar,liabilities=lr,full_equity=er,cfo=str(cfo),cfi=str(cfi),cff=str(cff),beginning_cash=str(begin),ending_cash=str(ending))))
 e[bsid]=Evidence(bsid,r.entity,r.scope,cal.source_id,cal.version,cal.document_date,cal.locator+'; consolidated balance sheet including noncontrolling interests','definition',(role,),'Reviewed total equity including NCI, rather than parent equity alone. Assets = liabilities + full consolidated equity.')
 fid='cash_change:'+role;facts=dict(r.facts);facts[fid]=replace(facts[fid],evidence_ids=(cashid,factid));r=replace(r,evidence=e,facts=facts)
 r=calculate_fact(r,fid,input_ids=('ending_cash:'+role,'beginning_cash:'+role),formula_version='CASH-CHANGE-v1')
 for kind,calc,reported,eids,reason in [('cash_bridge',cfo+cfi+cff,ending-begin,[cashid,factid],'Complete same-basis published cash flow bridge verified'),('balance_sheet_equation',liab+equity,assets,[bsid,factid],'Full consolidated equity including NCI verified')]:
  checks.append(dict(kind=kind,period_role=role,period=period.label,status='matched',unit='money',currency='USD',scale='1000000',calculated_value=calc,reported_value=reported,difference=calc-reported,evidence_ids=eids,reason=reason,source_locators=[cal.locator]))
# Explicitly disclose the conservative trade-receivable scope in the ratio view.
e=dict(r.evidence);eid='review:quick-assets';raw=re.sub(r'\s+',' ',(p/'2026-02-01.txt').read_text());loc=raw.index('Trade receivables, net of allowance',300000)
base=e['reviewed-passage:gross-debt'];roles=('fy_t_minus_1','fy_t')
e[eid]=replace(base,id=eid,locator=base.locator.split(';')[0]+'; Note 10 Receivables',content=raw[loc:loc+700],period_roles=roles)
tables=[]
for t in r.tables:
 notes=list(t.notes)
 if t.spec.key=='ratios':notes.append(Narrative('definition','supported',text='速動資產採現金加淨額客戶應收帳款的保守口徑，未納入供應商回饋應收款。FY2025 客戶應收款 USD 981m、供應商回饋 USD 67m，合計財報應收款 USD 1,048m。',claim_type='observation',evidence_ids=(eid,),period_roles=roles))
 tables.append(replace(t,notes=tuple(notes)))
r=replace(r,evidence=e,tables=tuple(tables));validate_report(r,expected_mode='annual');a=acceptance_result(r,checks)
write_json(out/'source_inputs.json',bundle);paths=write_report_artifacts(r,a,out,source_bundle=bundle);a=json.loads((out/'acceptance.json').read_text());write_dashboard(r,a,out)
deps=pathlib.Path.home()/'.cache/codex-runtimes/codex-primary-runtime/dependencies/node'
subprocess.run([str(deps/'bin/node'),str(p/'export_review.mjs'),str(out)],check=True)
cloud=ReviewCloud();cloud.ensure();runid=uuid.uuid4().hex;cloud.stage_bundle(runid,'CNM',bundle);cloud.publish(runid,'CNM',report_payload(r),a)
m=dict(run_id=runid,parent_run_id=initial['run_id'],entity='CNM',status='draft',cloud_status='published',final_report_accepted=False,reconciliations_matched=len(checks),outputs=paths,finished_at=datetime.now(timezone.utc).isoformat());cloud.record_run(runid,'CNM',m);write_json(out/'run_manifest.json',m);print(json.dumps(m,default=str))
