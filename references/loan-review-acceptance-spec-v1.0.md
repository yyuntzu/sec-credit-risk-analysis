# Loan Review Modification and Acceptance Specification v1.0

- Date: 2026-10-06.
- Calculation addendum: 2026-10-23. Incorporates the SEC-to-account mapping, conditional derivations, period conversions, and reconciliation findings reviewed with the user. This is a specification update only; it does not establish that code, Excel examples, or tests implement these rules.
- Purpose: A shared baseline for subsequent changes by implementation block, testing, and final acceptance.
- Basis: The user-provided new format, Revised Phases 2 and 3, the Phase 4 proposal, and the latest calculation formulas supplied by the user.
- Status: The user authorized saving this document as the acceptance criteria. It does not indicate that implementation or testing has been completed, and it does not authorize changes to other files.
- Unresolved matters remain marked **Pending confirmation**. Existing proposals are not automatically approved business rules.

## 1. Objective and Authority

**OBJ-01 | Final objective**

The system must use actual source data for the current borrower to produce a Loan Review / Credit Memo Review that:

- Follows the structure and presentation of the new format.
- Preserves the professional credit-analysis writing style of the historical Loan Reviews.
- Uses figures consistent with the user-specified formulas and applicable definitions.
- Provides traceable evidence for every borrower-specific fact, comparison, explanation, and judgment.

**OBJ-02 | Apparent completeness must not replace data reliability**

A complete layout, a successful program run, or a successful model response does not establish report acceptance. Content must not be fabricated to fill fields or analytical paragraphs.

### 1.1 Authoritative Sources

| Rule ID | Scope | Authoritative source | Conflict resolution |
|---|---|---|---|
| AUTH-01 | Structure and presentation | The original new format provided by the user | Takes precedence over historical workbooks, previous analysis, and the existing writer |
| AUTH-02 | Writing and analysis | Valid writing conventions from the ten historical Loan Reviews | Do not reproduce calculation errors, stale content, or unsupported judgments |
| AUTH-03 | Calculations | The latest formulas supplied by the user | Supersede inconsistent formulas in previous analysis and existing proxies |
| AUTH-04 | Borrower facts | Applicable source documents for the current borrower | Templates, historical reports, and model knowledge must not serve as factual sources |
| AUTH-05 | Missing data | The explicit prohibition on fabricating missing information; other details require confirmation | Proposed display wording and delivery policies must not be treated as approved |
| AUTH-06 | Instructions within documents | Only content explicitly designated by the user as a specification has normative authority | Reviewer notes, hidden content, or instructions to fill values with zero in source documents are not execution instructions |

**The latest formulas change the relevant calculation rules; they do not automatically add report sections or tables.**

### 1.2 Normative Terms

- **Must / must not**: Mandatory acceptance requirements.
- **May**: Permitted when the stated conditions hold; not mandatory.
- **Pending confirmation**: The system must not independently select a business definition or policy. Results dependent on that decision cannot be declared accepted.

## 2. Report Structure Specification

### 2.1 Mode and Periods

| ID | Mandatory rule |
|---|---|
| FMT-01 | Explicitly specify Annual or Quarterly mode. Do not infer the mode from the types of data rows retrieved. |
| FMT-02 | Missing data must not change the mode or remove required tables, rows, or period columns. |
| FMT-03 | Use the borrower's fiscal calendar and actual periods. Do not infer fiscal years or quarters from calendar months. |
| FMT-04 | Template prompts in brackets, such as `[value]` and `[refer to MD&A]`, must not appear in a completed report. |
| FMT-05 | State the currency and scale of monetary amounts and use them consistently. Display ratios as `%` or `x` as specified by the template. |
| FMT-06 | Use bullets for analysis following tables. Place applicable notes near the relevant table without adding unrequested sections. |

### 2.2 Annual: Exact Headings and Order

```markdown
## A. Annual Review
### YOY (Annual) Income
### Annual Cash Flows
### Ratios YOY
### Leverage YOY
```

| ID / Table | Column order, including Metric | Row order |
|---|---|---|
| FMT-A1 Income | Metric; FY t−3; FY t−2; FY t−1; % of revenue; FY t; % of revenue | The nine common income rows below |
| FMT-A2 Cash Flows | Metric; FY t−3; FY t−2; FY t−1; FY t | Beginning balance; Operating activities; Investing activities; Financing activities; Ending balance; Change |
| FMT-A3 Ratios | Metric; year-end t−3; year-end t−2; year-end t−1; year-end t | Current ratio; Quick ratio; Cash flow ratio; Debt ratio; Interest coverage ratio |
| FMT-A4 Leverage | Metric; year-end t−3; year-end t−2; year-end t−1; year-end t | Total debt; Debt service; Interest expense; LTM EBITDA; EBITDA basis; Total leverage ratio; EBITDA / Interest expense; Debt service coverage ratio |

Display rules:

- Annual income has **7 columns**; each remaining table has **5 columns**.
- Current, Quick, Cash flow, and Debt ratios use `%`.
- Interest coverage, Total leverage, EBITDA / Interest expense, and DSCR use `x`.
- If the EBITDA basis is identical across all annual columns, it may be replaced by a shared note **immediately after the EBITDA row**. Otherwise, show the basis separately for each column.
- Cash Flows columns represent full-year periods. Year-end columns in other tables do not mean every metric is an instant fact. LTM EBITDA, interest, and other duration metrics must retain their applicable duration.

### 2.3 Quarterly: Exact Headings and Order

```markdown
## B. Quarterly Review
### Financial Analysis
#### YTD (Quarterly) Income
#### Ratios YTD
#### Leverage Analysis YTD
```

