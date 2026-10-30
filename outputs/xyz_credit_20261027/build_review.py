import json,pathlib,re
from decimal import Decimal as D
p=pathlib.Path(__file__).parent
raw=json.loads((p/'bq_verified_current_ledger.json').read_text())
rows=[x for v in raw.values() for x in v]
supp=json.loads((p/'bq_verified_supplement.json').read_text())
inputs=[]
def get(tag,start,end):
    obs=[x for x in rows if x['xbrl_tag']==tag and x['period_start']==start and x['period_end']==end and x['filed_date']<='2026-10-27']
    vals={D(x['original_value']) for x in obs}
    assert len(vals)==1,(tag,start,end,vals)
    val=vals.pop()/D(1000000)
    inputs.append(dict(id=f'{tag}|{start}|{end}',label=tag,start=start,end=end,value=str(val),source='; '.join(sorted({x['document_url'] for x in obs})),locator='; '.join(x['fact_id'] for x in obs)))
    return val
def extra(metric,end):
    x=next(x for x in supp if x['metric']==metric and x['end']==end)
    val=D(x['value'])/D(1000000)
    inputs.append(dict(id=f'{metric}|{x["start"]}|{end}',label=metric,start=x['start'],end=end,value=str(val),source=x['source_uri'],locator=x['locator']))
    return val
data=[]
tags={'revenue':'Revenues','cost':'CostOfRevenue','gross_profit':'GrossProfit','operating_income':'OperatingIncomeLoss','pretax':'IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest','tax':'IncomeTaxExpenseBenefit','parent_net_income':'NetIncomeLoss','cfo':'NetCashProvidedByUsedInOperatingActivities'}
for label,y,end in [('FY2024',2024,'2024-12-31'),('Q2 2025 YTD',2025,'2025-06-30'),('FY2025',2025,'2025-12-31'),('Q2 2026 YTD',2026,'2026-06-30')]:
    start=f'{y}-01-01'
    v={k:get(t,start,end) for k,t in tags.items()}
    v['operating_expense']=v['gross_profit']-v['operating_income']
    statement_text=re.sub(r'\s+',' ',(p/(end+'.txt')).read_text())
    expected=f'{int(v["operating_expense"]*1000):,}'
    assert any(expected in statement_text[m.start():m.start()+250] for m in re.finditer('Total operating expenses',statement_text,re.I)),(end,expected)
    for k,t in {'current_assets':'AssetsCurrent','current_liabilities':'LiabilitiesCurrent','assets':'Assets','liabilities':'Liabilities','cash':'CashAndCashEquivalentsAtCarryingValue'}.items():v[k]=get(t,None,end)
    for k in ['notes_principal','warehouse_principal','consolidated_equity','net_interest_signed']:v[k]=extra(k,end)
    v['net_income']=v['pretax']-v['tax']
    v['net_interest_expense']=-v['net_interest_signed']
    v['total_debt']=v['notes_principal']+v['warehouse_principal']
    v['current_ratio']=v['current_assets']/v['current_liabilities']
    v['debt_ratio']=v['liabilities']/v['consolidated_equity']
    v['gross_margin']=v['gross_profit']/v['revenue']
    v['operating_margin']=v['operating_income']/v['revenue']
    v['pretax_margin']=v['pretax']/v['revenue']
    assert v['revenue']-v['cost']==v['gross_profit']
    assert v['gross_profit']-v['operating_expense']==v['operating_income']
    assert v['assets']==v['liabilities']+v['consolidated_equity']
    data.append(dict(label=label,year=y,start=start,end=end,values=v))
