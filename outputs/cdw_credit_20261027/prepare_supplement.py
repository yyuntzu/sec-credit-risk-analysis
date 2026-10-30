import json,pathlib,re,sys
from decimal import Decimal as D
sys.path.insert(0,'scripts')
from loan_review_contract import METRICS
p=pathlib.Path(__file__).parent
req=json.loads((p/'request.json').read_text())
facts=json.loads((p/'companyfacts.json').read_text())['facts']['us-gaap']
sub=json.loads((p/'submissions.json').read_text())['filings']['recent']
records=[]
def val(tag,start,end):
    obs=[x for x in facts[tag]['units']['USD'] if x.get('start')==start and x['end']==end and x['form'] in ('10-K','10-Q') and x['filed']<=req['as_of']]
    values={D(str(x['val'])) for x in obs}
    assert len(values)==1,(tag,start,end,values)
    return values.pop(),obs
for period in req['periods']:
    end,start=period['end'],period['start']
    i=next(i for i,x in enumerate(sub['reportDate']) if x==end and sub['form'][i] in ('10-K','10-Q'))
    acc=sub['accessionNumber'][i]
    uri='https://www.sec.gov/Archives/edgar/data/1402057/'+acc.replace('-','')+'/'+sub['primaryDocument'][i]
    text=re.sub(r'\s+',' ',(p/(end+'.txt')).read_text())
    def add(metric,start,value,locator,excerpt):
        records.append(dict(metric=metric,period_kind='instant' if start is None else 'duration',start=start,end=end,unit='USD',scale='1',value=str(value),status='sourced',reason='',definition=METRICS[metric].definition,basis='',source_id=acc,version=acc,document_date=sub['filingDate'][i],source_uri=uri,locator=locator,excerpt=excerpt,verification=dict(verified_by='Codex',verified_at=req['as_of'],method='checked_against_source')))
    expense,obs=val('SellingGeneralAndAdministrativeExpense',start,end)
    gp,_=val('GrossProfit',start,end); op,_=val('OperatingIncomeLoss',start,end)
    assert gp-expense==op
    add('operating_expense',start,expense,'Consolidated statements of operations, Selling and administrative expenses; verified gross profit minus S&A equals operating income',json.dumps(obs))
    equity,obs=val('StockholdersEquity',None,end)
    assets,_=val('Assets',None,end)
    current_liabilities,cl_obs=val('LiabilitiesCurrent',None,end)
    noncurrent_liabilities,ncl_obs=val('LiabilitiesNoncurrent',None,end)
    liabilities=current_liabilities+noncurrent_liabilities
    assert assets-liabilities==equity
    add('total_liabilities',None,liabilities,'Consolidated balance sheet, current liabilities plus noncurrent liabilities; independently reconciled to assets minus equity',json.dumps({'current':cl_obs,'noncurrent':ncl_obs}))
    add('net_worth',None,equity,'Consolidated balance sheet, total stockholders equity; assets minus total liabilities reconciled; no goodwill deduction',json.dumps(obs))
    debt,obs=val('DebtInstrumentCarryingAmount',None,end)
    # The gross note subtotal includes revolver, term loan, notes, receivable
    # financing and other debt, before issuance-cost deductions. 2026's new
    # interest-bearing product financing is separately classified in payables.
    extra=D(0)
    source=json.dumps(obs)
    if end=='2026-06-30':
        loc=text.index('Product Financing',text.index('5. Inventory Financing Agreements'))
        excerpt=text[loc:loc+1500]
        assert '62 million' in excerpt and 'interest expense' in excerpt
        extra=D(62000000);source+='\n'+excerpt
    add('total_debt',None,debt+extra,'Debt note gross debt components before issuance costs; include separately disclosed interest-bearing product financing of USD 62m in June 2026; exclude non-interest supplier financing and operating leases',source)
(p/'supplement.json').write_text(json.dumps(dict(schema_version=1,entity='CDW',cik=req['cik'],scope=req['scope'],purpose='current_borrower_evidence',records=records),indent=2))
print('Prepared',len(records),'source-verified supplement records; no net-interest substitution.')
