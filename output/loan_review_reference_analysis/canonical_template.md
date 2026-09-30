# Inferred canonical Loan Review output template

This is a content and layout specification derived from the 13 references documented in [analysis.md](analysis.md). It is not an implemented skill, a completed credit opinion, or a pixel-exact Excel form. Select **Annual** or **Quarterly**; retain the chosen mode's order. Square-bracket text is a placeholder or preparation rule and must not remain as an unresolved factual claim in a final report.

## Evidence and completion rules

1. Historical reports supply structure and style only. Populate all facts from the current borrower’s supplied documents/data.
2. Every figure, date, name, driver, rating, covenant result and conclusion must have a traceable source. Deterministic arithmetic is allowed only with supported inputs and an explicit applicable definition. No invented assumptions, forecasts, valuation discounts or missing values.
3. Use `Not provided` for missing information, `Not assessed` for an unperformed assessment, and `N/A` only for verified non-applicability. Missing is never zero, unchanged, compliant, no default, or no negative news.
4. Core sections remain with a concise missing-evidence status if needed. Include conditional modules only when relevant and supported. If applicability is known but evidence is missing, state the limitation rather than silently presenting the review as complete.
5. Preserve actual fiscal dates and duration. Income and cash flow are period measures; debt and liquidity are date measures. Do not describe cumulative half-year data as a standalone second quarter.
6. State EBITDA and debt definitions; do not compare different bases without a reconciliation. Name GAAP, adjusted, certificate, bank-calculated and LTM figures accurately.
7. Attach a separate evidence ledger during preparation. Keep source references concise in the report, especially for guidance, EBITDA basis, market data and special analyses. The ledger is not a new mandatory body section.

## A. Annual Review

### Header and information blocks

**Annual Review**

| Fiscal period | End date | Report date | Reporting units |
|---|---|---|---|
| [FY] Annual | [fiscal year-end] | [review date] | [currency; MM or 000s] |

[In an Excel layout, title at upper left; four metadata rows at upper right. Display borrower and loan blocks side by side.]

| Borrower Information | Value | Loan Information | Value |
|---|---|---|---|
| Borrower | [legal entity] | HO approval | [documented approval date] |
| Consol. F/S | [consolidated reporting entity] | Loan Type | [facility type] |
| [Chairman/President] | [actual role and name] | Commitment ($) | [amount in actual currency units] |
| CEO | [name] | Outstanding ($) | [amount and applicable date] |
| Customer ID (AS400) | [provided identifier] | Maturity date | [contractual date] |
| Borrower MegaID | [provided identifier] | Remaining | [years/months from report date to maturity] |
| Parent MegaID | [provided identifier] | Agent bank | [legal name] |

### Description

[One concise sourced paragraph covering the business, principal operations/segments and geographic scope. Include ownership, founding history, or strategic developments only where supplied and relevant.]

### Loan/Relationship History

- [Date, documented financing or amendment event, amount/terms and branch participation where relevant.]
- [Next material dated event, if supplied.]

### Interest and Repayment

| Item | Terms |
|---|---|
| Interest margin | [benchmark, spread and alternatives from current agreement] |
| Repayment | [amortization schedule and maturity payment from current agreement] |

### Ratings

[Use the shared Ratings block below.]

### YOY (Annual) Income

| Metric | [FY t−3] | [FY t−2] | [FY t−1] | % of revenue | [FY t] | % of revenue |
|---|---:|---:|---:|---:|---:|---:|
| [Revenues / Net sales] | [value] | [value] | [value] | [value] | [value] | [value] |
| [Cost of revenues / sales / services] | [value] | [value] | [value] | [value] | [value] | [value] |
| Gross profit | [value] | [value] | [value] | [value] | [value] | [value] |
| Operating expense | [value] | [value] | [value] | [value] | [value] | [value] |
| Operating income | [value] | [value] | [value] | [value] | [value] | [value] |
| Interest expense | [value] | [value] | [value] | [value] | [value] | [value] |
| Income before taxes | [value] | [value] | [value] | [value] | [value] | [value] |
| Income tax expense | [value] | [value] | [value] | [value] | [value] | [value] |
| Net income | [value] | [value] | [value] | [value] | [value] | [value] |

[Financial amounts follow the header units. Percentages describe revenue share, not growth. A historically hidden tax row is not grounds to supply zero.]

