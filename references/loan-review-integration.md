# Formal Loan Review integration

The default CLI, shell and versioned `/v2` HTTP entrypoints use `review_workflow.run_review()`.
Unversioned HTTP routes also retain the historical request shapes described below.
Financial results are calculated once by the existing formal contract. Dashboard,
Excel and BigQuery publication consume that same report; dbt does not recalculate
financial ratios or infer missing facts. The old `analyze_ticker()` function remains
a low-level compatibility API. Use `run_review()` for new Python integrations.

## Run locally

From the repository root, using Python with the project dependencies installed:

```bash
venv/bin/python scripts/agent_runner.py AMZN --request /path/to/request.json \
  --output-dir /tmp/amzn-review-new

# Fully offline, reproducible synthetic example (not borrower financial data):
venv/bin/python scripts/agent_runner.py SYNTHETIC-ONLY \
  --request examples/synthetic_review_request.json \
  --source-snapshot examples/synthetic_source_snapshot.json \
  --output-dir /tmp/synthetic-review-new

# Same workflow via shell; quoting and options are forwarded unchanged:
PYTHON="$PWD/venv/bin/python" bash scripts/run_analysis.sh AMZN \
  --request /path/to/request.json --output-dir /tmp/amzn-review-new
```

The output directory must be empty. If omitted, a unique
`$OUTPUT_DIR/review_<run_id>` directory is created (`OUTPUT_DIR=/tmp/sec_reports`
by default). One ticker/request per CLI run; HTTP supports a batch of reviews.
Explicit fiscal dates and calendar evidence remain mandatory. Ticker/FY labels
alone do not establish a valid reporting period. `--report-request` and
`--period-request` are aliases of `--request` on the default formal CLI.

Default outputs are `report.md`, `report.json`, `acceptance.json`,
`source_inputs.json`, `missing_data.csv`, `reconciliations.csv`,
`review_findings.md`, `dashboard.html`, `loan_review.xlsx`,
`excel_validation.json`, and `run_manifest.json`. `--no-html` / `--no-excel`
explicitly disable optional outputs. The manifest lists requested output
success/failure independently. An Excel error does not discard a valid Markdown
report or prevent cloud publication from being attempted.

Exit codes: **0 accepted**, **2 valid draft awaiting acceptance**, **1 execution or
requested output failure**. Invalid CLI arguments also use argparse's exit 2;
read its stderr for an input error versus JSON stdout for a completed draft.
`final_report_accepted` describes substantive report acceptance; manifest status
also accounts for failures in requested outputs/cloud publication.

## Excel runtime

The exporter uses bundled Node and `@oai/artifact-tool`, with no repository-local
package installation. Defaults are under
`~/.cache/codex-runtimes/codex-primary-runtime/dependencies/`.
Override `REVIEW_NODE` and `REVIEW_NODE_MODULES` (or `REVIEW_RUNTIME_ROOT`) for
other environments. Without this runtime, use `--no-excel` or install/configure
the supported runtime. Export failures are reported, never silently skipped.

The workbook has `Review` and `Sources` sheets, including the evidence registry.
It is generic for entity, annual/quarterly mode, currency and report
scale. Numeric source values retain original amount/scale. Calculated facts use
Excel formulas linked through formal `input_ids`. Every available numeric result
is compared to the canonical report before export. Source edits, blanks and zero
are recalculated and checked, then restored. Workbook verification uses the
artifact-tool engine; native Microsoft Excel is not automatically run.

## Cloud mode

```bash
export GCP_PROJECT_ID=your-project
export BQ_DATASET_ID=your_dataset
export BQ_LOCATION=US
export SEC_USER_AGENT='Your Name your-email@example.com'

venv/bin/python scripts/agent_runner.py AMZN --request /path/to/request.json \
  --execution cloud --output-dir /tmp/amzn-cloud-review-new
```

Requires Google Application Default Credentials with dataset/table read/write
permissions and a working `dbt-bigquery` installation. Project/dataset/location
are used by both storage and dbt profiles. `DBT_PROJECT_DIR`, `DBT_PROFILES_DIR`
and `DBT_TARGET` remain configurable. By default, a Python dbt script beside the
active interpreter is invoked using that interpreter, handling relocated virtualenv
shebangs automatically. `DBT_EXECUTABLE` selects a different dbt executable;
`DBT_PYTHON` optionally invokes a Python dbt script with a specific interpreter.
For a relocated virtualenv with a stale dbt shebang:

```bash
export DBT_EXECUTABLE="$PWD/venv/bin/dbt"
export DBT_PYTHON="$PWD/venv/bin/python"
```

Cloud sequence:

1. Validate/extract sources into the formal source bundle (no financial calculations).
2. Append run-scoped observations/inputs/evidence to `raw_review_sources`.
3. `dbt run` and `dbt test --select stg_loan_review_run_sources`.
4. Read only this run and entity, check exact JSON round-trip against the source
   bundle, then adopt sources and calculate the formal report.
5. Generate local deliverables. Only after final acceptance and every requested
   deliverable passes, append canonical report/facts/evidence/acceptance to
   `raw_review_results` without rounding Decimal payload strings. Drafts retain
   local outputs and cloud source/run audit records, with `blocked_acceptance`;
   delivery failures use `blocked_delivery`. Neither is a successful publication.
6. Build/test `tag:formal_review_marts`; write the final run manifest to
   `raw_review_runs`. A failed mandatory cloud step fails the run.

