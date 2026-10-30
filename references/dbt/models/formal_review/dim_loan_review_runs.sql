{{ config(materialized='view', tags=['formal_review_marts']) }}
select run_id, entity,
json_value(payload, '$.status') as status,
json_value(payload, '$.execution') as execution,
json_value(payload, '$.source') as source,
payload as run_payload, created_at
from {{ source('formal_review_raw', 'raw_review_runs') }}
qualify row_number() over(partition by run_id order by created_at desc) = 1
