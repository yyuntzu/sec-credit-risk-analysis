import json,pathlib,re
from decimal import Decimal as D
p=pathlib.Path(__file__).parent
ledger=json.loads((p/'bq_verified_current_ledger.json').read_text())
rows=[x for group in ledger.values() for x in group]
sources=[]
def get(tag,start,end):
    match=[x for x in rows if x['xbrl_tag']==tag and x['period_start']==start and x['period_end']==end and x['filed_date']<='2026-10-25']
    values={D(x['original_value']) for x in match}
    if len(values)!=1: raise ValueError((tag,start,end,values))
    value=values.pop()/D(1000000)
    sources.append(dict(tag=tag,start=start,end=end,value=str(value),fact_ids=[x['fact_id'] for x in match],source_urls=list({x['document_url'] for x in match})))
    return value
def duration(y,end):
    start=f'{y}-01-01'
    vals={key:get(tag,start,end) for key,tag in {
        'revenue':'RevenueFromContractWithCustomerExcludingAssessedTax','cost':'CostOfGoodsAndServicesSold',
        'operating_income':'OperatingIncomeLoss','interest':'InterestExpenseNonoperating',
        'tax':'IncomeTaxExpenseBenefit','net_income':'NetIncomeLoss','da':'DepreciationDepletionAndAmortization',
        'cfo':'NetCashProvidedByUsedInOperatingActivities'}.items()}
    vals['gross_profit']=vals['revenue']-vals['cost']
    vals['operating_expense']=vals['gross_profit']-vals['operating_income']
    vals['pretax']=vals['net_income']+vals['tax']
    vals['standard_ebitda']=sum(vals[k] for k in ['net_income','interest','tax','da'])
    return vals
periods=[('FY2024',2024,'2024-12-31'),('Q1 2025 YTD (3 months)',2025,'2025-03-31'),('FY2025',2025,'2025-12-31'),('Q2 2026 YTD (6 months)',2026,'2026-06-30')]
data=[]
for label,y,end in periods:
    v=duration(y,end)
    for k,t in {'current_assets':'AssetsCurrent','current_liabilities':'LiabilitiesCurrent','assets':'Assets','equity':'StockholdersEquity','cash':'CashAndCashEquivalentsAtCarryingValue'}.items():
        v[k]=get(t,None,end)
    v['liabilities']=v['assets']-v['equity']
    v['current_ratio']=v['current_assets']/v['current_liabilities']
    v['debt_ratio']=v['liabilities']/v['equity']
    if end.endswith('12-31'): v['ltm_ebitda']=v['standard_ebitda']
    else:
        prev=duration(y-1,f'{y-1}-12-31')
        same=duration(y-1,f'{y-1}'+end[4:])
        v['ltm_ebitda']=prev['standard_ebitda']+v['standard_ebitda']-same['standard_ebitda']
    data.append(dict(label=label,year=y,end=end,values=v))
prior=duration(2025,'2025-06-30'); current=data[-1]['values']
growth=(current['revenue']/prior['revenue']-1)*100
op0=prior['operating_income']/prior['revenue']*100; op1=current['operating_income']/current['revenue']*100
gm0=prior['gross_profit']/prior['revenue']*100; gm1=current['gross_profit']/current['revenue']*100
text=re.sub(r'\s+',' ',(p/'2026-06-30.txt').read_text())
evidence=[]
for pattern in ['Cash capital expenditures were','Interest expense was','Other Income \\(Expense\\), Net','AWS sales increased','North America sales increased','Free Cash Flow','Cost of Sales']:
    matches=list(re.finditer(pattern,text,re.I))
    for m in matches[-2:]: evidence.append(dict(pattern=pattern,offset=m.start(),excerpt=text[max(0,m.start()-100):m.start()+2000],source='2026-06-30.htm'))
uri='https://www.sec.gov/Archives/edgar/data/1018724/000101872426000026/amzn-20260630.htm'
notes=[
    f'Matched-period context: H1 2026 revenue was ${current["revenue"]:,.2f}m, up {growth:.2f}% against H1 2025, not against the requested Q1 2025 column. The filing attributes growth to AWS customer usage and higher retail unit volumes, third-party seller activity, advertising and subscriptions.',
    f'Implied gross margin was {gm1:.2f}% versus {gm0:.2f}% in H1 2025. This is revenue less cost of sales, not an Amazon-reported gross-profit subtotal; AWS infrastructure costs also appear elsewhere in operating expenses, limiting interpretation.',
    f'H1 operating margin increased from {op0:.2f}% to {op1:.2f}%. MD&A identifies AWS growth and retail operating leverage; continued infrastructure investment remains a material expense and funding requirement.',
    f'H1 interest expense increased from ${prior["interest"]:,.2f}m to ${current["interest"]:,.2f}m. The filing attributes the increase to debt, including new Notes issuances, and finance leases.',
    'H1 2026 pre-tax earnings include material non-cash Anthropic investment valuation and reclassification gains. Standard EBITDA retains these gains under the selected Net Income + Interest + Taxes + D&A definition; it should not be read as recurring cash earnings.',
]
ratio_notes=[f'Current ratio changed from {data[2]["values"]["current_ratio"]:.2f}x at December 2025 to {current["current_ratio"]:.2f}x at June 2026. Quick ratio remains pending verification of unrestricted cash, liquid securities and eligible net receivables; it is not substituted with current assets less inventory.',
    'Debt ratio below means total liabilities divided by consolidated equity. Total liabilities are derived from assets less equity and checked against the consolidated balance-sheet structure.']
