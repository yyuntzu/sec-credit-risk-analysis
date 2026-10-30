import json, pathlib, sys
sys.path.insert(0, 'scripts')
import sec_client
import agent_runner as runner

sec_client._CIK_CACHE['XYZ'] = '0001512673'
p = pathlib.Path(__file__).parent
client = sec_client.SECEdgarClient()
bq = runner.BigQueryLoader(project_id=runner.PROJECT_ID, dataset_id=runner.BQ_DATASET)
gcs = runner.GCSLoader(bucket_name=runner.GCS_BUCKET) if runner.GCS_BUCKET else None
bq.ensure_dataset()
for table in ['raw_income_statement','raw_balance_sheet','raw_cash_flow','raw_company']:
    bq.ensure_table(table)
result = runner.ingest_ticker('XYZ', client, bq, gcs)
(p/'ingest_result.json').write_text(json.dumps(result, indent=2, default=str))
print(json.dumps(result, indent=2, default=str))
