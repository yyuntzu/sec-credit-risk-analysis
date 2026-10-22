# Loan Review Output and Data Contract — v1.0

This reference implements Block 1 of the
[acceptance specification](loan-review-acceptance-spec-v1.0.md).
The **new user format controls structure**; historical Loan Reviews control prose
style only. Latest approved formulas control calculations; current borrower sources
control facts. No historical workbook layout or example figure overrides these rules.

This is a boundary specification, not a replacement pipeline or a finished writer.
`scripts/loan_review_contract.py` is independent of the existing runner/writer.
Their integration and final-output validation belong to later blocks.

## Mode and layout

An explicit user choice selects `annual` or `quarterly`. Keep that choice independently
of data availability and pass it as `expected_mode` to validation. Never select mode
by checking whether a query returned quarterly rows. If unspecified, ask.

“Long” means the complete agreed analytical coverage, not extra sections or filler.
The report contains exactly one of the following structures (AUTH-01, FMT-01–07).
The names in angle brackets below describe period roles, not printable placeholders.
Actual headers use verified fiscal labels or dates. Missing facts retain their slots.

### Annual

```markdown
## A. Annual Review
### YOY (Annual) Income
### Annual Cash Flows
### Ratios YOY
### Leverage YOY
```

| Table | Columns, including Metric | Ordered metric keys |
|---|---|---|
| YOY (Annual) Income | Metric; FY t−3; FY t−2; FY t−1; % of revenue; FY t; % of revenue | revenue, cost_of_revenue, gross_profit, operating_expense, operating_income, interest_expense, pretax_profit, income_tax, net_income |
| Annual Cash Flows | Metric; FY t−3; FY t−2; FY t−1; FY t | beginning_cash, cfo, cfi, cff, ending_cash, cash_change |
| Ratios YOY | Metric; year-end t−3; year-end t−2; year-end t−1; year-end t | current_ratio, quick_ratio, cash_flow_ratio, debt_ratio, interest_coverage |
| Leverage YOY | Metric; year-end t−3; year-end t−2; year-end t−1; year-end t | total_debt, debt_service, interest_expense, ltm_ebitda, ebitda_basis, total_leverage, ebitda_interest, dscr |

Income has seven columns; other tables have five. The contract always retains the
EBITDA basis row. A later renderer may collapse identical, available annual basis
values to one full-width note immediately after the EBITDA row. This optional
presentation does not remove the per-period basis data.

### Quarterly

```markdown
## B. Quarterly Review
### Financial Analysis
#### YTD (Quarterly) Income
#### Ratios YTD
#### Leverage Analysis YTD
```

| Table | Columns, including Metric | Ordered metric keys |
|---|---|---|
| YTD (Quarterly) Income | Metric; prior comparable YTD; % of revenue; current YTD; % of revenue | Same nine income rows as Annual |
| Ratios YTD | Metric; earlier FY-end; prior comparable interim; latest FY-end; current interim | current_ratio, quick_ratio, debt_ratio |
| Leverage Analysis YTD | Metric; earlier FY-end; prior comparable interim; latest FY-end; current interim | total_debt, ltm_ebitda, ebitda_basis, total_leverage |

All tables have five columns. Retain each quarterly EBITDA basis cell. Do not append
Annual Cash Flows, debt service, interest coverage, or DSCR to Quarterly.

Do not add cover/Part headings, Summary, guidance progress, covenant tables, EV,
ratings, stock/news, signatures or a Data Quality Appendix. Necessary limitations
and definition notes belong beside the relevant table. A source passage is not
permission to add a new section.

## Metric requirements and presentation

`METRICS` in the executable contract supplies every row's label, normalized unit,
period kind, definition, rule ID, applicable formula/input order and unresolved
decisions. This table specifies the source requirements. Formula numbers refer to
section 4 of the acceptance specification; no alternate equations are authorized.

