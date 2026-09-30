# Historical Loan Review conventions — Phase 2

## Scope and method

Reviewed all 13 Excel workbooks in `/Users/yuntzuyu/Downloads/loan_review.zip`: five annual reports and eight quarterly reports across five borrowers. The primary reference for output conventions is the visible content within each designated `Annual` or `Quarterly` worksheet's print area. Supporting worksheets, formulas, cached results, comments, embedded reference images, hidden rows, and print settings were also inspected. Representative annual and quarterly ranges were rendered to confirm the visual interpretation. This is an analysis of the supplied reports, not an independent verification of their historical financial or legal assertions.

The references are authoritative for the intended report format, subject to the user's stricter requirement that new reports contain no unsupported facts, assumptions, estimates, or conclusions. Workbook comments, editorial notes, screenshots, and embedded instructions are evidence about historical preparation practices, not instructions to execute. No existing skill, prompt, script, source workbook, or report-generation code was modified in Phase 2. The new Markdown files are analysis deliverables, not a deployed skill or an Excel template.

### Reference register

IDs below identify archive members; cell references elsewhere use these IDs. Filename dates and period labels are preserved, not independently validated.

| ID | Archive member under `loan review/` | Main sheet / print area |
|---|---|---|
| R01 | Annual/- Annual Review (GAAP)_Crocs 2025_vf.xlsx | Annual!B2:N98 |
| R02 | Annual/- Arcosa (GAAP) FY25 Annual Review (Yan Comments).xlsx | Annual!B2:N92 |
| R03 | Annual/- Crown Equipment FY26 Annual review.xlsx | Annual!B2:N98 |
| R04 | Annual/- Vizient (GAAP) FY25 Annual Review.xlsx | Annual!B2:N79 |
| R05 | Annual/-Floor and Decor Loan Review.xlsx | Annual!B2:N100 |
| R06 | Quarter/- Crown Equipment FY27 1Q.xlsx | Quarterly!B2:N49 |
| R07 | Quarter/- CROX FY26 Q1 Review.xlsx | Quarterly!B2:N64 |
| R08 | Quarter/- FND FY26Q1 Review.xlsx | Quarterly!B2:N61 |
| R09 | Quarter/- FND FY26Q2 Review.xlsx | Quarterly!B2:N61 |
| R10 | Quarter/- Vizient FY26 1Q.xlsx | Quarterly!B2:N55 |
| R11 | Quarter/- Vizient FY26 2Q.xlsx | Quarterly!B2:N55 |
| R12 | Quarter/~ Arcosa FY26 1Q.xlsx | Quarterly!B2:N57 |
| R13 | Quarter/~ Arcosa FY26 2Q (Yan Comments).xlsx | Quarterly!B2:N57 |

## 1. Inferred report architecture

There is one family of forms with **two distinct report modes**, not one universal section list. Both are compact bank credit-monitoring reports, built as bordered tables alternating with full-width commentary. Annual reviews add relationship context, cash flows, and debt-service analysis. Quarterly reviews concentrate on current developments and use a smaller financial package.

### Annual section order

| Order | Heading/content | Pattern and evidence |
|---|---|---|
| 1 | Annual Review; fiscal period, end date, report date, reporting units | All five, B2:N5 |
| 2 | Borrower Information / Loan Information | Side-by-side blocks, rows 6–13. R03 uses the company name as the left heading. |
| 3 | Description | One business-profile paragraph, B14:B15 in all five. |
| 4 | Loan/Relationship History | Dated financing, amendment, acquisition-financing, or branch-participation chronology, B16:B17. |
| 5 | Interest and Repayment | Interest margin and repayment schedule; around rows 18–21. |
| 6 | Ratings | S&P, Moody's, Fitch, Internal; corporate/facility ratings, outlook, review dates, recent action, followed by commentary. |
| 7 | YOY (Annual) Income | Nine standard financial lines; four fiscal years; common-size percentages for the latest two years; commentary immediately below. R01/R05 B30, R02/R04 B29, R03 B31. |
| 8 | Annual Cash Flows | Beginning cash, operating, investing, financing, ending cash, change; four years. R01/R05 B41, R02/R04 B40, R03 B42. |
| 9 | Ratios YOY | Current, quick, cash flow, debt, interest coverage; four year-end dates; narrative follows. |
| 10 | Leverage YOY / Leverage Analysis YOY | Debt, debt service, interest, LTM EBITDA, EBITDA basis, leverage and coverage ratios; four dates; narrative follows. |
| 11 | Specialized analysis, when applicable | Repayment-capacity test in R02 B65:B66; private-company Enterprise Value Analysis in R04 B65:B66. |
| 12 | Financial Covenants, when applicable/displayed | R01/R02/R04/R05 show a section with N/A; R03's covenant rows are hidden. |
| 13 | Stock Price; Stock History, for public borrowers with data | R01 B79:B91; R02 B73:B85; R05 B81:B93. R03's stock content is hidden; R04 has no public-stock block. |
| 14 | Dow Jones Negative News Search | Heading with search date; compact borrower/officer result paragraph. All five. |
| 15 | Summary | Numbered conclusions, 3–6 points in these annual reports. |
| 16 | Preparer / Division Head / CCO / GM | Approval/signature area, all five. |

