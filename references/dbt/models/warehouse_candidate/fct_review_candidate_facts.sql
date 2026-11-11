{{ config(materialized='view', tags=['formal_review_archive']) }}
select r.run_id,r.attempt_id,r.entity,r.scope,c.content_sha256,c.calculation_receipt_sha256,
 c.source_hash,c.plan_hash,c.precision_version,c.archive_integrity_passed,
 r.record_id as fact_id,json_value(r.payload,'$.metric') as metric,json_value(r.payload,'$.period_role') as period_role,
 json_value(r.payload,'$.status') as status,json_value(r.payload,'$.unit') as unit,json_value(r.payload,'$.currency') as currency,
 json_value(r.payload,'$.value') as value,
 if(json_value(r.payload,'$.unit')!='text',cast(json_value(r.payload,'$.value') as bignumeric),null) as value_numeric,
 json_value(r.payload,'$.original_value') as original_value,json_value(r.payload,'$.original_scale') as original_scale,
 json_value(r.payload,'$.definition') as definition,json_value(r.payload,'$.basis') as basis,
 json_value(r.payload,'$.start') as start,json_value(r.payload,'$.end') as `end`,json_value(r.payload,'$.period_kind') as period_kind,
 json_value(r.payload,'$.formula_id') as formula_id,json_value(r.payload,'$.formula_version') as formula_version,
 json_value_array(r.payload,'$.input_ids') as input_ids,json_value_array(r.payload,'$.evidence_ids') as evidence_ids,
 json_value_array(r.payload,'$.source_evidence_ids') as source_evidence_ids,
 r.payload as frozen_fact_payload,false as publication_eligible
from {{ ref('stg_review_candidate_records') }} r join {{ ref('int_review_candidate_checks') }} c using(table_attempt_id)
where r.record_kind='fact'
