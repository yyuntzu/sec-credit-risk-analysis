"""Exact-period Jazz quarterly source preparation; no missing-value proxies."""
import json, sys, pathlib, re, html
from decimal import Decimal as D
from html.parser import HTMLParser
sys.path.insert(0, 'scripts')
from loan_review_contract import METRICS
from loan_review_pipeline import STANDARD_EBITDA_BASIS
p=pathlib.Path(__file__).parent
base=p.parent/'jazz_credit_20261028'
facts=json.loads((base/'companyfacts.json').read_text())['facts']['us-gaap']
sub=json.loads((base/'submissions.json').read_text())['filings']['recent']
class Text(HTMLParser):
 def __init__(self): super().__init__(); self.parts=[]
 def handle_data(self,data): self.parts.append(data)
parser=Text();parser.feed((p/'2026-06-30.htm').read_text());raw=' '.join(' '.join(parser.parts).split());(p/'2026-06-30.txt').write_text(raw)
req=dict(schema_version=1,mode='quarterly',entity='JAZZ',cik='0001232524',scope='entity-wide',currency='USD',scale='1000000',as_of='2026-10-28',periods=[],evidence=[])
records=[]
def get(tag,start,end):
 rows=[x for x in facts[tag]['units']['USD'] if x.get('start')==start and x['end']==end and x['filed']<=req['as_of'] and x['form'] in ('10-K','10-Q','10-K/A','10-Q/A')]
 # Preserve original precise filing observations when later comparative presentation
 # merely rounds to millions. Conflicting originals are never silently resolved.
 first=min(x['filed'] for x in rows); selected=[x for x in rows if x['filed']==first]
 values={D(str(x['val'])) for x in selected}; assert len(values)==1,(tag,start,end,selected)
 return values.pop(),selected
def source(end):
 i=next(i for i,d in enumerate(sub['reportDate']) if d==end and sub['form'][i] in ('10-K','10-Q'))
 acc=sub['accessionNumber'][i];return acc,sub['filingDate'][i],'https://www.sec.gov/Archives/edgar/data/1232524/'+acc.replace('-','')+'/'+sub['primaryDocument'][i]
def add(metric,start,end,value,excerpt,basis=''):
 acc,filed,uri=source(end)
 records.append(dict(metric=metric,period_kind='instant' if start is None else 'duration',start=start,end=end,unit='text' if METRICS[metric].unit=='text' else 'USD',scale='1',value=str(value),status='sourced',reason='',definition=METRICS[metric].definition,basis=basis,source_id=acc,version=acc,document_date=filed,source_uri=uri,locator='SEC original exact-interval XBRL and reviewed statement; original precision retained, later rounded comparative not treated as restatement',excerpt=excerpt,verification=dict(verified_by='Codex',verified_at=req['as_of'],method='checked_against_source')))
