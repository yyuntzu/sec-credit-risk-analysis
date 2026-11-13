{{ config(materialized='view', tags=['formal_review_marts']) }}
with reports as (
    select run_id, payload from {{ source('formal_review_raw', 'raw_review_results') }}
    where record_kind = 'report'
    qualify row_number() over(partition by run_id order by created_at desc) = 1
), facts as (
select run_id, entity, record_id as fact_id,
json_value(payload, '$.metric') as metric,
json_value(payload, '$.period_role') as period_role,
json_value(payload, '$.status') as status,
json_value(payload, '$.value') as value_exact,
safe_cast(json_value(payload, '$.value') as bignumeric) as numeric_value,
json_value(payload, '$.unit') as unit,
json_value(payload, '$.currency') as currency,
json_value(payload, '$.formula_id') as formula_id,
json_value(payload, '$.period_kind') as period_kind,
json_value(payload, '$.start') as period_start,
json_value(payload, '$.end') as period_end,
json_value(payload, '$.definition') as definition,
json_value(payload, '$.reason') as reason,
json_value(payload, '$.basis') as basis,
payload as fact_payload, created_at
from {{ source('formal_review_raw', 'raw_review_results') }}
where record_kind = 'fact'
qualify row_number() over(partition by run_id, record_id order by created_at desc) = 1
)
select f.*,
json_value(r.payload, '$.mode') as review_mode,
json_value(r.payload, '$.scope') as scope,
json_value(r.payload, '$.currency') as report_currency,
json_value(r.payload, '$.scale') as report_scale,
a.final_report_accepted
from facts f
join reports r using(run_id)
join {{ ref('fct_loan_review_acceptance') }} a using(run_id, entity)
