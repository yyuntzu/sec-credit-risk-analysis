# Loan Review commentary — display policy and ratio attribution (2026-11-05)

## PM-approved behavior

- Display the model's analysis/summary with reference text from the financial filing.
- The current-period MD&A alone may explain a comparison with the prior period.
  Two separate filings or quotes covering both periods are not required.
- Do not perform commentary semantic validation, numerical-token matching, exact
  model fact-ID matching, or require an independent/manual source review.
- Commentary absence or provider failure must not prevent numeric report delivery
  or change otherwise valid financial acceptance/publication.
- Page-number and paragraph-location enhancements are deferred. Existing source
  URLs and MD&A character locators are retained; new sections use their own section character locators.

## Financial validation remains strict

Canonical financial values, formulas, fiscal-period comparability, missing numeric
inputs, source fact provenance, reconciliations, and mandatory financial dbt tests
remain validated. Commentary cannot modify the Report facts. Model-returned fact
IDs are not adopted as financial lineage; the application supplies canonical IDs.

`final_report_accepted` and publication gates depend on financial validation and
requested deliverable success. `commentary_complete` and `incomplete_commentary`
are informational. `commentary_required_for_acceptance` is false. A financially
accepted report can have an incomplete or failed commentary stage.

## Sources and display

Basic document identity, CIK, scope, fiscal context and publication cutoff are kept
so references identify the intended borrower/filing. These are source-routing
checks, not certification that the model's explanation is correct.

Live SEC commentary retrieves the current requested fiscal endpoint, plus an optional
prior comparison filing when it is listed. Missing older filings do not prevent current-period analysis. A bounded MD&A section can end at
an explicit next item or at the document end; it need not have both markers.

The model summary is shown as **模型分析**, without a pending-review label. Its
reference quote is displayed beneath it in Markdown, Dashboard and Excel, and
retained in JSON and BigQuery. No automatic semantic review is performed.

If a model reference is paraphrased, absent, or cannot be located verbatim, keep
its summary and show an actual excerpt from the identified source document instead.
Label that fallback explicitly as a reference excerpt rather than presenting the
model's invented/paraphrased words as original source text. The existing locator
format is unchanged. If no corresponding source text is available, show
**分析尚未取得** while preserving numeric tables.

Original quote display is limited to 1,000 characters per reference to fit workbook
cells. Longer model summaries are displayed across the existing wrapped Excel rows.
No content-level validation is added to the displayed summary.

## Inputs and modes

Use `--commentary PATH.json` or the Python/HTTP `commentary` object. An offline
snapshot can also carry a `commentary` object. Each bundle contains `documents`
and optional `claims`. Existing field schemas and offline examples remain usable;
legacy `review` fields are no longer required and are not used to approve analysis.

| Mode | Behavior |
| --- | --- |
| `auto` | SEC sources fetch current MD&A and call the configured model. Snapshot/BQ/workbook sources do not implicitly make network calls; supplied claims are displayed. |
| `model` | Generate summaries using supplied documents, or retrieve current documents for a SEC run. |
| `reviewed` | Compatibility name for displaying supplied documents/claims offline; no review record is required. |
| `off` | Skip generation. Missing commentary does not block financial acceptance. |

Model configuration uses `FORMAL_COMMENTARY_MODEL`, then `ANTHROPIC_MODEL`, then
its existing configured default. Provider credentials/model availability must be
configured for live generation. No live provider calls were made in local testing.

A document carries `id`, `entity`, `cik`, `scope`, `source_id`, `version`,
`document_date`, `source_url`, `section`, `periods`, and `text`. Sections are
`MD&A`, `Balance Sheet`, `Debt Note`, or `Equity Note`. Optional `filing_type`
retains amendment identity. A Balance Sheet may additionally contain bounded
`observations` with `tag`, `value`, `unit`, `scale`, `end`, and `locator`. A claim carries
`table`, `topic`, `explanation`, optional `citations` (`document_id`, `quote`), and
optional status/reason/attribution. Available canonical facts and the report context
are attached by the application, independently of the model's metadata.

## Artifacts and failures

- `report.json`: canonical numeric report and its displayed narratives.
- `commentary.json`: shared visible summaries, source excerpts, and availability.
- `commentary_inputs.json`: source documents and model/curated claims, saved before
  model invocation as well so provider failures retain the inputs.
- `ratio_commentary_analysis.json`: deterministic ratio, component-change,
  selected-line reconciliation, source-total comparison and provenance context.
