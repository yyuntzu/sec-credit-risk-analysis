import json, pathlib, sys
sys.path.insert(0, 'scripts')
import agent_runner as r
p=pathlib.Path(__file__).parent
def save(name,value):
    (p/name).write_text(json.dumps(value,indent=2,default=str))
    print(name, 'saved', flush=True)
bq=r.BigQueryLoader(project_id=r.PROJECT_ID,dataset_id=r.BQ_DATASET)
save('dbt_result.json',r.run_dbt('XYZ'))
save('dbt_marts.json',r.verify_marts_in_bq('XYZ',bq))
for name,fn in [
    ('kpis.json',lambda:r.query_kpis_from_bq('XYZ',bq)),
    ('annual.json',lambda:r.query_annual_financials('XYZ',bq,periods=['FY2024','FY2025'])),
    ('interim_candidates.json',lambda:r.query_quarterly_financials('XYZ',bq,quarter_labels=['Q2 2025','Q2 2026']))]:
    try: save(name,fn())
    except Exception as e: save(name+'.error.json',{'error':str(e)})
ingest=json.loads((p/'ingest_result.json').read_text())
gcs=r.GCSLoader(bucket_name=r.GCS_BUCKET)
uri=ingest['html_gcs_uris']['10-Q'][0]['gcs_uri']
text=r.read_filing_html_from_gcs(uri,gcs)
if not text: raise RuntimeError('No filing text loaded from GCS')
(p/'mda_input.txt').write_text(text)
try:
    save('commentary.json',r.generate_commentary(filing_text=text,metrics=r.ALL_METRICS,company_name=ingest['company_name'],period_label='10-Q for six months ended June 30, 2026; filed August 5, 2026'))
except Exception as e:
    save('commentary.error.json',{'type':type(e).__name__,'error':str(e)})
