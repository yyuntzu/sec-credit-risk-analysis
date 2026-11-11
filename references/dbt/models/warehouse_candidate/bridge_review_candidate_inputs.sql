{{ config(materialized='view', tags=['formal_review_archive']) }}
select run_id,attempt_id,entity,scope,fact_id as output_fact_id,input_position,input_fact_id,
 content_sha256,archive_integrity_passed,false as publication_eligible
from {{ ref('fct_review_candidate_facts') }},unnest(input_ids) input_fact_id with offset input_position
