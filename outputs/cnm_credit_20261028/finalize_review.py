"""Analyst-reviewed narratives over the canonical formal report; no new financial calculations."""
import json,pathlib,re,sys,uuid,shutil,subprocess,os
from dataclasses import replace
from datetime import date,datetime,timezone
sys.path.insert(0,'scripts')
from review_workflow import restore_report,write_json
from review_outputs import report_payload,write_dashboard
from loan_review_contract import Evidence,Narrative,validate_report
from loan_review_pipeline import acceptance_result,write_report_artifacts
from review_cloud import ReviewCloud
p=pathlib.Path(__file__).parent
original=p/'review_cloud'
out=p/'reviewed'
out.mkdir(exist_ok=True)
assert not any(out.iterdir()), 'Reviewed output directory must be empty'
from agent_runner import prepare_loan_review_source_stage
from loan_review_pipeline import report_from_source_bundle
initial=json.loads((original/'run_manifest.json').read_text())
cloud=ReviewCloud();cloud.ensure();run_id=uuid.uuid4().hex
bundle=prepare_loan_review_source_stage('CNM',json.loads((p/'request.json').read_text()),[json.loads((p/'supplement.json').read_text())],snapshot=json.loads((p/'reviewed_snapshot.json').read_text()))
bundle=cloud.stage_bundle(run_id,'CNM',bundle)
report,acceptance=report_from_source_bundle(bundle)
# Reuse the previously authorized dashboard decision only.
prior=restore_report(json.loads((original/'report.json').read_text()))
eid=prior.decisions['DEC-11']
report=replace(report,evidence={**report.evidence,eid:prior.evidence[eid]},decisions={**report.decisions,'DEC-11':eid})
raw=re.sub(r'\s+',' ',(p/'2026-02-01.txt').read_text())
sub=json.loads((p/'submissions.json').read_text())['filings']['recent']
i=next(i for i,x in enumerate(sub['reportDate']) if x=='2026-02-01' and sub['form'][i]=='10-K')
acc=sub['accessionNumber'][i];uri='https://www.sec.gov/Archives/edgar/data/1856525/'+acc.replace('-','')+'/'+sub['primaryDocument'][i]
ev=dict(report.evidence)
def passage(key,marker,length,roles,after=0):
    loc=raw.index(marker,after)
    eid='reviewed-passage:'+key
    ev[eid]=Evidence(eid,report.entity,report.scope,acc,acc,date.fromisoformat(sub['filingDate'][i]),f'{uri}; normalized filing text chars {loc}:{loc+length}; {marker}', 'passage',tuple(roles),raw[loc:loc+length])
    return eid