- `commentary_validation.json`: generation diagnostics, missing topics, or warning.
- `run_manifest.json`: commentary failure under `warnings`, not execution `errors`.

A failed model call writes **分析尚未取得** into all affected output formats and
retains the numeric report. Financial failures and actual requested output failures
still produce execution/delivery errors. File hashes and cross-format consistency
checks remain technical integrity checks, not semantic validation of commentary.

The BigQuery commentary view still exposes the same display content and references.
Legacy `reviewed` metadata is informational; mandatory dbt financial integrity tests
no longer require reviewed commentary or semantic commentary completeness.

## Offline example and tests

```bash
venv/bin/python scripts/agent_runner.py SYNTHETIC-ONLY \
  --request examples/synthetic_review_request.json \
  --source-snapshot examples/synthetic_commentary_snapshot.json \
  --commentary examples/synthetic_commentary.json \
  --commentary-mode reviewed \
  --output-dir /tmp/loan-review-commentary-display-new

REVIEW_EXCEL_TEST=1 venv/bin/python -m unittest discover -s tests
```

The example is synthetic and remains a draft because financial inputs/definitions
are incomplete, not because commentary lacks manual review. Tests cover current-only
MD&A, display without review, paraphrase/reference fallback, unchanged canonical
facts despite commentary numbers, incomplete ratio inputs with visible commentary,
financially accepted publication despite a model failure, and all output formats.

Live SEC, Anthropic, BigQuery, deployed HTTP, and native Microsoft Excel are not
verified by offline tests. Actual bundled artifact-tool XLSX export is exercised.

Local verification on 2026-10-31: **232 tests passed, no failures or skips**,
including actual bundled Excel export, offline dbt parsing, current-period-only
commentary, and accepted financial delivery despite model failure. The synthetic
CLI round trip displayed one current MD&A reference with no review record and
confirmed that every canonical financial fact was unchanged.


## Balance-sheet ratio attribution (2026-11-05)

Quarterly compares `latest_fy_end` to `current_interim`; Annual compares
`fy_t_minus_1` to `fy_t`. Both use the same `ratio_commentary_analysis` engine.
The liquidity paragraph compares current and quick ratios independently and
retains a missing quick ratio without discarding an available current comparison.

The source collector retains the current filing's Balance Sheet and bounded,
numbered Debt/Equity Notes alongside MD&A. It optionally retrieves the prior
comparison filing; current-only documents remain valid. Inline XBRL observations
must come from the selected Balance Sheet table, an exact requested instant,
matching CIK, a non-dimensional context and a simple currency unit. Original
value/scale/context locators are preserved. Unsupported transforms and unclassified
company tags stay as source text rather than guessed numeric input. Plain tables
remain readable even without inline observations. Unknown section layouts, missing
older filings and oversized sections can leave source gaps; provide an explicit
section snapshot when automatic extraction cannot identify a bounded body.

`loan_review_sources.balance_sheet_observations` also exposes eligible instant
observations already retained in the validated source bundle. Common payable,
prepaid, tax, lease, investment and equity tags are ingested into the same raw
ledger; no additional financial Fact definitions or BigQuery raw schema are needed.
The report's approved quick-assets/net-worth definitions remain authoritative.
Commentary does not infer quick assets or change the report's ratio formulas.

The deterministic pack contains canonical numerator/denominator changes and
growth, independent ratio movements, exact endpoint dates, individually ranked
component changes, source versions/locators and explicit partial/conflict states.
Source totals are compared with canonical totals. Only identified current-group
lines enter selected-line reconciliations; potential overlapping prepaid/other
subtotals are excluded from sums. A zero residual confirms the selected amounts,
not the semantic completeness of the chart of accounts. Missing items are not zero.

The model follows: ratio movement -> material balance-sheet composition ->
source-supported transaction/event explanation. Numerical composition can explain
an accounting driver without an explicit causal MD&A sentence. Procurement,
collection timing, refinancing and other business causes require filing evidence.
For debt ratio, analyze both Total Liabilities and Net Worth. Read new financing,
repayment and issuance costs together; gross proceeds do not establish net debt
growth. Keep principal separate from carrying amounts. Strong-liquidity or
compliance judgments need additional supporting evidence.

`ratio_commentary_analysis.json` is an audit input, not a second numeric report.
Model text still follows the display policy above: no manual-review gate or new
semantic validator. Missing commentary does not block financial acceptance. The
same canonical narratives and section references flow to Markdown, HTML, Excel and
`raw_review_results`/the existing BigQuery commentary view. No dbt schema change
or cloud deployment is required for the expanded text and passage locators.
