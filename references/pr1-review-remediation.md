# PR #1 review remediation — 2026-10-30

Branch: `codex/loan-review-integration`. Base: `origin/master`.
No merge or deployment is part of this change.

## Findings and changes

1. **High: incomparable YTD periods.** The contract checks actual durations
   against the declared fiscal quarter, permits month-end and 52/53-week
   calendars, and limits comparative duration differences to one week. A 91-day
   versus 273-day request is rejected before source retrieval or growth calculation.
2. **High: reconciliation PASS bypass.** Acceptance independently recomputes
   reviewed equations using canonical monetary facts. Source lineage, period,
   currency, component identity, signed amounts, and source-precision tolerance
   must agree. Generic fact/review evidence and contradictory reported PASS
   values cannot satisfy acceptance.
3. **High: covenant compatibility.** Existing legacy SQL KPI definitions are
   restored rather than replaced with unconditional NULLs. A complete legacy
   TTM requires four contiguous quarters spanning a full fiscal year. Covenant
   evaluations remain present when TTM is incomplete; duration-based covenants
   have `NO_DATA`, while an available point-in-time current ratio is evaluated.
   Unavailable evaluations do not display calculated headroom.
4. **High: non-blocking dbt tests.** Formal not-null and integrity tests use
   severity `error`; cloud dbt invocation also promotes warnings to errors.
   Unaccepted reports and failed deliverables cannot enter result publication.
   The cloud boundary independently verifies acceptance, and the acceptance
   view requires a successfully published, accepted run manifest before exposing
   `final_report_accepted=true`.
5. **Medium: HTTP compatibility.** Unversioned legacy batch, single-company,
   and HTML GET request shapes remain supported. They use existing warehouse
   mart definitions and are explicitly not formal acceptance. `/v2/run` and
   `/v2/analyze/<ticker>` require formal request envelopes. Existing unversioned
   formal envelopes remain supported too.
6. **Medium: restatement policy.** The latest explicit SEC amendment available
   by `as_of` supersedes earlier observations of the same concept and exact
   interval. Candidate and superseded IDs remain auditable. Ambiguous versions,
   non-amended disagreements, different concepts, and conflicting supplements
   remain conflicts; filing recency alone is not enough.
7. **Medium: stale validation artifacts.** Generated artifacts are removed from
   the PR tree. Newly generated validation receipts bind exact JSON and Markdown
   bytes with SHA-256 and identify the validator version. Saved-artifact checking
   independently validates arithmetic and rendered values; Excel export rejects
   stale receipts. The negative-tax regression regenerates parentheses and
   rejects a report tampered back to the old signed formatting.
8. **Low: local dependency symlinks.** All seven tracked local `node_modules`
   symlinks and the other generated outputs are removed from Git tracking.
   `outputs/` and `node_modules/` are ignored. Local artifact copies are preserved;
   existing commit history is not rewritten or purged.

## Reviewed reconciliation contract

Checks use `kind`, `period_role`, `terms`, `reported_fact_id`, `currency`,
`scale`, `tolerance`, `evidence_ids`, `status`, `calculated_value`,
`reported_value`, and `difference`.

Each term is `{"fact_id": "…", "coefficient": 1}`. Source values themselves
carry their actual signs; duplicate terms or negative coefficients are rejected.
The supported complete equations, in component order, are:

- `cash_bridge`: beginning cash + CFO + CFI + CFF + cash FX + other cash
  adjustments = ending cash. Explicit reviewed zero FX/other values are required
  when applicable; missing values never become zero. An available canonical cash
  change must also agree with ending minus beginning cash.
- `balance_sheet_equation`: total liabilities + approved consolidated net worth
  = total assets. A different equity/NCI definition requires a different explicit
  review rather than silently changing the equation.

The check must cite the canonical facts' source lineage. A review/definition
Evidence record must contain JSON binding exactly `kind`, `period_role`, `terms`,
`reported_fact_id`, `currency`, `scale`, and `tolerance`. This records the human
review of a complete same-basis bridge; arithmetic is still recomputed in code.
Source authenticity and semantic completeness remain human responsibilities.

Tolerance must be nonnegative and cannot exceed the sum of half-units of original
source precision, converted to report units. It is never derived from display
rounding. `matched` and `within_precision` are recomputed, not trusted from callers.
Unverified or failed checks remain acceptance blockers. Reconciliation approval
does not override any missing required facts, definitions, narratives, or limitations.

## Local verification executed

```bash
REVIEW_EXCEL_TEST=1 venv/bin/python -m unittest discover -s tests
```

**207 tests passed; no failures, errors, or skips**, including 28 new regression
tests in `tests/test_pr_review_regressions.py`. Existing assertions were updated
only where the intended amended-source, blocked-publication, versioned-HTTP, or
dbt-warning behavior changed.

Coverage includes real annual/quarterly bundled Node Excel exports, recalculation,
saved XLSX checks, independently reviewed reconciliation positives and negatives,
source amendment/as-of boundaries, actual covenant SQL execution against SQLite
after BigQuery-dialect translation, legacy EBITDA SQL execution, HTTP dispatch,
cloud failure handling with mocks, and offline dbt parsing with manifest severity
assertions. Formal source extraction and financial tests use synthetic inputs or
the existing extracted Nexstar workbook fixtures.

## Remaining validation limits

- No live SEC retrieval, BigQuery loads/queries, warehouse dbt execution,
  deployed HTTP request, GCS access, or Anthropic call was made.
- Excel was exercised with the bundled artifact-tool engine, not native Microsoft
  Excel. Formula behavior in native Excel remains unverified.
- Legacy marts deliberately preserve historical estimates and display labels for
  compatibility. They are not the formal calculation contract, cannot establish
  approved metric semantics, and are never adopted as formally accepted facts.
  The compatibility HTTP path requires working marts and has no raw-SUM fallback.
- Explicit amendment selection handles provable same-concept amendments only;
  ambiguous restatement/reclassification cases still require review.
- DEC-03 remains deliberately unresolved, and default sources without reviewed
  complete bridges remain drafts. This is a substantive acceptance blocker, not
  a software-test failure. Such drafts cannot claim successful cloud publication.
- The fixes have local regression verification. Live integration validation and
  reviewer approval are still required before claiming deployment readiness.
