# Loan Review Source Inputs — Block 2

Date: 2026-10-20. Baseline: [acceptance v1.0](loan-review-acceptance-spec-v1.0.md).
Scope: DATA-01/02/03, EVD-01/03, MISS-01/02/03; source-side AT-04/05/06/08/16/19/22.
This block prepares traceable inputs; it does not implement the calculation,
narrative, rendering or final delivery gates of Blocks 3–6.

## Data flow

```text
Explicit mode + verified fiscal calendar + review as-of
                     |
SEC companyfacts or an extracted snapshot or BigQuery candidate staging
                     |                          Reviewed structured supplement
                     |                                    |
Preserve tags, units, intervals, accession/version, original values and locators
                     |                                    |
                     +----------- entity/scope checks ----+
                                      |
                    Exact metric + start/end + unit matching
                                      |
                   All matching candidates retained with evidence IDs
                                      |
              Agreement -> sourced; disagreement -> conflict; absence -> missing
                                      |
                   <TICKER>_loan_review_sources.json
                   stage = source_inputs_only; final_report_accepted = false
```

No latest-filing rule is inferred. Different values, units, definitions or EBITDA
bases remain conflicting. Identical matching observations may supply one value
with **all** supporting evidence IDs; no accession is silently preferred.
The explicit `as_of` excludes later document versions but retains them in the audit
registry and lists the exclusion reason. It does not approve a restatement hierarchy.

## Components and compatibility

| File | Change and impact |
|---|---|
| `scripts/sec_client.py` | Verify requested CIK; correct instant concepts; preserve exact duration intervals even in a different filing form; retain original unit keys, amendments and all versions; create immutable fact IDs and source locators |
| `scripts/bq_loader.py` | Necessary persistence change: nullable additive audit columns; immutable financial fact ID MERGE key; exact-repeat batch deduplication; no mixed-ticker financial batches; only ingestion timestamp updates for a matched financial observation |
| `scripts/loan_review_sources.py` | Pure request/supplement validation, precise source matching, explicit conflict/missing states and source bundle serialization; independent of network, LLM or calculations |
| `scripts/agent_runner.py` | Add source-only entrypoint and CLI; save extracted ledgers in normal ingestion; parameterized BigQuery source reader; mark legacy reports unvalidated |
| `stg_loan_review_sources.sql` | Lossless union of raw candidate facts; no pivots, joins on end date, latest-version selection, alternate-tag sums or zero defaults |
| `loan_review_source_period_identity.sql` | dbt source-period invariant test; error severity |
| `tests/test_loan_review_sources.py` | Offline extraction, supplement, selection, loader, SQL execution and runner-boundary tests |

The new source staging is deliberate: existing wide staging and KPI marts contain
calculation assumptions belonging to Block 3. Routing new source inputs through
those pivots would immediately lose lineage and mix source selection with unfinished
calculation changes. They are not used by the new source-only entrypoint. Existing
legacy CLI/report behavior is retained but is **not** v1.0 accepted output. Increased
raw version/unit coverage is now checked by the equivalent-source adoption adapter
before legacy reads. Legacy calculations and final-format integration still need
the later blocks before final acceptance.

### Storage and rollout

When `ensure_table` is invoked, absent audit fields are added without deleting or
rewriting existing columns/rows. This code change does not itself deploy anything.
Financial fact identity includes ticker/CIK, scope, metric/tag/taxonomy, unit, kind,
actual start/end, filing form/accession/date, and original value. Same-day YTD and
standalone quarters, currency variants and restatements cannot overwrite each other.
Original numeric text is authoritative for the new source stage; the legacy FLOAT64
column remains for compatibility. No rounded legacy float reconstructs original text.

Legacy raw rows have null audit fields. Staging leaves them visible as `unverified`;
the source reader rejects them. Merely re-ingesting alongside those rows does not
remove them. An explicit migration/archival plan or a clean separately configured
dataset is required before using that existing dataset for the new source stage.
No destructive cleanup or cloud migration was performed for Block 2.