An explicit `Financial Analysis` umbrella heading appears in R03, but is not consistently present in the other annual forms. Preserve the financial subsection order; do not require an additional heading solely for uniformity.

### Quarterly section order

| Order | Heading/content | Pattern and evidence |
|---|---|---|
| 1 | Quarterly Review; reporting metadata | All eight, B2:N5. |
| 2 | Borrower Information / Loan Information | Rows 6–10: borrower, consolidated entity, chairman/president and CEO; maturity, remaining term and agent. Annual IDs, commitment, relationship history and pricing blocks are absent. |
| 3 | Ratings and commentary | B11:B17 in all eight. |
| 4 | Financial Analysis | B18 in all eight. |
| 5 | YTD (Quarterly) Income / YTD Income | B19:N28, followed by B29 commentary. Prior comparable YTD and current YTD, each with common-size percentages. |
| 6 | Ratios YTD | Rows 30–34: current, quick, debt ratios, four balance-sheet dates and 2–3 narrative bullets. R06 omits the B30 label but retains the table. |
| 7 | Leverage Analysis YTD | Usually rows 35–40: total debt, LTM EBITDA, basis note, leverage ratio, then three explanatory bullets. R07 uses rows 35–43; extra debt-service/coverage rows are hidden. |
| 8 | Specialized analysis, when applicable | R10/R11 private EV, R12/R13 repayment-capacity analysis. |
| 9 | Financial Covenants, when applicable/displayed | Visible in R06, R08–R11; hidden in R07; absent from the R12/R13 report body even though their summaries assert compliance. |
| 10 | Stock Price, for public borrowers with data | R07–R09 and R12–R13. No separate quarterly Stock History table. |
| 11 | Dow Jones Negative News Search | All eight. |
| 12 | Summary | 3–5 substantive points in these reports; R07 has four points misnumbered 1, 2, 3, 5. |
| 13 | Preparer / Division Head / CCO / GM | All eight. |

There is no recurring stand-alone `Risk Analysis`, `Recommendation`, executive summary at the start, SWOT, dashboard, or traffic-light scorecard. Risk assessment is woven into ratings, metric commentary, covenant analysis, special modules and the final Summary. The conclusion is a monitoring/credit assessment, not automatically a request to approve new lending.

## 2. Tables, comparisons and financial definitions

### Income and cash-flow tables

The income rows are revenues/net sales, cost of revenues/sales/services, gross profit, operating expense, operating income, interest expense, income before taxes, income tax expense and net income. Labels vary with the business and source statement. R03 hides the income-tax row; this is a presentation exception, not permission to infer tax as zero.

Annual layout: `Metric | FY t−3 | FY t−2 | FY t−1 | % | FY t | %`. Quarterly layout: `Metric | prior comparable YTD | % | current YTD | %`. The percent columns are common-size shares of revenue, **not growth columns**. Growth calculations often sit outside the print area in column O, supporting narrative only.

Quarterly income is generally cumulative YTD: R09/R11 describe first-half results, while R13 labels six-month totals “Q2.” Infer the duration from the statement period and source data, not the Q2 filename. Use an unambiguous `FYxx 1H (six months ended …)` or equivalent when cumulative. Fiscal year ends vary: R03/R06 use March year-end; R05/R08/R09 use specific retail fiscal dates. Calendar-quarter defaults would distort the reference pattern.

