# Loan Review skill execution

The natural-language skill routes report-generation requests to
`scripts/loan_review_skill.py`, via `scripts/run_loan_review_skill.sh`. This is the
warehouse candidate path, distinct from the retained standalone local/HTTP Python
workflow. Skill selection is enabled by its description and
`agents/openai.yaml: policy.allow_implicit_invocation=true`.

## Prepare inputs

Read the source request schema in `loan-review-source-inputs.md`; the examples in
`../examples/` demonstrate schema only. Supply a verified borrower request with
Annual/Quarterly mode, CIK, scope, currency, scale, as-of and exact fiscal dates
with calendar evidence. Ask only for unresolved user intent; use official SEC
filings to establish factual dates/CIK. Keep all required columns when unavailable.

The default source helper uses `SECEdgarClient.extract_financial_facts` followed by
`prepare_loan_review_source_stage` to retain raw candidates and evidence. It does
not call Python's report calculator. SEC fetches require a real `SEC_USER_AGENT`
contact. Review company-specific footnotes and supply evidence for unsupported
concepts instead of inserting proxies. MD&A/footnote causes need the current
borrower's reviewed documents, per [formal commentary](formal-commentary.md).

Supported source choices:

- Default SEC fetch: `--request request.json`.
- Fixed raw SEC snapshot: also `--source-snapshot snapshot.json`.
- Additional audited borrower records: repeat `--supplement supplement.json`.
- Already prepared complete source bundle: `--source-bundle bundle.json`; its
  request, borrower and scope must match. It cannot mix snapshots/supplements.
- Reviewed reconciliation envelope: `--reconciliations reviews.json`.
- Reviewed filing observations: `--commentary-documents documents.json`; the
  selected package's existing document schema checks still apply.

Complete bundles are fixed source inputs, not published financial results. A
financial review missing necessary definitions/reconciliations remains draft.

## Runtime and command

Run shell commands from the resolved skill root. The launcher chooses
`LOAN_REVIEW_PYTHON`, an active venv, repository venv or linked-main-worktree venv;
the runtime loader still enforces the selected package's dependency content lock.
Use `LOAN_REVIEW_PYTHON=/absolute/path/venv/bin/python` to select a known environment.
See `loan-review-integration.md#excel-runtime` for bundled Node/artifact-tool.

```bash
bash scripts/run_loan_review_skill.sh AMZN --request /absolute/path/request.json \
  --reconciliations /absolute/path/reviews.json \
  --commentary-documents /absolute/path/documents.json \
  --output-dir /absolute/path/new-amzn-loan-review
```

Use reviewed files only when provided/established; optional arguments can be omitted.
Excel is requested by default. `--no-excel` is for an explicit HTML/Markdown-only
request, not a silent response to export failure.

`loan-review-runtime.json` supplies isolated project, control/runtime bucket,
archive dataset, delivery bucket and required q18 policy. `--runtime-config` can
select another candidate configuration; individual project/bucket/dataset CLI
overrides or `GCP_PROJECT_ID`, `LOAN_REVIEW_CANDIDATE_BUCKET`,
`LOAN_REVIEW_ARCHIVE_DATASET`, `LOAN_REVIEW_DELIVERY_BUCKET` override those fields.
Only shadow namespaces are accepted. The wrapper never creates/selects a release
to repair a missing runtime and never initializes a production dataset. Its archive
dataset can be created within the configured isolated namespace.

The currently configured resources have seven-day testing retention; credentials
or runtime objects may expire. A credentials/network/configuration failure is
reported explicitly. Fix only the actual failed prerequisite, then use a new run
directory; avoid blindly retrying remote work that may still be running.

## Outputs and completion

`run_manifest.json` records independent stage results and actual output paths:

1. `source_bundle.json` and optional immutable copies of review/document inputs.
2. `selected/`: selected release/package receipt and pre-SQL GCS binding; nested
   `execution/calculation/` contains BigQuery facts, tests and calculation receipt.
3. `report/`: receipt-bound Markdown/JSON/HTML, commentary and default Excel.
4. `archive/`: BigQuery candidate fact/evidence/lineage/archive receipt.
5. `storage_receipt.json`: generation-pinned GCS report package commit.
6. `publication_preflight.json`: remaining formal gates, without publication.

Exit 2 / `draft` means every requested stage completed but publication is not
authorized. Exit 1 / `failed` preserves partial numeric reports and a stage/error
manifest, including export/storage failures. Read manifest outputs rather than
assuming a fixed path was created. Financial readiness is separate from technical
delivery. Formal defaults remain Python until explicit M4/M5 cutover; this skill
uses candidate dbt reports and does not invoke the old publisher.

For the precision rule, fixed-source package and remaining migration gaps, consult
`../docs/specs/dbt-q18-precision-validation-20261111.md`,
`../docs/specs/dbt-selected-runtime-validation-20261111.md` and
`../docs/specs/dbt-migration-completion-matrix.md` when investigating those stages.
