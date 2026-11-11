{{ config(severity='error', tags=['formal_review_archive']) }}
with failures as (
 select attempt_id as key from {{ ref('int_review_candidate_checks') }} where not archive_integrity_passed or publication_eligible
 union all
 select fact_id from {{ ref('fct_review_candidate_facts') }} where publication_eligible
 or (status in ('sourced','calculated') and value is null)
 or (status not in ('sourced','calculated') and value is not null)
 union all
 select b.output_fact_id from {{ ref('bridge_review_candidate_inputs') }} b
 left join {{ ref('fct_review_candidate_facts') }} f
 on f.run_id=b.run_id and f.attempt_id=b.attempt_id and f.entity=b.entity and f.scope=b.scope and f.fact_id=b.input_fact_id
 where f.fact_id is null or f.status not in ('sourced','calculated')
 union all
 select b.fact_id from {{ ref('bridge_review_candidate_evidence') }} b
 left join {{ ref('fct_review_candidate_evidence') }} e
 on e.run_id=b.run_id and e.attempt_id=b.attempt_id and e.entity=b.entity and e.scope=b.scope and e.evidence_id=b.evidence_id
 where e.evidence_id is null
)
select * from failures
