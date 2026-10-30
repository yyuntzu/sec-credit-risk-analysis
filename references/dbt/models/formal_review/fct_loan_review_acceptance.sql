{{ config(materialized='view', tags=['formal_review_marts']) }}
with acceptance as (
    select * from {{ source('formal_review_raw', 'raw_review_results') }}
    where record_kind = 'acceptance'
    qualify row_number() over(partition by run_id order by created_at desc) = 1
)
select a.run_id, a.entity,
coalesce(json_value(a.payload, '$.final_report_accepted') = 'true'
    and r.status = 'accepted'
    and json_value(r.run_payload, '$.cloud_status') = 'published', false) as final_report_accepted,
json_value(a.payload, '$.technical_validation_passed') = 'true' as technical_validation_passed,
json_value(a.payload, '$.rendered_validation_passed') = 'true' as rendered_validation_passed,
a.payload as acceptance_payload, a.created_at
from acceptance a
left join {{ ref('dim_loan_review_runs') }} r using(run_id, entity)
