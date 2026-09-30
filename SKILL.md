---
name: sec-credit-analysis
description: >
  Generate a bank-grade credit memo for any US public company using SEC EDGAR filings.
  Use when user mentions credit analysis, credit memo, financial analysis, SEC data,
  KPI dashboard, leverage ratios, or says things like "分析 AMZN 的信用風險",
  "run credit analysis for [TICKER]", "produce credit memo for [company]",
  "幫我寫 [TICKER] 的信用報告", "give me [COMPANY] credit analysis",
  "walmart credit analysis", "COST credit", "WMT financials".
  DATA SOURCE IS ALWAYS SEC EDGAR via scripts/agent_runner.py — never web search,
  never Moody's, never S&P websites. All financial data must come from
  the local pipeline (XBRL → BigQuery → credit_memo_writer).
---

# SEC Credit Risk Analysis Skill

## Why This Skill Exists

從 SEC EDGAR 到一份可交付主管的 credit memo，需要走兩條平行的數據路徑：
- **路徑 A（XBRL 結構化數據）**：抓 structured financial facts → 精確計算 KPI 和財務比率
- **路徑 B（HTML 原文申報）**：抓 10-K/10-Q 的完整 HTML → 讓 AI 讀取 MD&A、footnotes、管理層 guidance

兩條路徑的數據都存進 GCP，再由 AI 合併生成最終 credit memo。

---

## ❌ 禁止行為（最高優先級）

**以下行為在此 Skill 中絕對禁止，無論使用者怎麼問：**

| 禁止 | 原因 |
|------|------|
| `web_search` / `WebSearch` | 數據來源必須是 SEC EDGAR，不是新聞或評級機構網站 |
| 查詢 Moody's / S&P / Fitch 網站 | 評級意見≠財務數字，不能替代 XBRL 數據 |
| 查詢 Bloomberg / Yahoo Finance | 同上，且數字定義可能與 GAAP 不一致 |
| 直接回答財務問題（不跑 pipeline） | 所有數字必須來自 BQ，不能靠 training data 憑空產生 |
| 跳過 `agent_runner.py` 直接生成報告 | 報告數字必須有 BQ 數據支撐，否則不可交付 |

**正確且唯一的執行路徑：**
```
user input → SKILL.md → scripts/agent_runner.py → BQ/GCS → credit_memo_writer.py → credit memo
```

---

## 觸發條件

使用者提到以下任何一個，就啟動此 Skill：
- 任何股票 ticker + 信用/財務/KPI/分析/credit memo/dashboard
- "分析 [TICKER]"、"[TICKER] credit"、"[TICKER] financials"
- "幫我寫信用報告"、"跑 SEC 數據"、"EDGAR 財務"

### 必要輸入（觸發後必須確認）

| 參數 | 必填 | 格式 | 範例 |
|------|------|------|------|
| TICKER | ✅ | 大寫美股代號 | `WMT` |
| PERIODS | ✅ | 四個會計年度或季度，空格分隔 | `FY2022 FY2023 FY2024 FY2025` 或 `2024Y 2025Q1 2025Y 2026Q1` |

**如果使用者沒有提供四個期間，Agent 必須主動詢問：**

```
I need four fiscal year periods to generate the YOY credit memo.
Please confirm the periods — for example:
  FY2022 FY2023 FY2024 FY2025
Which four periods should I use for {COMPANY}?
```

**不得用猜測的期間直接執行。期間決定了 BQ query 的 date filter 和 credit memo 的欄位標題。**

### 季度 Loan Review 的累計期間規則

季度欄位必須使用年初至報告日的累計數字，不得把 Q2 或 Q3 誤當成單一三個月季度：

| 報告期 | 損益／現金流涵蓋期間 | 比較基準 | 報告必須回答 |
|--------|----------------------|----------|--------------|
| Q1 | 1/1–3/31（3M YTD） | 去年同期 3M YTD | 累計營運、全年目標達成率、同比表現 |
| Q2 | 1/1–6/30（6M YTD） | 去年同期 6M YTD | 累計營運、全年目標達成率、同比表現 |
| Q3 | 1/1–9/30（9M YTD） | 去年同期 9M YTD | 累計營運、全年目標達成率、同比表現 |

