{{ config(tags=['formal_review_marts']) }}
-- Run-scoped keys and evidence references must remain unique and complete.
with failures as (
select run_id, fact_id as key from {{ ref('fct_loan_review_facts') }} group by 1,2 having count(*) != 1
union all
select run_id, evidence_id from {{ ref('dim_loan_review_evidence') }} group by 1,2 having count(*) != 1
union all
select b.run_id, b.fact_id from {{ ref('bridge_loan_review_evidence') }} b
left join {{ ref('fct_loan_review_facts') }} f using(run_id, fact_id)
left join {{ ref('dim_loan_review_evidence') }} e using(run_id, evidence_id)
where f.fact_id is null or e.evidence_id is null
union all
select run_id, fact_id from {{ ref('fct_loan_review_facts') }}
where status not in ('sourced','calculated') and value_exact is not null
union all
select f.run_id, f.fact_id from {{ ref('fct_loan_review_facts') }} f
where f.report_scale is null or f.review_mode not in ('annual','quarterly')
)
select * from failures
