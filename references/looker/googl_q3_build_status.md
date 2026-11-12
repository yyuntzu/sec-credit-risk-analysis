# Alphabet Q3 Looker Studio 草稿建置狀態

## 已確認範圍

- 使用者選擇移除 B6 Debt to Equity 卡，範圍改為23個：11卡、9圖、3表。
- 使用者明確授權：先用既有 BigQuery 資料製作「未驗收草稿」。
- 比較2026Q3 YTD與2025Q3 YTD；BS另含2024及2025年度期末。
- 公司 GOOGL / Alphabet，CIK 0001652044，scope entity-wide，USD millions。
- 固定來源批次：`353f7c1b63c542ef8592be3f27322562`，來源截至2026-10-31。
- 原始批次 draft / blocked_acceptance；本次沒有改動正式結果或驗收狀態。

## 已完成

1. 直接查詢BigQuery來源與執行紀錄，確認公司、期間與未驗收狀態。
2. 建立7個獨立draft views，SQL保留於 `googl_q3_draft.sql`：
   `vw_googl_q3_draft_financials`、`vw_googl_q3_draft_ytd`、
   `vw_googl_q3_draft_income`、`vw_googl_q3_draft_cash_flow`、
   `vw_googl_q3_draft_balance_sheet`、`vw_googl_q3_draft_components_prior`、
   `vw_googl_q3_draft_components_current`。
3. 在使用者Looker Studio帳戶建立
   [Alphabet Q3草稿](https://lookerstudio.google.com/reporting/46ca7044-aa5b-4217-b6f2-ea16411a7cdb)。
4. 使用者手動加入 financials view；之後畫面確認資料面板列出該來源及欄位。
5. 產生 `googl_q3_chart_manifest.json`，列出23個元件的來源、指標、維度與圖形。

## 已執行資料驗證

BigQuery實際查詢結果：4列、4個唯一期間；收入卡只有1列非空；Cash Flow Ratio
只有2個可比YTD值；4個BS時點的 Assets-Liabilities-Equity 差額皆為0。
Income／Cash Flow／Balance Sheet明細各18／16／56資料格。
Debt Ratio未核准Net Worth定義，因此0個非空值；accepted=true的資料列為0。

來源數字與draft推導分開說明：毛利、營業費用、非流動餘額與部分比率是草稿
算術推導，未轉成正式canonical accepted facts。來源多版本數值衝突留NULL。
資料等式成立並不表示整份財務分析已驗收。

## 已知缺漏

- C2 Debt Ratio：Net Worth定義未核准，維持NULL。候選Liabilities/StockholdersEquity
  另存candidate欄位，不供C2代用，也不恢復已移除的B6。
- AP／PPE來源缺漏，其相關明細及差額組成留空。
- CF期初／期末現金、FX及其他橋接未核實，不用BS現金替代、不補0。
- 一個前期來源群組有衝突；每個來源群組只有唯一一致金額才採用。

## 尚未完成與接續位置

**已驗證的畫布資料元件數：0／23。** 不得把已建report或已連接source描述成圖表完成。
目前尚未排三頁或建立23個圖表；其餘6個view也尚未確認加入Looker資料來源。

瀏覽器分頁控制持續發生錯誤；native accessibility可讀取／操作部分選單，
但畫布座標操作回報無可用視窗，無法放置或拖曳元件。重建控制session後仍失敗。
現有report、資料來源和views均保留，待恢復畫布控制後接續，不重建新report。

恢復後依chart manifest逐一放置；每個元件驗證後才更新ui_status及總數。
先完成P1並核對本期收入，再複用樣式；對C2及缺漏明細顯示資料不足原因。
最後核對23個元件、3頁、實際期間、單位、draft標示、來源及分享權限。