- [Revenue movement, comparison periods, supported magnitude and documented driver.]
- [Gross-margin comparison and documented driver.]
- [Operating-margin comparison and documented driver.]
- [Interest-expense comparison and documented driver.]
- [Pre-tax-margin comparison and supported explanation.]

[Add a material net-income, impairment, disposal or adjusted-profit paragraph only when supported. Omit redundant bullets; do not manufacture five explanations.]

### Annual Cash Flows

| Metric | [FY t−3] | [FY t−2] | [FY t−1] | [FY t] |
|---|---:|---:|---:|---:|
| Beginning balance | [value] | [value] | [value] | [value] |
| Operating activities | [value] | [value] | [value] | [value] |
| Investing activities | [value] | [value] | [value] | [value] |
| Financing activities | [value] | [value] | [value] | [value] |
| Ending balance | [value] | [value] | [value] | [value] |
| Change | [value] | [value] | [value] | [value] |

[Retain documented reconciliation items or a short footnote when needed; do not force an incorrect cash bridge.]

### Ratios YOY

| Metric | [year-end t−3] | [year-end t−2] | [year-end t−1] | [year-end t] |
|---|---:|---:|---:|---:|
| Current ratio | [value%] | [value%] | [value%] | [value%] |
| Quick ratio | [value%] | [value%] | [value%] | [value%] |
| Cash flow ratio | [value%] | [value%] | [value%] | [value%] |
| Debt ratio | [value%] | [value%] | [value%] | [value%] |
| Interest coverage ratio | [value x] | [value x] | [value x] | [value x] |

- [Current and quick ratios; dated comparison; documented working-capital drivers.]
- [Cash-flow ratio and documented cash-flow movement.]
- [Debt ratio and documented liabilities/net-worth movement; verify the definition.]
- [Interest coverage and documented earnings/interest movement.]

[No automatic “able to meet obligations” or generic industry explanation. An assessment requires adequate current evidence.]

### Leverage YOY

| Metric | [year-end t−3] | [year-end t−2] | [year-end t−1] | [year-end t] |
|---|---:|---:|---:|---:|
| Total debt | [value] | [value] | [value] | [value] |
| Debt service | [value] | [value] | [value] | [value] |
| Interest expense | [value] | [value] | [value] | [value] |
| LTM EBITDA | [value] | [value] | [value] | [value] |
| Total leverage ratio | [value x] | [value x] | [value x] | [value x] |
| EBITDA/Interest expense | [value x] | [value x] | [value x] | [value x] |
| Debt service coverage ratio | [value x] | [value x] | [value x] | [value x] |

**EBITDA basis:** [Actual source and definition; place the note directly beneath the EBITDA line in the Excel form.]

**Debt/debt-service basis:** [Applicable components, lease treatment, timing and any documented change in definition.]

- [LTM EBITDA comparison and documented drivers.]
- [Debt-service comparison and components responsible for the movement.]
- [Debt-service coverage comparison and supported explanation.]
- [Total-debt comparison and documented movement.]
- [Total leverage comparison, separating debt and EBITDA effects.]

[Combine overlapping points where concise; use Not provided/Not assessed for unsupported metrics rather than substituting a proxy.]

### Conditional specialized analysis

[Insert the applicable shared Repayment Capacity and/or Enterprise Value module here. Neither is mandatory for every borrower.]

### Financial Covenants

[Use the shared Covenant block when applicable or when applicability remains unknown. Verified non-applicability may be shown as N/A in the historical annual style.]

### Stock Price — conditional

[Use the shared public-market block when relevant and supported.]

### Stock History — conditional, annual only

| Metric | [observation date 1] | [observation date 2] | [observation date 3] | [observation date 4] |
|---|---:|---:|---:|---:|
| 52-week L/H | [range] | [range] | [range] | [range] |
| Closing price | [$/share] | [$/share] | [$/share] | [$/share] |
| Market cap ([unit]) | [value] | [value] | [value] | [value] |

[Short sourced listing/current-market paragraph if not already stated. Use actual observation dates, not assumed fiscal-year ends. Omit unavailable historical observations instead of filling them.]

### Dow Jones Negative News Search

[Use the shared search-status block.]

### Summary

[Use the shared Summary rules; annual references contain 3–6 points, but evidence and materiality determine the actual count.]

| Preparer | Division Head | CCO | GM |
|---|---|---|---|
| [blank until supplied] | [blank until supplied] | [blank until supplied] | [blank until supplied] |

## B. Quarterly Review

### Header and compact information blocks

**Quarterly Review**