Annual cash flows use four fiscal-year columns and no separate common-size columns. Commentary usually discusses operating cash flow inside the cash-flow-ratio bullet instead of adding another long narrative below the cash table. Preserve source reconciliation items where needed: beginning cash plus three activity totals does not always equal ending cash without FX or other reconciling movements.

### Ratios and leverage

Annual ratio tables show four consecutive fiscal year ends. Quarterly ratio/leverage tables show four dates in this sequence: **earlier fiscal year-end; prior-year comparable interim date; latest completed fiscal year-end; current interim date**. The narrative usually compares the current interim balance with the latest year-end, while income compares matching YTD durations.

Current, quick, cash-flow and debt ratios are printed as percentages; interest coverage and leverage/coverage metrics use `x`. Typical precision is two decimals. Current and quick ratios are usually discussed together. References often compare liquidity with 100%, explain inventory effects, then discuss liabilities and equity movements. These are observed analytical habits, not automatic conclusions that a ratio alone proves ability to repay.

The `E-Loan` sheet supplies financial statements and many precomputed ratios. Main-sheet formulas pull its rows 197–200 and 203; those ratios are frequently stored as text, not locally derived formulas. Cross-checking liabilities and net worth shows that **Debt ratio follows liabilities/net worth**, not liabilities/assets. A future implementation must explicitly name and verify the denominator. Quick-ratio and cash-flow-ratio definitions also require confirmation from the supplied financial spreading methodology; a label alone is insufficient.

Annual leverage tables contain total debt, debt service, interest expense, LTM EBITDA, total leverage, EBITDA/interest expense and debt-service coverage. Quarterly printed tables reduce this to total debt, LTM EBITDA and total leverage. The annual workbook calculations commonly use short-term borrowing + current maturities + interest for debt service; this is an observed workbook convention and must not be silently replaced by capital expenditure. It is also not necessarily an actual cash principal-payment schedule.

EBITDA is not uniform: certificate EBITDA in R01–R04 and R06/R08/R10/R11; financial-statement EBITDA in R05; bank calculation in R07; 10-K/10-Q in R09; earnings-presentation EBITDA in R12/R13. R02 Annual!L59 has a reviewer comment requesting certificate EBITDA. That indicates the importance of the basis for that report, not an instruction to invent or always prefer an unavailable certificate.

Debt definitions change too. R08 includes lease-related liabilities and shows leverage around 3.54x; R09 uses a much narrower long-term borrowing balance and shows approximately 0.37x. This cannot be described as economic deleveraging without reconciling the scope change. Every new report needs consistent entity, currency, dates, debt definition and EBITDA basis across comparisons, or an explicit non-comparability note.

## 3. Writing conventions

### Tone, syntax and detail

The dominant voice is formal, factual, third-person bank credit writing. The recurring nouns are “the Company,” “the Borrower” and “the Branch.” Financial commentary is compact and metric-led. Common sentence structure is:

> [Metric] increased/decreased to [current amount or ratio] in/as of [current period] from [prior amount or ratio] in/as of [prior period], primarily due to [documented driver].

Use “in/for” for income and cash-flow periods; “as of” for balance-sheet and market dates. Distinguish percent changes from percentage-point margin movements. Preserve GAAP, adjusted, consolidated and LTM qualifiers. Do not interchange “net interest expense” with gross interest expense.

Income commentary normally has five bullets, ordered revenue → gross margin → operating margin → interest expense → pre-tax margin. The pattern is flexible: R10 has four and omits a gross-margin bullet; R13 adds net income because a disposal causes an exceptional change; R01 uses six numbered paragraphs to explain impairment and adjusted results. Include material available analysis, not filler to meet a count.

Annual ratio commentary typically has four bullets and leverage commentary four or five. Quarterly ratios have two or three and leverage three. Most ordinary bullets are one sentence, sometimes extended with a second causal detail. Material impairments, acquisitions, disposals and outlook changes merit longer paragraphs. The Description is a single compact paragraph; relationship history is a short dated chronology. Long narrative is concentrated in exceptional items and Summary.

### Explaining financial movements

