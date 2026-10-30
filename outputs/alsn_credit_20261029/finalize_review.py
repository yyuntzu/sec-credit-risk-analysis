import json,pathlib,sys
from dataclasses import replace
from datetime import date
from decimal import Decimal as D
sys.path.insert(0,'scripts')
from review_workflow import restore_report,write_json
from loan_review_contract import Evidence,Narrative,calculate_fact,validate_report
from loan_review_pipeline import acceptance_result,write_report_artifacts
p=pathlib.Path(__file__).parent;out=p/'delivery';out.mkdir(exist_ok=True)
r=restore_report(json.loads((p/'review/report.json').read_text()));ev=dict(r.evidence)
tags=json.loads((p/'companyfacts.json').read_text())['facts']['us-gaap'];audit=json.loads((p/'source_audit.json').read_text())
roles=tuple(x.role for x in r.periods);three=roles[1:];pair=roles[2:]
raw=(p/'2025-12-31.full.txt').read_text();a=audit['fy_t']
def passage(key,marker,length):
    i=raw.index(marker);eid='passage:'+key
    ev[eid]=Evidence(eid,r.entity,r.scope,a['source_id'],a['source_id'],date.fromisoformat(a['document_date']),a['source_uri']+f'; normalized full text chars {i}:{i+length}','passage',three,raw[i:i+length]);return eid
rev=passage('sales','North America On-Highway end market net sales were down',1900)
cost=passage('operating','Cost of sales for the year ended December 31, 2025',3600)
cf=passage('cash','Operating activities for the year ended December 31, 2025',2300)
debt=passage('debt','NOTE 8. DEBT',2800)
acq=passage('acquisition','NOTE 24. ACQUISITION',5200)
notes={
'revenue':('Sales rose 6.26% from USD 3,035m in FY2023 to 3,225m in FY2024, then fell 6.67% to 3,010m in FY2025. Management attributes the 2025 decline principally to weaker North American medium-duty and Class 8 vocational truck demand and weaker global off-highway demand; defense and overseas on-highway growth partly offset the decline.',(rev,)),
'gross_margin':('Gross margin was 48.43%, 47.41% and 48.60% in FY2023, FY2024 and FY2025. Management attributes the 2025 recovery to pricing, lower incentive compensation and the absence of 2024 UAW signing incentives, partly offset by unfavorable direct material costs.',(cost,)),
'operating_margin':('Operating profit rose from USD 919m in FY2023 to 992m in FY2024, then fell to 880m in FY2025. The FY2025 operating margin of 29.24% was 1.52 percentage points below FY2024; USD 64m of acquisition expenses and USD 29m of long-lived asset impairments weighed on earnings, partly offset by lower R&D spending.',(cost,acq)),
'pretax_margin':('Pretax profit was USD 827m, 897m and 804m in FY2023–FY2025. FY2025 net income fell 14.77% to USD 623m from 731m; lower operating earnings and a higher tax charge outweighed the improvement in other income.',(cost,)),
'liquidity':('Current ratios increased from 2.50x in FY2023 to 3.04x in FY2024 and 4.85x in FY2025. Year-end 2025 cash of USD 1,495m and unused revolving capacity of USD 745m preceded the January 2026 acquisition; these balances should not be treated as post-acquisition liquidity.',(cf,acq,debt)),
'cash_flow_ratio':('CFO increased from USD 784m in FY2023 to 801m in FY2024 and 836m in FY2025. Management attributes the latest increase to lower cash taxes and working-capital funding needs, the absence of prior-year UAW signing incentives and lower pension funding, partly offset by weaker gross profit and acquisition expenses.',(cf,)),
'debt_ratio':('Total liabilities divided by consolidated equity decreased from 307.54% in FY2023 to 223.20% in FY2024, then rose to 225.76% in FY2025. This metric measures liabilities relative to equity and differs from debt/EBITDA.',(debt,)),
'total_debt':('Debt principal declined from USD 2,518m in FY2023 to 2,414m in FY2024, then increased to 2,909m in FY2025. The USD 495m latest increase mainly reflects the USD 500m notes issued to help finance the Dana off-highway acquisition, less term-loan amortization.',(debt,acq)),
}
tables=[]
for t in r.tables:
    ns=[]
    for n in t.narratives:
        if n.topic in notes and n.status=='supported':
            text,ids=notes[n.topic];n=replace(n,text=text,claim_type='cause',evidence_ids=ids,period_roles=three)
        ns.append(n)
    extra=list(t.notes)
    if t.spec.key=='income':extra.append(Narrative('definition','supported',text='Allison Transmission Holdings, Inc. (ALSN), consolidated. USD millions; FY2023–FY2025 are years ended December 31. FY2022 is a reference column only. Disclosed net interest expense is USD 107m / 89m / 92m for FY2023 / FY2024 / FY2025. Gross interest expense was not independently verified and is left unavailable in the formal table.',claim_type='observation',evidence_ids=(cost,),period_roles=three))
    if t.spec.key=='leverage':extra.append(Narrative('definition','supported',text='The Dana off-highway acquisition closed January 1, 2026 for approximately USD 2,732m, funded with cash, the 2025 USD 500m notes, a USD 1,200m incremental term loan and revolver borrowings. FY2025 debt and earnings exclude the subsequent acquired operations and full acquisition financing, limiting their use for a current credit decision. Standard EBITDA and its leverage ratio remain unavailable pending verified gross interest; debt-service and DSCR component definitions also remain unresolved.',claim_type='observation',evidence_ids=(acq,debt),period_roles=pair))
    tables.append(replace(t,narratives=tuple(ns),notes=tuple(extra)))
