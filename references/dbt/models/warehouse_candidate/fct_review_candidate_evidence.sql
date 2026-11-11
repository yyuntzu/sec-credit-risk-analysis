{{ config(materialized='view', tags=['formal_review_archive']) }}
select r.run_id,r.attempt_id,r.entity,r.scope,c.content_sha256,c.archive_integrity_passed,
 r.record_id as evidence_id,json_value(r.payload,'$.kind') as kind,json_value(r.payload,'$.source_id') as source_id,
 json_value(r.payload,'$.version') as source_version,json_value(r.payload,'$.document_date') as document_date,
 json_value(r.payload,'$.locator') as locator,json_value(r.payload,'$.content') as content,
 json_value_array(r.payload,'$.period_roles') as period_roles,false as publication_eligible
from {{ ref('stg_review_candidate_records') }} r join {{ ref('int_review_candidate_checks') }} c using(table_attempt_id)
where r.record_kind='evidence'
