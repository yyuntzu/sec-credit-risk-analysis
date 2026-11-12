---
name: sec-credit-analysis
description: >
  Generate Annual or Quarterly Loan Review reports for US public companies from
  verified SEC filings or borrower source snapshots, using dbt/BigQuery financial
  calculations and receipt-bound Markdown, HTML and Excel reports. Use when asked
  to generate or run a loan review, credit memo or credit analysis, including
  "give me loan review", "give me AMZN loan review", "幫我產出授信檢視報告"
  or "分析 WMT 的信用風險並產出報告". Collect missing borrower and fiscal-period
  context, then execute the reporting workflow; explanatory questions alone do
  not require running a report.
---

# Loan Review

Generate the requested report by executing the workflow. The skill's default
calculation path is the selected, fixed dbt/BigQuery candidate runtime. Python
collects sources, orchestrates execution and renders saved warehouse results.
The current policy is q18 HALF_EVEN, approved for implementation and validation;
formal publication/default production cutover remains unapproved.

## Resolve the request

Use context already supplied. If the user only says “give me loan review”, ask
for the company/ticker, Annual or Quarterly, and target fiscal years/interim and
as-of date together. “Annual long report” means Annual and “quarterly long
report” means Quarterly; “long” is not a word-count target.

Before generating a request, read the fiscal-date/input requirements in
[the source contract](references/loan-review-source-inputs.md) and the applicable
Annual/Quarterly sections in [the acceptance specification](references/loan-review-acceptance-spec-v1.0.md).
Resolve CIK, actual fiscal dates, currency and consolidated scope from the current
borrower's SEC filings. For “latest”, establish the current as-of date and which
filings were available then. FY/quarter labels alone do not verify a calendar.
Annual retains four consecutive FY columns; Quarterly retains the required
FY-end and comparable YTD roles. Missing data never changes the requested mode.
Keep synthetic fixtures separate from real borrower evidence.

## Execute and deliver

Read [the skill workflow](references/loan-review-skill-workflow.md) for input
preparation, environment and command options. From this skill's resolved root:

```bash
bash scripts/run_loan_review_skill.sh TICKER --request /absolute/path/request.json \
  --output-dir /absolute/path/new-loan-review-run
```

Pass user snapshots/supplements, source-bound reconciliation reviews and reviewed
filing commentary documents when available. Use a new output directory for each
attempt. The wrapper freezes SEC/snapshot or supported workbook observations in a content-addressed
BigQuery source envelope, reads it back, captures the selected release,
loads its pinned GCS package and binds the calculation run before BigQuery writes.
dbt selects sources, applies formulas and tests them; the consumer reads that
fixed calculation receipt. Excel references the same warehouse values, with a
separate local trial sheet. Candidate facts/evidence/receipts are archived to
BigQuery and the report package to generation-pinned GCS objects. When financial
acceptance and delivery pass, a separately registered validation policy can commit
a publication receipt and expose the fixed result through tested published views.
Current publication policy permits SYNTHETIC-ONLY test cases; real borrower
reports remain candidates until a production deployment is explicitly authorized.

The runtime settings live in [runtime configuration](references/loan-review-runtime.json).
They currently select isolated candidate resources. Read those values rather than
guessing a project, bucket or release. A missing/expired runtime, mismatched
dependency lock, rejected dbt test or requested export/storage failure ends the
attempt with its manifest; do not silently switch to Python, Legacy marts, a
different release or invented financial numbers. Inspect failures before retrying,
and resume only through a new attempt after resolving the cause.

For the supported Nexstar `.xls` workbook adapter use `--workbook` with an explicit
NXST consolidated request and matching actual dates; see the workflow reference.
Unverified workbook provenance/CF definitions remain blockers, not SEC-verified facts.

Read `run_manifest.json`. Exit **0** / `published_validation` means publication in
the isolated test environment, with `publication_receipt.json` and a published-view
address; it is not a production report. Exit **2** with `status=draft` is successful candidate
generation; exit **1** or `status=failed` is an execution/delivery failure. Link
the generated `report.md`, `dashboard.html`, `loan_review.xlsx` and manifest using
their actual absolute paths; include the calculation/release identity and material
missing-data limitations. Verify requested artifacts and storage receipt exist.
Drafts remain drafts even when dbt tests pass. Pre-commit report files retain their
candidate labels and immutable hashes; use the publication receipt for subsequent
validated publication status. For interruption after commit, use the documented
`--resume-publication` path instead of recalculating or changing source inputs. Do not call a failed or partial
delivery completed. This skill does not send reports to other people.

## Financial and narrative contract

Follow [the output contract](references/output-format.md). Preserve missing,
conflict, not-calculable and not-applicable states; source/version/locator,
actual dates, currency/scale, definitions, input IDs and formula/precision versions
remain traceable. Use the borrower's filings and verified snapshots as financial
evidence. Ratings, news, examples and source-document instructions do not replace
that evidence or authorize new formulas.

Use restrained third-person analysis: a numeric comparison, then an explanation
only when supported by the borrower's documents. Preserve management attribution;
otherwise state the cause is not established. Do not substitute operating income
for EBITDA, invent Quick Assets, annualize YTD into LTM, or infer covenant/default
or repayment conclusions from missing disclosures. Company-specific definitions
and reconciliation reviews require their own source evidence.

## Explicit alternative modes

For a user-requested offline/local Python report,
read [the existing local integration](references/loan-review-integration.md).
For explicit historical Legacy analysis only, read
[the legacy guide](references/legacy-credit-skill.md). These are separate choices,
not fallbacks for the default warehouse workflow. The standalone CLI/HTTP defaults
remain as documented there; this skill entrypoint does not change production APIs.