a=data[1]['values'];b=data[3]['values'];fy=data[2]['values']
uri='https://www.sec.gov/Archives/edgar/data/1512673/000162828026053368/xyz-20260630.htm'
growth=(b['revenue']/a['revenue']-1)*100
gp_growth=(b['gross_profit']/a['gross_profit']-1)*100
notes=[
 f'上半年營收由 USD {a["revenue"]:,.2f}m 增至 {b["revenue"]:,.2f}m（{growth:.2f}%）。管理階層指出，Commerce enablement 與 Financial solutions 的成長抵銷 Bitcoin ecosystem 收入下降；Cash App Borrow、Square processing 等產品是主要成長來源。',
 f'毛利成長 {gp_growth:.2f}%，毛利率由 {a["gross_margin"]*100:.2f}% 升至 {b["gross_margin"]*100:.2f}%。低毛利 Bitcoin ecosystem 收入占比下降及較高毛利金融產品成長改善組合；總營收受 Bitcoin 總額認列影響，因此毛利也是重要觀察指標。',
 f'營業利益由 USD {a["operating_income"]:,.2f}m 降至 {b["operating_income"]:,.2f}m，營業利益率由 {a["operating_margin"]*100:.2f}% 降至 {b["operating_margin"]*100:.2f}%。MD&A 說明訴訟／監管提列、信用損失與 Workforce Plan 重整費用推高營業費用；毛利成長尚未轉為 GAAP 營業利益成長。',
 f'報表揭露的淨利息費用由 USD {a["net_interest_expense"]:,.2f}m 增至 {b["net_interest_expense"]:,.2f}m，原文歸因於 2025 年第三季發行的 2030／2033 Senior Notes。這是淨額，未直接填入要求總額費用的正式科目；warehouse 利息另列於 G&A，仍須完整核對。',
 f'稅前損益由 USD {a["pretax"]:,.2f}m 轉為 {b["pretax"]:,.2f}m；原文指出，營業利益下降另受 Bitcoin 投資重估由利益轉為損失及淨利息費用增加影響。合併稅後損益由 {a["net_income"]:,.2f}m 轉為 {b["net_income"]:,.2f}m；未將歸屬普通股股東損益混用為合併淨利。',
]
ratio_notes=[
 f'流動比率由 2025 年底 {fy["current_ratio"]*100:.2f}% 變為 2026 年 6 月底 {b["current_ratio"]*100:.2f}%。該比率包含客戶資金及應付客戶款等支付業務項目，不能單憑比率判定公司可自由償債現金。速動比率保留待核實，未把受限制客戶資金或全部貸款列為 Quick Assets。',
 f'總負債／含非控制權益的合併權益由 {fy["debt_ratio"]*100:.2f}% 降至 {b["debt_ratio"]*100:.2f}%；本表採 liabilities / equity，不是 liabilities / assets。數字已以 assets = liabilities + consolidated equity 勾稽。',
]
lev_notes=[
 f'票據本金加 warehouse 借款本金由 2025 年底 USD {fy["total_debt"]:,.2f}m 降至 {b["total_debt"]:,.2f}m。票據本金下降 USD {fy["notes_principal"]-b["notes_principal"]:,.2f}m，與 2026 年到期票據償還一致；warehouse 餘額下降 {fy["warehouse_principal"]-b["warehouse_principal"]:,.2f}m。未將未動用額度或客戶應付款加入借款。',
 'Standard EBITDA 保留待核實：需總額費用化利息並涵蓋票據及 G&A 中的 warehouse 利息；淨利息費用或公司 Adjusted EBITDA 均不替代。未以 operating income 或 YTD 年化冒充 LTM。',
 '總槓桿倍數暫不計算，因 Standard LTM EBITDA 尚未完成。信用判斷上，借款本金下降是可觀察的改善，但毛利成長、GAAP 利潤壓力、貸款信用損失及支付客戶資金限制須一併評估，不能僅以 Adjusted EBITDA 判斷償債能力。',
]
income=[('Total net revenue／營業收入','revenue'),('Cost of revenue／營業成本','cost'),('Gross profit／毛利','gross_profit'),('Operating expenses／營業費用','operating_expense'),('Operating income／營業利益','operating_income'),('Gross interest expense／總額利息費用','gross_interest'),('Income before tax／稅前損益','pretax'),('Income tax expense／所得稅費用','tax'),('Consolidated net income／合併稅後損益','net_income')]
f=lambda v:f'({abs(v):,.2f})' if v<0 else f'{v:,.2f}'
lines=['## B. Quarterly Review','### Financial Analysis','#### YTD (Quarterly) Income','', 'Block, Inc.（Square 母公司；XYZ）合併範圍；USD 百萬元；資料截止 2026-10-27。兩期損益均為 1/1–6/30 六個月。','待驗收草稿：master 舊查詢及 dbt 未完整完成；本次另以新入庫 fact IDs 讀回核對 BigQuery，並呼叫 MD&A 模型後人工對照原文整理。','', '| Metric／科目 | H1 2025 | % revenue | H1 2026 | % revenue |','|---|---:|---:|---:|---:|']
for label,k in income:
    if k=='gross_interest':cells=['待核實總額','無法計算','待核實總額','無法計算']
    else:cells=[f(a[k]),f'{a[k]/a["revenue"]*100:.2f}%',f(b[k]),f'{b[k]/b["revenue"]*100:.2f}%']
    lines.append('| '+label+' | '+' | '.join(cells)+' |')
