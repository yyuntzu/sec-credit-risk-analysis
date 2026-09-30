# Output Format Reference — Credit Memo Standard

按需載入 — Agent 生成報告時必須對照此文件，確保格式符合公司 credit memo 標準可直接交付主管審閱。

---

## 報告結構總覽

```
Section 1  — Cover / Header
Section 2  — YOY Income Statement  +  Commentary
Section 3  — Cash Flows
Section 4  — Ratios YOY            +  Commentary
Section 5  — Leverage YOY          +  Commentary
Section 6  — Enterprise Value Analysis
Section 7  — Financial Covenants
Section 8  — Summary
Appendix   — Data Quality Notes
```

---

## Section 1 — Cover Header

```
# Credit Memo: {Company Name} ({TICKER})
**Prepared by:** AI Credit Analysis Agent  
**Report Date:** {generated_date}  
**Analysis Period:** FY{n-3} – FY{n} (as of {period_end})  
**Overall Risk Flag:** 🔴 CRITICAL / 🟡 WARNING / 🟢 OK / 🔵 INCOMPLETE
```

---

## Section 2 — YOY Income Statement

### Quarterly Loan Review period basis

季度 Loan Review 的損益表與現金流一律採 YTD basis：Q1 = 1/1–3/31、Q2 = 1/1–6/30、Q3 = 1/1–9/30。Q2 與 Q3 必須分別使用 6 個月及 9 個月 XBRL duration facts，不得使用單一三個月季度數字。比較欄必須採去年同期相同累計期間。

Q2／Q3 的表格標題分別標示 `6M YTD`／`9M YTD`，commentary 除既有項目外必須包含：

- 本年度累計營運表現；
- 相較去年同期的 revenue、profitability 與 cash-flow 變化；
- YTD revenue／EBITDA 相對全年 management guidance 的達成率。Guidance 為區間時列示下限／中點／上限達成率；未揭露則標示 `Not disclosed`。

### Table format

| Account | FY{n-3} | FY{n-2} | FY{n-1} | % | FY{n} | % |
|---------|---------|---------|---------|---|-------|---|
| Revenues | | | | 100% | | 100% |
| Cost of revenues | | | | XX.XX% | | XX.XX% |
| Gross profit | | | | XX.XX% | | XX.XX% |
| Operating expense | | | | XX.XX% | | XX.XX% |
| Operating income | | | | XX.XX% | | XX.XX% |
| Interest expense | | | | XX.XX% | | XX.XX% |
| Income before taxes | | | | XX.XX% | | XX.XX% |
| Income tax expense | | | | XX.XX% | | XX.XX% |
| Net income | | | | XX.XX% | | XX.XX% |

**表格規則：**
- `%` 欄 = 該行項目 ÷ 當年 Revenue（common-size）
- `%` 欄**只出現在最近兩個會計年度**（FY{n-1} 和 FY{n}）
- 負數用括號表示：`(1,234)` ，% 顯示為負值
- 所有金額單位：USD millions，不顯示單位符號（標題列說明即可）

### Commentary block（≥5 bullets，緊接表格下方）

```
- Revenues: [YoY % change and primary driver]
- Gross margin: [direction and primary driver]
- Operating margin: [direction, key drivers — separate recurring vs non-recurring items]
- Interest expense: [direction and driver]
- Pre-tax margin / Net income: [direction and key driver]
```

**Agent 規則：**
- 若某行項目數據為 NO_DATA，bullet 需說明「not separately reported in XBRL filings」
- 非經常性項目（商譽減損、重組費用等）必須在 Operating margin bullet 中單獨標出

---

## Section 3 — Annual Cash Flows

| Item | FY{n-3} | FY{n-2} | FY{n-1} | FY{n} |
|------|---------|---------|---------|-------|
| Beginning balance | | | | |
| Operating activities | | | | |
| Investing activities | | | | |
| Financing activities | | | | |
| Ending balance | | | | |
| Change | | | | |

**Agent 規則：**
- Change = Ending balance − Beginning balance（驗算用，應與三項活動之和一致）
- Investing activities 通常為負值，用括號表示

---

## Section 4 — Ratios YOY

| Ratio | 12/31/FY{n-3} | 12/31/FY{n-2} | 12/31/FY{n-1} | 12/31/FY{n} |
|-------|---------------|---------------|---------------|-------------|
| Current ratio | XX.XXx | XX.XXx | XX.XXx | XX.XXx |
| Quick ratio | XX.XXx | XX.XXx | XX.XXx | XX.XXx |
| Cash flow ratio | XX.XXx | XX.XXx | XX.XXx | XX.XXx |
| Debt ratio | XX.XX% | XX.XX% | XX.XX% | XX.XX% |
| Interest coverage ratio | X.XXx | X.XXx | X.XXx | X.XXx |