| ID / Table | Column order, including Metric | Row order |
|---|---|---|
| FMT-Q1 Income | Metric; prior comparable YTD; % of revenue; current YTD; % of revenue | The nine common income rows |
| FMT-Q2 Ratios | Metric; earlier FY-end; prior comparable interim; latest FY-end; current interim | Current ratio; Quick ratio; Debt ratio |
| FMT-Q3 Leverage | Same as FMT-Q2 | Total debt; LTM EBITDA; EBITDA basis; Total leverage ratio |

Display rules:

- All three tables have **5 columns**.
- Retain an EBITDA basis row with a value for each quarterly comparison column.
- Do not automatically add Annual Cash Flows, Debt service, or DSCR rows.
- Compare YTD with the prior year's comparable YTD. Do not substitute a standalone quarter.

### 2.4 Nine Common Income Rows

Use the following order:

1. Revenues or Net sales.
2. Cost of revenues, Cost of sales, or Cost of services.
3. Gross profit.
4. Operating expense.
5. Operating income.
6. Interest expense.
7. Income before taxes.
8. Income tax expense.
9. Net income.

Select the applicable labels for the first two rows from the source line items. Do not use the slash-separated alternatives literally as final line-item names.

`% of revenue` means **the row amount divided by revenue for the same period**, not a growth rate. If revenue is missing or zero, do not unconditionally display the revenue share as 100%.

### 2.5 Content That Must Not Be Added Automatically

**FMT-07:** Do not add a cover, Part numbering, Borrower / Loan Information, Ratings, History, Covenants, EV, Stock, News, Summary, signatures, or a separate Data Quality Appendix merely because a historical workbook or the old skill included them.

Fonts, gray bands, merged cells, print scaling, and other historical Excel styling are also not established requirements for this format.

## 3. Narrative and Analysis Specification

### 3.1 Analytical Coverage by Section

| ID | Section | Topics and placement |
|---|---|---|
| NAR-01 | After the Annual / Quarterly income table | Revenue → gross margin → operating margin → interest expense → pre-tax margin |
| NAR-02 | Near Annual Cash Flows | Necessary cash-definition, FX, or other reconciliation notes; a long narrative is not mandatory |
| NAR-03 | After Annual Ratios | Current / quick ratios, cash flow ratio, debt ratio, and interest coverage |
| NAR-04 | After Annual Leverage | EBITDA, debt service, DSCR, total debt, and leverage; typically four or five bullets, with overlapping content combined |
| NAR-05 | After Quarterly Ratios | Typically two bullets: current / quick ratios and debt ratio; a material quick-ratio issue may receive a separate third bullet |
| NAR-06 | After Quarterly Leverage | Total debt, LTM EBITDA on a consistent basis, and leverage movement; default to debt-first ordering as in the new example |
| NAR-07 | Exceptional items | Additional impairment, disposal, adjusted-result, or net-income analysis may be included when supported and material |

These are topic-coverage requirements, **not unconditional narrative-count quotas**. Disclose limitations when data is insufficient; do not add generic filler.

### 3.2 Writing Rules

| ID | Mandatory rule |
|---|---|
| STYLE-01 | Use a formal, restrained, third-person banking credit-analysis tone. Avoid promotional language and vague evaluations. |
| STYLE-02 | Normally organize analysis as data → comparison → supported explanation → necessary and supported credit implication. The last two elements are not mandatory. |
| STYLE-03 | Ordinary bullets normally contain one or two sentences. Material exceptional items may require more space. |
| STYLE-04 | Distinguish duration periods from balance dates, gross from net, GAAP from adjusted results, consolidation scope, and YTD from LTM. |
| STYLE-05 | Compare income across comparable annual / YTD periods. Quarterly balance comparisons normally use the latest FY-end as the baseline. |
| STYLE-06 | Express margin differences in percentage points and growth rates in percentages. |
| STYLE-07 | Describe equal values as unchanged. Insufficient data must not produce an increase, decrease, improvement, or deterioration judgment. |
| STYLE-08 | Discuss risks and mitigants only when supported. Do not declare financial health, adequacy, or repayment ability based on a single ratio or an unapproved threshold. |
| STYLE-09 | A change in definition or scope must not be presented directly as operating improvement or deterioration. |
| STYLE-10 | Do not transfer historical company names, figures, explanations, terms, guidance, ratings, or credit status into the current report. |

**Causality boundary:** Figures can establish that revenue declined; the decline alone does not establish weaker demand. If the source is management commentary, preserve that attribution rather than presenting management's explanation as an independently verified fact.

## 4. Calculation Specification

### 4.1 General Requirements

| ID | Mandatory rule |
|---|---|
| CALC-01 | Perform financial calculations through deterministic code. The model must not independently fill in or estimate missing inputs. |
| CALC-02 | Retain the formula version and input fact IDs for every calculated value. |
| CALC-03 | Inputs must satisfy the formula's entity, scope, period, unit, and basis requirements. |
| CALC-04 | Missing required inputs must not be treated as zero. Zero requires an explicit zero in the direct source. |
| CALC-05 | Do not divide by zero. Do not take the absolute value of a negative denominator to make the result appear more favorable; explicitly address its presentation and interpretation. |
| CALC-06 | Calculate using unrounded values and apply display formatting only at the end. |
| CALC-07 | dbt, SQL fallback, Python, and reported values must be consistent. Different paths must not use different formulas for the same metric. |
| CALC-08 | Example values in the user's formula tables are not facts for a new borrower and are not test expectations without the corresponding inputs. |

Store percentage metrics as fractions (0.25 means 25%). When rendering plain numeric text, multiply once by 100 and append `%`; when applying an Excel percentage format, retain the fraction and let formatting perform the display conversion. Never scale twice. Do not multiply multiples or days by 100.

