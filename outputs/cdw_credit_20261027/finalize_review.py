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
report=restore_report(json.loads((original/'report.json').read_text()))
initial=json.loads((original/'run_manifest.json').read_text())
acceptance=json.loads((original/'acceptance.json').read_text())
bundle=json.loads((original/'source_inputs.json').read_text())
raw=re.sub(r'\s+',' ',(p/'2026-06-30.txt').read_text())
sub=json.loads((p/'submissions.json').read_text())['filings']['recent']
i=next(i for i,x in enumerate(sub['reportDate']) if x=='2026-06-30' and sub['form'][i]=='10-Q')
acc=sub['accessionNumber'][i];uri='https://www.sec.gov/Archives/edgar/data/1402057/'+acc.replace('-','')+'/'+sub['primaryDocument'][i]
ev=dict(report.evidence)
def passage(key,marker,length,roles,after=0):
    loc=raw.index(marker,after)
    eid='reviewed-passage:'+key
    ev[eid]=Evidence(eid,report.entity,report.scope,acc,acc,date.fromisoformat(sub['filingDate'][i]),f'{uri}; normalized filing text chars {loc}:{loc+length}; {marker}', 'passage',tuple(roles),raw[loc:loc+length])
    return eid
pair=('prior_interim','current_interim');bs=('latest_fy_end','current_interim')
h1=passage('h1-mda','Six months ended June 30, 2026 compared with the six months ended June 30, 2025',2500,pair)
debt=passage('debt','6. Debt',2400,bs,50000)
product=passage('product-financing','Product Financing',1500,bs,50000)
cash=passage('working-capital','Net income adjusted for the impact of non-cash items',3500,pair,120000)
balance=passage('balance-sheet','CONSOLIDATED BALANCE SHEETS (dollars and shares',2500,bs,39000)
source_notes={
 'revenue':'管理階層指出，各營運部門均有成長，客戶需求主要來自資料儲存與伺服器、筆記型／行動裝置、軟體及網路通訊產品。',
 'gross_margin':'管理階層指出，產品組合轉向較低毛利硬體，以及部分硬體類別毛利下降，抵銷營收成長帶來的部分毛利。',
 'operating_margin':'原文指出毛利率下降，且薪酬（含績效獎金）及工作場所優化費用增加，使營業利益成長落後營收成長。',
 'pretax_margin':'本期營業利益成長落後營收，原文另指出循環額度平均借款提高，使淨利息費用增加。稅率變動影響稅後結果，不作為稅前利益率變動原因。',
 'total_debt':'借款增加與循環額度新增動用 USD 175m，以及應收帳款融資餘額增加一致；本表另納入列於存貨融資應付款、具付息性質的新產品融資 USD 62m，排除不計息的供應商融資。',
}
tables=[]
for table in report.tables:
    narratives=[]
    for n in table.narratives:
        if n.status=='supported' and n.topic in source_notes:
            base=n.text.replace('所選來源輸入未附可核實的原因證據，本段僅作數值比較。','')
            ids=(debt,product) if n.topic=='total_debt' else (h1,)
            narratives.append(replace(n,text=base+source_notes[n.topic],claim_type='cause',evidence_ids=ids))
        elif n.status=='supported' and n.topic=='liquidity':
            base=n.text.replace('所選來源輸入未附可核實的原因證據，本段僅作數值比較。','')
            context='另就同期現金流觀察，上半年營業現金流由 USD 443.1m 降至 219.7m。MD&A 指出較高營收及收款時點推升應收帳款資金占用，客戶備貨及硬體成本增加推升存貨，貿易應付款增加僅部分抵銷；此為同期現金流說明，不直接代作年底至期中流動比率變化的原因。'
            narratives.append(replace(n,text=base+context,claim_type='cause',evidence_ids=(balance,cash),period_roles=('latest_fy_end','prior_interim','current_interim')))
        elif n.status=='supported':
            narratives.append(replace(n,text=n.text.replace('所選來源輸入未附可核實的原因證據，本段僅作數值比較。','此處僅作已核對數值的比較，未推定來源未說明的原因。')))
        else:narratives.append(n)
    notes=list(table.notes)
    if table.spec.key=='income':
        notes.append(Narrative('definition','supported',text='管理階層說明報表揭露的是利息費用淨額，增加主要來自循環額度平均借款提高；未以淨額填入要求總額費用的科目。',claim_type='management',evidence_ids=(h1,),period_roles=pair,attribution='CDW management, H1 2026 MD&A'))
    if table.spec.key=='leverage':
        notes.append(Narrative('definition','supported',text='2026 年 6 月的總債務口徑包含 Debt 附註的 gross debt USD 5,838.9m，加上新產品融資 USD 62m；未扣發行成本，未將不計息供應商融資或營業租賃重複加入。',claim_type='observation',fact_ids=('total_debt:current_interim',),evidence_ids=(debt,product),period_roles=('current_interim',)))
    tables.append(replace(table,narratives=tuple(narratives),notes=tuple(notes)))
