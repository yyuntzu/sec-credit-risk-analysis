{{ config(materialized='view', tags=['formal_review_archive']) }}
select run_id,attempt_id,entity,scope,fact_id,eid as evidence_id,'direct' as relationship,
 content_sha256,archive_integrity_passed,false as publication_eligible
from {{ ref('fct_review_candidate_facts') }},unnest(evidence_ids) eid
union all
select run_id,attempt_id,entity,scope,fact_id,eid,'source',content_sha256,archive_integrity_passed,false
from {{ ref('fct_review_candidate_facts') }},unnest(source_evidence_ids) eid
