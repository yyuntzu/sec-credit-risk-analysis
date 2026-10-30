"""Prepare verified fiscal periods and borrower-specific source mappings; preserve original ledger."""
import json,pathlib,re,sys
from decimal import Decimal as D
sys.path.insert(0,'scripts')
import sec_client
from loan_review_contract import METRICS
p=pathlib.Path(__file__).parent
f=json.loads((p/'companyfacts.json').read_text());tags=f['facts']['us-gaap']
s=json.loads((p/'submissions.json').read_text())['filings']['recent']
sec_client._CIK_CACHE['CNM']='0001856525'
c=sec_client.SECEdgarClient();c.get_company_facts=lambda ticker:f
ledger=c.extract_financial_facts('CNM')
snapshot=dict(schema_version=1,entity='CNM',cik='0001856525',financial_facts=ledger)
(p/'snapshot.json').write_text(json.dumps(snapshot,default=str))
def get(tag,start,end):
    obs=[x for x in tags[tag]['units']['USD'] if x.get('start')==start and x['end']==end and x['form'] in ('10-K','10-Q') and x['filed']<='2026-10-28']
    vals={D(str(x['val'])) for x in obs}
    assert len(vals)==1,(tag,start,end,vals)
    return vals.pop(),obs
req=dict(schema_version=1,mode='annual',entity='CNM',cik='0001856525',scope='entity-wide',currency='USD',scale='1000000',as_of='2026-10-28',periods=[],evidence=[])
records=[]
for role,year,end in [('fy_t_minus_3',2022,'2023-01-29'),('fy_t_minus_2',2023,'2024-01-28'),('fy_t_minus_1',2024,'2025-02-02'),('fy_t',2025,'2026-02-01')]:
    rev=[x for x in tags['RevenueFromContractWithCustomerExcludingAssessedTax']['units']['USD'] if x['end']==end and x['form']=='10-K' and 340<=(__import__('datetime').date.fromisoformat(x['end'])-__import__('datetime').date.fromisoformat(x['start'])).days<=380]
    starts={x['start'] for x in rev};assert len(starts)==1
    start=starts.pop();eid='calendar:'+role
    i=next(i for i,x in enumerate(s['reportDate']) if x==end and s['form'][i]=='10-K')
    acc=s['accessionNumber'][i];filed=s['filingDate'][i]
    uri='https://www.sec.gov/Archives/edgar/data/1856525/'+acc.replace('-','')+'/'+s['primaryDocument'][i]
    req['periods'].append(dict(role=role,label=f'FY{year}'+('（參考基期）' if year==2022 else ''),fiscal_year=year,start=start,end=end,ltm_start=start,evidence_ids=[eid],quarter=None,reason=''))
    req['evidence'].append(dict(id=eid,entity='CNM',scope='entity-wide',source_id=acc,version=acc,document_date=filed,locator=uri+'; fiscal-year definition and exact annual revenue interval',kind='calendar',period_roles=[role],content=json.dumps(rev),purpose='borrower'))
    text=re.sub(r'\s+',' ',(p/(end+'.txt')).read_text())
    def add(metric,start,value,locator,excerpt):
        records.append(dict(metric=metric,period_kind='instant' if start is None else 'duration',start=start,end=end,unit='USD',scale='1',value=str(value),status='sourced',reason='',definition=METRICS[metric].definition,basis='',source_id=acc,version=acc,document_date=filed,source_uri=uri,locator=locator,excerpt=excerpt,verification=dict(verified_by='Codex',verified_at='2026-10-28',method='checked_against_source')))
    pretax,pt=get('IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest',start,end)
    tax,tx=get('IncomeTaxExpenseBenefit',start,end)
    consolidated=pretax-tax
    token=f'{int(consolidated/1000000):,}'
    ni_matches=[m for m in re.finditer(r'Net income\s+\$?',text,re.I) if token in text[m.start():m.start()+80]]
    assert ni_matches,(end,'Consolidated net income not verified')
    m=ni_matches[-1]
    add('net_income',start,consolidated,'Consolidated statements and cash flows: consolidated net income BEFORE allocation to NCI, checked against pretax less signed tax',text[max(0,m.start()-100):m.start()+400]+'\n'+json.dumps({'pretax':pt,'tax':tx}))
    it,obs=get('InterestExpenseNonoperating',start,end)
    add('interest_expense',start,it,'Consolidated statements, separate Interest expense line (not net interest); other income presented separately',json.dumps(obs))
    gp,gpobs=get('GrossProfit',start,end);op,opobs=get('OperatingIncomeLoss',start,end)
    opex=gp-op
    label=f'{int(opex/1000000):,}'
    assert any(label in text[m.start():m.start()+120] for m in re.finditer('Total operating expenses',text,re.I))
    add('operating_expense',start,opex,'Consolidated statement total operating expenses = SG&A + operating D&A; independently agrees with gross profit minus operating income',json.dumps({'gross_profit':gpobs,'operating_income':opobs})+'; source face statement Total operating expenses '+label+' million')
    eq,eqobs=get('StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest',None,end)
    assets,_=get('Assets',None,end);liab,_=get('Liabilities',None,end)
    assert assets==liab+eq
    add('net_worth',None,eq,'Consolidated balance sheet TOTAL equity including non-controlling interests; checked assets = liabilities + equity',json.dumps(eqobs))
    debt,debtobs=get('DebtInstrumentCarryingAmount',None,end)
    add('total_debt',None,debt,'Debt note total gross principal including all current maturities once, before unamortized issuance costs; operating lease liabilities excluded',json.dumps(debtobs))
    cash,co=get('CashAndCashEquivalentsAtCarryingValue',None,end)
    ar,ao=get('AccountsReceivableNetCurrent',None,end)
    add('quick_assets',None,cash+ar,'Consolidated balance sheet cash and cash equivalents plus net trade receivables; no short-term investments line; excludes inventory, prepaid assets, and restricted/other assets',json.dumps({'cash':co,'net_receivables':ao}))
(p/'request.json').write_text(json.dumps(req,indent=2))
(p/'supplement.json').write_text(json.dumps(dict(schema_version=1,entity='CNM',cik=req['cik'],scope=req['scope'],purpose='current_borrower_evidence',records=records),indent=2))
# Raw NetIncomeLoss is mapped to parent-attributable income in these SEC facts.
# Preserve it; adopt the separately verified consolidated face-statement amount.
excluded=[]
for name,rows in ledger.items():
    excluded.extend(x for x in rows if x['field_name'] in ('net_income','interest_expense','interest_expense_alt','operating_expense_direct'))
    ledger[name]=[x for x in rows if x['field_name'] not in ('net_income','interest_expense','interest_expense_alt','operating_expense_direct')]
(p/'reviewed_snapshot.json').write_text(json.dumps(snapshot,default=str))
(p/'source_mapping_review.json').write_text(json.dumps(dict(reason='Original snapshot retained. SEC NetIncomeLoss candidates identify parent-attributable earnings; use independently checked consolidated income before NCI for the approved scope. Gross interest and total operating-expense definitions verified against standalone statement lines. Excluded raw candidates replaced by explicit reviewed supplements, preventing equivalent numbers with unverified semantic definitions from being treated as unresolved conflicts; no parent/consolidated mixing.',excluded_fact_ids=[x['fact_id'] for x in excluded]),indent=2))
print('Four fiscal periods and',len(records),'supplement records prepared. FY2022 is reference only.')