slots=[('earlier_fy_end',2024,None),('prior_interim',2025,2),('latest_fy_end',2025,None),('current_interim',2026,2)]
annual=json.loads((base/'supplement.json').read_text())['records']
for role,y,q in slots:
 start=f'{y}-01-01';end=f'{y}-'+('06-30' if q else '12-31');ltm=f'{y-1}-07-01' if q else start
 acc,filed,uri=source(end);v,obs=get('RevenueFromContractWithCustomerExcludingAssessedTax',start,end);eid='calendar:'+role
 req['periods'].append(dict(role=role,label=f'FY{y} Q2 YTD' if q else f'FY{y}',fiscal_year=y,start=start,end=end,ltm_start=ltm,evidence_ids=[eid],quarter=q,reason=''))
 req['evidence'].append(dict(id=eid,entity='JAZZ',scope='entity-wide',source_id=acc,version=acc,document_date=filed,locator=uri+'; fiscal cover and exact six-month/annual interval',kind='calendar',period_roles=[role],content=json.dumps(obs),purpose='borrower'))
 if not q:
  records.extend(x for x in annual if x['end']==end)
  for metric,tag in [('current_assets','AssetsCurrent'),('current_liabilities','LiabilitiesCurrent')]:
   value,obs=get(tag,None,end);add(metric,None,end,value,json.dumps(obs))
 else:
  for metric,tag in [('revenue','RevenueFromContractWithCustomerExcludingAssessedTax'),('operating_income','OperatingIncomeLoss'),('pretax_profit','IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments'),('income_tax','IncomeTaxExpenseBenefit'),('net_income','NetIncomeLoss')]:
   v,obs=get(tag,start,end);add(metric,start,end,v,json.dumps(obs))
  # Custom product cost is in the latest filing for both comparable six-month periods.
  h=(p/'2026-06-30.htm').read_text();costs=[]
  for m in re.finditer(r'<ix:nonFraction\b([^>]*)>(.*?)</ix:nonFraction>',h,re.S|re.I):
   a=dict(re.findall(r'([\w:-]+)="([^"]*)"',m[1]))
   if a.get('name')!='jazz:CostOfProductSalesExcludingAmortizationOfAcquiredDevelopedTechnologyAndIntangibleAssetImpairment':continue
   ctx=re.search(r'<xbrli:context\b[^>]*id="'+re.escape(a['contextRef'])+r'"[^>]*>(.*?)</xbrli:context>',h,re.S)
   if not ctx or 'explicitMember' in ctx[1] or start not in ctx[1] or end not in ctx[1]:continue
   costs.append(D(html.unescape(re.sub('<[^>]+>','',m[2])).replace(',','').strip())*D(10)**int(a.get('scale','0')))
  if len(set(costs))==1:
   cost=costs[0];rev=get('RevenueFromContractWithCustomerExcludingAssessedTax',start,end)[0];op=get('OperatingIncomeLoss',start,end)[0]
   for metric,value in [('cost_of_revenue',cost),('gross_profit',rev-cost),('operating_expense',rev-cost-op)]:
    add(metric,start,end,value,'2026 Q2 filing inline XBRL exact six-month context; acquired technology amortization excluded from product cost and retained in operating expense')
    records[-1].update(source_id='0001232524-26-000045',version='0001232524-26-000045',document_date='2026-08-03',source_uri=source('2026-06-30')[2])
  for metric,tag in [('net_worth','StockholdersEquity'),('total_liabilities','Liabilities'),('current_assets','AssetsCurrent'),('current_liabilities','LiabilitiesCurrent')]:
   try:v,obs=get(tag,None,end);add(metric,None,end,v,json.dumps(obs))
   except (KeyError,ValueError):pass
  cash,cr=get('CashAndCashEquivalentsAtCarryingValue',None,end);ar,ars=get('AccountsReceivableNetCurrent',None,end);inv,ir=get('Investments',None,end)
  add('quick_assets',None,end,cash+ar+inv,json.dumps(dict(cash=cr,receivables=ars,time_deposits=ir))+'; excludes inventory, prepayments, other assets; time deposits separate from cash')
  interest,obs=get('InterestIncomeExpenseNonoperatingNet',start,end);income,io=get('InvestmentIncomeInterest',start,end)
  add('interest_expense',start,end,-interest+income,json.dumps(dict(net=obs,investment_income=io))+'; reconstructed gross; approximate at disclosed component precision')
  components=[get(tag,None,end) for tag in ['LiabilitiesCurrent','LongTermDebtNoncurrent','OperatingLeaseLiabilityNoncurrent','DeferredIncomeTaxLiabilitiesNet','OtherLiabilitiesNoncurrent']]
  liabilities=sum(v for v,o in components);assets=get('Assets',None,end)[0];equity=get('StockholdersEquity',None,end)[0];assert liabilities+equity==assets
  add('total_liabilities',None,end,liabilities,json.dumps([o for v,o in components])+'; sum all balance-sheet liability subtotals; independently checked liabilities + equity = assets')
 # Standard EBITDA uses complete actual trailing twelve months, never YTD annualization.
 bridge=[]
 for tag,sign in [('NetIncomeLoss',1),('InterestIncomeExpenseNonoperatingNet',-1),('InvestmentIncomeInterest',1),('IncomeTaxExpenseBenefit',1),('Depreciation',1),('AmortizationOfIntangibleAssets',1)]:
  if q:
   a,ao=get(tag,f'{y-1}-01-01',f'{y-1}-12-31');b,bo=get(tag,start,end);c,co=get(tag,f'{y-1}-01-01',f'{y-1}-06-30');value=(a+b-c)*sign;obs=dict(annual=ao,current=bo,prior=co)
  else:value,obs=get(tag,start,end);value*=sign
  bridge.append(dict(tag=tag,value=str(value),observations=obs))
 add('ltm_ebitda',ltm,end,sum(D(x['value']) for x in bridge),json.dumps(bridge)+'; Standard EBITDA retains IPR&D and litigation expenses; gross interest inherits disclosed rounding',STANDARD_EBITDA_BASIS)
 add('ebitda_basis',ltm,end,STANDARD_EBITDA_BASIS,json.dumps(bridge),STANDARD_EBITDA_BASIS)
snap=json.loads((base/'reviewed_snapshot.json').read_text())
# Explicit reviewed mapping replaces only the corresponding raw candidates.
from loan_review_sources import SEC_FIELDS
excluded=[]
for statement,rows in snap['financial_facts'].items():
 kept=[]
 for row in rows:
  matched=any(row['field_name'] in SEC_FIELDS.get(x['metric'],()) and row['period_end']==x['end'] and row.get('period_start')==x['start'] for x in records)
  if matched: excluded.append(row['fact_id'])
  else: kept.append(row)
 snap['financial_facts'][statement]=kept
(p/'mapping_review.json').write_text(json.dumps(dict(excluded_fact_ids=excluded,reason='Replaced matching raw candidates with reviewed original-precision exact-period inputs. Later rounded comparative presentation is retained in original companyfacts and not silently treated as a restatement.'),indent=2))
(p/'request.json').write_text(json.dumps(req,indent=2))
(p/'supplement.json').write_text(json.dumps(dict(schema_version=1,entity='JAZZ',cik=req['cik'],scope=req['scope'],purpose='current_borrower_evidence',records=records),indent=2))
(p/'snapshot.json').write_text(json.dumps(snap))
print('Prepared',len(records),'reviewed source records')
