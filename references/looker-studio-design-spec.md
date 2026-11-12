# Looker Studio 財務儀表板設計規格 v0.1

狀態：設計驗證稿，尚未定版／部署。以使用者最新草案為基礎。
已確認：移除 ROA／ROE 與 B6 Debt to Equity 卡；保留三頁，共 23 個資料元件。
已確認（依使用者最新更正）：C1／C3 使用 Cash Flow Ratio＝營業活動淨現金流／
該期間期末流動負債；本 dashboard 移除 Cash Ratio。沿用既有 cash_flow_ratio 定義。
驗證範圍：規格一致性與目前程式支援；尚未驗證真實公司數據或 Looker 畫面。

## 1. 共同操作與版型

三頁共用公司、Annual/Quarterly 模式、單一 run_id、scope、幣別及金額單位。
上方顯示公司名稱、實際財報期間、完成時間與驗收／發布狀態；其下為控制列。
控制列不計入 23 個資料元件。資料來源連線固定，公司透過選擇條件切換。

| 頁面 | 第一列 | 中段 | 下段 | 元件數 |
| --- | --- | --- | --- | --- |
| Profit and Loss | P1–P4 四卡 | P7–P10，兩欄兩列 | P11 損益比較表 | 9 |
| Cash Flow | C1–C2 兩卡 | C3 全寬組合圖 | C4 現金流比較表 | 4 |
| Balance Sheet | B1–B5 五卡，分兩列 | B7–B10，兩欄兩列 | B11 資產負債比較表 | 10 |

合計 11 張卡、9 張圖、3 張表。移除 P5/P6/B6，其他 ID 保留，避免引用錯位。
背景、字型、留白採同一範本；金額與百分比以軸標題／圖例分辨。
負數保留符號，零值與資料不足分開；不以紅綠自動判斷財務好壞。

## 2. 期間與選取規則

| 模式 | 損益／現金流圖與表 | 資產負債圖與表 | 卡片預設 |
| --- | --- | --- | --- |
| Annual | request 的四個完整年度，按實際期末排序 | 相同四個年度期末 | 最後一個 request 年度／期末 |
| Quarterly | prior_interim 與 current_interim 兩個可比 YTD；按實際日期標示 | earlier_fy_end、prior_interim、latest_fy_end、current_interim 四時點 | current_interim YTD／期末 |

使用者可以在該 run 的可用期間內選卡片期間，跨頁保持一致；duration 卡選期間、
instant 卡取該期間期末。Quarterly 的 BS 比較可獨立選 request 中的兩個時點。
第一版不提供任意日曆日期加總，也不讓單一日期控制誤刪期初餘額或前期比較。
P1–P4 是「選定單一期間」的值，不加總四年或兩個 YTD。

所有「近12個月」「月度欄位」「Today」「Accumulate」改成明確 request 期間。
Quarterly P7–P10 第一版只有兩個 YTD 比較點，圖形風格保留，標題寫「YTD 比較」。
C3 柱圖使用可驗證 BS 現金的四個時點；Cash Flow Ratio 折線每點使用同公司、
同 scope 與幣別的指定期間 CFO／該期末流動負債。Annual 比較四個全年；Quarterly
只顯示兩個可比 YTD 的比率點，年度期末位置不混入全年 CFO 比率，並保留缺值斷點。
缺任一輸入保留缺值，不把 CFO 年化，也不將 FY 與 YTD 比率視為同口徑趨勢。
8／12季、月度及 TTM 擴充另行設計，未列入第一版。

## 3. 指標與圖表規格

所有正式值由共用 calculation/source contract 產生，再供 Review 與 BI 使用。
下列新增公式是設計提案；定版前不改動正式財務計算。