The source staging is separate from the legacy `+tag:marts` selection. After schema
readiness and deployment authorization, the relevant dbt commands are:

```bash
venv/bin/dbt run --select stg_loan_review_sources --project-dir references/dbt --profiles-dir references/dbt
venv/bin/dbt test --select tag:loan_review_sources --project-dir references/dbt --profiles-dir references/dbt
```

These cloud commands are documentation, not a statement that they were executed.

## Request schema

The source-only CLI requires a JSON request with **exactly** these keys:

| Field | Requirement |
|---|---|
| schema_version | `1` |
| mode | `annual` or `quarterly`, chosen by user |
| entity | Exact normalized ticker/entity identity, also passed to runner |
| cik | Ten-digit CIK string |
| scope | Explicit source scope; SEC companyfacts are retained as `entity-wide`, not silently relabeled parent/consolidated |
| currency | Requested monetary currency; no implicit conversion |
| scale | Positive decimal string, such as `1000000`, explicitly chosen |
| as_of | ISO review cutoff date; requested periods cannot end after it |
| periods | Four ordered Period objects from Block 1, including actual fiscal dates and calendar evidence IDs |
| evidence | Calendar Evidence objects from Block 1, with borrower, scope, document version/date, locator and original supporting content |

Every Period object includes `role`, `label`, `fiscal_year`, `start`, `end`,
`ltm_start`, `evidence_ids`, `quarter` and `reason`. The field list and fiscal roles
are defined in [the output contract](output-format.md). Dates are ISO strings;
unknown dates are null with a reason. No calendar-quarter or companyfacts `fy/fp`
guess is made. Companyfacts `fy/fp` are kept as **filing context**, not fact-year truth.

Every calendar Evidence object includes `id`, `entity`, `scope`, `source_id`,
`version`, `document_date`, `locator`, `kind` (`calendar`), `period_roles`, `content`,
and `purpose` (`borrower`). Calendar evidence must be available by the review cutoff.

## Reviewed structured supplemental evidence

The first supported route for a Compliance Certificate or other non-SEC evidence
is reviewed JSON, not automatic PDF/XLSX parsing. The envelope has exactly:

- `schema_version: 1`
- `entity`, `cik`, `scope`: must match the requested borrower and scope.
- `purpose: "current_borrower_evidence"`: historical/style/sample inputs are rejected.
- `records`: list of records with the following fields.

| Field | Requirement |
|---|---|
| metric | A metric key from the Block 1 catalog |
| period_kind | `instant` or `duration`, appropriate for the metric |
| start, end | Exact source interval; start is null for an instant |
| unit, scale | Currency and positive scale for money; `text`, `percent`, `multiple` or `percentage_points` with scale 1 for other metrics; percentages are fractions |
| value | Explicit numeric value/text when sourced; null for unavailable/not applicable |
| status | `sourced`, `not_disclosed` or `not_applicable` |
| reason | Required for non-disclosure/inapplicability; state the material actually reviewed |
| definition | Actual source metric definition, not a guessed standard formula |
| basis | Required for EBITDA/basis/leverage; retain actual adjustments |
| source_id, version, document_date | Document identity, version and ISO date |
| source_uri, locator | Retrievable document location and precise page/cell/section |
| excerpt | Original supporting excerpt; treated as data, never execution instructions |
| verification | `verified_by`, ISO `verified_at`, and `method: "checked_against_source"` |

A verification record is an auditable reviewer assertion, not cryptographic proof
or automatic confirmation that the source says what the JSON claims. The reviewer
must actually compare the input against the source document. The program checks
structure, identity, periods and values; semantic authenticity remains a separate
review requirement. It does not open arbitrary source URIs or execute source text.

