# Reusable Looker Studio visualization

## Outcome and current boundary

The user designs one report template with fixed tables, charts and formatting.
Subsequent company reviews publish data to the same BigQuery schema. The report
selects the company and run, preserving its layout. Reuse the data connection;
changing companies normally changes filters, not the connected table.

The formal cloud publisher and dbt views already exist. `review_delivery.py` now
generates a configured run-specific URL and shared delivery receipt through the
formal workflow. It does not create a dashboard or verify its remote rendering.
The user selected Looker Studio, Google's drag-and-drop report product. Use its
BigQuery connector and report controls; enterprise LookML setup is outside this branch.

## Workflow

For the specifically user-authorized Alphabet 2026Q3 draft, resume from
[its build status](looker/googl_q3_build_status.md). Its isolated draft views and
unaccepted labels are separate from the accepted-run publication workflow below.
The report and source connection exist; its 23 chart components are not yet placed.

For dashboard design or specification validation, read
[the 23-component design draft](looker-studio-design-spec.md) before implementing
the template. Its unresolved decisions remain explicit; ROA/ROE are excluded.

1. Obtain the existing Looker Studio template URL/ID, BigQuery project/dataset and
   intended company/run selection behavior. Reuse configuration already supplied.
2. Execute the formal workflow in `loan-review-integration.md` with cloud execution.
   Retain the generated entity and run ID. Local-only output does not refresh BQ.
3. Check the final run manifest: `status=accepted`, `cloud_status=published`, and
   `final_report_accepted=true`. Draft or failed runs retain their local outputs;
   describe visualization publication as blocked rather than showing an older run
   as the requested run.
4. Connect the template to formal views below using Looker Studio's BigQuery
   connector. Configure company (`entity`) and run (`run_id`) controls and verify
   their scope includes every intended chart. When charts use different data
   sources, verify filter compatibility explicitly; sharing a visible field name
   alone does not establish that a control filters every source.
5. Select `entity` and a single `run_id` throughout the report. An explicitly
   requested historical run stays selected. If latest-run selection is requested,
   implement a shared selector over accepted, published runs, partitioned by entity,
   review mode, scope, currency and scale; use manifest completion time and a stable
   run-ID tie-break. `vw_looker_review_runs` now supplies this selector as
   `is_latest_accepted_run`; `vw_looker_review_facts` exposes the flag with facts.
   Explicit historical-run selection must not also apply the latest-only filter.
6. Verify at least two companies and a repeated run for one company: all charts,
   titles, commentary and period columns switch together; values match each run's
   `report.json`; missing values remain missing. Check the connector's refresh/cache
   behavior before claiming newly published data are visible.

Completion means the configured template displays the selected run correctly and
the verified report URL is available. Until then, distinguish data publication from
template connection and successful rendering. Construct automatic filtered links
using the actual template/filter configuration. Treat `link_ready` as URL
construction only; verify the remote report before calling it end-to-end delivery.

## Automatic delivery configuration

Every formal run now writes `delivery.json` and includes the same object under
`run_manifest.json.delivery` and CLI/HTTP results. It lists existing Review, Excel
and local Dashboard outputs and a separate `looker_studio` state:

- `not_configured`: no URL configuration supplied; local outputs still delivered.
- `blocked`: this run is draft/failed/local or cloud publication did not succeed.
- `link_ready`: accepted/published run with a configured URL; `render_verified=false`.

Use `examples/looker_config.example.json` as a schema example, replacing the report
ID and URL parameter names with actual configured values. It is not active config.
`url_parameter_names` contains the URL names shown by Looker Studio's Manage
variables (parameters), which may differ from display names or data-source IDs.
Entity and run ID are required; mode is optional. Names must be unique.

```bash
venv/bin/python scripts/agent_runner.py AMZN --request /path/to/verified-request.json \
  --execution cloud --looker-config /path/to/looker-config.json \
  --output-dir /tmp/amzn-review-new

# Optional persistent per-environment configuration for later formal runs:
export LOOKER_STUDIO_CONFIG=/path/to/looker-config.json
```

HTTP `/v2/analyze/AMZN` accepts the same structured config as `looker_config`.
HTTP does not accept a path to a config file. Shell forwards the CLI option.
Invalid configuration fails before source retrieval and output-directory creation.
A final cloud manifest failure retracts the link from the local delivery receipt.

One-time template setup: create text parameters for company, run and optional
mode; enable URL overrides; bind them to filtering in all chart data sources.
For a shared source this can use a calculated Boolean equality condition between
`entity`/`run_id` and their respective parameters, applied as an include filter.
Parameters alone do not filter data. Keep explicit-run links free of latest-only
filters. Verify the actual URL with two companies and two runs, then save those
parameter names in configuration. Sharing permissions are configured separately.
See [Google's parameter documentation](https://docs.cloud.google.com/data-studio/parameters).

## Formal data contract

For phased implementation and remaining delivery work, read
[the delivery plan](looker-delivery-plan.md). The two new Looker views are included
in the existing formal publication selection; they have not yet been deployed or
verified against live BigQuery/Looker Studio.

| View | Purpose and grain |
| --- | --- |
| `vw_looker_review_facts` | Accepted/published facts with DATE-typed endpoints and latest-run flag; primary shared Looker Studio source. |
| `vw_looker_review_runs` | Accepted/published run contexts and deterministic latest-run selection. |
| `fct_loan_review_facts` | One fact per run/entity/fact ID: metric, period role, dates, value, unit, formula, mode, scope, report currency and scale. |
| `dim_loan_review_runs` | Run status and original manifest in `run_payload`. |
| `fct_loan_review_acceptance` | Financial acceptance gated by accepted/published run status. |
| `fct_loan_review_commentary` | Display analysis and references; multiple entries per run. |
| `dim_loan_review_evidence` | Source evidence registry. |
| `bridge_loan_review_evidence` | Fact/evidence relationships within a run. |

Join run/acceptance metadata using `run_id` and `entity`. Keep commentary and
evidence at their own grains, or aggregate them before joins; directly joining
multiple evidence/commentary rows to facts duplicates financial amounts.

Use `numeric_value` for charting and preserve `value_exact` for audit comparison.
Respect fact status, unit, report scale, scope, actual fiscal dates and review mode.
Ratios and balance-sheet snapshots are not additive measures. Select the intended
metric/period/fact rather than summing runs, periods or currencies. Missing numeric
values remain null. Use canonical ratios instead of rebuilding formulas in Looker.

Annual and quarterly can share styling but require their respective formal period
layouts. Filter mode explicitly or use separate pages in the same template.
Commentary availability is informational and does not change financial acceptance.

## Data flow

```text
agent_runner.py → review_workflow.run_review()
  → validated source bundle
  → review_cloud.py: raw_review_sources → dbt staging → verified read-back
  → loan_review_pipeline.py / loan_review_contract.py: canonical Report
  → commentary + Markdown / JSON / HTML / Excel
  → acceptance and delivery gates
  → review_cloud.py: raw_review_results + raw_review_runs
  → dbt formal review views
  → configured Looker Studio template: entity + run selection
```

Legacy `fct_credit_kpis` and its companion marts retain historical definitions;
use the formal views above for this branch.

## Product documentation

- [BigQuery connector](https://docs.cloud.google.com/data-studio/connect-to-google-bigquery)
- [Data freshness](https://docs.cloud.google.com/data-studio/manage-data-freshness)