report=replace(report,evidence=ev,tables=tuple(tables))
validate_report(report,expected_mode='quarterly')
acceptance=acceptance_result(report,acceptance['reconciliations'],acceptance.get('source_limitations',()))
write_json(out/'source_inputs.json',bundle)
paths=write_report_artifacts(report,acceptance,out,source_bundle=bundle)
acceptance=json.loads((out/'acceptance.json').read_text())
write_dashboard(report,acceptance,out)
# Use the current generic exporter, adding only the already-reviewed Narrative
# and notes display to the output view. All source/formula logic is unchanged.
builder=pathlib.Path('scripts/export_loan_review_excel.mjs').read_text()
anchor=' reviewRanges.push([table.spec.key,`A${start}:G${row}`]);'
assert anchor in builder
addition='''
 row++;
 for(const n of [...table.narratives,...table.notes]) {
  const prose=n.status==='supported'?n.text:`${n.topic}: ${n.reason}`;
  review.getRange(`A${row}:G${row}`).merge();
  review.getRange(`A${row}`).values=[[text(prose)]];
  review.getRange(`A${row}:G${row}`).format={wrapText:true,rowHeight:Math.max(36,16*Math.ceil(prose.length/100))};
  row++;
 }
'''
(p/'export_review.mjs').write_text(builder.replace(anchor,addition+anchor))
deps=pathlib.Path.home()/'.cache/codex-runtimes/codex-primary-runtime/dependencies/node'
if not (p/'node_modules').exists():(p/'node_modules').symlink_to(deps/'node_modules',target_is_directory=True)
subprocess.run([str(deps/'bin/node'),str(p/'export_review.mjs'),str(out)],check=True)
cloud=ReviewCloud();cloud.ensure();run_id=uuid.uuid4().hex
cloud.stage_bundle(run_id,'CDW',bundle)
cloud.publish(run_id,'CDW',report_payload(report),acceptance)
manifest=dict(run_id=run_id,parent_run_id=initial['run_id'],entity='CDW',execution='cloud',status='draft',cloud_status='published',final_report_accepted=False,workflow='formal report followed by evidence-bound analyst narrative review; unchanged canonical financial calculations',outputs=paths,stages={'source_round_trip':'passed','formal_financial_validation':'passed','analyst_narratives':'source_checked','excel':'passed','dashboard':'passed','cloud_publish':'passed'},finished_at=datetime.now(timezone.utc).isoformat())
manifest['outputs'].update(excel_path=str((out/'loan_review.xlsx').resolve()),dashboard_path=str((out/'dashboard.html').resolve()))
cloud.record_run(run_id,'CDW',manifest);write_json(out/'run_manifest.json',manifest)
print(json.dumps(manifest,indent=2))