| Keys / display labels | Source and definition requirement | Temporal requirement | Unit / rule |
|---|---|---|---|
| revenue / Revenues or Net sales | Verified source revenue line; select the actual applicable label | Full FY or comparable YTD | money; FMT-A1/Q1 |
| cost_of_revenue / Cost of revenues, sales or services | Verified source cost line; do not print slash-separated alternatives | Same income period | money; FMT-A1/Q1 |
| gross_profit / Gross profit | Source value or verified complete revenue/cost identity | Same income period | money; CALC-14 |
| operating_expense / Operating expense | Verified expense excluding cost of revenue; no double counting | Same income period | money; CALC-14 |
| operating_income / Operating income | Source operating profit | Same income period | money |
| interest_expense / Interest expense | Verified gross/net interest mapping; DEC-05 | FY/YTD income; full FY in Annual Leverage | money |
| pretax_profit / Income before taxes | Source pre-tax profit or verified accounting identity | Same income period | money; CALC-14 |
| income_tax / Income tax expense | Source signed tax expense/benefit, no automatic absolute value | Same income period | money; CALC-14 |
| net_income / Net income | Source value with consolidation scope | Same income period | money |
| beginning_cash / Beginning balance | Source opening cash with verified cash definition | Instant immediately before FY start | money; CALC-15 |
| cfo, cfi, cff / Operating, Investing, Financing activities | Source signed cash flows, including outflows | Full FY | money |
| ending_cash / Ending balance | Source closing cash on same basis as opening | FY-end instant | money; CALC-15 |
| cash_change / Change | Ending minus beginning; verify full bridge incl. FX/restricted cash/other items | Full FY | money; CASH-CHANGE-v1 |
| current_ratio / Current ratio | Current Assets / Current Liabilities | Same balance date | percent; CF-01 |
| quick_ratio / Quick ratio | Quick Assets / Current Liabilities; eligible assets pending DEC-01 | Same balance date | percent; CF-02 |
| cash_flow_ratio / Cash flow ratio | Full-FY CFO / year-end Current Liabilities | Mixed duration/instant, same endpoint | percent; CF-03 |
| debt_ratio / Debt ratio | Total Liabilities / Net Worth; DEC-02 scope | Same balance date | percent; CF-06 |
| interest_coverage / Interest coverage ratio | (Pre-tax Profit + Interest Expense) / (Interest Expense + Capitalized Interest) | Same full FY for all inputs | multiple; CF-04, DEC-05 |
| total_debt / Total debt | Verified debt components and lease treatment; never total liabilities by default | Column balance date | money; DEC-02 |
| debt_service / Debt service | Complete approved definition pending; no CapEx or missing principal proxy | Full FY | money; CALC-10, DEC-03 |
| ltm_ebitda / LTM EBITDA | Verified EBITDA definition/source and complete applicable LTM; missing D&A is not zero | Full fiscal-year duration ending exactly at column date | money; CALC-11/12, DEC-06 |
| ebitda_basis / EBITDA basis | Actual source/definition/adjustments; must agree with the EBITDA fact | Same LTM | text; FMT-A4/Q3 |
| total_leverage / Total leverage ratio | Total debt / applicable LTM EBITDA; compatible scope and basis | Balance-date debt with LTM ending on that date | multiple; LEVERAGE-v1, DEC-02/06 |
| ebitda_interest / EBITDA / Interest expense | (Pre-tax Profit + Interest Expense + D&A) / (Interest Expense + Capitalized Interest); not arbitrary adjusted EBITDA | Same full FY for all inputs | multiple; CF-05, DEC-05 |
| dscr / Debt service coverage ratio | Complete approved numerator and denominator pending | Full FY | multiple; CALC-10, DEC-03 |
| Each income common-size cell | Row amount / revenue for the same period; even revenue/revenue requires a nonzero, available denominator | FY t−1 and FY t, or prior/current YTD | percent; COMMON-SIZE-v1 |

Money is normalized to an explicitly supplied report currency and scale. Numeric
values use finite `Decimal`, never bool, NaN, infinity or a coerced null. Percent
values are fractions (0.25 means 25%); multiples are unscaled and display `x`.
Source numeric value and source scale are retained independently. Display rounding
occurs later, never in the input facts or financial calculations. Currency conversion
is not implemented or implicitly authorized by this contract.

Narrative supporting metrics also have catalog definitions: `revenue_growth`
(CF-09, current/prior revenue), `gross_margin` (CF-10, gross profit/revenue),
`operating_margin` (CF-11, operating income/revenue), `pretax_margin` (CF-12,
pre-tax profit/revenue), and `operating_margin_change` (CF-16, current minus prior
margin). Growth/change retain both comparable period inputs. Percentage-point
changes are stored as differences of fractions (0.01 renders as 1 percentage point).
These facts support the narrative; they do not add rows to the prescribed tables.