leverage_notes=['Total debt and leverage remain pending full reconciliation of borrowings, finance leases and financing obligations. Operating leases are excluded under the previously approved policy; the legacy mart borrowing subtotal is not presented as complete debt.',
    'The filing reports H1 2026 cash capital expenditure of $96.3bn versus $71.4bn operating cash flow, alongside substantial strategic investment outflows and new borrowing. Credit implication: investment spending is absorbing operating cash generation and increasing reliance on financing. These MD&A amounts are rounded source disclosures.',
    'Standard EBITDA is calculated for exact LTM windows using prior FY + current YTD - prior comparable YTD for interim dates. It includes non-cash investment gains and has not been substituted with adjusted EBITDA or operating income.']
fmt=lambda v:f'({abs(v):,.2f})' if v<0 else f'{v:,.2f}'
income=[('Net sales','revenue'),('Cost of sales','cost'),('Implied gross profit','gross_profit'),('Operating expense excluding cost of sales','operating_expense'),('Operating income','operating_income'),('Gross interest expense','interest'),('Income before taxes','pretax'),('Income tax expense','tax'),('Net income','net_income')]
lines=['## B. Quarterly Review','### Financial Analysis','#### YTD (Quarterly) Income','',
    'AMZN consolidated; USD millions; as of 2026-10-25. Requested dates retained. Q1 2025 is three months and Q2 2026 is six months: their income amounts are not directly comparable and no growth rate between those columns is calculated.',
    'Draft: master-branch legacy report queries were blocked by older rows missing company identity; the newly ingested BigQuery records were separately verified by immutable IDs. dbt failed; no final v1.0 acceptance is claimed.','',
    '| Metric | Q1 2025 YTD (3 months) | % sales | Q2 2026 YTD (6 months) | % sales |','|---|---:|---:|---:|---:|']
for label,key in income:
    a=data[1]['values']; b=current
    lines.append(f'| {label} | {fmt(a[key])} | {a[key]/a["revenue"]*100:.2f}% | {fmt(b[key])} | {b[key]/b["revenue"]*100:.2f}% |')
lines+=['']+['- '+n for n in notes]+['',f'Source: [Amazon Q2 2026 10-Q, MD&A and financial statements]({uri}).','', '#### Ratios YTD','', '| Metric | 2024-12-31 | 2025-03-31 | 2025-12-31 | 2026-06-30 |','|---|---:|---:|---:|---:|']
for label,key in [('Current ratio','current_ratio'),('Debt ratio (liabilities / equity)','debt_ratio')]:
    lines.append('| '+label+' | '+' | '.join(f'{x["values"][key]*100:.2f}%' for x in data)+' |')
lines.insert(len(lines)-1,'| Quick ratio | Pending verification | Pending verification | Pending verification | Pending verification |')
lines+=['']+['- '+n for n in ratio_notes]+['','#### Leverage Analysis YTD','', '| Metric | 2024-12-31 | 2025-03-31 | 2025-12-31 | 2026-06-30 |','|---|---:|---:|---:|---:|',
    '| Total debt | Pending reconciliation | Pending reconciliation | Pending reconciliation | Pending reconciliation |',
    '| LTM Standard EBITDA | '+' | '.join(fmt(x['values']['ltm_ebitda']) for x in data)+' |',
    '| EBITDA basis | NI + Interest + Taxes + D&A | NI + Interest + Taxes + D&A | NI + Interest + Taxes + D&A | NI + Interest + Taxes + D&A |',
    '| Total leverage | Not calculable | Not calculable | Not calculable | Not calculable |','']+['- '+n for n in leverage_notes]
(p/'AMZN_credit_review.md').write_text('\n'.join(lines))
result=dict(schema_version='requested-date-review-1',final_report_accepted=False,branch='master',currency='USD',scale=1000000,periods=data,income_rows=income,income_notes=notes,ratio_notes=ratio_notes,leverage_notes=leverage_notes,source=uri,limitations=['Non-comparable requested interim lengths','Quick assets pending verification','Total debt and leverage pending lease and financing obligation reconciliation','Legacy report queries rejected older rows missing CIK','dbt run failed; existing marts are not proof of this run acceptance'])
(p/'review_data.json').write_text(json.dumps(result,indent=2,default=str))
(p/'source_evidence.json').write_text(json.dumps(dict(financial=sources,narrative=evidence),indent=2,default=str))
print('Draft saved; exact requested periods retained; no cross-duration growth calculation.')