### 4.2 Confirmed Formulas

| ID | Metric | Approved formula |
|---|---|---|
| CF-01 | Current ratio | Current Assets / Current Liabilities |
| CF-02 | Quick ratio | Quick Assets / Current Liabilities |
| CF-03 | Cash flow ratio | Net Cash Inflow (Outflow) From Operating Activities / Current Liabilities |
| CF-04 | Interest Coverage Ratio | (Pre-tax Profit + Interest Expense) / (Interest Expense + Capitalized Interest) |
| CF-05 | EBITDA / Interest Expense | (Pre-tax Profit + Interest Expense + Depreciation & Amortization) / (Interest Expense + Capitalized Interest) |
| CF-06 | Debt Ratio | Total Liabilities / Net Worth |
| CF-07 | Fixed Asset To Net Worth Ratio | Fixed Assets / Net Worth |
| CF-08 | Fixed Assets To Long Term Capital Ratio | (Fixed Assets + Funds & Investments) / (Net Worth + Long Term Liabilities) |
| CF-09 | Revenue growth rate | (Current Year Revenues − Previous Year Revenues) / Previous Year Revenues |
| CF-10 | Gross profit margin | Gross Profit / Revenues |
| CF-11 | Operating profit margin | Operating Profit / Revenues |
| CF-12 | Pre-tax profit margin | Pre-tax Profit / Revenues |
| CF-13 | Return On Net Worth | ((Pre-tax Profit / Months) × 12) / Average Net Worth |
| CF-14 | Return On Asset | ((Pre-tax Profit / Months) × 12) / Average Total Assets |
| CF-15 | Financial Expense Ratio | Interest Expense / Revenues |
| CF-16 | Change In Operating Profit Margin | Current Operating Profit Margin − Previous Operating Profit Margin |

Calculate CF-16 using the user's formula, but label the change in **percentage points** to distinguish it from relative growth.

| ID | Turnover metric | Times formula | Days formula |
|---|---|---|---|
| CF-17 | Accounts Receivable Turnover | (Revenues / Months × 12) / Average (Accounts Receivable + Bad Debt Allowance) | 365 / Times |
| CF-18 | Accounts Payable Turnover | (Operating Costs / Months × 12) / Average Accounts Payable | 365 / Times |
| CF-19 | Inventory Turnover | (Operating Costs / Months × 12) / Average (Inventory + Provision For Inventory Devaluation) | 365 / Times |
| CF-20 | Fixed Asset Turnover | (Revenues / Months × 12) / Average Fixed Assets | 365 / Times |
| CF-21 | Total Asset Turnover | (Revenues / Months × 12) / Average Total Assets | 365 / Times |

**Confirmation of a formula does not confirm all component definitions.** Quick Assets eligibility, the sampling method for averages, and source-sign mapping for allowances still require verification. They must not be inferred from metric names alone.

Metrics absent from the new format remain calculation rules; they do not require extra tables or an expanded implementation scope for this report.

### 4.3 Other Required Report Calculations

| ID | Rule |
|---|---|
| CALC-09 | Total leverage ratio uses Total debt / applicable LTM EBITDA. The scope and dates must be compatible; do not calculate it when the applicable definitions remain unconfirmed. |
| CALC-10 | Complete approved definitions for debt service and DSCR remain outstanding. Do not use interest + CapEx, unsupported principal amounts, or an arbitrarily selected numerator. |
| CALC-11 | LTM must cover a complete fiscal-year duration ending on the specified date, including applicable 52- or 53-week fiscal years. Do not present fewer than four quarters, overlapping YTD periods, or the nearest available older TTM as LTM for that date. |
| CALC-12 | Missing D&A must not cause Operating income to replace EBITDA. Preserve the actual basis of source-reported EBITDA. |
| CALC-13 | CF-05 must not substitute another adjusted or covenant EBITDA value for its specified numerator. If the values differ, preserve and explain the difference in definitions. |
| CALC-14 | Derive gross profit, pre-tax profit, and similar values only through confirmed, applicable accounting identities with complete inputs. Do not automatically take the absolute value of tax benefits. |
| CALC-15 | Beginning cash, ending cash, and change must use a consistent cash definition. Do not infer missing values from the three activity categories when FX, restricted-cash, or other reconciliation information is incomplete. |

Previous coverage formulas omitting Capitalized Interest, and conclusions treating the two coverage measures as the same metric, no longer apply.

### 4.4 SEC 原始科目、統一科目與最終報表的計算邊界

本節補充既有 CF、CALC、DATA 規則，不更改第 2 節的 Annual／Quarterly 最終報表結構，也不核准第 9 節仍待確認的定義。工作底稿可以比最終報表有更多科目與對照欄；不得將底稿的所有欄位、比率或差異表自動加入最終報表。

查找參考：[AI 財務資料擷取參考準則](loan-review-extraction-reference.md)及[逐科目索引](loan-review-account-reference.md)重用本規格與現有代碼，保留原Excel出現紀錄、候選tags及待確認事項；此連結不將候選定義／映射升格為已核准，也不代表已接入程式。