pair=('fy_t_minus_1','fy_t')
mda=passage('operations','Net sales for fiscal 2025',4200,pair,200000)
cash=passage('cash-flow','Operating Activities',2500,pair,240000)
debt=passage('gross-debt','6) DEBT',3500,pair,300000)
reasons={
 'revenue':'管理階層指出，銷量與收購帶動平均每日銷售額增加 4.8%，但 FY2025 比 FY2024 少一週，全年營收成長為 2.8%。',
 'gross_margin':'管理階層指出，毛利改善措施及採購、定價紀律，使毛利率由 26.6% 提高至 26.9%。',
 'operating_margin':'毛利增加 USD 79m，但 SG&A 增加 USD 76m，來自收購、人員薪酬福利、配送成本與科技投入，營業利益僅增加 USD 3m。',
 'interest_expense':'管理階層指出，前一年度定期貸款利差修訂、較低利率及 ABL 借款減少，使利息費用由 USD 142m 降至 120m。',
 'pretax_margin':'營業利益僅增加 USD 3m；利息費用減少 USD 22m，有助稅前利益由 USD 577m 升至 607m。稅率變動不作為稅前利益率的原因。',
 'cash_flow_ratio':'管理階層指出，現金利息與現金所得稅各減少 USD 64m，加上較高淨利，使營業現金流增至 USD 650m；較高營運資金占用部分抵銷改善。',
 'total_debt':'債務附註顯示，ABL 餘額由 USD 93m 降至零，兩筆定期貸款亦攤還；本表採扣除發行成本前本金，總額由 USD 2,283m 降至 2,166m。',
 'total_leverage':'依本報告標準 EBITDA，FY2025 為 USD 919m，FY2024 為 913m；債務本金下降是槓桿由 2.50 倍降至 2.36 倍的主要算術因素。此 EBITDA 並非公司 covenant／Adjusted EBITDA。',
}
tables=[]
for table in report.tables:
 ns=[]
 for n in table.narratives:
  if n.status=='supported' and n.topic in reasons:
   ids=(cash,) if n.topic=='cash_flow_ratio' else (debt,) if n.topic in ('total_debt','total_leverage') else (mda,)
   base=n.text.replace('所選來源輸入未附可核實的原因證據，本段僅作數值比較。','')
   ns.append(replace(n,text=base+reasons[n.topic],claim_type='cause',evidence_ids=ids,period_roles=pair))
  else:ns.append(n)
 notes=list(table.notes)
 if table.spec.key=='income':
  notes.append(Narrative('definition','supported',text='FY2023 截至 2024-01-28；FY2024 截至 2025-02-02（53 週）；FY2025 截至 2026-02-01（52 週）。FY2022 僅為系統年度格式的參考基期。淨利採合併淨利、包含非控制權益；EBITDA 使用現金流量表完整 D&A，避免與損益表 D&A 重複加計。',claim_type='observation',evidence_ids=(mda,),period_roles=pair))
 if table.spec.key=='liquidity':
  notes.append(Narrative('definition','supported',text='速動資產採現金加淨額客戶應收帳款的保守口徑；供應商回饋應收款未確認現金變現性而排除。FY2025 客戶應收款 USD 981m、供應商回饋 USD 67m，合計財報應收款 USD 1,048m。',claim_type='observation',period_roles=pair))
 tables.append(replace(table,narratives=tuple(ns),notes=tuple(notes)))
report=replace(report,evidence=ev,tables=tuple(tables))
validate_report(report,expected_mode='annual')
acceptance=acceptance_result(report,acceptance['reconciliations'],acceptance.get('source_limitations',()))
write_json(out/'source_inputs.json',bundle)
paths=write_report_artifacts(report,acceptance,out,source_bundle=bundle)
acceptance=json.loads((out/'acceptance.json').read_text())
write_dashboard(report,acceptance,out)
# Use the current generic exporter, adding only the already-reviewed Narrative
# and notes display to the output view. All source/formula logic is unchanged.
(p/'export_review.mjs').write_text(pathlib.Path('outputs/cdw_credit_20261027/export_review.mjs').read_text())
deps=pathlib.Path.home()/'.cache/codex-runtimes/codex-primary-runtime/dependencies/node'
if not (p/'node_modules').exists():(p/'node_modules').symlink_to(deps/'node_modules',target_is_directory=True)
subprocess.run([str(deps/'bin/node'),str(p/'export_review.mjs'),str(out)],check=True)
cloud.publish(run_id,'CNM',report_payload(report),acceptance)
manifest=dict(run_id=run_id,parent_run_id=initial['run_id'],entity='CNM',execution='cloud',status='draft',cloud_status='published',final_report_accepted=False,workflow='formal report followed by evidence-bound analyst narrative review; unchanged canonical financial calculations',outputs=paths,stages={'source_round_trip':'passed','formal_financial_validation':'passed','analyst_narratives':'source_checked','excel':'passed','dashboard':'passed','cloud_publish':'passed'},finished_at=datetime.now(timezone.utc).isoformat())
manifest['outputs'].update(excel_path=str((out/'loan_review.xlsx').resolve()),dashboard_path=str((out/'dashboard.html').resolve()))
cloud.record_run(run_id,'CNM',manifest);write_json(out/'run_manifest.json',manifest)
print(json.dumps(manifest,indent=2))