Historical examples are never a factual source. A familiar template structure, the
same metric name or a claimed EBITDA basis does not authorize transferring another
borrower's data. Identity/scope/purpose mismatches fail before selection.

## Missing, zero, conflicts and pending definitions

- Missing tag or unmatched interval: `missing`, value null, with reviewed-input scope.
  This is not a statement that the whole SEC filing lacks the disclosure.
- Explicit numeric source zero: `sourced`, value `"0"`, with evidence IDs.
- Document explicitly does not disclose an item: `not_disclosed`, value null,
  accepted only through a reviewed supplemental record with locator/excerpt/reason.
- Confirmed not applicable: `not_applicable`, value null and reviewed evidence.
- Different values, units, definitions or bases: `conflict`, value null and every
  competing candidate ID retained. No silently chosen restatement or alternative tag.
- Ratios/common-size and other formula outputs: `not_calculable` at this stage,
  explicitly reserved for Block 3. Source-reported values remain in the evidence
  registry and do not bypass the approved calculation requirements.

Required ratio inputs, including capitalized interest, D&A and Quick Assets, have
explicit slots even when missing. No absent component becomes zero. Receivables,
allowance and inventory source facts are retained in the ledger; this does not
approve their aggregation into Quick Assets. No Net Worth/Total Debt proxy or EBITDA
source-priority policy is silently chosen. `pending_decisions` carries the existing
DEC references; a sourced candidate does not mean that definition is approved for
final report use. DEC-01–09 remain governed by v1.0. This block implements the
user-authorized first non-SEC route in DEC-10: reviewed structured input.

## How to run and inspect

Offline, using a previously extracted source ledger:

```bash
venv/bin/python scripts/agent_runner.py TICKER \
  --source-request /absolute/path/request.json \
  --source-snapshot /absolute/path/source_facts.json \
  --supplement /absolute/path/reviewed_certificate.json
```

Omit `--source-snapshot` to retrieve SEC companyfacts; no LLM, writer, or legacy
financial enrichment is invoked in this source-only branch. `--supplement` may be
repeated. The snapshot envelope contains `schema_version`, `entity`, `cik`, and
`financial_facts` with the three extracted statement lists. Normal `ingest_ticker`
also saves this ledger beside its other output files.

The Python API `prepare_loan_review_source_stage` can read an explicitly supplied
BigQuery loader instead. It uses `stg_loan_review_sources` with bound ticker/CIK
parameters, validates returned rows again and has no fallback to legacy KPI tables.
A missing view or invalid lineage is an explicit failure.

The output filename is `<TICKER>_loan_review_sources.json` inside a unique run directory (use the returned path), containing request context,
fixed input slots, source candidates, evidence IDs, exclusion reasons and conflict
count. `source_inputs_prepared` means preparation finished; it does **not** mean
all fields are available or the final report passed. `final_report_accepted` is false.
The source-only branch returns before dbt financial transformations, `_enrich_rows`,
MD&A generation and the report writer.

## Tests and acceptance boundary

```bash
venv/bin/python -m unittest discover -s tests -p 'test_loan_review_*.py' -v
```

The source tests use isolated synthetic documents. They execute the rendered
candidate staging SQL in SQLite to verify lossless union behavior; BigQuery loader
calls are mocked, and runner tests use offline snapshots. This is **not** a live
BigQuery/dbt deployment test. Production SQL compilation/execution, old-row migration,
end-to-end report generation and actual source-document semantic review remain
separate gates. No fixture or synthetic approval is copied into borrower output.

### Local verification result (2026-10-20)

- 88 unittest cases passed: 49 existing Block 1 cases plus 39 Block 2 cases.
- Offline CLI roundtrip passed, including SEC snapshot and reviewed supplement.
- Candidate staging and the dbt period-invariant query executed against SQLite fixtures.
- Both rendered SQL files parsed successfully using the BigQuery dialect in sqlglot.
- `git diff --check` passed.
- Live SEC/GCP execution, production dbt execution and schema migration were not run.

