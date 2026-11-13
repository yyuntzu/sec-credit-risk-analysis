# Review + Looker Studio delivery plan

最新設計以 [23元件設計驗證稿](looker-studio-design-spec.md) 為準；ROA/ROE 已依使用者要求移除。

目標：使用者指定公司及財報期間後，同一次工作交付正式 Review、既有本地
Dashboard，以及連到同公司、同批次內容的 Looker Studio 報表。

## 目前進度

| 階段 | 狀態 | 完成條件 |
| --- | --- | --- |
| 工程設定 | 已存在；GitHub repository 已確認可連線 | 沿用 docs/agents 的 tracker、labels、single-context 設定。 |
| 正式 Review / 本地 HTML / Excel | 已有實作 | 每次以 manifest 確認實際輸出結果。 |
| BigQuery 正式發布 | 已有實作，這次未執行雲端驗證 | 財務驗收及交付成功後，cloud_status=published。 |
| Looker 基礎展示 views | 本次新增，待雲端驗證 | vw_looker_review_runs / vw_looker_review_facts。 |
| 三頁、23 元件範本 | 已移除B6；Alphabet草稿已建report及source，尚未放置元件 | 公司、批次及模式切換時所有元件一致。 |
| 自動回傳對應 dashboard URL | 已實作配置式連結與 delivery.json；待真實範本驗證 | accepted/published 後產生 link_ready；不等於遠端已驗證。 |
| 任選多季趨勢 | 待設計 | 與正式 quarterly YTD 比較區分，補來源與期間轉換。 |

## 依序執行

1. 先固定最小交付：一家公司、一組符合正式 Quarterly contract 的比較期間。
   使用者可以用自然語言指定期間；agent 必須確認公司身分、實際 fiscal 日期及
   as-of，建立既有 request schema，再呼叫 agent_runner.py。這不是 CLI 已有的
   任意季度清單解析功能。指定數個獨立季度的趨勢，須另行取得足夠歷史資料。
2. 完成指標對照表：23 元件逐一對應 canonical metric、期間種類、單位、來源與
   缺值呈現。使用者最新更正為 Cash Flow Ratio=CFO/該期間期末流動負債，dashboard
   移除 Cash Ratio；沿用既有 cash_flow_ratio 公式。新增定義需先確認及實作，不能在 Looker 另算
   出與 Review 不同的正式數字。Balance Sheet 明細仍需盤點來源映射。
3. 使用正式 cloud workflow 發布。新增的兩個 views 帶 formal_review_marts tag，
   現有 review_cloud.py 的 publish selection 會納入，無須改 legacy marts。
   views 在 run manifest 記錄 accepted/published 之後才會顯示該批資料。
4. 提供或建立 Looker Studio 範本，連接 vw_looker_review_facts。第一版盡量共用
   此資料來源，避免跨來源 controls 無法一起切換。數值用 numeric_value，保留
   value_exact；依 metric、period_role、實際日期及 unit 設定表格與圖表。
   比率及餘額選定單一 fact；只有確認唯一資料格時才可用聚合呈現。
5. 設定公司、模式及批次控制。明確選 run_id 時，允許歷史批次；「最新」模式才
   使用 is_latest_accepted_run=true。最新按公司、模式、scope、幣別與 scale 分組，
   不代表最新財報期間，也不表示最近一次嘗試成功；畫面應顯示完成時間與實際期間。
6. Python delivery adapter 已加入正式 CLI／Shell／HTTP。下一步在實際範本設定並
   測試 URL parameters，提供 looker_config 讓 dashboard URL、entity、run_id 與
   publication 狀態一起交付；實際期間由同run正式報告提供。
   固定範本 URL 只能代表入口，不能宣稱已自動選中本次公司及批次。
7. 端到端驗收：兩家公司、同公司兩次執行、歷史批次、缺值及發布失敗。對照
   report.json 檢查圖表數值；確認 refresh 後所有元件同步，並測試真實分享權限。

## 第一版使用者交付

```text
Review：本次 Markdown / Excel
本地 Dashboard：本次 HTML
Looker Studio：已驗證的公司與批次連結（串接完成後）
公司、實際期間、模式、run_id、財務驗收與發布狀態
```

