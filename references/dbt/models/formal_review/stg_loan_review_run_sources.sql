{{ config(materialized='view', tags=['formal_review_sources']) }}
select * from {{ source('formal_review_raw', 'raw_review_sources') }}
qualify row_number() over(partition by run_id, record_kind, record_id order by created_at desc) = 1
