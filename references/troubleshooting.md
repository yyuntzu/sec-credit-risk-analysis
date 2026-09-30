# Troubleshooting Reference

按需載入 — 只有在 pipeline 報錯或輸出異常時才需要看。

---

## CIK 查詢失敗

**症狀：** `ValueError: Cannot resolve CIK for ticker 'XXX'`

**原因 & 處理：**
1. Ticker 拼錯 → 確認大小寫，試 `GOOGL` vs `GOOG`
2. 非美股 → SEC EDGAR 只收錄在美國上市的公司（ADR 通常有）
3. SEC rate limit → 等 10 秒後重試，確認 `SEC_USER_AGENT` 有設定真實 email
4. 公司改名/被收購 → 用公司全名搜尋 `https://www.sec.gov/cgi-bin/browse-edgar?company={name}&action=getcompany`

---

## Balance Sheet 數據全部是 null

**症狀：** `stg_balance_sheet` 所有欄位為 null，但 income statement 正常

**原因：** 使用了舊版 `sec_client.py`（v1/v2 有 bug：BS entries 因 `start=None` 被 duration filter 過濾掉）

**修復：** 確認使用 `scripts/sec_client.py`（v3），`BALANCE_SHEET_TAGS` 走 point-in-time 邏輯

---

## EBITDA 顯示「(approx)」

**症狀：** Dashboard 顯示 `ebitda_calc_method = 'Operating Income (approx)'`

**原因：** `DepreciationDepletionAndAmortization` tag 在此公司的 XBRL 中缺失（很常見）

**這是預期行為**，不是 bug。報告中已標記，分析師知道這是近似值。

---

## dbt run 失敗

**症狀：** `dbt run` 回傳非 0 exit code

**處理：**
1. 確認 `references/dbt/profiles.yml` 設定正確（見 `references/architecture.md`）
2. 確認 BQ 有 `raw_income_statement` 等原始表（先跑 ingest）
3. `agent_runner.py` 會自動 fallback 到 inline BQ query，不會完全失敗

---

## dbt marts 沒有真的存到 BigQuery（2026-07 修復的歷史 bug，供之後排錯參考）

**症狀：** `dbt` 顯示有跑、`agent_runner.py` 沒有報錯，但 BigQuery `sec_raw`
dataset 裡完全沒有 `fct_credit_kpis` / `dim_company` 等表，或表存在但沒有
資料。credit memo 一直走 inline fallback（PARTIAL），Looker 接不到東西。

**根因（曾經同時存在 3 個問題）：**
1. **Profile 檔名錯誤**：dbt 規定設定檔必須叫 `profiles.yml`（有 s），
   舊版檔案叫 `profile.yml`（無 s），dbt 完全讀不到，等同沒有 profile。
2. **DBT_PROJECT_DIR 指到不存在的路徑**：`agent_runner.py` 預設指向
   `scripts/dbt`，但真正的 dbt project（models/seeds/dbt_project.yml）
   在 `references/dbt/`。`run_dbt()` 抓到 FileNotFoundError 之後被當成
   `{"skipped": true}` 靜默吞掉，看起來像「dbt 沒裝」，其實是路徑錯。
3. **profile 名稱兜不起來**：`dbt_project.yml` 裡的 `profile:` 曾經寫
   `sec_financial`，但 profile 檔案裡的頂層 key 是 `sec_credit`，兩者對
   不上，dbt 會報 `ProfileNotFound`。

**目前狀態（已修復）：**
- 設定檔：`references/dbt/profiles.yml`（正確檔名），頂層 key `sec_credit`
- `references/dbt/dbt_project.yml`：`profile: 'sec_credit'`，與上面一致
- `agent_runner.py` 的 `DBT_PROJECT_DIR` 預設指向 `references/dbt`
- `run_dbt()` 用 `--select +tag:marts`（不是 `fct_credit_kpis+`），確保
  `dim_company` / `dim_filing` / `fct_financial_statement_line_items`
  這些不在 fct_credit_kpis 下游的 mart 也會被建到
- `verify_marts_in_bq()` 在每次 `dbt run` 之後直接查
  `INFORMATION_SCHEMA.TABLES` + row count，把結果放進
  `output["dbt_marts"]` —— 這是唯一能證明「mart 真的存到 BigQuery」的
  依據，不要只看 `output["dbt"]["success"]`

**如果未來又發生類似狀況，檢查順序：**
1. `ls references/dbt/profiles.yml`（檔名有沒有 s）
2. `references/dbt/dbt_project.yml` 的 `profile:` 值，跟
   `references/dbt/profiles.yml` 的頂層 key 是否完全一樣
3. `agent_runner.py` 的 `DBT_PROJECT_DIR` 環境變數（若有設定會覆蓋預設值）
   是否真的指到有 `dbt_project.yml` 的資料夾
4. 手動跑一次確認錯誤訊息：
   ```bash
   cd references/dbt
   dbt run --select +tag:marts --profiles-dir . --project-dir . --target prod
   ```

---

## TTM 計算結果為 null / `is_full_ttm = false`

**症狀：** `fct_credit_kpis.is_full_ttm = false`，TTM 指標為 null

**原因：** 該 ticker 在 BQ 中的季度資料不足 4 期

**處理：**
- 新公司或剛上市的公司正常，等累積 4 季後自動修復
- 確認 `period_days BETWEEN 70 AND 110` 有篩到資料：
  ```sql
  SELECT period_end, period_days, COUNT(*) 
  FROM sec_raw.raw_income_statement
  WHERE ticker = 'TICKER' AND filing_type = '10-Q'
  GROUP BY 1, 2 ORDER BY 1 DESC
  ```

---

## 數值異常大或異常小

**症狀：** Revenue 顯示 `$0.0M` 或 `$999999.9M`

**可能原因：**
1. XBRL 數值單位不是 USD（某些公司用 thousands）→ 看 `raw_*.unit` 欄位
2. 公司重述（restatement）導致舊數值被覆蓋 → 確認 `filed_date` 是最新版
3. YTD 累計值沒被過濾掉 → 確認 `period_days` 在合理範圍

---

## BigQuery 寫入失敗

**症狀：** `BigQuery insert failed: [{'index': 0, 'errors': [...]}]`

**處理：**
1. 檢查 Service Account 是否有 `bigquery.dataEditor` 角色
2. 確認 BQ table schema 有 `period_days` 欄位（v3 新增）
   ```bash
   bq show --schema sec_raw.raw_income_statement
   ```
3. 舊表需要 migrate：
   ```sql
   ALTER TABLE sec_raw.raw_income_statement
   ADD COLUMN IF NOT EXISTS period_days INT64;
   ```
