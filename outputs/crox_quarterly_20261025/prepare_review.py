import json, pathlib, re, sys
from decimal import Decimal
sys.path.insert(0, 'scripts')
from loan_review_contract import METRICS
from loan_review_pipeline import STANDARD_EBITDA_BASIS

p = pathlib.Path(__file__).parent
raw = json.loads((p/'companyfacts.json').read_text())['facts']['us-gaap']
req = json.loads((p/'request.json').read_text())
sub = json.loads((p/'submissions.json').read_text())['filings']['recent']
records = []
def fact(tag, start, end):
    rows = [x for x in raw[tag]['units']['USD'] if x.get('start') == start and x['end'] == end and x['filed'] <= req['as_of'] and x['form'] in ('10-K','10-Q','10-K/A','10-Q/A')]
    vals = {Decimal(str(x['val'])) for x in rows}
    assert len(vals) == 1, (tag, start, end, vals)
    return vals.pop(), rows

def add(metric, start, end, value, locator, excerpt, basis=''):
    i = next(i for i, d in enumerate(sub['reportDate']) if d == end and sub['form'][i] in ('10-K', '10-Q'))
    acc = sub['accessionNumber'][i]
    uri = 'https://www.sec.gov/Archives/edgar/data/1334036/'+acc.replace('-','')+'/'+sub['primaryDocument'][i]
    records.append(dict(metric=metric, period_kind='instant' if start is None else 'duration', start=start, end=end, unit='text' if METRICS[metric].unit=='text' else 'USD', scale='1', value=str(value), status='sourced', reason='', definition=METRICS[metric].definition, basis=basis, source_id=acc, version=acc, document_date=sub['filingDate'][i], source_uri=uri, locator=locator, excerpt=excerpt, verification=dict(verified_by='Codex', verified_at=req['as_of'], method='checked_against_source')))

for slot in req['periods']:
    end, start = slot['end'], slot['start']
    text = re.sub(r'\s+', ' ', (p/(end+'.txt')).read_text())
    ni, _ = fact('NetIncomeLoss', start, end)
    interest, _ = fact('InterestExpenseNonoperating', start, end)
    m = list(re.finditer(r'Interest expense', text, re.I))
    excerpt = '\n'.join(text[max(0,x.start()-100):x.start()+500] for x in m[:3])
    add('interest_expense', start, end, interest, 'Consolidated statements of operations: separate Interest income and Interest expense lines; gross expense, not net interest', excerpt)
    gp, _ = fact('GrossProfit', start, end)
    oi, _ = fact('OperatingIncomeLoss', start, end)
    # Statement has SG&A plus separately presented impairments; total excludes cost of sales.
    m = list(re.finditer(r'Gross profit', text, re.I))[-1]
    add('operating_expense', start, end, gp-oi, 'Consolidated statements of operations: gross profit less operating income; independently checked SG&A plus goodwill/asset impairment lines', text[m.start():m.start()+650])
    eq, _ = fact('StockholdersEquity', None, end)
    # Consolidated balance sheet presents one total equity, no separate noncontrolling equity.
    m = re.search(r'Total stockholders', text, re.I)
    add('net_worth', None, end, eq, 'Consolidated balance sheet, total stockholders equity; consolidated scope, without goodwill deduction', text[m.start()-200:m.start()+220])
    # Face principal is disclosed separately from issuance-cost net carrying value.
    m = re.search(r'Total face value of long-term borrowings\s+([\d,]+)', text, re.I)
    assert m
    debt = Decimal(m.group(1).replace(',',''))*1000
    assert not re.search(r'finance lease|financing lease', text, re.I)
    add('total_debt', None, end, debt, 'Borrowings note: total face value of long-term borrowings; principal before issuance costs; all listed facilities included once; operating leases excluded. Full-text lease review found no finance lease obligation.', text[m.start()-400:m.start()+500])
    # Deliberately retain quick-assets verification as unresolved: cash restrictions and
    # eligible investment completeness require further review, beyond name matching.
    tags = ['NetIncomeLoss','InterestExpenseNonoperating','IncomeTaxExpenseBenefit','DepreciationDepletionAndAmortization']
    components = []
    for tag in tags:
        if slot['quarter'] is None:
            v, obs = fact(tag,start,end)
            components.append((tag, v, obs))
        else:
            y = slot['fiscal_year']
            a, ar = fact(tag, f'{y-1}-01-01', f'{y-1}-12-31')
            b, br = fact(tag, start, end)
            c, cr = fact(tag, f'{y-1}-01-01', f'{y-1}-06-30')
            components.append((tag, a+b-c, {'formula':'prior FY + current YTD - prior comparable YTD','annual':ar,'current':br,'prior':cr}))
    bridge = {'definition':STANDARD_EBITDA_BASIS, 'components':[{'tag':t,'value':str(v),'source_observations':obs} for t,v,obs in components], 'impairment_treatment':'No impairment addback under approved Standard EBITDA.'}
    add('ltm_ebitda', slot['ltm_start'], end, sum(v for _,v,_ in components), 'SEC companyfacts exact-interval Standard EBITDA bridge, each component FY + current YTD - prior YTD for interim dates; see excerpt for observations', json.dumps(bridge), STANDARD_EBITDA_BASIS)
    add('ebitda_basis', slot['ltm_start'], end, STANDARD_EBITDA_BASIS, 'Approved Standard EBITDA definition applied to SEC component bridge', json.dumps(bridge), STANDARD_EBITDA_BASIS)

supp = dict(schema_version=1,entity='CROX',cik='0001334036',scope='entity-wide',purpose='current_borrower_evidence',records=records)
(p/'supplement.json').write_text(json.dumps(supp,indent=2))
snapshot=json.loads((p/'snapshot.json').read_text())
removed=[]
for statement, rows in snapshot['financial_facts'].items():
    removed.extend(x for x in rows if x['field_name'] in ('interest_expense','interest_expense_alt'))
    snapshot['financial_facts'][statement]=[x for x in rows if x['field_name'] not in ('interest_expense','interest_expense_alt')]
(p/'reviewed_snapshot.json').write_text(json.dumps(snapshot))
(p/'source_mapping_review.json').write_text(json.dumps({'reason':'Raw interest labels require gross-interest verification under DEC-05. Replaced by exact-period reviewed supplements tied to separate gross expense and interest income lines. Original snapshot remains unchanged; no financial amounts changed.', 'excluded_raw_interest_fact_ids':[x['fact_id'] for x in removed]},indent=2))
print('Prepared',len(records),'reviewed supplemental records; original SEC ledger preserved.')
