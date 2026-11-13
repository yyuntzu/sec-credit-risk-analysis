{{ config(materialized='view', tags=['formal_review_marts']) }}
select run_id, entity,
json_value(payload, '$.fact_id') as fact_id,
json_value(payload, '$.evidence_id') as evidence_id
from {{ source('formal_review_raw', 'raw_review_results') }}
where record_kind = 'fact_evidence'
qualify row_number() over(partition by run_id, record_id order by created_at desc) = 1
