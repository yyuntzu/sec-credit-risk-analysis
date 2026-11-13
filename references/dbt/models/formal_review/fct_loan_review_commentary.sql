{{ config(materialized='view', tags=['formal_review_marts']) }}
with commentary as (
    select run_id, entity, record_id as commentary_id,
        json_value(payload, '$.table') as table_key,
        json_value(payload, '$.kind') as entry_kind,
        json_value(payload, '$.topic') as topic,
        json_value(payload, '$.status') as status,
        json_value(payload, '$.claim_type') as claim_type,
        json_value(payload, '$.explanation') as explanation,
        json_value(payload, '$.display.text') as display_text,
        json_value(payload, '$.display.reviewed') = 'true' as reviewed,
        payload as commentary_payload, created_at
    from {{ source('formal_review_raw', 'raw_review_results') }}
    where record_kind = 'commentary'
    qualify row_number() over(partition by run_id, entity, record_id order by created_at desc) = 1
)
select c.*, a.final_report_accepted
from commentary c
join {{ ref('fct_loan_review_acceptance') }} a using(run_id, entity)