| ID | 規則 |
|---|---|
| CALC-16 | 採兩步驟資料映射：先將 SEC 原始科目對應至統一會計科目，再由統一科目及核准計算結果填入最終報表。AI 可提出科目與附註對應，但金額計算、期間轉換及勾稽由確定性程式執行。 |
| CALC-17 | 原始揭露值、統一科目值與推導值必須可分辨。原文名稱、tag／namespace、原始數值、單位、期間、合併範圍、申報版本及來源位置不得被標準化結果覆蓋；計算值保留公式版本與輸入 fact IDs。 |
| CALC-18 | 逐公司、逐期間、逐科目判斷取值方式；不得永久指定某家公司「一律推算毛利」，也不得只依英文名稱或 Excel 行號對應。缺少 API tag 只代表目前未取得，須記錄是否已查閱申報主表、附註、自訂標籤或其他適用申報，不能直接宣稱財報未揭露。 |
| CALC-19 | 同一科目已有適用的直接揭露值時，保留該值及其證據；可另計算恆等式作勾稽。若兩者不符，並列來源值、推導值及差額，不得靜默覆寫、選最大值或用調整數湊平。衝突處理仍依 DATA-03／DEC-07。 |
| CALC-20 | 總額、小計及明細應形成可核對的科目層級。相同來源的替代 tag、同義名稱、含商譽無形資產合計與其組成項目、應收／應付小計與其明細，不得重複加總。只有確認互不重疊且完整的明細才能產生小計或合計。 |

建議檢查底稿至少能回答：最終報表欄位 → 統一科目 → 原始科目或計算公式 → 輸入事實 → SEC 文件與儲存格／表格／附註位置。這是邏輯要求，不指定新增資料庫或重寫現有 pipeline。

### 4.5 直接取值與條件式推導公式

以下是 CALC-14 的具體推導方法，**只有列示的適用條件成立時才可使用**。任一必要輸入缺失、定義未確認、合併範圍不同或來源衝突時，不得產生看似完整的數字。不得為了完成另一個公式而循環反推輸入。

| ID | 項目 | 公式／方法 | 適用條件與限制 |
|---|---|---|---|
| DER-01 | Gross Profit／毛利金額 | Revenues − Cost of Revenue | 優先保留適用的直接揭露毛利；推導時營收與成本必須同期間、同範圍，且成本為對應營收成本，不是包含其他營業費用的總費用。若主表另有影響毛利的項目，須先確認完整恆等式。 |
| DER-02 | Cost of Revenue／營收成本 | Revenues − Gross Profit | 僅在直接成本未取得、毛利有獨立來源且 DER-01 的會計結構成立時使用。不得同時以未知成本推毛利，再以該毛利反推成本。 |
| DER-03 | Operating Expense／不含營收成本的營業費用 | Gross Profit − Operating Income | 僅適用於兩者之間完全由該類營業費用構成的列報。若另有營業收益、重組、減損或其他獨立調整，須確認其歸屬及符號後使用完整橋接式。不得不加核對地將 `CostsAndExpenses` 當成不含 COGS 的費用。 |
| DER-04 | Operating Income／營業利益 | Gross Profit − Operating Expense | 與 DER-03 相同的完整橋接條件；不得重複扣除已含在成本中的折舊、攤銷或其他費用。 |
| DER-05 | Pre-tax Profit／稅前利益 | Net Income + signed Income Tax Expense | 只限淨利與所得稅對應同一稅前損益範圍，且沒有未處理的停業單位、非控制權益或其他橋接項。所得稅費用為正、利益為負；不得使用 `abs(tax)`。若有橋接項，須有來源及經確認的完整公式。 |
| DER-06 | Net Income／稅後淨利 | Pre-tax Profit − signed Income Tax Expense | 與 DER-05 相同的適用條件；不得把 continuing operations、歸屬母公司淨利與合併淨利直接互換。 |
| DER-07 | 小計與合計 | Σ 已確認、不重疊的組成項目（依來源符號處理減項） | 資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。 |
| DER-08 | Working-paper cash bridge／現金勾稽 | Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項 | 期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |

「Gross Profit」是金額，「Gross Profit Margin」是比率；不得以含糊的 `Margin Profit` 作為兩者共用科目。毛利率、營業利益率及稅前淨利率依 CF-10–12 計算；是否取得直接毛利、是否使用 DER-01，必須在每一期資料的狀態與證據中標示。

補充顯示／計算規則（不新增最終報表列）：

| ID | 項目 | 公式與條件 |
|---|---|---|
| DER-09 | Common-size／營收占比 | 同期科目金額 ÷ 同期 Revenues。營收自身的占比也須先確認營收可用且非0；占比不是成長率。 |
| DER-10 | Annual cash change／年度現金變動 | 同口徑 Ending Cash − Beginning Cash。另以 DER-08 核對橋接；不可直接將 CFO＋CFI＋CFF 視為所有情況下的完整變動。 |
| DER-11 | Net Profit Margin／淨利率（若另外納入分析範圍） | 同期、同範圍 Net Income ÷ Revenues。此處記錄定義，不自動增加第 2、3 節的表格列或敘述要求。 |

### 4.6 FY、QTD、YTD 與 LTM 期間轉換