The tests establish the source-only boundary's behavior. They do not establish that
legacy calculation/report paths comply with v1.0 or that real evidence is authentic.

## Block 2 review corrections (2026-10-21)

- Legacy KPI, annual and quarterly readers now validate exact source equivalence
  before reading either marts or fallbacks. This supersedes the initial
  cardinality-only guard, which blocked even equal-valued repeated disclosures.
  Same-entity/scope/concept/interval/unit/status/basis observations with equal
  original Decimal values are adopted once, retaining every evidence ID.
  Different tags are not assumed equivalent merely because values match.
  Missing audit metadata, conflicts and unsupported legacy currencies still stop
  the reader. Checks cover the borrower's full raw history; no as-of/version
  selection policy is invented.
- Each reader saves a versioned `legacy_source_adoptions` snapshot containing
  adopted rows, definitions and all source evidence. The pipeline returns the
  paths in `source_adoption_paths`. Representative IDs are selected deterministically
  only after equivalence is proven; no latest filing decides the accepted value.
  All observed filing forms remain available for legacy form filters, including
  the base form of amendments. The raw ledger is never rewritten or deleted.
- When equivalents were collapsed, the reader bypasses raw-derived marts and
  executes its existing financial SQL on parameterized JSON rows from the accepted
  snapshot. Every raw fallback uses this snapshot, never raw table SUMs. KPI
  income rows group by period rather than representative filing metadata so that
  equivalent sources cannot split one period into incomplete rows. Display filing
  metadata uses MAX, while the snapshot retains each actual contributing filing.
  If no collapse is needed, the existing mart-first route remains available.
  Query/validation/write failures do not silently become a successful empty report.
- This is source adoption, not approval of the legacy formulas or report format.
  Original decimals decide equivalence; existing legacy FLOAT64 calculations are
  unchanged. SEC raw facts are base-unit observations; the source-only structured
  supplement route also supports exact scale normalization. No currency conversion
  or new alternate-definition approval is introduced. Large parameter snapshots
  may hit BigQuery request limits and must fail explicitly; no lossy fallback is used.
- Source CLI parsing supports both `--source-request path` and
  `--source-request=path`; orphan snapshot/supplement options fail before dispatch.
  Expected input/file errors produce a nonzero exit and an explicit error message.
- Calendar evidence/period objects and reference lists, SEC row objects and
  snapshot statement lists are checked before conversion. Invalid nested inputs
  report a validation error rather than leaking a TypeError.
- `write_source_bundle` now returns the actual saved `Path`. Each call allocates a
  unique run directory under the requested output parent, writes/fsyncs temporary
  bytes, and atomically renames them to the JSON filename. Callers must use the
  returned `source_inputs_path` or `source_ledger_path`, not a fixed ticker path.
  Repeated/concurrent runs cannot overwrite prior snapshots. Failed publication
  returns no success path; cleanup is best effort and preserves the original error.

No formulas, narrative generation, final writer, cloud deployment or legacy-row
migration were changed by these corrections.

### Review correction verification (2026-10-21)

The regression suite covers the previous CLI, nested-input and atomic snapshot
fixes plus equivalent filing versions, exact precision, scale normalization,
missing-versus-zero, conflicting definitions/units/bases, borrower isolation,
and separate YTD/quarter/year intervals. Executed legacy-query tests pass the
actual parameter snapshots into SQLite after translating BigQuery syntax, and
check KPI, annual and quarterly revenue/cash/CFO values are not doubled. The
original SQL is also parsed with the BigQuery dialect (sqlglot, test dependency).
This is not live BigQuery execution. No deployment, migration or commit was run.

- Final local regression result: **115 tests passed**, including the previous 101
  cases (with the obsolete equal-value blocking expectation updated) and 14 new
  equivalence/query cases. `git diff --check` passed.
