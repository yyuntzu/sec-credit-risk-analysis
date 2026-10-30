import json,sys,pathlib
from dataclasses import replace
from datetime import date
from decimal import Decimal as D
sys.path.insert(0,'scripts')
from review_workflow import restore_report,write_json
from loan_review_contract import Evidence,Narrative,validate_report
from loan_review_pipeline import acceptance_result,write_report_artifacts
p=pathlib.Path(__file__).parent;src=p/'review_v2';out=p/'delivery';out.mkdir(exist_ok=True)
r=restore_report(json.loads((src/'report.json').read_text()));raw=(p/'2026-06-30.txt').read_text();ev=dict(r.evidence)
uri='https://www.sec.gov/Archives/edgar/data/1232524/000123252426000045/jazz-20260630.htm'
def passage(key,marker,length):
 pos=raw.index(marker);eid='passage:'+key
 ev[eid]=Evidence(eid,'JAZZ','entity-wide','0001232524-26-000045','0001232524-26-000045',date(2026,8,3),uri+f'; normalized text characters {pos}:{pos+length}', 'passage',('prior_interim','latest_fy_end','current_interim'),raw[pos:pos+length]);return eid
rev=passage('revenue','Xywav product sales increased',4700)
cost=passage('cost','Cost of Product Sales Cost of product sales',1100)
expense=passage('expenses','Selling, General and Administrative Expenses Selling',5900)
exception=passage('iprd-prv','Acquired In-Process Research and Development Acquired',1000)
interest=passage('interest','Interest Expense, Net Interest expense',700)
liquidity=passage('liquidity','Liquidity and Capital Resources As of June 30, 2026',2200)
debt=passage('debt','9. Debt The following table',3600)
explanations={
 'revenue':('管理階層指出，Xywav 六個月銷量增加12%、Epidiolex/Epidyolex增加13%，以及Zepzelca等產品成長帶動營收；Xyrem銷量下降21%，部分抵銷成長。',(rev,)),
 'gross_margin':('管理階層指出，成本增加主要來自權利金及存貨提列，收購存貨公允價值加價費用減少USD12.8m部分抵銷；本表產品成本不含取得技術攤銷。2025成本採2026比較欄的百萬精度，相關毛利及費用為近似值。',(cost,)),
 'operating_margin':('去年同期包含Chimerix/Modeyso acquired IPR&D及Xyrem訴訟和解USD172m；本期acquired IPR&D包含AbCellera USD56m及Werewolf USD21m。另本期認列PRV出售稅前利益USD122.8m，故獲利回升不能全部視為經常性營運改善。',(expense,exception)),
 'interest_expense':('管理階層指出，定期貸款利息下降及利息收入增加使淨利息下降；本表費用化總利息另加回投資利息收入重建，並保留披露精度限制。',(interest,)),
 'pretax_margin':('收購IPR&D及訴訟費用同比減少、營收成長及PRV出售利益支持稅前結果改善；PRV USD122.8m為一次性利益。',(rev,expense,exception)),
 'ltm_ebitda':('LTM採前一完整年度加當期YTD減前年同期YTD，沒有年化。Standard EBITDA保留收購IPR&D、訴訟費用及PRV出售利益；2026年6月LTM已移出2025上半年大額費用並納入PRV利益，不能全部視為經常性成長。',(expense,exception)),
 'liquidity':('2026年6月底，現金、約當現金與投資合計約USD2.2bn；未動用循環額度USD885m另列，不加入速動資產。2030 Notes因股價條件符合轉列流動，2026 Notes已於6月到期償還；應區分流動分類與實際現金到期風險。',(liquidity,debt)),
}
tables=[]
for t in r.tables:
 ns=[]
 for n in t.narratives:
  if n.status=='supported' and n.topic in explanations:
   text,ids=explanations[n.topic];ns.append(replace(n,text=n.text.replace('所選來源輸入未附可核實的原因證據，本段僅作數值比較。','')+text,claim_type='cause',evidence_ids=ids))
  else:ns.append(n)
 notes=list(t.notes)
 if t.spec.key=='leverage':
  notes.append(Narrative('definition','supported',text='2025及2026年6月底借款本金分別約USD5,426m及4,395m；它們尚未包含已核實的同期融資租賃負債，故不替代Total Debt或計算完整總槓桿。正式口徑為本金加融資租賃、排除營業租賃。EBITDA包含PRV一次性利益，並受利息收入與2026披露精度限制。',claim_type='observation',evidence_ids=(debt,exception),period_roles=('prior_interim','current_interim')))
 if t.spec.key=='income':
  notes.append(Narrative('definition','supported',text='所得表僅比較2025及2026年1月1日至6月30日六個月YTD。四個資產負債與LTM觀察日保留FY2024、2025Q2、FY2025及2026Q2。2026申報改採百萬顯示；原先精確申報值保留，沒有將比較欄四捨五入視為重編。',claim_type='observation',evidence_ids=(rev,),period_roles=('prior_interim','current_interim')))
 tables.append(replace(t,narratives=tuple(ns),notes=tuple(notes)))
r=replace(r,evidence=ev,tables=tuple(tables));validate_report(r,expected_mode='quarterly')
bundle=json.loads((src/'source_inputs.json').read_text());a=acceptance_result(r,[])
paths=write_report_artifacts(r,a,out,source_bundle=bundle)
write_json(out/'run_manifest.json',dict(entity='JAZZ',mode='quarterly',execution='local',status='draft',final_report_accepted=False,parent_run_id=json.loads((src/'run_manifest.json').read_text())['run_id'],outputs=paths))
print(json.dumps(dict(technical=a['technical_validation_passed'],accepted=a['final_report_accepted'])))
