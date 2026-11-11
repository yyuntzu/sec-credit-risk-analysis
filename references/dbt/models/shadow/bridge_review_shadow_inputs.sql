{{ config(materialized='table', tags=['formal_review_shadow']) }}
select f.run_id,f.entity,f.fact_id as output_fact_id,pos as input_position,iid as input_fact_id,
 f.source_hash,f.plan_hash,f.precision_version
from {{ ref('fct_review_shadow_facts') }} f,unnest(f.input_ids) iid with offset pos
