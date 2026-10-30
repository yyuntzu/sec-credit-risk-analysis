import json,pathlib,re,sys
from decimal import Decimal
sys.path.insert(0,'scripts')
import agent_runner as r
from google.cloud import bigquery
p=pathlib.Path(__file__).parent
facts=json.loads((p/'companyfacts.json').read_text())['facts']['us-gaap']
sub=json.loads((p/'submissions.json').read_text())['filings']['recent']
records=[]
for end in ['2024-12-31','2025-06-30','2025-12-31','2026-06-30']:
    i=next(i for i,x in enumerate(sub['reportDate']) if x==end and sub['form'][i] in ('10-K','10-Q'))
    uri='https://www.sec.gov/Archives/edgar/data/1512673/'+sub['accessionNumber'][i].replace('-','')+'/'+sub['primaryDocument'][i]
    text=re.sub(r'\s+',' ',(p/(end+'.txt')).read_text())
    for metric,tag in [('notes_principal','DebtInstrumentCarryingAmount'),('consolidated_equity','StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest'),('net_interest_signed','InterestIncomeExpenseNonoperatingNet')]:
        start=end[:4]+'-01-01' if metric=='net_interest_signed' else None
        obs=[x for x in facts[tag]['units']['USD'] if x.get('start')==start and x['end']==end and x['form'] in ('10-K','10-Q') and x['filed']<='2026-10-27']
        values={Decimal(str(x['val'])) for x in obs}
        assert len(values)==1,(metric,end,values)
        records.append(dict(entity='XYZ',scope='consolidated',metric=metric,start=start,end=end,value=str(values.pop()),currency='USD',source_scale='1',source_uri=uri,locator='SEC companyfacts us-gaap:'+tag,excerpt=json.dumps(obs),formula='',input_metrics=''))
    # Read the disclosed maturity schedule for the ENTIRE warehouse balance,
    # rather than mistaking the current portion for total warehouse debt.
    matches=list(re.finditer(r'future scheduled principal payments',text,re.I))
    found=[]
    for m in matches:
        snippet=text[max(0,m.start()-180):m.start()+900]
        if 'Warehouse' not in snippet: continue
        total=re.search(r'Total\s+\$\s*([\d,]+)',snippet)
        if total: found.append((Decimal(total.group(1).replace(',',''))*1000,snippet))
    assert found,(end,'warehouse maturity schedule unavailable')
    assert len({x[0] for x in found})==1,(end,found)
    value,excerpt=found[0]
    records.append(dict(entity='XYZ',scope='consolidated',metric='warehouse_principal',start=None,end=end,value=str(value),currency='USD',source_scale='1000',source_uri=uri,locator='Indebtedness note, Warehouse Funding Facilities, complete principal maturity schedule total (in thousands)',excerpt=excerpt,formula='',input_metrics=''))
(p/'reviewed_supplement.json').write_text(json.dumps(records,indent=2))
client=r.BigQueryLoader(project_id=r.PROJECT_ID,dataset_id=r.BQ_DATASET).client
table=f'{r.PROJECT_ID}.{r.BQ_DATASET}.xyz_credit_review_evidence_20261027'
schema=[bigquery.SchemaField(k,'STRING') for k in records[0]]
job=client.load_table_from_json(records,table,job_config=bigquery.LoadJobConfig(schema=schema,write_disposition='WRITE_EMPTY'))
job.result()
read=[dict(x) for x in client.query(f'SELECT * FROM `{table}`').result()]
assert len(read)==len(records)
(p/'bq_verified_supplement.json').write_text(json.dumps(read,indent=2))
(p/'supplement_storage.json').write_text(json.dumps({'bigquery_table':table,'records_verified':len(read)},indent=2))
print('Supplement source records stored and verified:',len(read))
