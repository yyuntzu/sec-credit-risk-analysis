{{ config(materialized='view', tags=['formal_review_marts']) }}
select run_id, entity, record_id as evidence_id,
json_value(payload, '$.locator') as locator,
json_value(payload, '$.kind') as kind,
payload as evidence_payload, created_at
from {{ source('formal_review_raw', 'raw_review_results') }}
where record_kind = 'evidence'
qualify row_number() over(partition by run_id, record_id order by created_at desc) = 1
