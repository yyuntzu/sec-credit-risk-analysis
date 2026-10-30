"""Borrower-specific source mapping; raw ledger and exact source precision retained."""
import sys,json,pathlib,re,html
from decimal import Decimal as D
sys.path.insert(0,'scripts')
import sec_client
from loan_review_contract import METRICS
p=pathlib.Path(__file__).parent
f=json.loads((p/'companyfacts.json').read_text());tags=f['facts']['us-gaap'];s=json.loads((p/'submissions.json').read_text())['filings']['recent']
sec_client._CIK_CACHE['JAZZ']='0001232524';c=sec_client.SECEdgarClient();c.get_company_facts=lambda ticker:f
ledger=c.extract_financial_facts('JAZZ');snap=dict(schema_version=1,entity='JAZZ',cik='0001232524',financial_facts=ledger)
(p/'snapshot.json').write_text(json.dumps(snap,default=str))
def get(tag,start,end):
 rows=[x for x in tags[tag]['units']['USD'] if x.get('start')==start and x['end']==end and x['form']=='10-K' and x['filed']<='2026-10-28']
 vals={D(str(x['val'])) for x in rows};assert len(vals)==1,(tag,start,end,vals)
 return vals.pop(),rows
req=dict(schema_version=1,mode='annual',entity='JAZZ',cik='0001232524',scope='entity-wide',currency='USD',scale='1000000',as_of='2026-10-28',periods=[],evidence=[]);records=[];audit={}
for role,y in zip(['fy_t_minus_3','fy_t_minus_2','fy_t_minus_1','fy_t'],[2022,2023,2024,2025]):
 start=f'{y}-01-01';end=f'{y}-12-31';i=next(i for i,x in enumerate(s['reportDate']) if x==end and s['form'][i]=='10-K');acc=s['accessionNumber'][i];filed=s['filingDate'][i];uri='https://www.sec.gov/Archives/edgar/data/1232524/'+acc.replace('-','')+'/'+s['primaryDocument'][i]
 raw=(p/(end+'.txt')).read_text();h=(p/(end+'.htm')).read_text();eid='calendar:'+role
 rev,revrows=get('RevenueFromContractWithCustomerExcludingAssessedTax',start,end)
 req['periods'].append(dict(role=role,label=f'FY{y}'+('（參考基期）' if y==2022 else ''),fiscal_year=y,start=start,end=end,ltm_start=start,evidence_ids=[eid],quarter=None,reason=''))
 req['evidence'].append(dict(id=eid,entity='JAZZ',scope='entity-wide',source_id=acc,version=acc,document_date=filed,locator=uri+'; 10-K annual cover, year ended December 31 and exact annual revenue interval',kind='calendar',period_roles=[role],content=json.dumps(revrows),purpose='borrower'))
 def inline(tag,instant=False):
  out=[]
  for m in re.finditer(r'<ix:nonFraction\b([^>]*)>(.*?)</ix:nonFraction>',h,re.S|re.I):
   a=dict(re.findall(r'([\w:-]+)="([^"]*)"',m[1]));
   if a.get('name')!=tag:continue
   ctx=re.search(r'<xbrli:context\b[^>]*id="'+re.escape(a['contextRef'])+r'"[^>]*>(.*?)</xbrli:context>',h,re.S)
   assert ctx
   if 'explicitMember' in ctx[1] or 'typedMember' in ctx[1]:continue
   if end not in ctx[1] or (not instant and start not in ctx[1]):continue
   v=D(html.unescape(re.sub('<[^>]+>','',m[2])).replace(',','').strip())*(D(10)**int(a.get('scale','0')))*(-1 if a.get('sign')=='-' else 1)
   out.append(v)
  assert len(set(out))==1,(tag,y,out)
  return out[0]
 def add(metric,st,value,loc,content):
  records.append(dict(metric=metric,period_kind='instant' if st is None else 'duration',start=st,end=end,unit='USD',scale='1',value=str(value),status='sourced',reason='',definition=METRICS[metric].definition,basis='',source_id=acc,version=acc,document_date=filed,source_uri=uri,locator=loc,excerpt=content,verification=dict(verified_by='Codex',verified_at='2026-10-28',method='checked_against_source')))
 bs=raw[raw.index('JAZZ PHARMACEUTICALS PLC CONSOLIDATED BALANCE SHEETS'):];bs=bs[:bs.index('The accompanying notes')]
 st=raw[raw.index('JAZZ PHARMACEUTICALS PLC CONSOLIDATED STATEMENTS OF INCOME'):];st=st[:st.index('The accompanying notes')]
 cf=raw[raw.index('JAZZ PHARMACEUTICALS PLC CONSOLIDATED STATEMENTS OF CASH FLOWS'):];cf=cf[:cf.index('The accompanying notes')]
 cost=inline('jazz:CostOfProductSalesExcludingAmortizationOfAcquiredDevelopedTechnologyAndIntangibleAssetImpairment');op,_=get('OperatingIncomeLoss',start,end)
 add('cost_of_revenue',start,cost,'Income statement: Cost of product sales EXCLUDES acquired technology amortization; royalties included in total revenue',st)
 add('gross_profit',start,rev-cost,'Reviewed presentation identity: TOTAL revenue minus reported product cost; amortization remains in operating expense',st)
 add('operating_expense',start,rev-cost-op,'All operating expenses EXCLUDING product cost; includes R&D, SG&A, amortization, acquired IPR&D and impairment where present',st)
 pt,ptrows=get('IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments',start,end)
 add('pretax_profit',start,pt,'Reported pretax line before equity-method losses; DO NOT infer from net income plus tax',st)
 dep,deprows=get('Depreciation',start,end);am,amrows=get('AmortizationOfIntangibleAssets',start,end)
 add('da',start,dep+am,'Cash flow statement: exact depreciation PLUS intangible asset amortization; rounded PP&E D&A tag excluded; lease asset amortization already included, not added again',cf+'\n'+json.dumps(dict(depreciation=deprows,intangible_amortization=amrows)))
 # Net interest is not substituted as gross. The explicit reconstruction inherits
 # the published investment-income rounding (nearest $0.1m), not false precision.
 net,nrows=get('InterestIncomeExpenseNonoperatingNet',start,end);income,irows=get('InvestmentIncomeInterest',start,end)
 gross=-net+income
 note='Gross expensed interest reconstructed as reported net expense '+str(-net)+' plus reported investment interest income '+str(income)+'. Investment income is published to nearest USD 0.1m: gross interest and dependent EBITDA/leverage are approximate within that source precision; no cash-interest proxy or rounding-up to unreported exact precision.'
 add('interest_expense',start,gross,'Income statement net interest + Note Cash and Available-for-Sale Securities interest income; reconstructed gross at disclosed component precision',note+'\n'+json.dumps(dict(net_interest=nrows,investment_interest=irows)))
 eq,eqrows=get('StockholdersEquity',None,end);assets,assetrows=get('Assets',None,end)
 assert 'noncontrolling interests' not in bs.lower()
 add('net_worth',None,eq,'Balance sheet complete consolidated shareholders equity; no separate NCI equity presented',bs)
 components={tag:get(tag,None,end)[0] for tag in ['LiabilitiesCurrent','LongTermDebtNoncurrent','OperatingLeaseLiabilityNoncurrent','DeferredIncomeTaxLiabilitiesNet','OtherLiabilitiesNoncurrent']}
 liab=sum(components.values());assert liab+eq==assets,(y,liab,eq,assets)
 add('total_liabilities',None,liab,'Sum all face-statement current/noncurrent liability subtotals, independently checked against Assets - total equity',bs+'\n'+json.dumps(components,default=str))
 debt,drows=get('DebtInstrumentCarryingAmount',None,end);lease,lrows=get('FinanceLeaseLiability',None,end)
 add('total_debt',None,debt+lease,'Gross debt principal BEFORE issuance costs, PLUS finance lease liabilities; exclude operating leases, add current portions only once',json.dumps(dict(gross_debt=drows,finance_lease=lrows)))
 cash,_=get('CashAndCashEquivalentsAtCarryingValue',None,end);ar,_=get('AccountsReceivableNetCurrent',None,end);invest,_=get('Investments',None,end)
 # Time deposits have original maturities >3 months and <1 year, no restricted
 # investment amount presented in the complete balance sheet / securities note.
 add('quick_assets',None,cash+ar+invest,'Cash + current time-deposit investments + NET trade receivables; no duplicated securities included in cash; exclude inventory/prepaids/other current assets',bs)
 audit[role]=dict(year=y,assets=str(assets),liabilities=str(liab),equity=str(eq),gross_interest=str(gross),net_interest=str(-net),investment_income=str(income),da=str(dep+am),gross_principal=str(debt),finance_lease=str(lease),balance_sheet=bs,cash_flow=cf,statement=st,source_uri=uri,source_id=acc,document_date=filed)