| ID | 期間／方法 | 計算規則與條件 |
|---|---|---|
| PER-01 | FY | 使用經核實的完整會計年度起訖日；不得將 10-K 文件中的所有期間都視為當年度，也不得強制套用曆年。 |
| PER-02 | QTD 與 YTD | QTD 是單季流量，YTD 是會計年度開始至本期末的累計流量。10-Q 可同時含不同期間；須以每個事實的實際 start／end、單位及範圍判斷，不只依文件類型、`fy/fp` 或截止日。 |
| PER-03 | 由累計推單季 | Q2 QTD = Q2 YTD − Q1 YTD；Q3 QTD = Q3 YTD − Q2 YTD；Q4 QTD = FY − Q3 YTD。輸入須為同一會計年度、相容版本及相同範圍／單位的累計值，並確定差額對應完整單季。 |
| PER-04 | 由單季形成累計 | YTD = 從該會計年度開始至指定季末的完整、連續、不重疊 QTD 加總。不得再加已含在 YTD 中的季度。 |
| PER-05 | LTM 橋接 | LTM = 前一完整 FY + 本期 YTD − 前一年可比較 YTD。三項定義、範圍、單位及版本須相容，且組合後精確涵蓋指定截止日往前一個完整會計年度；52／53週或期間變更須另行核對。亦可使用完整、連續、不重疊的四個季度。 |
| PER-06 | 年化不等於 LTM | CF-13–14、CF-17–21 的流量年化依已核實的 Months 與適用規則處理；不得以 YTD×2、QTD×4 或任何年化近似值代替實際 LTM EBITDA。Months 與平均餘額取樣仍受 DEC-04 約束，不將示範檔的月份或平均方式升格為核准定義。 |
| PER-07 | 時點餘額 | 資產負債表使用指定日期的餘額；不得以相鄰季度餘額相減來建立「單季資產負債表」，也不得將年度或季度餘額相加形成 YTD。 |
| PER-08 | 前期比較及成長 | CF-09 比較完整年度對完整年度，或本期 YTD 對前一年可比較 YTD；QTD 比較僅適用於明確要求的單季分析。缺少前期值時補查適用歷史申報，不以另一期間替代，也不從公布比率倒推基期。 |

上述轉換只適用於具有加總性的流量金額。百分比、比率、EPS、加權平均股數及平均餘額不得直接依上述加減法轉換；必須使用各自經確認的計算方法。由 QTD 或 YTD 衍生的資料須明確標示為計算值。

### 4.7 勾稽、差異與示範檔修正

| ID | 規則 |
|---|---|
| REC-01 | 同一日期、同一合併範圍及單位下核對 Assets = Liabilities + Equity；先查核是否包含非控制權益及其他來源列示的權益項目。不得把差額補進 Other Assets／Other Liabilities。 |
| REC-02 | 同一定義下核對本期期初現金與前期末現金，以及 DER-08 的本期現金橋接。前期 BS 現金與 CF 現金若定義不同，須先以附註建立橋接，不能直接判定為錯誤。 |
| REC-03 | 每項差異保留來源原值、計算結果、差額方向、幣別／單位、期間、來源位置、使用公式及調查狀態。差額採「計算值－來源值」；百分比差額採百分點，不當成相對成長率。 |
| REC-04 | 差異原因分成公式錯誤、映射／重複加總、期間、單位、範圍／定義、版本、缺少組成資料、顯示精度或尚待查明。沒有證據時不得選定原因；不能只看到 Excel 不一致就宣稱 SEC 財報錯誤。 |
| REC-05 | 計算精度與顯示精度分開驗證；保留未捨入中間值。容許差須依實際來源精度與核准顯示規則設定，不以擴大容許差消除公式錯誤。差異清單屬內部核對材料；最終報表僅在適用表格旁呈現必要註記，依 FMT-07 不自動新增附錄。 |

**本對話示範檔的更正記錄：**

- 固定資產對長期資金比率必須採 CF-08，分子包括 **Funds & Investments**。先前示範公式只用 Fixed Assets，對 Nexstar 各期產生的該項差異是示範公式的誤報，不能當成原始財報有誤的證據。
- 例：Nexstar 工作底稿 2025 年數據，金額單位為千美元，`(1,158,000 + 396,000) / (2,062,000 + 6,222,000) = 0.1875905359729599`，顯示為 **18.76%**，與原檔相符。來源為 `Year/E-loan YYYY_Nexstar 2025.xls`，`Report1!R26`、`R24`、`R70`、`R54`；來源比率為 `R205`。此為使用者工作底稿核對例，尚非 SEC 原始申報核驗，也不核准其金額移用到其他公司／期間。
- CF-04／05 的分母不能漏掉 Capitalized Interest；資本化利息、D&A、呆帳備抵及存貨跌價備抵的未取得值不能當0。CF-17／19 也不能在未確認組成項目及符號時，直接以淨應收款或淨存貨替代已核准的分母。
- 先前示範對原檔空白暫填0、速動資產組成、平均餘額取樣及現金橋接的假設，均不是正式規格或實作驗收依據。正式計算須重新核對本文件規則及適用 SEC 來源。
- Nexstar e-loan 底稿中曾出現現金橋接差異、跨期現金差異，以及同一金額的債務清償／投資減損／匯兌名稱不同。這些是待調查線索；須查核 SEC 原始主表、現金及受限制現金調節、匯率、停業單位與附註，不直接以調節數消除，也不宣稱已確定原因。

### 4.8 補查資料與正式交付完整性

| ID | 規則 |
|---|---|
| SRC-01 | 缺少必要輸入時，先列出「公司、科目、期間、定義、已查材料、尚需來源」的補查清單；同公司適用申報中的比較欄、較早的10-K／10-Q、主表與附註可作候選證據，仍須符合實體、期間、單位、版本及範圍要求。 |
| SRC-02 | 所有必要輸入有來源、經核准推導或有證據確認不適用，且必要勾稽已完成解釋，才可主張該數值已完成核驗。找到 tag、填滿 Excel、程式執行成功或來源層完成，不等於最終報表已驗收。 |
| SRC-03 | 使用者要求「最終報表不要有數字缺失」是資料補查與核驗目標，不授權補0、估計、從比率反推或使用未核准代理值。確實未揭露、仍有衝突或定義未決時，保留狀態與原因；正式交付及不適用項目的呈現仍依第6節與 DEC-08，不在此自行建立豁免清單。 |

## 5. Data and Evidence Contract

These are **minimum logical requirements**, not approval of a particular Python class, database migration, or storage architecture.

### 5.1 Minimum Information for Each Financial Fact