r=replace(r,tables=tuple(tables),evidence=ev);checks=[]
for period in r.periods:
    role=period.role;a=audit[role];e=dict(r.evidence);text=(p/(period.end.isoformat()+'.full.txt')).read_text()
    fxrows=[x for tag in tags if 'EffectOfExchangeRateOnCash' in tag for x in tags[tag]['units']['USD'] if x.get('start')==period.start.isoformat() and x['end']==period.end.isoformat() and x['form']=='10-K'];vals={D(str(x['val']))/1000000 for x in fxrows};assert len(vals)==1,(role,vals);fx=vals.pop()
    get=lambda m:r.facts[m+':'+role].value
    cashcalc=get('cfo')+get('cfi')+get('cff')+fx;cashreported=get('ending_cash')-get('beginning_cash');assert cashcalc==cashreported
    assets=D(a['assets'])/1000000;liab=D(a['liabilities'])/1000000;eq=D(a['equity'])/1000000;assert assets==liab+eq
    ids=[]
    for kind,marker in [('cash','Effect of exchange rate changes on cash'),('equity','TOTAL LIABILITIES')]:
        idx=text.index(marker);eid='review:'+kind+':'+role;e[eid]=Evidence(eid,r.entity,r.scope,a['source_id'],a['source_id'],date.fromisoformat(a['document_date']),a['source_uri']+f'; normalized text chars {idx}:{idx+1400}','definition',(role,),text[idx:idx+1400]+'; independently checked full statement arithmetic; cash basis cash and cash equivalents.');ids.append(eid)
    sourceid='review:source-values:'+role
    e[sourceid]=Evidence(sourceid,r.entity,r.scope,a['source_id'],a['source_id'],date.fromisoformat(a['document_date']),a['source_uri']+'; balance sheet and full cash flow statement','fact',(role,),json.dumps(a)+'; CFO/CFI/CFF and FX checked against full source cash flow statement: '+str((get('cfo'),get('cfi'),get('cff'),fx)))
    facts=dict(r.facts);fid='cash_change:'+role;facts[fid]=replace(facts[fid],evidence_ids=(ids[0],sourceid));r=replace(r,facts=facts,evidence=e);r=calculate_fact(r,fid,input_ids=('ending_cash:'+role,'beginning_cash:'+role),formula_version='CASH-CHANGE-v1')
    for kind,calc,reported,eid,reason in [('cash_bridge',cashcalc,cashreported,ids[0],f'Full bridge includes disclosed FX {fx}m; no plug'),('balance_sheet_equation',liab+eq,assets,ids[1],'Consolidated assets equal liabilities plus total equity')]:checks.append(dict(kind=kind,period_role=role,period=period.label,status='matched',unit='money',currency='USD',scale='1000000',calculated_value=calc,reported_value=reported,difference=calc-reported,evidence_ids=(eid,sourceid),reason=reason,source_locators=[a['source_uri']]))
# Remove stale automated reconciliation limitation after the complete bridge review.
r=replace(r,tables=tuple(replace(t,notes=tuple(n for n in t.notes if '現金／資產勾稽仍有未解釋項目' not in n.text)) for t in r.tables))
validate_report(r,expected_mode='annual');acceptance=acceptance_result(r,checks)
bundle=json.loads((p/'review/source_inputs.json').read_text());write_json(out/'source_inputs.json',bundle);paths=write_report_artifacts(r,acceptance,out,source_bundle=bundle)
write_json(out/'run_manifest.json',dict(entity='ALSN',execution='local',parent_run_id=json.loads((p/'review/run_manifest.json').read_text())['run_id'],final_report_accepted=False,reconciliations_matched=len(checks),outputs=paths))
print(json.dumps({k:v for k,v in json.loads((out/'acceptance.json').read_text()).items() if k in ('technical_validation_passed','rendered_validation_passed','acceptance_blockers')},default=str))