excluded=[]
precision_excluded=[]
for name,rows in ledger.items():
 excluded.extend(x['fact_id'] for x in rows if x['field_name'] in ('da','operating_expense_direct'))
 ledger[name]=[x for x in rows if x['field_name'] not in ('da','operating_expense_direct')]
 # Reviewed annual precision selection, not an automatic earliest/latest rule.
 # FY2025 10-K reports in thousands; the 2026 Q2 comparative reports in millions.
 # The three aggregate differences fall within the latter's USD 0.05m precision.
 for x in list(ledger[name]):
  if x.get('period_end')=='2025-12-31' and x['field_name'] in ('cash','current_assets','current_liabilities') and x.get('filing_type')=='10-Q':
   precision_excluded.append(x)
   ledger[name].remove(x)
assert len(precision_excluded)==6
(p/'precision_selection_review.json').write_text(json.dumps(dict(reason='FY2025 annual original amounts in thousands retained for cash, current assets and current liabilities. Later Q1/Q2 comparative aggregate amounts are rounded to millions, differences within USD 0.05m. This is an explicit reviewed selection; original snapshot retained. Reviewed Q2 balance sheet: outputs/jazz_quarterly_20261028/2026-06-30.htm.',excluded_observations=precision_excluded),indent=2,default=str))
(p/'reviewed_snapshot.json').write_text(json.dumps(snap,default=str));(p/'request.json').write_text(json.dumps(req,indent=2));(p/'supplement.json').write_text(json.dumps(dict(schema_version=1,entity='JAZZ',cik=req['cik'],scope=req['scope'],purpose='current_borrower_evidence',records=records),indent=2));(p/'source_audit.json').write_text(json.dumps(dict(periods=audit,excluded_raw_fact_ids=excluded,reason='Rounded PP&E D&A tag is incomplete D&A. Original snapshot preserved. Gross interest reconstructed with disclosed investment-income rounding; approximations explicitly retained.'),indent=2))
print('Prepared',len(records),'supplements and four annual slots (FY2022 reference only).')
for role,a in audit.items():print(role,'interest~',D(a['gross_interest'])/1000000,'DA',D(a['da'])/1000000,'debt', (D(a['gross_principal'])+D(a['finance_lease']))/1000000)