| Category | Information that must be available |
|---|---|
| Identity | Fact ID, borrower/entity, and consolidation scope |
| Metric | Metric and definition / basis |
| Period | Instant or duration; balance date or start/end; fiscal period role |
| Value | Original value, normalized value, currency, and unit / scale |
| Source | Source ID, document version / date, and locator such as XBRL tag, page, cell, or passage |
| Calculation | For derived values: formula ID / version and all input fact IDs |
| Status | Directly sourced, calculated, missing, conflicting, not calculable, or confirmed not applicable |

**DATA-01:** A shared metric name and end date do not establish that two records are the same fact. Different start dates, scopes, versions, and bases must remain distinguishable.

**DATA-02:** Do not simply add alternative XBRL tags. First establish whether they are alternative representations or genuinely separate components to avoid double counting.

**DATA-03:** Do not silently select among restated values or conflicting sources. Apply the approved version-selection policy.

### 5.2 Minimum Evidence for Each Statement

| Statement type | Required support |
|---|---|
| Amount, date, or ratio | Corresponding facts or a traceable calculation |
| Current / prior comparison | Both sets of facts, comparison periods, and comparability |
| Explanation of a change | A source passage that actually supports the stated cause |
| Management explanation | The passage and attribution to management |
| Credit judgment | Supporting data, an applicable evaluation basis, and an appropriately limited scope |
| Statement of insufficient data | The actual scope of material reviewed and a record of the missing information |

**EVD-01:** The presence of an evidence ID does not establish a statement's validity. Check that the entity, period, scope, and meaning support the statement.

**EVD-02:** When only an excerpt has been reviewed, state only that the provided / reviewed material does not support the claim. Do not claim the entire filing lacks the disclosure.

**EVD-03:** Keep historical style references separate from current borrower evidence. Test data, dashboard samples, and template figures must not enter the factual dataset.

## 6. Missing Data and Exception Handling

### 6.1 Confirmed Mandatory Rules

| ID | Rule |
|---|---|
| MISS-01 | Missing ≠ zero. |
| MISS-02 | Not extracted ≠ not disclosed in the document. |
| MISS-03 | Not calculable ≠ not applicable. |
| MISS-04 | Without evidence for a cause, describe only the verifiable change; do not add a causal explanation. |
| MISS-05 | Unconfirmed definitions, incomplete components, or conflicting sources must not produce apparently definitive figures. |
| MISS-06 | Preserve the required structure when data is missing, with limitations visible at the relevant location. |
| MISS-07 | Missing data must not trigger substitute formulas, estimates, or default credit judgments. |

### 6.2 Presentation and Delivery Policies Pending Confirmation

The following remain proposals, not approved rules:

| Situation | Proposed presentation |
|---|---|
| Missing source / component | `Unavailable` plus a brief reason |
| Unconfirmed definition | `Unavailable — definition not verified` |
| Conflicting sources | Explicitly identify the conflict and the sources involved |
| Not calculable, such as a zero denominator | Explicitly state that it is not calculable and explain why |
| Confirmed not applicable | `Not applicable` |

A decision is still required on which omissions permit delivery with limitations and which must block final delivery. Until that policy is confirmed, output with critical omissions must not be labeled a completed substantive credit assessment.

## 7. Executable Acceptance Cases

Every test must reference the applicable rule IDs and include:

**Input fixture → independently established expected result → actual result → pass / fail → failure reason.**

Expected results must not be generated by the same calculation logic under test. Synthetic data may be used for testing, but must be explicitly isolated and must not populate borrower reports.

