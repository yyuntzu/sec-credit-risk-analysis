{{ config(severity='error', tags=['formal_review_marts', 'looker_studio']) }}
with failures as (
    select run_id, entity, fact_id as problem
    from {{ ref('vw_looker_review_facts') }}
    group by 1, 2, 3 having count(*) != 1
    union all
    select run_id, entity, 'ineligible_run'
    from {{ ref('vw_looker_review_facts') }} f
    left join {{ ref('fct_loan_review_acceptance') }} a using (run_id, entity)
    where not coalesce(a.final_report_accepted, false)
    union all
    select min(run_id), entity, 'latest_run_count'
    from {{ ref('vw_looker_review_runs') }}
    group by entity, review_mode, scope, report_currency, report_scale
    having countif(is_latest_accepted_run) != 1
)
select * from failures
