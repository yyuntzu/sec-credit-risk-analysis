"""
BigQuery Loader — 將結構化財務數據寫入 BigQuery raw tables
Tables:
  - raw_income_statement
  - raw_balance_sheet
  - raw_cash_flow
  - raw_company
"""

import logging
import uuid
from datetime import datetime
from google.cloud import bigquery
from google.api_core.exceptions import NotFound

logger = logging.getLogger(__name__)

# BigQuery Schema 定義
FINANCIAL_STATEMENT_SCHEMA = [
    bigquery.SchemaField("ticker",            "STRING",    mode="REQUIRED"),
    bigquery.SchemaField("field_name",        "STRING",    mode="REQUIRED"),
    bigquery.SchemaField("xbrl_tag",          "STRING"),
    bigquery.SchemaField("value",             "FLOAT64"),
    bigquery.SchemaField("unit",              "STRING"),
    bigquery.SchemaField("period_start",      "DATE"),
    bigquery.SchemaField("period_end",        "DATE"),
    bigquery.SchemaField("period_days",       "INTEGER"),   # ← add this line
    bigquery.SchemaField("filing_type",       "STRING"),
    bigquery.SchemaField("accession_number",  "STRING"),
    bigquery.SchemaField("filed_date",        "DATE"),
    bigquery.SchemaField("ingested_at",       "TIMESTAMP"),
    # Additive audit columns. Existing rows remain NULL; new observations do not backfill them. Do not
    # fabricate provenance for historical raw data.
    *[bigquery.SchemaField(name, "STRING") for name in (
        "fact_id", "cik", "scope", "namespace", "original_value", "period_kind",
        "source_version", "source_url", "document_url", "source_locator", "filing_fiscal_period"
    )],
    bigquery.SchemaField("filing_fiscal_year", "INTEGER"),
]

RAW_COMPANY_SCHEMA = [
    bigquery.SchemaField("ticker",        "STRING",  mode="REQUIRED"),
    bigquery.SchemaField("cik",           "STRING"),
    bigquery.SchemaField("company_name",  "STRING"),
    bigquery.SchemaField("sic",           "STRING"),
    bigquery.SchemaField("sic_desc",      "STRING"),
    bigquery.SchemaField("state_inc",     "STRING"),
    bigquery.SchemaField("fiscal_year_end", "STRING"),
    bigquery.SchemaField("exchanges",     "STRING"),   # JSON array as string
    bigquery.SchemaField("ingested_at",   "TIMESTAMP"),
]

TABLE_SCHEMAS = {
    "raw_income_statement": FINANCIAL_STATEMENT_SCHEMA,
    "raw_balance_sheet":    FINANCIAL_STATEMENT_SCHEMA,
    "raw_cash_flow":        FINANCIAL_STATEMENT_SCHEMA,
    "raw_company":          RAW_COMPANY_SCHEMA,
}