| ID | 元件 | 資料／口徑 | 呈現 |
| --- | --- | --- | --- |
| P1 | Total Revenue | revenue，選定年度或 YTD | 金額卡 |
| P2 | Gross Profit | gross_profit，同 P1 期間 | 金額卡 |
| P3 | Operating Profit (Loss) | operating_income，同 P1 期間 | 金額卡 |
| P4 | Net Profit (Loss) | net_income，同 P1 期間 | 金額卡 |
| P7 | Revenue, Operating Costs and Margin | revenue；total_expenses=cost_of_revenue+operating_expense（需驗證互斥完整）；operating_margin | 收入／費用分組柱，營益率右軸折線 |
| P8 | Gross Profit and Margin | gross_profit / gross_margin | 金額左軸、百分比右軸，雙折線 |
| P9 | Operating Profit and Margin | operating_income / operating_margin | 同 P8 |
| P10 | Net Profit and Margin | net_income；新增 net_margin=net_income/revenue | 同 P8 |
| P11 | Income Statement | 見第4節固定行序 | Pivot table，科目列、期間欄 |
| C1 | Cash Flow Ratio | cash_flow_ratio=cfo/current_liabilities；分母為該 CFO 期間期末餘額 | 倍數卡，2位小數 |
| C2 | Debt Ratio | 現行 debt_ratio=total_liabilities/net_worth；Net Worth 定義須核對 | 百分比卡，2位小數 |
| C3 | Cash and Cash Equivalents | BS 現金及約當現金；折線用對應期間 cash_flow_ratio | 現金左軸柱、Cash Flow Ratio右軸線（倍數） |
| C4 | Cash Flow Overview | 見第4節固定行序 | Pivot table，科目列、期間欄 |
| B1 | Total Assets | total_assets，選定期末 | 金額卡 |
| B2 | Total Liabilities | total_liabilities，同 B1 截止日 | 金額卡 |
| B3 | Total Equity | total_equity；只有定義一致時映射 net_worth | 金額卡 |
| B4 | Assets / Equity | total_assets/total_equity，新增公式 | 倍數卡，2位小數 |
| B5 | Liabilities / Assets | total_liabilities/total_assets，新增公式 | 百分比卡，2位小數 |
| B7 | Asset Composition | current_assets、noncurrent_assets | 普通堆疊柱，金額軸 |
| B8 | Liabilities and Equity | current_liabilities、noncurrent_liabilities、total_equity | 普通堆疊柱，金額軸 |
| B9 | Prior Selected Balance Sheet | request 的前期比較時點；見第4節 component | Assets / Liabilities and Equity 兩柱 |
| B10 | Current Selected Balance Sheet | request 的當期比較時點；同 B9 component | 同 B9，標題含實際日期 |
| B11 | Balance Sheet | 見第4節固定行序 | Pivot table，科目列、截止日欄 |

百分比底層保存比值：0.86 顯示 86.00%；倍數 0.86 顯示 0.86x。
C2 使用總負債／Net Worth；B6 已依使用者要求移除。分母零或缺資料留空並顯示原因；
負權益保留符號與提示，不把負比率解釋成改善。權益為負時堆疊需保留正負方向，
顯示淨合計，不把正向柱高當成資產負債等式成立的證據。

## 4. 明細完整性與勾稽

P11 建議採現有正式順序：Revenue、Cost of Revenue、Gross Profit、Operating
Expense、Operating Income、Interest Expense、Pre-tax Profit、Income Tax、Net
Income。若保留 Other Income／Expense，須依來源分類增加，不以單一 Other
Expense 列代替未解釋的全部差額；收入、利息、稅額與一次性項目避免重複。
變更草案七列為此行序是設計建議，待定版；不改變資料元件數。

C4：Beginning Cash、CFO、CFI、CFF、FX Effect、Other Adjustments、Cash Change、
Ending Cash。FX 與 Other 若合併，需標示包含範圍，不能再分別加入。

```text
Ending Cash = Beginning Cash + CFO + CFI + CFF + FX Effect + Other Adjustments
Cash Change = Ending Cash - Beginning Cash
```

CF 現金可能含 restricted cash；C3 使用 BS cash and cash equivalents。
兩者未確認同定義前不互相代用；來源有差額時保留來源調節與說明。

B11 建議行序（小計另標示，不能再與組成明細加總）：

1. Cash and Cash Equivalents
2. Accounts Receivable, Net
3. Other Current Assets, excluding Cash and AR（含存貨等其餘流動資產）
4. Total Current Assets（小計）
5. Property, Plant and Equipment, Net
6. Other Non-current Assets, excluding PPE
7. Total Assets（總計）
8. Accounts Payable
9. Other Current Liabilities, excluding AP
10. Total Current Liabilities（小計）
11. Non-current Liabilities
12. Total Liabilities（小計）
13. Total Equity
14. Total Liabilities and Equity（總計）

新增其他流動資產行以補齊原草案遺漏的存貨／預付款等；other noncurrent assets
明確排除 PPE。AR/AP/PPE 缺失時保留空值，不以總額推定個別科目。

B9/B10 component：Assets 端為 Cash、Other Current Assets excluding Cash、
Non-current Assets；另一端為 Current Liabilities、Non-current Liabilities、Equity。
B11 的 Other Current Assets 排除 Cash+AR，B9/B10 只排除 Cash，兩者分開命名。
差額推導只在來源範圍、日期、版本、單位一致且已核准 identity 時採用。

## 5. 欄位與展示層

沿用正式 facts/evidence/runs 作權威來源，無需再建立另一套 raw 財報計算。
草案三張 fct_* 是邏輯資料集合；六張 vw_* 是待設計展示介面，不是已存在資料表。
目前新增的 vw_looker_review_facts / vw_looker_review_runs 只提供基礎，不足以
單獨完成23元件。其長表仍含 common-size 與 supporting facts，不能按 metric
名稱直接 SUM 全部資料。