- Q2 XBRL duration fact 應約為 160–200 天；Q3 應約為 250–290 天。不得使用約 70–110 天的單季 duration fact。
- Balance Sheet 與 leverage 使用各季末時點；Income Statement 與 Cash Flow 使用上述 YTD 累計期間。
- 全年目標達成率 = 當期 YTD 實績 ÷ 管理層全年 guidance。若 guidance 是區間，至少列示相對於下限、中點與上限的達成率；若 filing 未提供 guidance，明確標示 `Not disclosed`，不得自行假設。
- Q2／Q3 commentary 必須明確寫出：YTD 營運方向、相較去年同期的變化，以及全年 revenue／EBITDA guidance 的達成進度。

### Total Debt 定義

所有報告及 leverage ratio 統一使用財報債務科目計算：

`Total Debt = Short-Term Loans（含 Short-Term Notes Payable）+ Long-Term Liabilities Maturing Within One Year + Long-Term Liabilities`

- 優先使用三個組成項目的 XBRL facts，不得以 Total Liabilities 代替 Total Debt。
- `DebtCurrent` 僅在短期借款與一年內到期長期負債未分列時作為 current-debt fallback。
- 若 filing 只提供包含流動與非流動部分的 aggregate long-term debt tag，使用該 aggregate 作 fallback，且不得再加 current maturities 造成重複計算。
- 缺少任何必要組成項目時，於 Data Quality Notes 揭露採用的 fallback 或 `NO_DATA`。

---

## Agent 心態

> 這份報告最終給主管審閱的 credit memo，語言需要 bank-appropriate：factual、no editorializing。
> 核心問題只有一個：「這公司能不能還債？」所有 section 都在回答這個問題。
> 數字來自 XBRL（路徑 A）；narrative、forward guidance、non-recurring items 來自原文 HTML（路徑 B）。
> 數據缺失不是失敗，要明確標記 NO_DATA 並給替代指標，在 Appendix 列影響。
> 非經常性項目（商譽減損等）必須在 commentary 中單獨說明，不能讓它靜默扭曲 GAAP 比率。

## ✅ 強制執行路徑（每次觸發都必須走這條路）

```
Step 0: source scripts/setup.sh          ← 確認環境變數
Step 1: python scripts/agent_runner.py {TICKER} --periods FY2022 FY2023 FY2024 FY2025
        └─ 內部自動走：SEC API → BQ → dbt（或 fallback） → credit_memo_writer
Step 2: 輸出 /tmp/sec_reports/{TICKER}_credit_memo.md
Step 3: 輸出 /tmp/sec_reports/{TICKER}_dashboard.html
```

**如果 `agent_runner.py` 執行失敗：**
1. 看錯誤訊息 → 查 references/troubleshooting.md
2. 只有在 pipeline 完全無法執行時，才可以用 XBRL 數字做 partial report
3. 任何情況下都不能用 web search 補充財務數字

---

## 完整 Workflow

