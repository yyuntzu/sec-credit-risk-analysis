# Architecture Reference

按需載入 — 只有在需要了解技術細節、debug、或修改 pipeline 時才看這份文件。

---

## 系統架構

```
User Input (ticker)
     │
     ▼
sec_client.py ──► SEC EDGAR API
  ├── resolve_cik()        ← 動態查詢（company_tickers.json → search API → browse-edgar）
  ├── get_company_facts()  ← XBRL companyfacts
  └── extract_financial_facts()
          │
          ├── income_statement rows
          ├── balance_sheet rows
          └── cash_flow rows
               │
     ┌─────────┼─────────────┐
     ▼         ▼             ▼
bq_loader   gcs_loader   (backup)
 (BQ write)  (GCS JSON)
     │
     ▼
dbt run --select fct_credit_kpis+
  (fallback: inline BQ query in agent_runner.py)
     │
     ▼
dashboard_generator.py → HTML
generate_markdown_report() → .md
```

---

## XBRL Period Validation 邏輯

這是最容易出 bug 的地方，原始版本有已知 bug。

**Income Statement / Cash Flow（duration 型）**
- 10-K：340–380 天（全年）
- 10-Q：70–110 天（單季，排除 YTD 累計值）
- 沒有 `start` 欄位 → 過濾掉

**Balance Sheet（point-in-time 型）**
- 只有 `end` 日期，沒有 `start`
- ❌ 不能做 duration filter（原版 bug：所有 BS 數據會被過濾掉）
- ✅ 直接接受，用 `end` 做 dedup key

```python
BALANCE_SHEET_TAGS = frozenset({
    "Assets", "AssetsCurrent",
    "CashAndCashEquivalentsAtCarryingValue",
    "Liabilities", "LiabilitiesCurrent",
    "LongTermDebt", "StockholdersEquity",
    "RetainedEarningsAccumulatedDeficit",
})
```

---

## BigQuery Schema

**raw_income_statement / raw_balance_sheet / raw_cash_flow**（同一 schema）

| 欄位 | 型別 | 說明 |
|------|------|------|
| ticker | STRING | 大寫股票代號 |
| field_name | STRING | 標準化名稱（e.g. `revenue`, `cash`） |
| xbrl_tag | STRING | 原始 US-GAAP tag |
| value | FLOAT64 | 原始值（非 /1e6） |
| period_start | DATE | IS/CF 有值；BS 為 null |
| period_end | DATE | 所有 statement 皆有 |
| period_days | INTEGER | BS 為 null |
| filing_type | STRING | `10-K` 或 `10-Q` |
| accession_number | STRING | SEC 申報編號 |
| filed_date | DATE | 申報日期 |
| ingested_at | TIMESTAMP | 寫入時間 |

**Partition**: `filed_date` (MONTH) · **Cluster**: `ticker`, `filing_type`

---

## dbt DAG

```
raw_income_statement ─┐
raw_balance_sheet    ─┤─► stg_* ─► int_financials_combined
raw_cash_flow        ─┘              │
raw_company          ─► stg_company ─► dim_company
                                     ▼
                              int_ttm_metrics (TABLE, partitioned)
                                     │
                    ┌────────────────┼────────────────┐
                    ▼                ▼                 ▼
             int_liquidity    int_leverage      int_coverage
             int_cash_flow
                    └────────────────┼─────────────────┘
                                     ▼
                              fct_credit_kpis (TABLE)
                                     │
                    ┌────────────────┘
                    ▼
             fct_covenant_status
             fct_financial_statement_line_items (drill-through, built directly from stg_*)
             dim_filing (built directly from stg_income_statement)
```

`dim_company`、`dim_filing`、`fct_financial_statement_line_items` 不是
`fct_credit_kpis` 的下游節點 —— 用 `--select fct_credit_kpis+` 不會建到它們。

**實際 dbt project 位置**：`references/dbt/`（`dbt_project.yml` +
`profiles.yml` 都在這裡；`agent_runner.py` 的 `DBT_PROJECT_DIR` 預設值就是
指這裡）。

