"""Bind reviewed SEC passages and full reconciliations to the canonical JAZZ report."""
import sys,json,pathlib,re,uuid,subprocess
from dataclasses import replace
from datetime import date,datetime,timezone
from decimal import Decimal as D
sys.path.insert(0,'scripts')
from review_workflow import restore_report,write_json
from review_outputs import report_payload,write_dashboard
from loan_review_contract import Evidence,Narrative,calculate_fact,validate_report
from loan_review_pipeline import acceptance_result,write_report_artifacts
from review_cloud import ReviewCloud
p=pathlib.Path(__file__).parent;original=p/'verified_annual';out=p/'delivery_final';out.mkdir(exist_ok=True);assert not any(out.iterdir())
r=restore_report(json.loads((original/'report.json').read_text()));old=json.loads((original/'run_manifest.json').read_text());bundle=json.loads((original/'source_inputs.json').read_text());audit=json.loads((p/'source_audit.json').read_text())['periods'];raw=(p/'2025-12-31.txt').read_text();tags=json.loads((p/'companyfacts.json').read_text())['facts']['us-gaap']
ev=dict(r.evidence);pair=('fy_t_minus_1','fy_t');three=('fy_t_minus_2','fy_t_minus_1','fy_t');allroles=tuple(x.role for x in r.periods);latest=audit['fy_t']
def passage(key,marker,length,roles=pair,after=470000):
 loc=raw.index(marker,after);eid='reviewed-passage:'+key
 ev[eid]=Evidence(eid,r.entity,r.scope,latest['source_id'],latest['source_id'],date.fromisoformat(latest['document_date']),latest['source_uri']+f'; normalized text chars {loc}:{loc+length}; '+marker,'passage',tuple(roles),raw[loc:loc+length]);return eid