```
PHASE 1 — 數據抓取與儲存
══════════════════════════════════════════════════════

  [SEC EDGAR API]
       │
       ├─ 路徑 A：XBRL structured facts
       │   sec_client.extract_financial_facts(ticker)
       │        │
       │        ├─ GCS: gs://bucket/sec/{ticker}/facts/{date}/facts.json
       │        └─ BigQuery:
       │             sec_raw.raw_income_statement
       │             sec_raw.raw_balance_sheet
       │             sec_raw.raw_cash_flow
       │             sec_raw.raw_company
       │
       └─ 路徑 B：HTML 原文申報
           sec_client.get_latest_filings(ticker, "10-K", count=4)
           sec_client.get_latest_filings(ticker, "10-Q", count=4)
                │
                ├─ GCS（主要存放）:
                │   gs://bucket/sec/{ticker}/raw_filings/{date}/{accession}/{filename}.htm
                │
                └─ BigQuery（索引 + 摘要）:
                     sec_raw.raw_filing_index
                     欄位: ticker, filing_type, period_end, filed_date,
                           accession_number, gcs_uri, ingested_at


PHASE 2 — 計算 KPI ＋ 落地 dbt marts（dbt pipeline）
══════════════════════════════════════════════════════

  BigQuery raw tables
       │
       └─ dbt run --select +tag:marts \
              --vars '{"target_ticker": "AMZN"}' \
              --profiles-dir references/dbt --project-dir references/dbt
              │
              └─ 輸出（全部是 BigQuery 實體表，materialized='table'）：
                       sec_raw.dim_company
                       sec_raw.dim_filing
                       sec_raw.fct_credit_kpis
                       sec_raw.fct_covenant_status
                       sec_raw.fct_financial_statement_line_items
                       （見 references/architecture.md for full DAG）

  ⚠️ 注意：`--select fct_credit_kpis+` 只會建 fct_credit_kpis 的下游，
     dim_company / dim_filing / fct_financial_statement_line_items 不在它
     的下游，永遠不會被建到。一定要用 `+tag:marts`（見 agent_runner.py
     的 run_dbt()），才能把「所有」marts 落地成實體表，Looker 才有完整資料可接。

  ✅ dbt run 之後，agent_runner.py 會自動呼叫 verify_marts_in_bq()：
     直接查 BigQuery INFORMATION_SCHEMA.TABLES + 每張表的 row count，
     確認 5 張 mart 表真的存在、真的有這支 ticker 的資料。
     結果存在 output["dbt_marts"]，CLI 執行完會印出
     「dbt marts → 5/5 landed in BigQuery」這行 —— 這是判斷「dbt marts
     是否真的存到 BigQuery」的唯一依據，不要只看 dbt exit code。

  ⚠️ 若 dbt 不可用（未安裝 / profiles.yml 設定錯誤 / project dir 找不到）：
     → 先嘗試查已有的 fct_credit_kpis 表
     → 表不存在則 fallback inline query（TTM/YoY/Covenant 欄位缺失，報告標記 PARTIAL）
     見 references/troubleshooting.md


PHASE 3 — 生成 Credit Memo
══════════════════════════════════════════════════════

  數字來源（路徑 A）            原文來源（路徑 B）
  ─────────────────             ──────────────────
  fct_credit_kpis               GCS HTML → AI 閱讀
  fct_covenant_status           提取：
  int_ttm_metrics               - MD&A 段落
        │                       - Interest expense footnote
        │                       - Management guidance (FY+1)
        │                       - Non-recurring items 說明
        │                       - Covenant definitions
        └──────────┬────────────┘
                   │
                   ▼
         generate_credit_memo()
                   │
                   ├─ Credit Memo（Markdown）← 主要交付物，可交主管
                   │   按 references/output-format.md 格式：
                   │   S1 Cover → S2 IS + Commentary → S3 Cash Flows
                   │   S4 Ratios + Commentary → S5 Leverage + Commentary
                   │   S6 EV Analysis → S7 Covenants → S8 Summary
                   │   Appendix: Data Quality Notes
                   │
                   └─ HTML Dashboard（輔助視圖）
                       KPI Cards + Liquidity Chart + Cash Flow
                       Revenue/EBITDA Trend + Covenant Table
```

---

## GCP 儲存位置一覽

| 數據類型 | 儲存位置 | 用途 |
|----------|----------|------|
| XBRL facts（JSON） | `GCS: sec/{ticker}/facts/{date}/` | 原始備份 / audit trail |
| 10-K/10-Q HTML 原文 | `GCS: sec/{ticker}/raw_filings/{date}/{accession}/` | AI 閱讀原文、長期存檔 |
| Filing 索引 | `BQ: sec_raw.raw_filing_index` | 快速查詢 GCS URI，不用掃 GCS |
| 結構化財務數據 | `BQ: sec_raw.raw_income_statement` 等 4 張表 | dbt 計算來源 |
| 計算後 KPI | `BQ: sec_raw.fct_credit_kpis` | 報告數字直接取用；Looker 主要 fact table |
| Covenant 狀態 | `BQ: sec_raw.fct_covenant_status` | Section 7 數據來源；Looker covenant 表 |
| 公司維度 | `BQ: sec_raw.dim_company` | Looker filter / join key（ticker → 公司名稱、產業）|
| 申報期間維度 | `BQ: sec_raw.dim_filing` | Looker filter（fiscal_year、fiscal_quarter、10-K/10-Q）|
| 財務科目明細 | `BQ: sec_raw.fct_financial_statement_line_items` | Looker drill-through（單一科目逐期趨勢）|

以上 5 張表都是 `dbt run --select +tag:marts` 的輸出，materialized='table'，
是 BigQuery 裡「真正的表」（不是 view），可以直接當 Looker / Looker Studio
的 data source。詳見下方「Looker / Looker Studio 串接」。

---

## Looker / Looker Studio 串接（管理層財務 Dashboard）

**目的**：讓 manager 一眼看出公司財務狀況的 dashboard，資料來源就是上面 5 張
BigQuery mart 表 —— 不需要另外寫 ETL，dbt 已經把資料整理成可以直接拖拉的維度表
（dim_company / dim_filing）和事實表（fct_credit_kpis / fct_covenant_status /
fct_financial_statement_line_items）。