The reports move from result to comparison to cause: sales mix/volume/acquisitions for revenue; pricing, tariffs, freight or input costs for gross margin; SG&A, depreciation or impairment for operating margin; debt balance and interest rates for interest; then the combined pre-tax effect. Liquidity explanations reference current assets and liabilities; debt-ratio explanations reference liabilities and equity; leverage explanations distinguish debt changes from EBITDA changes.

For future reports, the arithmetic proves only the movement. A causal clause requires source support. If no driver is documented, retain the numerical comparison and say the supplied materials do not explain the movement, or omit the causal clause. Do not infer tariffs, inventory seasonality, management strategy, industry characteristics, or repayment causes merely because they appeared in a historical report.

### Positive and negative developments

The references often place deterioration and mitigating factors together: reported impairment losses alongside adjusted profitability and cash flow; weak markets alongside business diversification; increased interest alongside stronger operating results. R01 and R04 expand impairment explanations; R13 adds disposal-driven income. Preserve this balanced ordering only when both sides have evidence. A non-cash charge alone does not establish that core performance is stable or that there is no credit deterioration.

Risks are specific to the borrower and metric: profitability pressure, liquidity, leverage, maturities, tariffs, end-market demand, acquisition integration and covenant exposure. There is no standard catalogue that every report must contain. Unsupported positives must be excluded just as strictly as unsupported negatives.

### Conclusions

All 13 summaries open with a no-default assertion and a credit-risk assessment; most also state debt-servicing ability. Additional numbered points address actual performance, significant events, management guidance and sometimes a monitoring commitment. These are recurring **topics**, not reusable factual sentences. The generator cannot pronounce “no default,” “acceptable,” “in compliance,” or “the Branch concluded” without current evidence or an actual supplied credit decision.

Guidance is attributed to an earnings call, release or presentation and remains management's forecast, not the model's forecast. A recurring closing sentence about monitoring represents a branch action and should be included only when that action is provided or authorized. No fixed minimum of five Summary points is supported by the archive.

Spelling mistakes, inconsistent capitalization, duplicated words, numbering gaps and pasted cell references are accidental defects. Match the formal concise register while correcting them; do not imitate errors to achieve stylistic fidelity.

## 4. Formatting conventions

| Feature | Observed convention | Canonical implication |
|---|---|---|
| Medium | Excel form with merged cells and a defined B:N print block | Preserve tabular form when implemented in Excel; Markdown here specifies content rather than exact pagination. |
| Title | Centered, bold, Times New Roman 20 pt; large merged region at upper left | Use the Annual/Quarterly Review title, with metadata at upper right. |
| Body | Predominantly Times New Roman 14 pt in workbook coordinates; some 12 pt and Arial 16 pt cells | Use Times New Roman as the principal face. Mixed historical fonts are not a semantic rule. |
| Section headers | Bold, light gray fill, black borders | Repeat the restrained monochrome hierarchy; no decorative dashboard styling. |
| Tables | Bold row labels; centered date/period headers; bordered numeric cells | Keep financial periods aligned and distinguish amounts from common-size percentages. |
| Commentary | Wrapped, left-aligned, full-width merged cells below each table | Keep analysis next to the figures it interprets; expand row heights to prevent clipping. |
| Bullets | Hyphen-led lines for financial analysis; numbered Summary; occasional numbered exceptional-item analysis | One level of bullets; no invented deep outline. |
| Numbers | Comma-separated amounts, commonly rounded to whole reporting units; margins commonly two decimals; multiples two decimals plus x | Calculate before rounding; keep small material amounts precise enough to remain meaningful. |
| Units | MM or 000s in metadata; prose often uses $…MM/million; stock price in dollars/share | Specify and validate each block's units. Loan commitments may be actual dollars while financial tables use scaled units. |
| Dates | Metadata often m/d/yy; financial-date headers/prose often m/d/yyyy | Keep full and distinct statement, report, rating, search and market dates. |
| Sign-off | Four horizontally arranged roles at the end | Leave signatures/approvals empty until actually supplied. |
| Print | All 13 main sheets portrait; stored scales vary 45–63%; main sheet paperSize unset | No single historical scale, page count or paper size can be inferred. Check final pagination for the chosen output medium. |

Screenshots, rating extracts and EBITDA/cash-flow exhibits mainly support the workbook in other sheets or outside the print block. They do not establish a mandatory chart or image section in the report body. R07's visualization sheet contains older-period charts, illustrating why the workbook's full contents must not automatically become report content.