必備鍵與上下文：entity、run_id、review_mode、scope、currency、report_scale、
fact_id、metric、period_role、period_start/end、period_kind、unit、status、reason、
value_exact/numeric_value、formula_id/version、input_ids、evidence_ids。
部分欄位現存於 fact_payload，尚需展示 view 提取；period label／fiscal_year／quarter
須從正式 Report periods 取得。source_document_id／filed_date 須經 evidence 映射，
不能把 run created_at 或 metric 當作來源申報日／原始 XBRL tag。

| 草案欄位 | canonical 對應 |
| --- | --- |
| operating_expenses | operating_expense（排除 cost_of_revenue） |
| income_tax_expense | income_tax |
| opening_cash / closing_cash | beginning_cash / ending_cash，保留 CF 現金定義 |
| operating/investing/financing_cash_flow | cfo / cfi / cff |
| net_change_in_cash | cash_change |
| cash_and_cash_equivalents | BS source metric，不能自動以 ending_cash 替代 |
| total_equity | 與 net_worth 做 scope、非控制權益及定義對應後採用 |

每個展示資料格固定一個 canonical fact；排除 :pct: common-size facts，依 unit
及 fact_id 區分金額、比率與輸入，防止輸入與計算結果重複。資料格重複時回報
衝突，不能靠 MAX 隱藏。相同比率跨期不 SUM；BS 餘額不跨日 SUM。
statement pivot 停用跨期間總計／全科目總計，因包含小計、期初期末與非加總科目。

預設展示已 accepted/published 的批次；選歷史 run 時不套 latest-only。
latest 是同公司／模式／scope／幣別／scale 最近完成且成功的 run，不保證是最新
財報期間。失敗或 draft 的本次請求需明示，不用舊成功批次冒充本次。

## 6. 規格驗證結果與待決策

| ID | 結果 | 狀態 |
| --- | --- | --- |
| D1 | 移除 ROA/ROE，總數23，P&L 4卡；另移除B6卡 | 使用者已確認 |
| D2 | C1/C3：CFO/期間期末流動負債，名稱 Cash Flow Ratio；移除 dashboard Cash Ratio | 使用者最新更正已確認，取代先前選擇 |
| D3 | P11 採正式9列；B11 改完整14列；C4 納入FX | 本稿設計建議，待審閱 |
| D4 | 單一期間卡片、Quarterly YTD比較、C3實際時點，取消近12個月 | 本稿設計建議，待審閱 |
| D5 | net_margin、B4/B5、BS identity定義；cash_flow_ratio沿用既有公式 | 其餘待定版；新增指標仍待來源／公式實作 |

目前 Quarterly report_layout 沒有 cash_flows 表，也未預設 cash_flow_ratio 列；
雖然 contract 已有公式，不能宣稱季度值已生成／發布。Quarterly C1/C3/C4 必須補
supporting facts、來源擷取、計算、驗證及發布。BS 明細同樣需要正式事實映射。

## 7. 實作後驗收案例（目前為測試設計，尚未執行）

| 案例 | 預期結果 |
| --- | --- |
| 兩家公司切換 | 23元件、標題、日期及引用同步，無跨公司資料。 |
| 同公司兩run＋歷史選取 | 一次只顯示一run；最新與歷史模式不互相遮蔽。 |
| Annual四年 | 卡片取單一年；圖表／表四年順序正確，不產生四年總卡。 |
| Quarterly | income/CF只用可比YTD；BS四時點；無月度插值、YTD相加。 |
| 正式數值核對 | 每個已存在的canonical fact與同run report.json一致；新增supporting facts可回溯來源。 |
| common-size重複 | 同metric金額與百分比不混加；重複資料格報錯。 |
| 來源／單位 | scale不重複除百萬；BS現金與含restricted cash的CF現金不互代。 |
| 缺值與零 | missing/conflict/not_calculable/not_applicable各保留狀態；確認零可顯示0。 |
| 負數與零分母 | 虧損、負權益保留；零分母不輸出Infinity或補0。 |
| 會計勾稽 | 毛利／營業利益／稅前稅後、現金bridge、資產=負債+權益各保留檢查。 |
| 展示精度 | 先用精確值核對canonical；最後才四捨五入，展示差異不覆蓋財務驗收結果。 |
| 發布／刷新／連結 | 最新run實際可見；URL選中公司與run；驗證權限和快取後再宣稱交付成功。 |

## 8. 圖表能力依據

Looker Studio 的 Combo chart 可分別設定柱／線；本稿雙軸配置仍需在實際範本
驗證。參見 [官方圖表文件](https://docs.cloud.google.com/data-studio/line-chart-and-combo-chart-reference)。
科目列、期間欄的明細採 [Pivot table](https://docs.cloud.google.com/data-studio/pivot-table-reference)。