**把所有 marts（含上游依賴）一次落地成 BigQuery 實體表**：
```bash
cd references/dbt
dbt run --select +tag:marts \
  --vars '{"target_ticker": "AMZN"}' \
  --profiles-dir . --project-dir . --target prod
```
`agent_runner.py` 的 `run_dbt()` 就是照這個指令跑的（用絕對路徑取代
`.`），跑完後 `verify_marts_in_bq()` 會查 BigQuery 確認 5 張 mart 表
（dim_company, dim_filing, fct_credit_kpis, fct_covenant_status,
fct_financial_statement_line_items）真的落地、真的有這支 ticker 的資料。

⚠️ `--vars '{"target_ticker": ...}'` 目前**沒有任何 model 真的讀取**它
（`references/dbt/macros/` 是空的，SQL 裡也沒有 `var(...)` 呼叫）——
`dbt_project.yml` 裡宣告了這個 var，但從未被使用。傳這個參數目前只是
佔位，不會縮小任何 model 的掃描範圍；`dbt run` 每次都是全 ticker 重建。
若要做 incremental 優化，需要在 staging models 裡加上讀取
`var('target_ticker')` 的 WHERE 條件（可以做成 `ticker_filter()` macro）。

---

## 已知數據缺失 / XBRL tag 陷阱

| 欄位 | 原因 | 目前處理 |
|------|------|----------|
| gross_profit | 有些 filer（如 AMZN，2009年後）完全沒再標 `GrossProfit` tag | `_enrich_rows()`（agent_runner.py）用恆等式反推：`revenue_m − cost_of_sales_m` |
| operating_expense | 不是任何單一 XBRL tag，各公司內部拆法不同（R&D+S&M+G&A / SG&A+攤銷 / ...） | `_enrich_rows()` 用恆等式反推：`gross_profit_m − operating_income_m`。這個定義**不含 COGS**——跟毛利、營業利益中間那一段費用一致，不管公司內部怎麼拆都成立，不用逐家對應 tag |
| interest_expense | 有些 filer 換過 tag（例如 AMZN：`InterestExpense` 用到 2024-03-31 為止，之後改用 `InterestExpenseNonoperating`） | `sec_client.py` 兩個 tag 都收，分別標成 `interest_expense` / `interest_expense_alt`；`stg_income_statement.sql` 和 agent_runner.py 的 raw fallback 都用 `COALESCE`（優先新資料）。仍有公司完全不單獨報告 interest expense，coverage ratio 這時仍會是 null |
| D&A | 放在附註而非主表 | EBITDA ≈ Operating Income（缺 D&A 時的近似值，`ebitda_calc_method` 會標記） |
| debt_repayment | 分散在多個 tag | DSCR 分母缺失，改用 CFO/Debt |

**⚠️ `CostsAndExpenses` 地雷**：AMZN 等公司會用 `us-gaap:CostsAndExpenses` 標記「Total operating expenses」，但這個 tag 的範圍**包含 COGS**（`Revenue − CostsAndExpenses = Operating Income`）。跟上面 `operating_expense` 欄位的定義（不含 COGS）是兩個不同範圍——千萬不要把 `CostsAndExpenses` 直接接進 `operating_expense_m`，COGS 會被重複扣一次，數字全錯。

---

## GCP 環境變數

| 變數 | 預設值 | 說明 |
|------|--------|------|
| GCP_PROJECT_ID | focus-heuristic-438521-v4 | GCP project |
| BQ_DATASET_ID | sec_raw | BigQuery dataset |
| GCS_BUCKET_NAME | （空，跳過備份）| GCS backup bucket |
| SEC_USER_AGENT | — | SEC 要求真實 email |
| DBT_PROJECT_DIR | references/dbt | dbt project 路徑（含 dbt_project.yml + profiles.yml）|
| OUTPUT_DIR | /tmp/sec_reports | 報告輸出目錄 |
