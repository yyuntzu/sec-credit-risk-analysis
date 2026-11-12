# Total Debt: as-reported adoption and disjoint components

User-authorized policy, 2026-11-07. Version: `as-reported-debt-2026-11-07`.
Applies to formal Annual and Quarterly Loan Review. The existing setup configuration
and legacy dbt KPI calculations are unchanged.

## Definition and priority

Total Debt is borrowing amounts at the report endpoint, as disclosed. Prefer an
explicit total from a mapped debt concept, verified current-borrower supplement
(e.g. a Debt Note total), or an exact supported workbook label. Definition prose
need not equal the contract's description word-for-word. A liabilities subtotal
is not a borrowing total.

When no explicit total is available, use one of these disjoint routes:

1. All current debt + noncurrent long-term debt.
2. Short-term borrowings excluding long-term current maturities + the long-term
   borrowing aggregate including those maturities.

If all current debt is absent, it can be calculated as short-term borrowings +
current maturities of long-term debt, but both parts must be explicitly available.
The current maturities are never added again to a long-term aggregate that already
includes them. Alternative complete routes must agree; otherwise Total Debt stays
not calculable. An explicit reported total has priority over component estimates;
all component observations remain in the source/report audit data.

The source categories and allowed input pairs live in `scripts/debt_policy.py`.
Only documented borrowing concepts enter those categories. Finance-lease-inclusive
borrowing lines are accepted with their disclosed scope, without adding a second
lease amount. Operating lease liabilities and trade payables remain excluded as
standalone components. `ShortTermBorrowings` and `ShortTermNotesPayable` are
alternative source candidates, never automatically added together because their
coverage may overlap. Different candidate amounts remain conflicts.

## Amount basis and unavailable inputs

Use reported carrying amounts by default without reconstructing gross principal
or issuing-cost adjustments. Explicitly identified principal amounts are retained
and labelled as principal; principal and carrying values cannot be mixed within
a calculated subtotal/total. The source basis, original value/scale, definition,
version and locator stay available in the Report and shared outputs.

Preserve company/scope, exact instant date, currency, scale, as-of and amendment
checks. Missing rows are not zero; explicitly sourced zero is usable. Negative
borrowing amounts retain their source and a clarification state. A rejected or
conflicting reported total cannot be bypassed with an automatic component sum.
Other source/definition checks (including Net Worth and EBITDA) remain in place.
The workbook adapter accepts only exact optional `Total Debt`, `Short-term Debt`
and `Long-term Debt` labels; broad `Long Term Liabilities` is not inferred to be debt.

## Calculation and delivery

`TOTAL-DEBT-v1` adds one approved pair. `CURRENT-DEBT-v1` adds short-term
borrowings and current maturities. Calculated facts retain formula version and
input IDs and are independently recomputed by the final arithmetic validator.
Excel uses the same addition chain and checks recalculated values against Report.
Markdown/HTML show the borrowing basis next to the leverage table; Excel Sources
retains it beside each amount. JSON/BigQuery retain the same Fact fields and
additional supporting facts, so no warehouse schema migration is required.

`Debt ratio` remains **Total Liabilities / Net Worth**. `Total leverage` remains
**Total Debt / applicable LTM EBITDA**. A valid Total Debt value alone does not
establish covenant compliance or final financial acceptance.

New source bundles include the supporting borrowing slots. Regenerate source
inputs to apply these mappings to historical data; reusing an immutable older
cloud source-run bundle does not retroactively add missing slots. Existing saved
reports must be rerun to gain the new calculation. No live SEC/provider/cloud calls
are needed by the regression tests.
