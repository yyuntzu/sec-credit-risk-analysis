# Evidence-bound Loan Review commentary

Formal reports now contain source-based cause commentary as well as numerical
comparisons. The same canonical narratives feed Markdown, JSON, Dashboard,
Excel, and BigQuery. The legacy string-only commentary API is retained.

## Execution modes

The CLI, Python `run_review`, and formal HTTP envelopes accept `commentary_mode`:

| Mode | Behavior |
| --- | --- |
| `auto` (default) | SEC sources retrieve matching MD&A and generate model proposals. Snapshot/BQ/workbook sources do not implicitly call SEC or the model. Supplied documents/claims are applied offline. |
| `model` | Generate proposals using supplied documents; SEC source may retrieve the documents first. Requires the configured Anthropic credentials/model. |
| `reviewed` | Use supplied documents/claims without network calls in the commentary stage. The name does not grant approval: each claim still needs its explicit source-review record. |
| `off` | Skip commentary generation. Missing required source-based causes still block substantive acceptance. |

Use `--commentary PATH.json` for the CLI, or a `commentary` object in Python/HTTP.
An offline source snapshot may also contain a `commentary` object. A directly
supplied commentary object takes precedence over the snapshot copy.

Live model selection follows `FORMAL_COMMENTARY_MODEL`, then `ANTHROPIC_MODEL`,
then the existing legacy module's default. Verify the selected model is available
to your account. No live provider call was made during local validation.

## Offline runnable example

The examples below are **synthetic test data**, not a borrower assessment:

```bash
venv/bin/python scripts/agent_runner.py SYNTHETIC-ONLY \
  --request examples/synthetic_review_request.json \
  --source-snapshot examples/synthetic_commentary_snapshot.json \
  --commentary examples/synthetic_commentary.json \
  --commentary-mode reviewed \
  --output-dir /tmp/loan-review-commentary-example-new
```

The directory must be absent or empty. The example contains a reviewed revenue
explanation and exact source passages from both comparison periods. Other facts
and causes remain incomplete, so the expected exit is **2 (draft)**. Add
`--no-excel` to run without the bundled Node/artifact-tool runtime.

The resulting Excel Review sheet includes the explanation, source quotes, and
review label immediately below the income table. Sources retains the complete
evidence registry. The same text appears in Markdown and Dashboard.

## Document and claim inputs

The bundle has `documents` and optional `claims` lists. Each document requires:

- `id`, `entity`, ten-digit `cik`, `scope`, `source_id`, `version`;
- `document_date`, `source_url`, `section` set to `MD&A`, and the original `text`;
- `periods`: exact `{role, start, end}` objects matching the canonical request.

Identity, scope, publication date versus `as_of`, and exact fiscal coverage are
validated. A document cannot predate its covered period. Each section is limited
to 80,000 characters and a document set to 320,000. Production borrower evidence
cannot use the synthetic-only `fixture://` source scheme.

Automatic SEC retrieval checks the submissions CIK, matches each requested fiscal
endpoint and filing form, excludes filings later than `as_of`, and consults older
submissions archives when needed. It retrieves the original primary filing and
extracts a bounded Item 7 (10-K) or Item 2 (10-Q) body. It never substitutes an
arbitrary document half when section identification fails. SEC primary-document
URLs and hashes are retained. Character offsets refer to the normalized extracted
section archived in `commentary_inputs.json`, not raw HTML byte offsets.

Each supplied claim identifies `table`, `topic`, `status`, `claim_type`,
`explanation`, `fact_ids`, `period_roles`, and `citations` containing exact
`{document_id, quote}` objects. Management claims also require `attribution`.
Facts and periods must exactly match the existing canonical comparison. Quotes
must be short exact source passages covering both comparison periods; invented
quotes and numerical claims absent from facts/citations are rejected.

For `status: missing`, supply an explicit `reason`; the report preserves its
numeric comparison and displays the analysis gap. Missing canonical comparison
facts cannot be replaced by prose.

## Source review and substantive acceptance

Model output is a visible **proposal awaiting review**. Exact-quote, number, and
period validation does not prove that a paraphrase correctly explains causality.
The model cannot approve its own output: any model-supplied `review` is discarded.

A reviewer may supply this record on a checked claim:

```json
{
  "review": {
    "verified_by": "Reviewer identity",
    "verified_at": "2026-10-30",
    "method": "checked_against_source"
  }
}
```

Review dates cannot predate the cited documents. The resulting review Evidence
binds the exact text, topic/table, claim type, canonical fact IDs, period roles,
and source passage IDs. Changing the narrative invalidates that review binding.
The record is an audit assertion: a human must verify document authenticity and
that each quotation supports the explanation. It is not a cryptographic identity
or an automated semantic guarantee.

All required narrative topics need independently reviewed source-based causes
before `commentary_complete` is true. Numeric comparison alone is insufficient.
Other financial/definition/reconciliation acceptance gates remain unchanged.

## Artifacts, storage, and failures

- `report.json` remains the canonical Report/Fact/Evidence/Narrative object.
- `commentary.json` contains its narratives, notes, shared visible text, quotes,
  source locations, and review state. It is derived, not separately generated.
- `commentary_inputs.json` archives the used documents and claims.
- `commentary_validation.json` records mode, model when invoked, version,
  incomplete topics, or the explicit stage error.
- Validation receipts bind `commentary.json`, `report.json`, and `report.md`.
  Saved-artifact checking recomputes commentary from canonical narratives.
- Excel adds narrative/quote rows beneath each table, preserving the existing
  Review/Sources sheet names and canonical numeric/formula bindings.
- Accepted cloud publication writes canonical commentary records to the existing
  raw results table. `fct_loan_review_commentary` exposes explanation, visible
  text, source/review payload, and final run acceptance. Mandatory integrity
  checks reject accepted narrative entries without reviewed causal analysis.

Provider failures, invalid evidence, or invalid model output retain numeric local
reports and record `stages.commentary=failed` plus an error. The run cannot claim
successful publication. Missing material without a provider error yields an
explicit draft/incomplete stage. Disabling commentary does not bypass acceptance.

A workbook-only source has no independently verified SEC CIK/fiscal request, so
it cannot silently obtain borrower MD&A identity. Use the formal SEC/snapshot
request workflow with verified identity and periods for source-based commentary.

## Validation

```bash
REVIEW_EXCEL_TEST=1 venv/bin/python -m unittest discover -s tests
```

Tests cover source identity/as-of/period/quote errors, unsupported numeric claims,
review-binding tampering, model self-approval prevention, HTTP and SEC adapter
wiring, model failure with preserved drafts, canonical cross-format text and
source consistency, BigQuery record payloads, and saved XLSX commentary rows.
SEC, model, and cloud calls are mocked. Actual bundled-runtime Excel export and
an offline synthetic CLI round trip are exercised; native Excel and live SEC,
Anthropic, BigQuery, and deployed HTTP services remain untested.

Local validation on 2026-10-30: **229 tests passed with no skips**, including
22 new commentary regressions and actual annual/quarterly/commentary XLSX exports.
The synthetic CLI example returned draft exit 2 with report, dashboard, and Excel
stages passing. The income-sheet preview was visually inspected for explanation,
quotes, source identifiers, and review status.