**Ratio 定義：**
- Current ratio = Current Assets / Current Liabilities
- Quick ratio = (Current Assets − Inventory) / Current Liabilities  
  ⚠️ SEC XBRL 常缺 Inventory → 用 Current Assets / Current Liabilities 近似，標記 `(approx)`
- Cash flow ratio = TTM CFO / Current Liabilities
- Debt ratio = Total Liabilities / Total Assets（顯示為 %）
- Interest coverage ratio = LTM EBITDA / Interest Expense  
  ⚠️ Interest Expense 缺失時：顯示 `N/A`，在 commentary 說明

### Commentary block（4 bullets）

```
- Current/Quick ratio: [direction, level vs prior year, liquidity assessment]
- Cash flow ratio: [direction and driver]
- Debt ratio: [direction and driver — distinguish liability increase vs equity change]
- Interest coverage ratio: [direction; if negative or N/A, explain basis]
```

> ⚠️ **Special rule — non-cash impairment：**
> 若 interest coverage ratio 因非現金商譽減損而為負，Agent 必須補充：
> "Excluding the non-cash goodwill impairment, adjusted interest coverage remains healthy
> at [X.XXx] based on LTM EBITDA per Compliance Certificate."

---

## Section 5 — Leverage YOY

| Item | 12/31/FY{n-3} | 12/31/FY{n-2} | 12/31/FY{n-1} | 12/31/FY{n} |
|------|---------------|---------------|---------------|-------------|
| Total debt | | | | |
| Debt service | | | | |
| Interest expense | | | | |
| LTM EBITDA* | | | | |
| *From Compliance Certificate | | | | |
| Total leverage ratio | X.XXx | X.XXx | X.XXx | X.XXx |
| LTM EBITDA / Interest expense | X.XXx | X.XXx | X.XXx | X.XXx |
| Debt service coverage ratio | X.XXx | X.XXx | X.XXx | X.XXx |

**Leverage Calculation Definitions：**
- **Total debt** = Short-term loans + Current portion of LT debt + Long-term bank loans
- XBRL implementation：Short-Term Loans（含 Short-Term Notes Payable）+ Long-Term Liabilities Maturing Within One Year + Long-Term Liabilities。`DebtCurrent` 與 aggregate `LongTermDebt` 只能作 fallback，不得與其已包含的明細重複加總。
- **Debt service** = Interest expense + Scheduled principal payments (current year)
- **Total leverage ratio** = Total Debt / LTM EBITDA
- **LTM EBITDA / Interest** = LTM EBITDA / Interest Expense
- **Debt service coverage ratio** = LTM EBITDA / Debt Service
- **LTM EBITDA source priority：** ① Compliance Certificate Adjusted EBITDA → ② dbt `int_ttm_metrics` 計算值 → ③ Operating Income（標記 approx）

**Agent 規則：**
- 若使用 Compliance Certificate 數字，在 `*` 欄位說明來源
- 若 interest expense = null（SEC XBRL 缺失），相關比率顯示 `N/A`，在 commentary 說明替代指標（cfo_to_debt_ratio）

### Commentary block（5 bullets）

```
- LTM EBITDA: [direction and driver]
- Debt service: [direction and driver]
- Debt service coverage ratio: [direction and key driver]
- Total debt: [direction and driver]
- Total leverage ratio: [direction; compare to covenant threshold if applicable]
```

---

## Section 6 — Enterprise Value Analysis

One paragraph. Must include all four elements:

1. 公司性質說明（private / public）
2. 估值方法（industry benchmark EV/EBITDA multiple 或 market cap）
3. Implied EV 計算
4. Senior Secured Coverage Ratio = Implied EV / Senior Secured Debt

**Template（private company）：**

```
As a private company, [Company] does not have publicly traded equity, so its enterprise
value (EV) cannot be directly determined from market data. However, using the industry
benchmark multiple of [X.XXx], the borrower's implied EV is approximately $[X.X] billion.
The Senior Secured Coverage Ratio stands at [X.XXx], indicating [strong/adequate/weak]
asset coverage for the [facility type]. (Please refer to the attachment)
```

**Template（public company）：**

```
[Company] is publicly traded on [Exchange] under ticker [{TICKER}]. As of [date],
the market capitalization is approximately $[X.X] billion, implying an EV of $[X.X] billion
(inclusive of net debt of $[X.X] billion). This represents [X.XXx] EV/LTM EBITDA,
[in line with / at a premium to / at a discount to] the sector median of [X.XXx].
The Senior Secured Coverage Ratio stands at [X.XXx].
```

