{{ config(materialized='view', tags=['formal_review_marts', 'looker_studio']) }}
-- Long-form facts: no cross-period sums, no model text/evidence fan-out.
select f.* except (period_start, period_end),
    safe_cast(f.period_start as date) as period_start,
    safe_cast(f.period_end as date) as period_end,
    r.finished_at, r.is_latest_accepted_run
from {{ ref('fct_loan_review_facts') }} f
join {{ ref('vw_looker_review_runs') }} r
    on f.run_id = r.run_id and f.entity = r.entity
    and f.review_mode = r.review_mode and f.scope = r.scope
    and f.report_currency = r.report_currency and f.report_scale = r.report_scale