| Test ID | Scenario | Required result |
|---|---|---|
| AT-01 | Complete Annual data | All four tables have the correct headings, hierarchy, order, rows, columns, and narrative placement |
| AT-02 | Complete Quarterly data | All three tables and the Financial Analysis hierarchy conform, without extra annual tables or rows |
| AT-03 | A missing year / missing quarterly data | Preserve required columns and mode; do not drop columns or switch modes |
| AT-04 | Non-calendar / 52- or 53-week fiscal year | Correct fiscal roles and actual periods, without calendar-based guessing |
| AT-05 | Same end date with different durations | Quarterly, YTD, and Annual records are not incorrectly joined or deduplicated |
| AT-06 | Zero, missing, and equal values | Distinguish them; equal values are not described as increases or improvements |
| AT-07 | Coverage with capitalized interest | CF-04 / CF-05 include it correctly in the denominator and remain distinct metrics |
| AT-08 | Missing capitalized interest or D&A | Do not assume zero or generate substitute EBITDA / coverage |
| AT-09 | Unconfirmed Quick Assets | Do not substitute CA minus inventory or the current ratio |
| AT-10 | Debt ratio | Use liabilities / net worth, not liabilities / assets |
| AT-11 | Missing principal / DSCR definition | Do not substitute CapEx or assume zero principal |
| AT-12 | Zero / negative denominators and tax benefits | No division by zero, arbitrary absolute values, or misleading favorable / unfavorable judgments |
| AT-13 | Incomplete / overlapping LTM | Do not mark it as valid LTM or base a leverage judgment on it |
| AT-14 | FX / restricted-cash reconciliation | Use a consistent cash bridge; do not backsolve missing values when components are absent |
| AT-15 | Figures without an explanation | Describe the comparison only; do not generate an unsupported cause |
| AT-16 | Passage for the wrong company / period | Do not use it as narrative evidence |
| AT-17 | Changed debt / EBITDA basis | State that the values are not directly comparable; do not misrepresent the change as organic improvement |
| AT-18 | Presence / absence of a material exceptional item | Add analysis only when supported and material; do not enforce a filler bullet quota |
| AT-19 | Historical borrower or sample contamination | Exclude it from current facts and narrative |
| AT-20 | Writer / other export | Tables and prose agree; no independent filling of values, factual rewriting, or residual placeholders |
| AT-21 | Different calculation paths | dbt, SQL fallback, and Python produce consistent results and statuses for the same inputs |
| AT-22 | Source conflicts / restatements | Apply the approved policy; disclose unresolved matters rather than silently selecting values |
| AT-23 | Writing quality | Manually check professional tone, specific comparisons, terminology, and analytical depth; keyword matching alone is insufficient |
| AT-24 | SEC → 統一科目 → 最終報表映射 | 逐公司、逐期間追溯來源；自訂標籤或 API 缺項不能直接判為未揭露，同義 tag 與小計／明細不得重複加總（CALC-16–20） |
| AT-25 | 毛利、成本與營業費用推導 | 以完整且定義相容的獨立輸入驗證 DER-01–04；測試包含 COGS 的總費用、其他營業收益及循環反推被拒絕的案例 |
| AT-26 | 稅前／稅後損益橋接 | DER-05／06 保留稅益符號；停業單位、非控制權益或其他未處理橋接項使簡式不適用時，不輸出錯誤推導值 |
| AT-27 | QTD／YTD／FY 轉換 | 依 PER-01–04、07–08 驗證同季截止日的不同期間、完整差分與加總、非加總性指標及基期缺失；不得改變最終 Quarterly 的YTD欄位 |
| AT-28 | LTM 與年化的區別 | PER-05／06 使用完整相容 FY＋YTD－同期YTD，或四個連續季度；不接受 YTD×2、QTD×4、重疊或不完整期間作 LTM |
| AT-29 | 固定資產對長期資金比率漏項回歸 | CF-08 分子包含 Funds & Investments；以有非零投資的獨立 fixture 驗證，防止再以 Fixed Assets 單獨作分子。上述 Nexstar 底稿例僅在來源 fixture 一併提供時使用 |
| AT-30 | 占比與百分比顯示 | DER-09 驗證同期間分母、營收缺失／零值與負值；0.25以Excel百分比顯示為25%，不得變成2500%；百分點與成長率分開驗證 |
| AT-31 | 完整現金橋接與跨期現金 | DER-08／10、REC-01–04 驗證受限制現金、匯率、停業單位、期初與前期末定義、資產負債及現金勾稽；不以差額補進其他科目 |
| AT-32 | 來源值與計算值不符 | 依 CALC-19、REC-03–05 同時保留兩者與差額；未知原因保持待查，不把錯誤公式造成的差異誤報為來源錯誤 |
| AT-33 | 補查與數字完整性 | SRC-01–03 保留補查範圍及證據；缺歷史基期、不適用、未揭露、衝突及示範填0各自分辨，不宣稱已核驗或以示範值通過正式驗收 |

Numerical tests must use unrounded expected values. Display tests must validate formatting separately. Specify calculation tolerances and display precision explicitly; do not conceal formula errors with overly broad tolerances.

## 8. Implementation Blocks and Test Gates

| Block | Applicable rules | Completion criteria for the block |
|---|---|---|
| 1. Specification and contract | AUTH, FMT, DATA, MISS | Every output element maps to data requirements, rule IDs, and tests |
| 2. Extraction and traceability | DATA, EVD | Identity, period, unit, source, and missing-data status propagate completely |
| 3. Calculations | CALC, CF | Approved formulas are correct; undefined items are not filled in; results agree across paths |
| 4. Narrative | NAR, STYLE, EVD | Comparisons and explanations are supported; missing data does not produce false conclusions |
| 5. Writer | FMT, MISS | Render the new format faithfully without changing validated content |
| 6. Integration | All | Automated tests and manual checks pass from source input through the final report |

**CHANGE-01:** Every change must identify its rule IDs, affected files, necessity, and impact. Do not refactor unrelated functionality.

**CHANGE-02:** When a shared metric's definition changes, do not retain its old name and thresholds in a way that silently changes its meaning. Verify compatibility with other consumers.

**CHANGE-03:** After completing each block, deliver:

- The actual scope of changes.
- The tests executed and their results.
- Reviewable output or differences.
- Unresolved rules, limitations, and impacts.

**CHANGE-04:** Tests that were not run, were blocked, or were skipped do not count as passed. Distinguish narrative regression tests using fixed fixtures from evaluations of actual model-generated output.

**CHANGE-05:** Passing a block does not mean the final report has passed. Integration acceptance must jointly verify format, calculations, evidence, narrative, and regression results for affected functionality.

## 9. Decisions Pending Confirmation

| ID | Pending decision | Affected scope |
|---|---|---|
| DEC-01 | Eligible assets and exclusions for Quick Assets | Quick ratio |
| DEC-02 | Definitions of Net Worth and Total Debt, treatment of leases, and consolidation scope | Debt ratio and leverage |
| DEC-03 | Complete debt service and DSCR definitions | Annual Leverage |
| DEC-04 | Average balances, Months, and allowance sign mapping | ROA, RONW, and turnover ratios; address when included in scope |
| DEC-05 | Gross / net interest expense and source mapping for capitalized interest | CF-04 / CF-05; the formulas themselves are confirmed |
| DEC-06 | Resolution of multiple EBITDA sources and policy for adjusted bases | LTM EBITDA and leverage |
| DEC-07 | Review as-of and restatement version policy | All historical comparisons |
| DEC-08 | Missing-value display wording and delivery-blocking rules for critical omissions | Reports with missing data |
| DEC-09 | File type, monetary scale, precision, and negative-number display | Writer and visual acceptance |
| DEC-10 | Initial non-SEC support through structured inputs or including automated parsing of original documents | Extraction scope |
| DEC-11 | Whether the dashboard is part of the same delivery | Regression and evidence acceptance for other outputs |