---

## Section 7 — Financial Covenants

| Requirement | Equation | Threshold | Actual | Pass/Fail |
|-------------|----------|-----------|--------|-----------|
| [Covenant name] | [Formula] | [≤ or ≥ X.XXx] | [X.XXx] | ✅ Pass / ❌ Fail |

若無財務維持條款：寫 `N/A — No financial maintenance covenants in credit agreement.`

**Agent 規則：**
- 必須說明 measurement date 及數字來源
- 常見 covenants：Consolidated Net Leverage Ratio、Interest Coverage Ratio、Fixed Charge Coverage Ratio
- Actual 值來自 `fct_covenant_status.actual_value`；若為 null 標記 `NO_DATA — see Appendix`

---

## Section 8 — Summary

Numbered list，最少 5 points，使用 bank-appropriate 語言，避免主觀評語。

```
1. No default or event of default has occurred. [OR: describe any default/waiver/amendment]
2. The credit risk is [acceptable/elevated/etc.]; the Branch concluded the Company
   is [capable/not capable] of servicing its debt obligations.
3. [Forward-looking: management's FY+1 revenue and EBITDA guidance, if available]
4. [Non-recurring item explanation — e.g., goodwill impairment, restructuring charge;
   required if any non-cash item distorted GAAP metrics in this period]
5. [Overall credit narrative: core operating performance, ratings agencies' view if public,
   branch monitoring commitment]
6. [Optional: strategic or operational update relevant to credit quality]
```

**Point-by-point rules：**
- Point 1：永遠先處理 covenant compliance / default status
- Point 2：永遠包含 branch credit conclusion
- Point 3：有 earnings release 就必須納入 forward guidance
- Point 4：有非現金或非經常性項目扭曲 GAAP 時必填
- Point 5：整體信用品質定性描述

---

## Appendix — Data Quality Notes

每份報告結尾必須附上此區塊（即使所有欄位都有數據）。

```
> ⚠️ Data Quality Notes
> 
> | Field | Status | Reason | Impact |
> |-------|--------|--------|--------|
> | interest_expense | NO_DATA | Not separately tagged in XBRL filing | Interest coverage ratio = N/A; replaced by CFO/Debt ratio |
> | D&A | NO_DATA | Reported in footnotes only | EBITDA = Operating Income (approx); overstated by D&A amount |
> | short_term_debt | APPROX | Using long_term_debt as proxy | Total debt may be understated |
> | inventory | NO_DATA | Not tagged | Quick ratio = Current ratio (approx) |
>
> All figures sourced from SEC EDGAR XBRL filings via data.sec.gov.
> Compliance Certificate figures, where used, sourced from [document name / date].
```

只列出實際缺失或近似的欄位；全部正常時寫：`All key fields available. No data quality issues noted.`

---

## 數值格式規則

| 數值類型 | 格式 | 範例 |
|----------|------|------|
| 金額（報表用，millions） | `1,234.5` | `48,234.5` |
| 金額摘要（B 級） | `$X.XB` | `$2.1B` |
| 金額摘要（M 級） | `$XXX.XM` | `$482.3M` |
| 比率（coverage/leverage） | `X.XXx` | `3.24x` |
| 百分比（margin / debt ratio） | `XX.XX%` | `21.43%` |
| 負數（報表行項目） | `(1,234.5)` | `(482.3)` |
| 缺失值 | `N/A` | — |
| 近似值 | `X.XXx (approx)` | `3.24x (approx)` |

---

## HTML Dashboard Layout（快速參考視圖，非正式交付）

```
┌─────────────────────────────────────────────────────┐
│ CREDIT FINANCIAL ANALYSIS    [Company ▼]  [Date ▼]  │
├─────────────────────────────────────────────────────┤
│  Net Sales  │ Gross Margin │ Op Margin │ Net Income  │
│  LTM EBITDA │ Tot Leverage │ Int Cover │    DSCR     │
├──────────────────────┬──────────────────────────────┤
│  Liquidity Ratios    │  Cash Flow Summary            │
│  (horizontal bar)    │  (horizontal bar waterfall)   │
├─────────────────────────────────────────────────────┤
│  Revenue & EBITDA Trend  (grouped bar, chronological)│
├─────────────────────────────────────────────────────┤
│  Covenant Status                                     │
│  covenant_name │ requirement │ actual │ headroom │ 🟢 │
└─────────────────────────────────────────────────────┘
```

> HTML dashboard 為輔助工具，**正式交付主管的是 Markdown/Word 格式的 credit memo**（Sections 1–8 + Appendix）。