若報告為 draft，交付本地稿件及阻擋原因；目前政策不將 draft 發布到正式 Looker
資料來源。若使用者也要草稿 dashboard 上雲，需另訂 draft 資料通道及可見標示，
不能把舊批次當成本次結果。

## 23 元件來源盤點

「既有」表示 contract 已有欄位，不保證每個公司／期間都有可用值。
「待補」表示尚不能僅靠這次新增的 Looker views 完成。

| ID | 元件 | canonical 對應或待辦 |
| --- | --- | --- |
| P1 | 收入 | revenue，既有。 |
| P2 | 毛利 | gross_profit，既有。 |
| P3 | 營業利益 | operating_income，既有。 |
| P4 | 淨利 | net_income，既有。 |
| P7 | 收入／費用／營益率趨勢 | revenue / operating_margin 既有；總費用需驗證 cost_of_revenue + operating_expense 的完整性。 |
| P8 | 毛利／毛利率 | gross_profit / gross_margin，既有。 |
| P9 | 營業利益／營益率 | operating_income / operating_margin，既有。 |
| P10 | 淨利／淨利率 | net_income 既有；net_margin 公式待補。 |
| P11 | 損益比較表 | 先採既有 INCOME_ROWS；Other Income/Expense 展示映射待補，保留稅前及稅額以核對。 |
| C1 | Cash Flow Ratio | 已確認 CFO/該期間期末流動負債；沿用 cash_flow_ratio，季度來源與輸出仍待補。 |
| C2 | Debt Ratio | debt_ratio，既有；遵守 total_liabilities/net_worth。 |
| C3 | 現金／Cash Flow Ratio趨勢 | 柱圖用 BS cash and cash equivalents；折線用對應期間 cash_flow_ratio，Quarterly只比較可比YTD。 |
| C4 | 現金流比較表 | beginning_cash / cfo / cfi / cff / cash_change / ending_cash；cash_fx / cash_other 保留勾稽。 |
| B1 | 總資產 | total_assets，既有 supporting fact。 |
| B2 | 總負債 | total_liabilities，既有。 |
| B3 | 權益 | net_worth，與草案 total_equity 的定義對應待確認。 |
| B4 | 資產／權益 | 待補公式；權益口徑同 B3。 |
| B5 | 負債／資產 | 待補公式，標明分子為總負債。 |
| B7 | 資產組成趨勢 | current_assets / total_assets 已有；非流動資產需驗證來源或核准差額推導。 |
| B8 | 負債／權益組成趨勢 | current_liabilities / total_liabilities / net_worth 已有；非流動負債同上。 |
| B9 | 前期資產負債比較 | 待補互斥完整的 component 映射；使用實際前期截止日。 |
| B10 | 本期資產負債比較 | 同 B9；標題使用最新選定申報期末，不用 Today。 |
| B11 | 資產負債明細表 | 待補 AR、AP、PPE、其他資產／負債的正式明細映射與去重。 |

現有 supporting fact／observations 不代表每個明細都已進正式發布的 facts。
新增指標需連接來源、公式版本、input_ids、測試及雲端輸出，再納入圖表。

## 驗證邊界

dbt parse 僅確認專案解析與依賴，不能證明 BigQuery SQL 執行或 Looker 顯示成功。
部署後執行資料唯一性、latest selector 與數值核對。現有 publisher 在最終 manifest
寫入前執行 dbt tests，因此新 run 的可見性仍需發布後查詢驗收。

展示層首次驗證：dbt parse 通過。自動交付整合後：完整 unittest suite 共272個，
268通過、4略過；新增10個交付測試涵蓋URL編碼、批次分離、draft/local/發布失敗
阻擋、設定驗證、HTTP、環境設定與最終manifest失敗撤回連結。主skill格式驗證
及git diff --check通過。真實CLI以synthetic snapshot產生Review、HTML及delivery.json，
預期為draft且不提供Looker URL；該次示範停用Excel。未呼叫SEC／模型或發布雲端，
新增SQL資料測試與23元件遠端顯示仍待實際驗收。

Looker URL 參數須在實際報表配置後驗證，參見
[Google parameters 文件](https://docs.cloud.google.com/data-studio/parameters)。