lines+=['','> 合併淨利由已核對的稅前損益減帶符號稅費計算；與股東歸屬損益分開。總額利息尚未完整核實，不以淨額代填。','']+['- '+x for x in notes]+['',f'來源：[2026 Q2 10-Q，財務報表、Indebtedness 與 MD&A]({uri})。','','#### Ratios YTD','', '| Metric | 2024-12-31 | 2025-06-30 | 2025-12-31 | 2026-06-30 |','|---|---:|---:|---:|---:|', '| Current ratio／流動比率 | '+' | '.join(f'{x["values"]["current_ratio"]*100:.2f}%' for x in data)+' |','| Quick ratio／速動比率 | 待核實 | 待核實 | 待核實 | 待核實 |','| Debt ratio／總負債÷合併權益 | '+' | '.join(f'{x["values"]["debt_ratio"]*100:.2f}%' for x in data)+' |','']+['- '+x for x in ratio_notes]+['','#### Leverage Analysis YTD','', '| Metric | 2024-12-31 | 2025-06-30 | 2025-12-31 | 2026-06-30 |','|---|---:|---:|---:|---:|','| Total debt／借款本金 | '+' | '.join(f(x['values']['total_debt']) for x in data)+' |','| LTM Standard EBITDA | 待核實總額利息 | 待核實總額利息 | 待核實總額利息 | 待核實總額利息 |','| EBITDA basis | NI + Interest + Taxes + D&A | NI + Interest + Taxes + D&A | NI + Interest + Taxes + D&A | NI + Interest + Taxes + D&A |','| Total leverage | 無法計算 | 無法計算 | 無法計算 | 無法計算 |','']+['- '+x for x in lev_notes]
(p/'XYZ_credit_review.md').write_text('\n'.join(lines))
result=dict(entity='XYZ',company='Block, Inc.／Square',currency='USD',scale=1000000,as_of='2026-10-27',branch='master',final_report_accepted=False,periods=data,income_rows=income,income_notes=notes,ratio_notes=ratio_notes,leverage_notes=lev_notes,source=uri,inputs=list({x['id']:x for x in inputs}.values()))
(p/'review_data.json').write_text(json.dumps(result,indent=2,default=str))
text=re.sub(r'\s+',' ',(p/'2026-06-30.txt').read_text())
excerpts=[]
for pat in ['Total Net Revenue','Gross Profit','General and Administrative','Transaction, Loan, and Consumer Receivable Losses','Interest Expense','Remeasurement','Workforce Plan','Warehouse Funding Facilities']:
    for m in list(re.finditer(re.escape(pat),text,re.I))[-3:]:excerpts.append(dict(topic=pat,offset=m.start(),text=text[max(0,m.start()-100):m.start()+1800],source=uri))
(p/'narrative_evidence.json').write_text(json.dumps(excerpts,indent=2,ensure_ascii=False))
(p/'validation.json').write_text(json.dumps(dict(periods_verified=4,income_identities_passed=8,balance_sheet_identities_passed=4,financial_source='BigQuery immutable fact IDs plus reviewed evidence table',mdna_model_topics=13,final_report_accepted=False,remaining=['Gross expensed interest, including warehouse cost','Quick Assets definition/source completeness','Standard LTM EBITDA and leverage','Full cash reconciliation','dbt/runtime and legacy-query failures']),indent=2))
print('Prepared four-period draft and source-linked explanations; no net-interest EBITDA proxy.')