**前提**：先確認 `output["dbt_marts"]` 顯示 5/5 都 landed（見上方 PHASE 2），
表示這些表在 BigQuery 裡已經有實際資料，Looker 才連得到東西。

**串接步驟（Looker Studio，最快）**：
1. 前往 https://lookerstudio.google.com → 建立 → 資料來源
2. 選擇連接器 **BigQuery**
3. 選 Project：`focus-heuristic-438521-v4` → Dataset：`sec_raw`
4. 逐一加入這 5 張表當資料來源（或用「自訂查詢」寫 JOIN，把 dim_company /
   dim_filing 跟 fct_credit_kpis 連起來，一次拉全部欄位）
5. 建議的管理層 dashboard 版面：
   - 頂部：KPI 卡片（Revenue、EBITDA、Net Income、Leverage、Current Ratio）
     ← 來自 `fct_credit_kpis`，用 `dim_company.company_name` 當標題
   - 趨勢圖：Revenue / EBITDA / Net Income 逐季／逐年折線圖
     ← `fct_financial_statement_line_items`，用 `dim_filing.period_label` 當 X 軸
   - Covenant 燈號表：綠/黃/紅 ← `fct_covenant_status`
   - 篩選器：ticker（`dim_company`）、fiscal_year / filing_type（`dim_filing`）

**若是企業版 Looker（非 Looker Studio）**：資料來源設定方式相同（Connect →
BigQuery → `sec_raw` dataset），差別在需要先建 LookML view 對應這 5 張表；
若之後要做，回來這裡新增 `references/dbt/` 對應的 LookML explore 定義。

---

## 核心判斷原則

| 情況 | 處理方式 |
|------|----------|
| interest_expense = null in XBRL | 查 HTML footnote；若仍缺，標記 NO_DATA，用 cfo_to_debt 替代 |
| D&A = null in XBRL | 查 HTML footnote；若仍缺，EBITDA ≈ Operating Income，標記 (approx) |
| Management guidance 缺失 | Section 8 Point 3 標記「Not disclosed in filing period」|
| dbt 不可用，fct_credit_kpis 表存在 | 直接查表，跳過 dbt，報告正常生成 |
| dbt 不可用，表也不存在 | Inline fallback query，報告標記 ⚠️ PARTIAL DATA |
| ticker 查不到 CIK | 提示使用者確認 ticker，嘗試公司全名搜尋 |
| HTML 原文超過 context window | 只讀取 MD&A section + Financial Statements section，跳過 boilerplate |

---

## 輸出格式

見 `references/output-format.md`（8-section credit memo 完整規格）。

## 技術細節

見 `references/architecture.md`（XBRL period logic、BQ schema、dbt DAG、GCS 路徑規範）。

---

## Claude Code 執行前置步驟

**第一次執行時必做（環境沒設定會直接報錯）：**

```bash
# Step 1: source 環境設定
source scripts/setup.sh

# Step 2: 確認 GCP 登入（若顯示 ⚠️ Not logged in）
gcloud auth application-default login

# Step 3: 執行分析
python scripts/agent_runner.py COST
```

**常見錯誤對照：**

| 錯誤訊息 | 原因 | 解法 |
|----------|------|------|
| `Unknown skill: sec-credit-analysis` | Claude Code 嘗試呼叫不存在的內建指令 | 忽略，直接讀 SKILL.md 執行 scripts/ |
| `GCP_PROJECT_ID not set` | 環境變數未設定 | `source scripts/setup.sh` |
| `google.auth.exceptions.DefaultCredentialsError` | 未登入 GCP | `gcloud auth application-default login` |
| `Table not found: sec_raw.fct_credit_kpis` | dbt 未跑過 | 正常，會自動 fallback 到 inline query |
| `output["dbt_marts"]` 顯示表 missing/empty | dbt run 失敗或未涵蓋該 model（見 references/troubleshooting.md「dbt marts 沒有真的存到 BigQuery」） | 檢查 `output["dbt"]` 的 error 訊息；確認 `references/dbt/profiles.yml` 存在且 profile 名稱與 dbt_project.yml 一致 |
| `Cannot resolve CIK for ticker 'XXX'` | ticker 錯誤或非美股 | 確認 ticker 拼法，見 references/troubleshooting.md |