class BigQueryLoader:
    def __init__(self, project_id: str, dataset_id: str):
        self.client = bigquery.Client(project=project_id)
        self.dataset_ref = f"{project_id}.{dataset_id}"

    def ensure_dataset(self):
        """建立 dataset 若不存在"""
        try:
            self.client.get_dataset(self.dataset_ref)
        except NotFound:
            dataset = bigquery.Dataset(self.dataset_ref)
            dataset.location = "US"
            self.client.create_dataset(dataset)
            logger.info(f"Created dataset {self.dataset_ref}")

    def ensure_table(self, table_name: str):
        """建立 table 若不存在（partition by filed_date）"""
        table_ref = f"{self.dataset_ref}.{table_name}"
        try:
            table = self.client.get_table(table_ref)
            expected = TABLE_SCHEMAS.get(table_name, FINANCIAL_STATEMENT_SCHEMA)
            existing = {f.name for f in table.schema}
            additions = [f for f in expected if f.name not in existing]
            if additions:
                table.schema = list(table.schema) + additions
                self.client.update_table(table, ["schema"])
        except NotFound:
            schema = TABLE_SCHEMAS.get(table_name, FINANCIAL_STATEMENT_SCHEMA)
            table = bigquery.Table(table_ref, schema=schema)

            # 按 filed_date 做 time-based partitioning（節省查詢費用）
            if table_name != "raw_company":
                table.time_partitioning = bigquery.TimePartitioning(
                    type_=bigquery.TimePartitioningType.MONTH,
                    field="filed_date",
                )
                table.clustering_fields = ["ticker", "filing_type"]

            self.client.create_table(table)
            logger.info(f"Created table {table_ref}")

    def upsert_rows(self, table_name: str, rows: list[dict]) -> int:
        """
        真正的 MERGE upsert（之前這裡雖然叫 upsert_rows、註解也寫「MERGE」，
        但實作只有 insert_rows_json() —— 純 streaming insert，沒有任何去重。
        後果：同一支股票每被分析一次，raw_income_statement 等表就會把整批
        XBRL 資料再原樣 INSERT 一次；下游 query_annual_financials() /
        query_quarterly_financials() 對這些表做 SUM()，數字就被疊加放大
        （分析過 2 次 revenue 就變 2 倍，以此類推）。

        改法：
          1. 用 load job（非 streaming）把這批 rows 寫進一張隨機命名的
             staging table —— streaming insert 寫入後最多 90 分鐘會卡在
             streaming buffer，無法被同一張表的 MERGE 引用；load job 沒有
             這個限制，寫完馬上可以 MERGE。
          2. 用唯一鍵把 staging table MERGE 進正式 table（有則更新、無則新增），
             從源頭阻止重複列繼續累積。
          3. 刪掉 staging table。
        """
        if not rows:
            return 0

        table_ref = f"{self.dataset_ref}.{table_name}"
        schema = TABLE_SCHEMAS.get(table_name, FINANCIAL_STATEMENT_SCHEMA)
        all_fields = [f.name for f in schema]

        # 唯一鍵：raw_company 每個 ticker 只保留最新一筆 metadata；
        # Financial fact_id covers borrower/CIK, scope, tag, unit, interval,
        # accession, filing date and original value. Versions never overwrite one another.
        merge_keys = (
            ["ticker"] if table_name == "raw_company"
            else ["fact_id"]
        )
        update_fields = ([f for f in all_fields if f not in merge_keys]
                         if table_name == "raw_company" else ["ingested_at"])

        clean_rows = []
        seen = {}
        for row in rows:
            clean = dict(row)
            clean.setdefault("ingested_at", datetime.utcnow().isoformat())
            if table_name != "raw_company":
                if not clean.get("fact_id"):
                    raise ValueError("Financial rows need immutable fact_id; re-extract legacy rows")
                identity = clean["fact_id"]
                comparable = {k: v for k, v in clean.items() if k != "ingested_at"}
                if identity in seen:
                    if seen[identity] != comparable:
                        raise ValueError("Conflicting rows share a fact_id")
                    continue
                seen[identity] = comparable
            clean_rows.append(clean)

        staging_ref = f"{self.dataset_ref}.{table_name}_staging_{uuid.uuid4().hex[:8]}"

        try:
            job_config = bigquery.LoadJobConfig(
                schema=schema,
                write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
                source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
            )
            load_job = self.client.load_table_from_json(
                clean_rows, staging_ref, job_config=job_config
            )
            load_job.result()

            # NULL-safe equality is required for point-in-time balance-sheet
            # facts, whose period_start is normally NULL.
            on_clause = " AND ".join(
                f"T.{k} IS NOT DISTINCT FROM S.{k}" for k in merge_keys
            )
            update_clause = ", ".join(f"{f} = S.{f}" for f in update_fields)
            insert_cols = ", ".join(all_fields)
            insert_vals = ", ".join(f"S.{f}" for f in all_fields)

            merge_sql = f"""
            MERGE `{table_ref}` T
            USING `{staging_ref}` S
            ON {on_clause}
            WHEN MATCHED THEN
              UPDATE SET {update_clause}
            WHEN NOT MATCHED THEN
              INSERT ({insert_cols}) VALUES ({insert_vals})
            """
            merge_job = self.client.query(merge_sql)
            merge_job.result()
            affected = merge_job.num_dml_affected_rows or 0
        finally:
            self.client.delete_table(staging_ref, not_found_ok=True)

        logger.info(f"Upserted {affected} rows into {table_ref} ({len(clean_rows)} source rows)")
        return affected

    def load_financial_data(self, ticker: str, financial_facts: dict) -> dict:
        """
        將 sec_client.extract_financial_facts() 的輸出寫入對應 BQ tables
        
        financial_facts = {
            'income_statement': [...],
            'balance_sheet': [...],
            'cash_flow': [...],
        }
        """
        table_map = {
            "income_statement": "raw_income_statement",
            "balance_sheet":    "raw_balance_sheet",
            "cash_flow":        "raw_cash_flow",
        }

        # Validate the whole batch before the first write.
        for data_type in table_map:
            for row in financial_facts.get(data_type, []):
                if row.get("ticker") != ticker:
                    raise ValueError("Financial batch contains a different borrower")
        stats = {}
        for data_type, table_name in table_map.items():
            rows = financial_facts.get(data_type, [])
            if rows:
                count = self.upsert_rows(table_name, rows)
                stats[table_name] = count

        return stats

    def load_company_metadata(self, ticker: str, submission_data: dict) -> int:
        """寫入 raw_company metadata"""
        row = {
            "ticker":          ticker,
            "cik":             submission_data.get("cik"),
            "company_name":    submission_data.get("name"),
            "sic":             submission_data.get("sic"),
            "sic_desc":        submission_data.get("sicDescription"),
            "state_inc":       submission_data.get("stateOfIncorporation"),
            "fiscal_year_end": submission_data.get("fiscalYearEnd"),
            "exchanges":       str(submission_data.get("exchanges", [])),
            "ingested_at":     datetime.utcnow().isoformat(),
        }
        return self.upsert_rows("raw_company", [row])
