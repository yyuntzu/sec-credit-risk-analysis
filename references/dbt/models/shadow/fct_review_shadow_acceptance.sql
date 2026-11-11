{{ config(materialized='table', tags=['formal_review_shadow']) }}
-- Financial readiness is separate from precision approval and publication.
with metadata as (
 select run_id,entity,json_value(payload,'$.scope') as scope,
 json_value(payload,'$.source_hash') as source_hash,json_value(payload,'$.plan_hash') as plan_hash,
 json_value(payload,'$.precision_version') as precision_version,
 json_value_array(payload,'$.required_fact_ids') as required_fact_ids,
 json_value_array(payload,'$.source_limitations') as source_limitations,
 json_value_array(payload,'$.decisions') as decisions,
 array_length(json_query_array(payload,'$.request.periods'))*2 as expected_reconciliations
 from {{ ref('stg_review_shadow_inputs') }} where record_kind='metadata'
), required_cells as (
 select m.run_id,m.entity,
 array_agg(if(f.status is null or f.status not in ('sourced','calculated'),fid,null) ignore nulls order by fid) as unavailable_fact_ids
 from metadata m,unnest(m.required_fact_ids) fid
 left join {{ ref('fct_review_shadow_facts') }} f on f.run_id=m.run_id and f.entity=m.entity and f.fact_id=fid
 group by m.run_id,m.entity
), reconciliations as (
 select run_id,entity,count(*) as reconciliation_count,countif(verified) as verified_reconciliations
 from {{ ref('fct_review_shadow_reconciliations') }} group by run_id,entity
), assessed as (
 select m.*,c.unavailable_fact_ids,r.reconciliation_count,r.verified_reconciliations,
 array_concat(
   m.source_limitations,
   if(array_length(c.unavailable_fact_ids)>0,['Required report cells are unavailable or definitions unresolved'],array<string>[]),
   if('DEC-08' not in unnest(m.decisions),['DEC-08 missing-data/delivery policy remains unapproved'],array<string>[]),
   if('DEC-09' not in unnest(m.decisions),['DEC-09 presentation policy remains unapproved'],array<string>[]),
   if(r.reconciliation_count is distinct from m.expected_reconciliations or r.verified_reconciliations is distinct from m.expected_reconciliations,
      ['Reconciliation is incomplete or contains unexplained differences'],array<string>[])
 ) as acceptance_blockers
 from metadata m join required_cells c using(run_id,entity)
 left join reconciliations r using(run_id,entity)
)
select *,array_length(acceptance_blockers)=0 as substantive_data_ready,
 false as precision_approved,false as final_report_accepted,false as publication_eligible
from assessed