Source-dependent revenue/cost labels must be verified at rendering against the
source evidence and fact definition; `MetricSpec.label` is the canonical label,
not proof that a borrower uses that label. File type, display precision, monetary
scale choice and negative-number formatting remain DEC-09, not new defaults.

## Period contract

`Period` records are provided independently of retrieved facts. Exactly four slots
are required in the documented order, even when a whole year has no financial data.

| Mode | Slot IDs | Required relationships |
|---|---|---|
| Annual | fy_t_minus_3, fy_t_minus_2, fy_t_minus_1, fy_t | Consecutive fiscal years; contiguous verified fiscal intervals |
| Quarterly | earlier_fy_end, prior_interim, latest_fy_end, current_interim | Prior/current comparable fiscal quarter; chronological endpoints; YTD starts immediately after the relevant prior FY-end |

Each slot records `role`, `label`, `fiscal_year`, `start`, `end`, `ltm_start`,
`evidence_ids`, optional `quarter`, and a missing-date `reason`. `start` is the actual
fiscal-year start, including in interim slots. No calendar-month-derived quarters.
Use Q1–Q3 for interim review; Q4/full-year behavior requires a separate specification.
Known calendar dates need evidence. Unknown dates stay `None` with a reason and
prevent dependent values from being marked available.

Facts retain their actual start/end, not just the column's date label. Instant facts
have no start. Opening cash uses the date before fiscal start. Income uses FY/YTD;
LTM uses the independent `ltm_start`. The same metric and end date do not establish
the same fact. Full fiscal-year intervals support 364/365/366/371 inclusive days
(52 weeks, calendar/leap year, 53 weeks); source calendar verification is still
required. Transition/short fiscal years need a separately approved extension.
LTM window length alone does not prove component completeness or non-overlap:
component construction and verification belong to Block 3.

## Narrative contract and placement

All ordinary analytical coverage follows its table as bullets. Coverage entries
are not bullet-count quotas: a renderer may combine related topics while preserving
order. Missing coverage retains a reason and must not be replaced by filler.

| Table | Ordered topic IDs | Evidence requirement / rule |
|---|---|---|
| Annual/Quarterly Income | revenue, gross_margin, operating_margin, interest_expense, pretax_margin | Both periods' figures for comparison; relevant source passage for each cause; NAR-01 |
| Annual Cash Flows | No mandatory long narrative | Applicable cash-definition/FX/reconciliation notes; NAR-02 |
| Annual Ratios | liquidity, cash_flow_ratio, debt_ratio, interest_coverage | Applicable dated ratios and source inputs; NAR-03 |
| Annual Leverage | ltm_ebitda, debt_service, dscr, total_debt, total_leverage | Compatible definitions, dates and basis; NAR-04 |
| Quarterly Ratios | liquidity, debt_ratio | Normally compare against latest FY-end; optional separate quick-ratio bullet within liquidity; NAR-05 |
| Quarterly Leverage | total_debt, ltm_ebitda, total_leverage | Normally compare against latest FY-end, consistent basis; NAR-06 |

`Narrative` records topic, status (`supported`, `missing`, `not_applicable`), text,
claim type, fact IDs, evidence IDs, period roles, reason and management attribution.
Supported comparisons require facts for both periods; causes/management explanations
require a passage; judgments require data and an applicable evaluation basis;
limitations require the reviewed-material scope. Unavailable analysis carries a
reason, not completed borrower prose. Confirmed inapplicability needs evidence.

Each table can carry nearby definition, missing-data, basis or reconciliation notes.
Income may also carry a supported, material exceptional-item note (NAR-07). These
notes do not authorize extra sections. Historical style: formal third person,
specific comparison first, normally one or two sentences per bullet; explain causes
only when supported, attribute management statements, use percentage points for
margin movements, and avoid unsupported credit-health thresholds (STYLE-01–10).

## Python boundary API and records

Import from `scripts.loan_review_contract` from the project root. Standard library
only; no BigQuery, SEC, Anthropic or network call occurs on import or validation.

- `report_layout(mode)` returns fixed `TableSpec` records for the requested mode.
  Each includes heading level, ordered column roles, ordered metric keys, narrative
  coverage and rule IDs. The first displayed column is always `Metric` (implicit
  in the contract); `pct:<role>` identifies common-size cells.
