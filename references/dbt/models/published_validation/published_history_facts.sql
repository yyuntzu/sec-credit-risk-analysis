{{ config(materialized='view', tags=['loan_review_published']) }}
select r.publication_id,r.run_id,r.attempt_id,r.entity,r.scope,c.report_mode,c.source_hash,c.plan_hash,c.code_hash,c.precision_version,
 json_value(c.commit_payload,'$.calculation_receipt_sha256') as calculation_receipt_sha256,
 r.record_id as fact_id,json_value(r.payload,'$.metric') as metric,json_value(r.payload,'$.period_role') as period_role,
 json_value(r.payload,'$.unit') as unit,json_value(r.payload,'$.status') as status,
 json_value(r.payload,'$.value') as value_exact,
 if(json_value(r.payload,'$.unit')!='text',cast(json_value(r.payload,'$.value') as bignumeric),null) as value_numeric,
 r.payload as fact_payload,true as published,'validation' as deployment
from {{ ref('stg_publication_records') }} r join {{ ref('int_publication_checks') }} c using(table_publication_id)
where r.record_kind='fact' and c.publication_valid