rev=passage('revenue','Xywav product sales increased by 12%',5000,three)
cost=passage('cost','Cost of Product Sales',900,three)
expense=passage('expense','Selling, General and Administrative Expenses',5900,three)
iprd=passage('iprd','Acquired In-Process Research and Development Acquired IPR&D expense',750,three)
interest=passage('interest','Interest Expense, Net Interest expense',1050,three)
cf=passage('cash-flow','Operating activities Net cash provided by operating activities decreased',4300,three)
debt=passage('debt','11. Debt The following table',10000)
invest=passage('cash-investments','4. Cash and Available-for-Sale Securities',2500)
bs=passage('balance','JAZZ PHARMACEUTICALS PLC CONSOLIDATED BALANCE SHEETS',2200)
inc=passage('income-statement','JAZZ PHARMACEUTICALS PLC CONSOLIDATED STATEMENTS OF INCOME',1850,three)
oci=passage('comprehensive-income','JAZZ PHARMACEUTICALS PLC CONSOLIDATED STATEMENTS OF COMPREHENSIVE INCOME',1600,three)
texts={
'revenue':('管理階層指出，FY2025 Xywav 銷量增加 14%、營收增加 12%，Epidiolex/Epidyolex 銷量增加 7%、營收增加 9%，帶動整體營收成長；Xyrem 受高鈉 oxybate 競爭及患者轉用 Xywav 影響，下滑 38%，部分抵銷成長。',(rev,)),
'gross_margin':('管理階層指出，產品組合及收購存貨公允價值加價費用增加，使成本上升。本表以「總營收（含權利金）減產品成本」計毛利，且取得技術攤銷列營業費用；與公司僅以淨產品銷售額計算的 87.5%／88.3% 毛利率分母不同。',(cost,inc)),
'operating_margin':('管理階層指出，FY2025 acquired IPR&D USD 947.862m，包括 Chimerix 的 Modeyso USD 905.4m 及 Saniona upfront USD 42.5m；SG&A 另受 Xyrem 反壟斷和解 USD 233.5m、Avadel 和解 USD 90m，以及薪酬與商業投入增加影響。R&D 減少 USD 101.3m，僅部分抵銷費用增幅。',(expense,iprd)),
'interest_expense':('管理階層指出，定期貸款利息下降，部分被 2030 Notes 全年利息及投資利息收入減少抵銷，使淨利息費用減少 USD 43.046m。表內採淨費用加回明確揭露投資利息收入重建「費用化總額」，受利息收入披露至 USD 0.1m 的精度限制，金額及相關 EBITDA／槓桿為近似值。',(interest,invest)),
'pretax_margin':('收購 IPR&D 及和解等營運費用使營業結果轉虧，利息淨費用減少僅部分抵銷，稅前損失為 USD 627.859m。稅益不作為稅前變動原因，且報導稅前項目位於 equity-method investee loss 之前，不能以淨利加稅費直接取代。',(expense,iprd,inc)),
'liquidity':('截至 FY2025 年底，2026 Notes USD 1,000m 轉列流動到期，帶動流動負債增加；同時 Chimerix 收購及還債消耗現金，使流動比率下降。現金加短期定存投資為 USD 2,441.899m，另有 USD 885m 未動用循環額度；兩者性質分列，未將額度加進速動資產。',(bs,debt,invest,cf)),
'cash_flow_ratio':('FY2025 CFO 減少 USD 40.135m；管理階層指出，現金支付訴訟和解 USD 323.5m，部分被銷售收現成長與應計費用支付時點抵銷。此比率亦受 2026 Notes 轉列流動到期、年末流動負債增加影響，不能全歸因於現金流下降。',(cf,bs)),
'debt_ratio':('合併負債下降與定期貸款償還一致。雖年度淨損使保留盈餘減少，外幣換算等其他綜合利益及資本項目使合併權益仍高於前年底；本表採總權益、不扣商譽或無形資產。',(bs,debt,inc)),
'ltm_ebitda':('Standard EBITDA 保留 acquired IPR&D 與和解費用，未將其加回；FY2025 大額費用使此 EBITDA 下降。加回的 D&A 僅為現金流量表折舊加無形資產攤銷，不包含存貨公允價值加價、股權薪酬或 IPR&D。利息總額重建的披露精度限制亦適用。',(expense,iprd,inc)),
 'total_debt':('FY2025 自願償還定期貸款 USD 750m，另有 USD 31m 定期攤還。總債務採本金加融資租賃，從 USD 6,196.509m 降至 5,414.379m，排除發行成本抵減與營業租賃。',(debt,cf)),
 'total_leverage':('債務本金雖下降，但保留收購及和解費用的 Standard EBITDA 分母降幅更大，槓桿因此顯著上升。此數值並非公司 Adjusted EBITDA 或契約槓桿，不可據此推定違約；因投資利息收入披露精度，EBITDA 與倍數為近似值。',(expense,iprd,debt)),
}
tables=[]
for t in r.tables:
 ns=[]
 for n in t.narratives:
  if n.status=='supported' and n.topic in texts:
   text,ids=texts[n.topic]
   if n.topic=='debt_ratio':ids=ids+(oci,)
   base=n.text.replace('所選來源輸入未附可核實的原因證據，本段僅作數值比較。','');ns.append(replace(n,text=base+text,claim_type='cause',evidence_ids=ids))
  else:ns.append(n)
 notes=list(t.notes)
 if t.spec.key=='income':
  notes.append(Narrative('material_exception','supported',text='FY2024 營收由 USD 3,834.204m 增至 4,068.950m，營業利益由 578.580m 增至 716.630m；管理階層指出 Xywav、Epidiolex 及授權學名藥權利金帶動成長。FY2025 淨損 USD 356.148m，另包含 USD 272.443m 稅益及 USD 0.732m equity-method loss；不可將該稅益視為現金流入。',claim_type='cause',evidence_ids=(rev,expense,inc),period_roles=three))
  notes.append(Narrative('definition','supported',text='FY2023–FY2025 均為截至 12 月 31 日完整年度；FY2022 僅為參考基期。利息總額由淨費用加投資利息收入重建，收入披露至 USD 0.1m，故總額及依賴它的 EBITDA、槓桿為近似值，2 位小數為顯示格式。取得技術攤銷未納入產品成本，保留在營業費用。',claim_type='observation',evidence_ids=(inc,invest),period_roles=pair))
 if t.spec.key=='ratios':notes.append(Narrative('definition','supported',text='速動資產包括現金及約當現金、短期定存投資與淨額應收帳款；現金中的 money-market funds 不再重複計入投資。排除存貨、預付款與其他流動資產。資本化利息未取得可核對的明確金額，CF-04／CF-05 保留待確認，未假設為零。',claim_type='observation',evidence_ids=(invest,bs),period_roles=pair))
 tables.append(replace(t,narratives=tuple(ns),notes=tuple(notes)))
