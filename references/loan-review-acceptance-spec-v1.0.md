# Loan Review Modification and Acceptance Specification v1.0

- Date: 2026-10-06.
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

For percentage metrics below, multiply the formula result by 100 and display `%`. Do not multiply multiples or days by 100.

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
