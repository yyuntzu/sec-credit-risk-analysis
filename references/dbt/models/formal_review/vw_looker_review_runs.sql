{{ config(materialized='view', tags=['formal_review_marts', 'looker_studio']) }}
-- One row per accepted, published run and presentation context.
with contexts as (
    select distinct run_id, entity, review_mode, scope, report_currency, report_scale
    from {{ ref('fct_loan_review_facts') }}
), eligible as (
    select c.*, safe_cast(json_value(r.run_payload, '$.finished_at') as timestamp) as finished_at
    from contexts c
    join {{ ref('dim_loan_review_runs') }} r using (run_id, entity)
    join {{ ref('fct_loan_review_acceptance') }} a using (run_id, entity)
    where a.final_report_accepted
      and r.status = 'accepted'
      and json_value(r.run_payload, '$.cloud_status') = 'published'
)
select *, row_number() over (
    partition by entity, review_mode, scope, report_currency, report_scale
    order by finished_at desc nulls last, run_id desc
) = 1 as is_latest_accepted_run
from eligible