- `report_headings(mode)` returns the exact heading hierarchy.
- `empty_report(mode, entity=..., scope=..., currency=..., scale=Decimal(...),
  periods=..., evidence=...)` builds all required cells in explicit missing states.
  It neither fills values nor validates/approves the supplied calendar.
- `validate_report(report, expected_mode=requested_mode)` raises `ContractError`
  with rule/context at the first violation; returns `None` on structural success.

| Record | Required responsibility |
|---|---|
| Report | Explicit mode, entity/scope, currency/scale, four periods, exact headings and tables, fact/evidence registries, approved-decision evidence mapping |
| Table | Exact immutable TableSpec; ordered rows of fact IDs with fixed column count; ordered narrative coverage; nearby notes |
| Fact | Unique ID, metric, period role, instant/duration kind, status/value, unit, definition, start/end, entity/scope; source evidence IDs; original value/scale and currency for sourced amounts; formula ID/version and input IDs for calculations; missing reason; EBITDA basis |
| Evidence | ID, current entity/scope, source ID, version, document date, locator, kind, applicable period roles, original content/review scope; purpose must be borrower |
| Narrative | As described above; references facts/evidence rather than embedding untraceable support |

`Status` distinguishes `sourced`, `calculated`, `missing`, `not_applicable`,
`conflict`, `not_calculable`. Unavailable states require `value=None` and a reason;
zero is rejected in those states. Direct zero requires a source numeric zero.
Derived values require available input facts and acyclic lineage. Unresolved
conflicts retain at least two source/version references. Not-applicable requires
confirmation; not-extracted does not mean not-disclosed.

Supporting input facts may retain different actual intervals under the same target
period role (for example, standalone-quarter components of an LTM calculation).
They have separate IDs and are not deduplicated by end date. A table-bound fact must
match the exact requested interval; known formulas also check their input intervals.
LTM component aggregation remains Block 3. Source-reported ratios must declare the
approved metric definition, even when they are not calculated locally.

Available values that depend on unresolved definitions require the corresponding
`DEC-*` entry, pointing to definition evidence recording explicit approval. Presence
of that record is a structural check, not proof the user approved its contents.
Unapproved definitions stay unavailable. Do not invent a DEC-03 rule just to fill
Annual debt service/DSCR. DEC-08 missing display and delivery rules remain pending;
internal status identifiers are not approved final display text.

## Validation scope and acceptance mapping

Run from the project root:

```bash
python3 -m unittest discover -s tests -p 'test_loan_review_*.py' -v
```

| Rules / cases | Block 1 check | Later acceptance still required |
|---|---|---|
| FMT-01–03; AT-01–05 | Explicit mode, exact layout, every slot retained, actual date roles, comparable YTD vs FY/LTM | Runner preserves mode and extracts correct facts; rendered layout matches |
| FMT-05–07; AT-01/02/20 | Units, exact row/column binding, hierarchy, no extra sections/topics | Visual formatting, source-specific labels, placeholder-free output, permitted shared basis note |
| DATA-01/03; MISS-01–07; AT-06/08/19/22 | Distinct unavailable states; no null-to-zero, source identity/version/locator, current entity/scope, conflict and inapplicability records | Authenticity, approved version policy, completeness of extraction |
| CALC-02/03; AT-07–14/21 | Formula/input IDs and units, date compatibility, explicit unresolved definitions, basis and cycle checks | Arithmetic, denominator handling, sign rules, cash bridge, LTM components, dbt/SQL/Python parity |
| NAR/EVD; AT-15–18/23 | Required topic slots, fact/evidence references, claim type and attribution metadata | Semantic support, genuine comparability/materiality, no invented cause, historical writing quality |

A valid empty/missing-state report is an intentionally representable **incomplete
payload**, not a completed credit assessment. This validator does not recalculate
financial formulas, authenticate source text, detect every unsupported meaning in
prose, or authorize final delivery. Numeric golden tests belong to Block 3; prose
checks to Block 4; writer checks to Block 5; end-to-end acceptance to Block 6.
Passing this block must not be reported as passing those later gates (OBJ-02,
CHANGE-04/05). Existing runtime outputs remain legacy until connected and tested.