r=replace(r,evidence=ev,tables=tuple(tables));checks=[]
for period in r.periods:
 role=period.role;a=audit[role];e=dict(r.evidence);src=a['source_id'];docdate=date.fromisoformat(a['document_date']);uri=a['source_uri']
 def evidence(key,kind,content,loc):
  eid=key+':'+role;e[eid]=Evidence(eid,r.entity,r.scope,src,src,docdate,uri+'; '+loc,kind,(role,),content);return eid
 factid=evidence('review:statement','fact',json.dumps(a),'Consolidated balance sheet, cash flow statement and verified liability components')
 bsid=evidence('review:equity','definition','All face-statement liabilities summed independently. No NCI equity line presented; complete consolidated equity used. '+a['balance_sheet'],'balance sheet complete liability/equity scope')
 cashid=evidence('review:cash','definition','Opening and closing cash & equivalents share identical scope. Full bridge explicitly includes reported FX; no inferred FX or restricted-cash plug. '+a['cash_flow'],'cash flow statement, all flows plus FX')
 get=lambda metric:r.facts[metric+':'+role].value
 rows=[x for x in tags['EffectOfExchangeRateOnCashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents']['units']['USD'] if x.get('start')==period.start.isoformat() and x['end']==period.end.isoformat() and x['form']=='10-K'];fxvals={D(str(x['val']))/1000000 for x in rows};assert len(fxvals)==1;fx=fxvals.pop()
 assert get('ending_cash') is not None and get('beginning_cash') is not None
 cashcalc=get('cfo')+get('cfi')+get('cff')+fx;cashreported=get('ending_cash')-get('beginning_cash');assert cashcalc==cashreported
 assets=D(a['assets'])/1000000;liab=D(a['liabilities'])/1000000;equity=D(a['equity'])/1000000;assert assets==liab+equity
 fid='cash_change:'+role;facts=dict(r.facts);facts[fid]=replace(facts[fid],evidence_ids=(cashid,factid));r=replace(r,evidence=e,facts=facts);r=calculate_fact(r,fid,input_ids=('ending_cash:'+role,'beginning_cash:'+role),formula_version='CASH-CHANGE-v1')
 for kind,calc,reported,ids,reason in [('cash_bridge',cashcalc,cashreported,(cashid,factid),'Complete source bridge including reported FX '+str(fx)+' million'),('balance_sheet_equation',liab+equity,assets,(bsid,factid),'Sum of source liability rows plus full consolidated equity')]:checks.append(dict(kind=kind,period_role=role,period=period.label,status='matched',unit='money',currency='USD',scale='1000000',calculated_value=calc,reported_value=reported,difference=calc-reported,evidence_ids=ids,reason=reason,source_locators=[uri]))
validate_report(r,expected_mode='annual');a=acceptance_result(r,checks)
write_json(out/'source_inputs.json',bundle);paths=write_report_artifacts(r,a,out,source_bundle=bundle);a=json.loads((out/'acceptance.json').read_text());write_dashboard(r,a,out)

write_json(out/'run_manifest.json', dict(entity='JAZZ',execution='local',parent_run_id=old['run_id'],final_report_accepted=a['final_report_accepted'],reconciliations_matched=len(checks),outputs=paths))
print(json.dumps(a,default=str))
