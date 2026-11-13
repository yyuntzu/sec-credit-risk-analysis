# Integration validation — 2026-10-27

Base: `codex/new-feature` / `48f88d0`.
Working branch: `codex/loan-review-integration`.

## Completed checks

- `REVIEW_EXCEL_TEST=1 venv/bin/python -m unittest discover -s tests`:
  **179 tests passed**, including real bundled-runtime annual and quarterly
  Excel generation, formula recalculation, missing/zero propagation, canonical
  value verification and saved XLSX formula/sheet checks.
- Annual workbook: 174 formal facts verified, 130 output bindings.
- Quarterly workbook: 112 formal facts verified, 64 output bindings.
- Workbook previews reviewed for report/source sheets and leverage tables;
  report and detail widths are independent and text rows wrap.
- Actual CLI and shell offline round trips passed with draft exit code 2.
- HTTP single/batch formal routes, invalid requests and explicit draft status passed.
- Cloud tests verified run-scoped reads, exact source round-trip, idempotent job
  IDs, source reuse, canonical publication and explicit failure handling using mocks.
- Relocated virtualenv dbt-script invocation verified using the active interpreter.
- Actual `dbt parse` passed with BigQuery adapter; 6 formal models and their
  schema/integrity tests are present in the parsed manifest.
- `bash -n scripts/run_analysis.sh`, Node syntax check and `git diff --check` passed.

## Verification boundaries

No live SEC fetch, BigQuery writes/queries, dbt warehouse execution, or Anthropic
calls were performed. Cloud permissions, warehouse SQL execution/cost and remote
deployment artifact delivery remain environment-dependent. Excel was recalculated
with artifact-tool, not native Microsoft Excel.

Workbook export checks use the repository's previously extracted Nexstar golden
fixtures, not a new independent verification of SEC disclosures. Those source
limitations remain visible in report acceptance and the generated draft artifacts.
Passing software tests does not imply a borrower's report passed substantive
acceptance, completed cash reconciliation, or approved CFADS/debt-service definitions.
