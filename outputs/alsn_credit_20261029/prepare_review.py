import json,pathlib,re,sys
from html.parser import HTMLParser
from decimal import Decimal as D
sys.path.insert(0,'scripts')
import sec_client
from loan_review_contract import METRICS
p=pathlib.Path(__file__).parent
class Text(HTMLParser):
    def __init__(self):super().__init__();self.parts=[];self.skip=0
    def handle_starttag(self,t,a):
        if t in ('script','style','head','ix:header'):self.skip+=1
    def handle_endtag(self,t):
        if t in ('script','style','head','ix:header'):self.skip-=1
    def handle_data(self,t):
        if not self.skip:self.parts.append(t)
for x in p.glob('*.htm'):
    parser=Text();parser.feed(x.read_text());x.with_suffix('.full.txt').write_text(re.sub(r'\s+',' ',' '.join(parser.parts)))
f=json.loads((p/'companyfacts.json').read_text());tags=f['facts']['us-gaap']
s=json.loads((p/'submissions.json').read_text())['filings']['recent']
sec_client._CIK_CACHE['ALSN']='0001411207'
c=sec_client.SECEdgarClient();c.get_company_facts=lambda ticker:f
ledger=c.extract_financial_facts('ALSN')
snapshot=dict(schema_version=1,entity='ALSN',cik='0001411207',financial_facts=ledger)
(p/'snapshot.json').write_text(json.dumps(snapshot,default=str))
req=dict(schema_version=1,mode='annual',entity='ALSN',cik='0001411207',scope='entity-wide',currency='USD',scale='1000000',as_of='2026-10-29',periods=[],evidence=[])
for role,year in zip(('fy_t_minus_3','fy_t_minus_2','fy_t_minus_1','fy_t'),range(2022,2026)):
    start=f'{year}-01-01';end=f'{year}-12-31';eid='calendar:'+role
    i=next(i for i,x in enumerate(s['reportDate']) if x==end and s['form'][i]=='10-K')
    acc=s['accessionNumber'][i];filed=s['filingDate'][i];uri='https://www.sec.gov/Archives/edgar/data/1411207/'+acc.replace('-','')+'/'+s['primaryDocument'][i]
    obs=[x for x in tags['RevenueFromContractWithCustomerExcludingAssessedTax']['units']['USD'] if x.get('start')==start and x['end']==end and x['form']=='10-K']
    assert obs
    req['periods'].append(dict(role=role,label=f'FY{year}'+(' (reference)' if year==2022 else ''),fiscal_year=year,start=start,end=end,ltm_start=start,evidence_ids=[eid],quarter=None,reason=''))
    req['evidence'].append(dict(id=eid,entity='ALSN',scope='entity-wide',source_id=acc,version=acc,document_date=filed,locator=uri+'; fiscal-year cover and annual sales interval',kind='calendar',period_roles=[role],content=json.dumps(obs),purpose='borrower'))
(p/'request.json').write_text(json.dumps(req,indent=2))
print('Request and SEC ledger ready')
records=[];audit={}
def get(tag,start,end):
    rows=[x for x in tags[tag]['units']['USD'] if x.get('start')==start and x['end']==end and x['form']=='10-K' and x['filed']<=req['as_of']]
    vals={D(str(x['val'])) for x in rows};assert len(vals)==1,(tag,start,end,vals)
    return vals.pop(),rows
for period in req['periods']:
    start,end=period['start'],period['end'];e=next(x for x in req['evidence'] if x['id']==period['evidence_ids'][0]);text=(p/(end+'.full.txt')).read_text()
    def add(metric,start,value,locator,excerpt):
        records.append(dict(metric=metric,period_kind='instant' if start is None else 'duration',start=start,end=end,unit='USD',scale='1',value=str(value),status='sourced',reason='',definition=METRICS[metric].definition,basis='',source_id=e['source_id'],version=e['version'],document_date=e['document_date'],source_uri=e['locator'].split(';')[0],locator=locator,excerpt=excerpt,verification=dict(verified_by='Codex',verified_at=req['as_of'],method='checked_against_source')))
    gp,gpo=get('GrossProfit',start,end);op,opo=get('OperatingIncomeLoss',start,end)
    # Face-statement operating expenses include SG&A, R&D and any impairment.
    add('operating_expense',start,gp-op,'Consolidated income statement: all operating expenses below gross profit, including impairment',json.dumps(dict(gross_profit=gpo,operating_income=opo)))
    eq,eo=get('StockholdersEquity',None,end);assets,ao=get('Assets',None,end);liab,lo=get('Liabilities',None,end)
    assert assets==liab+eq
    add('net_worth',None,eq,'Consolidated total stockholders equity; no separate noncontrolling equity in balance sheet; checked Assets = Liabilities + Equity',json.dumps(eo))
    cash,co=get('CashAndCashEquivalentsAtCarryingValue',None,end);ar,aro=get('AccountsReceivableNetCurrent',None,end)
    add('quick_assets',None,cash+ar,'Consolidated balance sheet: cash plus net receivables; marketable securities are non-current, excluded; inventory and other assets excluded',json.dumps(dict(cash=co,receivables=aro)))
    debt,do=get('LongTermDebt',None,end);di=text.index('NOTE 8. DEBT');debttext=text[di:di+2200]
    assert f'{int(debt/1000000):,}' in debttext
    assert re.search(r'not a party to any fin\s*ance leases',text)
    add('total_debt',None,debt,'Note 8 total debt principal BEFORE current maturities and deferred financing costs; current portion counted once; Note 10 no finance leases; operating leases excluded',debttext)
    dep,dpo=get('Depreciation',start,end);am,amo=get('AmortizationOfIntangibleAssets',start,end)
    add('da',start,dep+am,'Cash flow statement and notes: PP&E depreciation plus intangible amortization only; excludes financing-cost amortization and impairments',json.dumps(dict(depreciation=dpo,amortization=amo)))
    audit[period['role']]=dict(assets=str(assets),liabilities=str(liab),equity=str(eq),cash=str(cash),debt=str(debt),source_uri=e['locator'].split(';')[0],source_id=e['source_id'],document_date=e['document_date'])
(p/'supplement.json').write_text(json.dumps(dict(schema_version=1,entity='ALSN',cik=req['cik'],scope=req['scope'],purpose='current_borrower_evidence',records=records),indent=2))
# The disclosed interest line is NET expense. It cannot establish gross expense.
excluded=[]
for name,rows in ledger.items():
    excluded.extend(x for x in rows if x['field_name'] in ('interest_expense','interest_expense_alt','operating_expense_direct'))
    ledger[name]=[x for x in rows if x['field_name'] not in ('interest_expense','interest_expense_alt','operating_expense_direct')]
(p/'reviewed_snapshot.json').write_text(json.dumps(snapshot,default=str))
(p/'source_audit.json').write_text(json.dumps(audit,indent=2))
(p/'excluded_mappings.json').write_text(json.dumps(dict(reason='Net interest is not gross expense. Retain Standard EBITDA and interest coverage as unavailable pending verified gross expense and capitalized interest; do not substitute company Adjusted EBITDA.',records=excluded),default=str,indent=2))