## 5. Fixed, conditional and borrower-specific classification

“Fixed” means a recurring structural slot, not guaranteed availability of its factual content.

| Class | Elements | Rule |
|---|---|---|
| A — Core in both modes | Title/metadata; borrower and loan information; ratings; income table + commentary; ratios + commentary; leverage + basis + commentary; negative-news section; Summary; sign-off roles | Preserve these slots. If evidence is missing, show a concise unavailable/not assessed status rather than a fabricated answer. |
| A — Annual-specific | Description; relationship history; interest/repayment; four-year income and cash flows; fuller ratio and coverage package | Preserve annual order and detail. Missing years remain unavailable; never fill historical columns from another borrower. |
| A — Quarterly-specific | Compact front matter; Financial Analysis heading; two-period YTD income; four-date balance/leverage comparisons | Use actual fiscal dates and duration. Do not append the entire annual package automatically. |
| B — Covenant content | Requirement, equation, dated tests and compliance conclusion | Applicable covenant and current evidence control inclusion. References inconsistently omit or show N/A. Unknown is not N/A. |
| B — Public market content | Stock Price and EV/EBITDA; annual Stock History | Public listing plus dated evidence required. Market benchmark and fair-value interpretation are separate evidentiary requirements. |
| B — Private-company valuation | Enterprise Value Analysis and secured coverage | Only when a relevant documented valuation is provided; do not choose a multiple, private-company discount or estimate. |
| B — Repayment test | 5–7-year capacity paragraph | Only when applicable and a documented scenario/methodology is supplied. Do not assume unchanged FCF or no new debt. |
| B — Material events | Impairment, adjusted-profit bridge, disposals, acquisitions, refinancing, outlook, monitoring action | Include only material, current, documented developments; vary length with complexity. |
| C — Never transfer | Names, officers, IDs, facility terms, dates, ratings, balances, financial figures, ratio values, benchmarks, forecasts, causes, risk assessments, covenant thresholds, compliance/default/search results and approvals | Obtain anew for the current borrower. Even familiar institutional-sounding sentences can contain borrower-specific assertions. |

## 6. Differences and inferred rules

| Difference | Evidence | Inferred rule / confidence |
|---|---|---|
| Annual versus quarterly scope | Five annual and eight quarterly main sheets | Two modes, high confidence. |
| Public versus private market sections | Public R01/R02/R05/R07–R09/R12/R13; private R03/R04/R06/R10/R11 | Public stock module conditional; private EV is optional, not universal. High confidence for observed pattern. |
| Repayment-capacity module | R02/R12/R13 only | Borrower/facility-specific analytical requirement, not general boilerplate. Applicability to another loan cannot be inferred from these reports alone. |
| EBITDA basis changes | R02 vs R12; R08 vs R09; explicit notes below EBITDA | Select and disclose the actual source/basis; reconcile changes. No universal source-priority hierarchy can be inferred. |
| Greater detail for unusual earnings | R01 impairment; R04 impairment; R13 disposal | Add an explanation where the event materially affects comparability. High confidence. |
| Shorter Q1 explanation | R10 omits gross-margin bullet, R11 includes it | Evidence/materiality-driven detail, not rigid bullet counts. Moderate confidence; omission could also be editorial. |
| Covenant display varies | R03/R07 hidden; R12/R13 absent; others N/A or tests | No universal all-visible rule established. Canonical proposal retains a status slot when applicability is unknown, suppressing only verified non-applicable detail. |
| Stock History appears only annually | Three public annual reports, no quarterly versions | Annual historical comparison; quarterly current snapshot. High confidence within this sample. |
| Labels and officer titles vary | Leverage YOY vs Leverage Analysis YOY; Chairman vs President | Normalize equivalent headings where useful; preserve actual officer role and source financial terminology. |

## 7. Reference defects that must not become template rules

These observations identify internal inconsistencies or stale artifacts, not independently adjudicated corrections to the underlying borrower facts.