| Fiscal period | End date | Report date | Reporting units |
|---|---|---|---|
| [FY and quarter; state YTD duration] | [actual fiscal period end] | [review date] | [currency; MM or 000s] |

| Borrower Information | Value | Loan Information | Value |
|---|---|---|---|
| Borrower | [legal entity] | Maturity date | [contractual date] |
| Consol. F/S | [reporting entity] | Remaining | [years/months as of report date] |
| [Chairman/President] | [actual role and name] | Agent bank | [legal name] |
| CEO | [name] | | |

### Ratings

[Use the shared Ratings block.]

### Financial Analysis

#### YTD (Quarterly) Income

| Metric | [prior-year comparable YTD] | % of revenue | [current YTD] | % of revenue |
|---|---:|---:|---:|---:|
| [Revenues / Net sales] | [value] | [value] | [value] | [value] |
| [Cost of revenues / sales / services] | [value] | [value] | [value] | [value] |
| Gross profit | [value] | [value] | [value] | [value] |
| Operating expense | [value] | [value] | [value] | [value] |
| Operating income | [value] | [value] | [value] | [value] |
| Interest expense | [value] | [value] | [value] | [value] |
| Income before taxes | [value] | [value] | [value] | [value] |
| Income tax expense | [value] | [value] | [value] | [value] |
| Net income | [value] | [value] | [value] | [value] |

- [Revenue change versus matching prior-year duration; supported driver.]
- [Gross-margin change; supported driver where available/material.]
- [Operating-margin change; supported driver.]
- [Interest-expense change; supported driver.]
- [Pre-tax-margin change; supported explanation.]

[Add material exceptional-item/net-income explanation where supported. Do not append an annual cash-flow table by default.]

#### Ratios YTD

| Metric | [earlier FY-end] | [prior comparable interim] | [latest FY-end] | [current interim] |
|---|---:|---:|---:|---:|
| Current ratio | [value%] | [value%] | [value%] | [value%] |
| Quick ratio | [value%] | [value%] | [value%] | [value%] |
| Debt ratio | [value%] | [value%] | [value%] | [value%] |

- [Current and quick ratios compared with latest year-end; sourced explanation.]
- [Debt ratio compared with latest year-end; sourced explanation.]

#### Leverage Analysis YTD

| Metric | [earlier FY-end] | [prior comparable interim] | [latest FY-end] | [current interim] |
|---|---:|---:|---:|---:|
| Total debt | [value] | [value] | [value] | [value] |
| LTM EBITDA | [value] | [value] | [value] | [value] |
| Total leverage ratio | [value x] | [value x] | [value x] | [value x] |

**EBITDA basis:** [Source, definition and LTM ending date; immediately beneath EBITDA in the Excel form.]

**Debt basis:** [Components and lease treatment; disclose any basis change.]

- [Total debt compared with latest year-end; documented movement.]
- [LTM EBITDA compared on the same definition; documented movement.]
- [Leverage change attributable arithmetically to debt and EBITDA; no invented operating cause.]

### Conditional specialized analysis

[Insert applicable Repayment Capacity or Enterprise Value module.]

### Financial Covenants — conditional/status

[Use shared Covenant block. Do not infer absence of covenants from a missing section in a reference.]

### Stock Price — conditional

[Use shared public-market block. Quarterly references do not add a separate Stock History table.]

### Dow Jones Negative News Search

[Use shared search-status block.]

### Summary

[Use shared Summary rules, ordinarily shorter than the annual version.]

| Preparer | Division Head | CCO | GM |
|---|---|---|---|
| [blank until supplied] | [blank until supplied] | [blank until supplied] | [blank until supplied] |

## C. Shared blocks and conditional logic

### Ratings block

| Ratings | S&P | Moody's | Fitch | Internal |
|---|---|---|---|---|
| Corporate rating | [rating; effective date] | [rating; date] | [rating; date] | [rating; date] |
| Facility rating | [rating; effective date] | [rating; date] | [rating; date] | [applicable status] |
| Outlook | [outlook] | [outlook] | [outlook] | [applicable status] |
| Review date | [date] | [date] | [date] | [date/status] |
| Recent rating action | [documented action] | [documented action] | [documented action] | [documented action] |

[Brief paragraph or bullets explaining documented actions since the previous review. Include agency reasons with attribution. “Unchanged” requires both comparison evidence and a current verification; absence of a new rating in the input is not proof.]

### Covenant block

