{{ config(materialized='view', tags=['formal_review_marts']) }}
select run_id, entity,
json_value(payload, '$.final_report_accepted') = 'true' as final_report_accepted,
json_value(payload, '$.technical_validation_passed') = 'true' as technical_validation_passed,
json_value(payload, '$.rendered_validation_passed') = 'true' as rendered_validation_passed,
payload as acceptance_payload, created_at
from {{ source('formal_review_raw', 'raw_review_results') }}
where record_kind = 'acceptance'
qualify row_number() over(partition by run_id order by created_at desc) = 1