| Reference | Observation | Required handling in future generation |
|---|---|---|
| R03 Annual!B67:N91 | Covenant and stock rows hidden; stock prose names CDW and Computer Services | Exclude hidden stale text from canonical structure and never transfer it to a borrower. |
| R08/R09 Quarterly!B46 | Hidden compliance paragraph refers to 2024 despite 2026 report periods | Hidden text is not current compliance evidence. |
| R02 `Ratings` embedded image | Image names Terex Corp., not the workbook borrower | Validate entity inside an exhibit, not just its filename or sheet location. |
| R06 `Stock` supporting sheet | Contains Arcosa market screenshots in a Crown workbook | Reject cross-borrower source contamination. |
| R02 Annual!B64 / I61 / L61 | Narrative says leverage is “up” from 3.82x to 2.46x | Generate direction from validated values, not copied prose. |
| R02 Annual!B80 | Stated EV 5,200 and EBITDA 619 imply about 8.40x; prose says 8.92x | Reconcile table, arithmetic and narrative before issuing a conclusion. |
| R05 Annual!B65 / I60 / L60 | EBITDA growth prose says 14.75%; underlying 512.5 to 538.1 is about 5.0% | Recompute growth from consistent source values. |
| R01 Annual!B40 / B95 | Operating analysis reports positive operating income; Summary calls it an operating loss | Require cross-section consistency. |
| R04 Annual!N5 / L30 | MM header, but displayed revenue 2,232,117 with #,##0 format and prose in millions | Resolve unit mismatch; number format does not secretly scale this value. |
| R06 Quarterly!N5 / B29 | Table unit 000s, but interest narrative labels 35,115 as MM | Convert units once and validate the prose against the table. |
| R08 vs R09 Quarterly!B36:L39 | Debt and EBITDA bases change sharply | Compare only like definitions or explicitly disclose non-comparability. |
| R09 Quarterly!B38 / B54 | EBITDA note says 10-K/10-Q; market commentary says certificate | Source labels must match the actual basis used. |
| R10 Quarterly!B45 vs Financial Covenant!B4:C4 | Main report states net leverage ≤5.25x; supporting test names first-lien net leverage ≤5.50x | Resolve covenant identity/threshold from current agreement and certificate. |
| R11 Financial Covenant!B1:D4 | Supporting test still dated first quarter although main report is second quarter | Do not assert a current-period bank retest from an old exhibit. |
| R04/R10/R11 EV calculation!C9:E12 | Calculation applies a 30% private-company discount; body references undiscounted industry multiple | Valuation assumptions must be explicit and documented; do not inherit this discount. |
| R12 Quarterly!B50 and stock screenshot | Text close 124.44; screenshot close 124.14 | Resolve source conflicts instead of picking a convenient number. |
| R13 Quarterly!B48/B50 and stock screenshot | Report's 52-week range reproduces screenshot daily low/high; screenshot separately labels 52-week values | Preserve field meaning during extraction. |
| R13 cash-flow screenshots and B42 | Supporting company FCF includes disposal proceeds; report defines FCF as CFO less capex | Reconcile FCF definitions before any repayment analysis. |
| R11 Quarterly!B52; R07!B61 | Stray `+B11:N52` in Summary; numbering skips a point | Remove editorial artifacts and number actual points consecutively. |

All summaries' no-default statements, news-search negatives, “acceptable” conclusions and covenant assertions require fresh evidence even when perfectly formatted. Absence of a negative item in the supplied files does not prove that a search or default check occurred.

## 8. Implications for a later implementation phase

The companion [canonical template](canonical_template.md) separates observed format from evidence requirements. A later implementation should introduce annual/quarterly selection, conditional modules, explicit financial definitions, fiscal-period metadata, and claim-level provenance. Financial statements alone cannot populate loan terms, internal ratings, agency actions, covenant retests, negative-news results or branch decisions.

Retain an evidence ledger alongside the final report: each amount and factual clause should map to current-borrower document/page/cell, relevant dates, units, entity, definition and any deterministic formula. This ledger is a proposed grounding control, not an observed additional report section. Arithmetic from supported inputs is permitted; choosing unsupplied assumptions or producing new estimates is not.

Validation should cover entity identity, period duration, units, financial definitions, arithmetic, table/prose consistency, causal support, source conflicts, actual search/test status, and removal of hidden/stale references. Preserve the historical style only after these checks pass. The user’s evidence requirement takes precedence when a historical convention would otherwise encourage unsupported reassuring language.