These pending matters block only business decisions that depend on them. They need not prevent test design for rules that are already clear, but assumed answers must not be used to claim acceptance.

**Track subsequent changes through rule ID → implementation location → test case → actual evidence. The final objective is achieved only when the new format, correct calculations, source support, and historical writing style all conform.**


### 9.1 使用者核准紀錄（2026-10-24）

核准依據：使用者在逐項白話說明後指示「approve all pending case and run test again」。以下記錄對先前明確建議的核准；未選定的選項不自行補定。本節是業務決策紀錄，不代表來源事實已查證、程式已實作或正式報表已通過驗收。

| ID | 本次核准範圍 | 尚待選定／執行限制 |
|---|---|---|
| DEC-01 | 速動資產納入可自由動用現金及約當現金、可迅速變現短期投資、扣備抵後應收帳款；排除存貨、預付款、受限制現金及性質未明其他流動資產；不得重複計入，明細不足不計算。 | 每家公司來源仍須證明符合此口徑。 |
| DEC-02 | Net Worth採包含非控制權益的合併總權益，不自行扣商譽／無形資產；Total Debt納入有息借款、公司債、當期到期部分及融資租賃；採一致合併範圍；Total Debt不等同Total Liabilities。 | 營業租賃負債是否納入尚未選定；整項不得當作無條件完成。 |
| DEC-03 | 優先採明確貸款契約／授信範本定義；無定義時保持待確認，不以CapEx代本金或自行選DSCR分子。 | 尚未指定契約、分子、應付／實付本息及租賃處理。 |
| DEC-04 | 平均餘額採期初與期末平均，缺期初不算；年度與YTD分開，年化不得稱LTM；完整月份才用月份換算；備抵依來源符號且只扣一次。 | 特殊／不完整期間另確認；不自動新增報表比率。 |
| DEC-05 | 採費用化利息總額，不扣利息收入；僅有淨額時補查附註；資本化利息另取明確揭露且避免重複；未揭露不當0。 | CF-04／05公式不變；仍須取得來源證據。 |
| DEC-06 | 區分一般、Adjusted及契約EBITDA；同範圍同定義比較；Adjusted須明確指定並有完整調節；LTM用實際連續12個月，不以年化替代；未解衝突保留。 | 正式槓桿採哪種EBITDA尚未選定。 |
| DEC-07 | 每次指定as-of，僅使用當日以前公開來源；採截止日前適用最新正式重編並留原版及差異；截止日後重編另列更新，不改寫當時報告。 | 必須有實際公布／版本證據。 |
| DEC-08 | 區分未揭露、待確認、來源衝突、無法計算、不適用；可產待驗收草稿，必要科目／核心比率／必要勾稽未完成不標正式通過。 | 沿用既有必要驗收條件，不新增缺值豁免。 |
| DEC-09 | Excel為主要檔案，Quarter／Year分頁；繁中並保留英文；同表明示且統一幣別單位；金額／百分比／倍數顯示2位小數，負數括號；完整精度計算，顯示才四捨五入；缺值依DEC-08。 | 金額單位元／千元／百萬元尚未選定；現有Markdown輸出不因此視為Excel交付完成。 |
| DEC-10 | 初期支援有固定期間、單位及來源的結構化輸入與已驗證Excel適配器；任意格式Excel／PDF解析列後續；標明非SEC來源。 | Nexstar適配器不視為通用解析器。 |
| DEC-11 | 本階段交付Excel／正式報表、來源、缺資料與驗收結果；Dashboard不納入本階段共同交付。 | 日後加入Dashboard另驗收。 |

不得將本節直接轉成所有Report的通用PASS或來源Evidence；待確認子項、缺資料與勾稽差異仍必須保留。程式及輸出是否符合本節須另行驗證。


### 9.2 使用者補充核准（2026-10-24）

本節優先於9.1中對應的未選選項，其他已核准限制維持不變。

| ID | 明確核准內容 | 仍須核驗的條件 |
|---|---|---|
| DEC-02 | Total Debt不包含營業租賃負債；融資租賃及其他已核准有息債務範圍沿用9.1。 | 來源必須能區分營業／融資租賃，避免當期與非流動部分重複加總。 |
| DEC-03 | DSCR = Cash Flow Available for Debt Service（CFADS）／Debt Service。 | 本式已核准，但CFADS包含／排除項目，以及Debt Service的本金、利息、租賃與應付／實付口徑尚未提供；不得自行用CFO、EBITDA、CapEx或其他代理值替代。必要組成未確定時仍為無法計算。 |
| DEC-06 | 採Standard EBITDA：Net Income + Interest + Taxes + Depreciation & Amortization（D&A），不採Adjusted或契約EBITDA。 | 沿用合併範圍及精確期間；Interest依DEC-05採費用化利息總額；Taxes保留稅費／稅益符號，不取絕對值；D&A不得重複加總；不得以營業利益代替本式；LTM仍須完整連續12個月。Net Income的具體來源範圍仍需與合併及非控制權益處理一致，不僅憑同名採用。 |
| DEC-09 | 正式報表金額採百萬元（million），標示實際幣別；其他精度／負數／缺值規則沿用9.1。 | 原始值與來源單位保留；顯示換算不代表匯率轉換，例如千美元除以1000顯示為百萬美元；百分比與倍數不套用金額縮放。 |

本節記錄使用者核准，不代表程式已完成對應實作、SEC來源已核實或Nexstar勾稽差異已解除。DEC-03組成定義仍待補充，不能將僅有公式視為完整償債政策。
