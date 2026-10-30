import json,pathlib,sys
sys.path.insert(0,'scripts')
import agent_runner as r
from google.cloud import bigquery
p=pathlib.Path(__file__).parent
ingest=json.loads((p/'ingest_result.json').read_text())
ledger=json.loads(pathlib.Path(ingest['source_ledger_path']).read_text())
bq=r.BigQueryLoader(project_id=r.PROJECT_ID,dataset_id=r.BQ_DATASET)
result={}
for statement,source in ledger['financial_facts'].items():
    ids=[x['fact_id'] for x in source]
    config=bigquery.QueryJobConfig(query_parameters=[bigquery.ArrayQueryParameter('ids','STRING',ids)])
    sql=f'SELECT * FROM `{r.PROJECT_ID}.{r.BQ_DATASET}.raw_{statement}` WHERE fact_id IN UNNEST(@ids)'
    rows=[dict(x) for x in bq.client.query(sql,job_config=config).result()]
    r.validate_sec_rows(rows,entity='AMZN',cik='0001018724')
    assert set(x['fact_id'] for x in rows)==set(ids)
    result[statement]=rows
    print(statement,len(rows),'current-ingestion facts verified',flush=True)
(p/'bq_verified_current_ledger.json').write_text(json.dumps(result,indent=2,default=str))