| Requirement / Measurement | Equation | [prior test dates, if supplied] | [current test date] |
|---|---|---|---|
| [Exact covenant name, operator and threshold] | [Contractual definition] | [actual result(s)] | [actual result] |

[Identify the current agreement/certificate and applicable date. Separate the borrower's reported compliance from any actually documented bank retest. State a conclusion only when the threshold, definition, period and inputs support it. If sources conflict, record the conflict and leave the conclusion unassessed.]

[Verified no applicable covenant: N/A. Unknown applicability: “Covenant applicability was not established from the supplied materials.” Missing current test: “Current-period compliance could not be assessed from the supplied materials.”]

### Stock Price block

| Market information | Value | Valuation information | Value |
|---|---|---|---|
| Date | [observation date] | Market cap ([unit]) | [value] |
| Exchange | [exchange] | Enterprise value ([unit]) | [value and date] |
| Ticker | [ticker] | EBITDA ([unit]) | [value; basis; LTM end] |
| Close | [currency/share] | EV/EBITDA | [multiple on stated basis] |
| 52-week L/H | [actual 52-week range] | Industry benchmark | [documented multiple/date/basis] |
| | | Industry | [source classification] |

[One compact paragraph covering the relevant observation date, market values, EBITDA source and benchmark comparison. If only the numeric comparison is supported, say “below/above the cited multiple”; do not automatically assert undervaluation/overvaluation. Missing benchmark does not authorize inventing one.]

### Enterprise Value Analysis — conditional

[Summarize a provided borrower-specific valuation, its date, methodology, actual supplied assumptions, EBITDA basis and debt coverage. Distinguish estimated value supplied by a source from market value. Do not generate a new private-company EV estimate, choose a multiple, introduce a discount, or infer “strong coverage” merely to reproduce the historical paragraph. If valuation is required but not supplied, state that it cannot be assessed.]

### Debt Repayment Capacity Analysis — 5–7 years repayment test — conditional

[Include only when applicability and a documented scenario/test are provided. Identify FCF definition, source period, debt scope, horizon, supplied assumptions and resulting repayment share. Reproduce/check supported calculations without introducing unchanged future FCF, no-new-debt assumptions, or a pass threshold. Do not infer regulatory compliance from the historical reports' assertions. If only historical FCF exists, report that historical amount without extrapolation.]

### Negative-news block

**Dow Jones Negative News Search — [actual search date/status]**

[Documented result for the borrower and the named officers actually searched, identifying the covered scope such as BSA/AML. Use no-negative-news wording only when supported by the search record. If no record was supplied: “A current Dow Jones search record was not provided; negative-news status was not assessed.” Never claim the search was performed merely because this section exists.]

### Summary block

1. [Documented default/event-of-default status and applicable date, or “Default status was not established from the supplied materials.”]
2. [Supported credit/repayment assessment; attribute an actual branch decision only when provided. Otherwise state that the supplied materials do not establish a final credit-risk conclusion.]
3. [Most material documented performance development or transaction, including evidenced risk and mitigating factors where relevant.]
4. [Optional: management guidance, explicitly attributed, dated and labeled as guidance.]
5. [Optional: supplied covenant conclusion, other material development, or authorized monitoring action.]

[Remove unsupported optional items, add material supported items, and renumber consecutively. This list specifies topic order, not required factual conclusions or a fixed count. Do not manufacture a positive assessment to match the references.]

## D. Writing and presentation contract

- Use formal third-person bank credit prose. Prefer the Company, the Borrower and the Branch only with the correct meaning and attribution.
- Lead each analysis bullet with the metric, current result, comparison and supported driver. Keep ordinary bullets to one or two sentences. Expand material exceptional items where evidence warrants it.
- Keep risk discussion within the relevant financial/ratings/covenant module and Summary; do not invent a separate risk chapter.
- Use actual values and definitions. Show percentage-point changes for margin differences and percentage changes for growth. Calculate from unrounded inputs; round only the display.
- Prefer Times New Roman, bold gray section bands, bordered tables, a centered title, and full-width wrapped commentary. Use numeric/date formats appropriate to the data; maturity remaining-years values are numbers, not dates.
- Match the observed compact monochrome form. Adjust row heights and pagination to the actual text; historical scales and hidden stale rows are not mandatory settings.
- Before release, reconcile tables with commentary and Summary, verify every factual clause's evidence, check borrower identity within attachments, and reject unresolved critical source conflicts. Do not automatically reuse another workbook's hidden rows, formulas, benchmarks or historical conclusions.