Raw tables are append-only. Deterministic load job IDs prevent duplicate retries
of the same run payload. dbt views deduplicate run/key records and preserve prior
runs. No financial value is summed across source versions. New marts:

- `fct_loan_review_facts`: formal fact/status/value/formula; unavailable is null.
- `dim_loan_review_evidence`: source/definition/review evidence.
- `bridge_loan_review_evidence`: run-scoped fact/evidence relationships.
- `fct_loan_review_acceptance`: technical/rendered/substantive acceptance flags.
- `dim_loan_review_runs`: requested outputs and publication/execution status.

Join by `run_id` and filter acceptance/run status as appropriate. The acceptance
view exposes final acceptance only after the run manifest records both `accepted`
and `published`; failed warehouse validation cannot expose an accepted run. Exact values and original payloads are preserved alongside
BI-friendly numeric casts; BIGNUMERIC/Excel floating-point precision limits still
apply. Existing legacy marts are retained and are not the formal result source.

Reuse a previously staged **SEC/snapshot** formal source bundle with its exact
original request (new fiscal periods/as-of/supplements require a new source run):

```bash
venv/bin/python scripts/agent_runner.py AMZN --request /path/to/original-request.json \
  --source bigquery --source-run-id PREVIOUS_32_CHARACTER_RUN_ID \
  --execution cloud --output-dir /tmp/amzn-reused-review-new
```

Without `--source-run-id`, `--source bigquery` explicitly builds
`stg_loan_review_sources`, then uses the existing lossless raw SEC ledger reader.
That backend requires the legacy `raw_income_statement`, `raw_balance_sheet` and
`raw_cash_flow` tables to have been populated with complete lineage metadata.
Formal cloud mode stores its own run-scoped bundles; it does not rewrite legacy
raw financial tables. Local mode can read BQ sources but does not publish results.

## Workbook source

```bash
venv/bin/python scripts/agent_runner.py NXST --source workbook \
  --workbook /path/to/nexstar.xls --mode annual --review-date 2026-10-27 \
  --output-dir /tmp/nxst-workpaper-review-new
```

Quarterly requires `--mode quarterly --quarter 1|2|3`. The read-only `.xls`
adapter remains specific to the validated Nexstar Report1 layout; arbitrary
company workbooks are not inferred. Its source data are routed through the same
calculation, output and optional cloud stages. Workbook provenance restrictions
remain acceptance blockers; a review date does not establish SEC publication
date or independently verified CIK. Do not supply a separate request/supplement
to this adapter, as its calendar/identity come from the validated workbook.

## HTTP

Start the existing Flask service with `venv/bin/python scripts/agent_runner.py`.
`POST /v2/analyze/AMZN` uses an inline JSON envelope:

```json
{
  "review_request": {"schema_version": 1, "...": "full existing request contract"},
  "source": "sec",
  "execution": "local",
  "html": true,
  "excel": true,
  "supplements": []
}
```

For offline requests use `source: "snapshot"` and `source_snapshot` with the full
snapshot object. For BQ reuse supply `source_run_id`. HTTP accepts structured
JSON, not arbitrary workbook/server file paths. `POST /v2/run` accepts
`{"reviews": [{"ticker": "AMZN", "review_request": {"...": "full request"}}]}`.
HTTP 400 means malformed options/request, 500 execution/output failure, 200 a
completed review; inspect `status`/`final_report_accepted` to distinguish a draft.
Artifact paths in responses are server-local; use local files or your deployment's
artifact delivery layer. Existing `/memo/<ticker>` serves legacy files only.

The unversioned `/run` still accepts `{"tickers": ["AMZN"]}` and GET uses the
configured default tickers. `/analyze/AMZN` still accepts an empty body or `html`,
and GET can serve the generated HTML. These calls explicitly use the legacy
pipeline and existing warehouse marts, not formal source adoption. Their results
always have `final_report_accepted=false`; legacy Markdown includes a notice.
The historical KPI definitions and calendar-year labels are compatibility
estimates, not the approved formal metric definitions. Warehouse availability,
SEC ingestion, and any configured MD&A service are still required by that path.
There is no raw-SUM fallback when the compatibility marts are unavailable.
Unversioned routes also accept formal envelopes for existing formal clients;
`/v2` never silently falls back to legacy execution.

## Compatibility and verification

`--legacy --period-request request.json` explicitly selects the historical
BigQuery/Memo workflow. `--source-request` explicitly selects source-only staging.
The historical MD&A LLM path is isolated to legacy mode. Formal narratives remain
evidence-bound; this integration does not invent a new LLM approval path.

Run `venv/bin/python -m unittest discover -s tests -v`.
For parser-only dbt verification (no cloud queries):

```bash
venv/bin/python venv/bin/dbt parse --project-dir references/dbt \
  --profiles-dir references/dbt --target-path /tmp/review-dbt-parse \
  --log-path /tmp/review-dbt-logs
```

The cloud boundary is tested offline with mocked clients and explicit run-ID,
round-trip, publication and failure assertions. Live SEC/GCP/dbt query execution
requires configured network access/credentials. No production cloud writes are
performed by the unit tests. DEC-03/CFADS/debt-service definitions and missing
company-specific evidence continue to block final acceptance when applicable.

## Review remediation

See [PR #1 remediation](pr1-review-remediation.md) for the eight findings, strict
reconciliation schema, regression tests, publication gates, and verification limits.
Run artifacts under `outputs/` and local `node_modules` links are ignored; create
new deliverables locally rather than committing validation receipts or raw filings.
