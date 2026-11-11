{{ config(materialized='table', tags=['formal_review_shadow']) }}
-- Review claims are raw input. Every numeric result, source bound and eligibility
-- flag below is recomputed from SQL facts, never supplied by a Python PASS flag.
with preferred_facts as (
 select * from {{ ref('int_review_shadow_calculated') }}
 qualify row_number() over(partition by run_id,entity,period_role,metric order by starts_with(fact_id,'input:'),contains_substr(fact_id,':pct:'))=1
), roles as (
 select distinct run_id,entity,scope,period_role,currency,scale,as_of
 from {{ ref('int_review_shadow_calculated') }} where unit='money'
), equations as (
 select r.*, 'balance_sheet_equation' as kind,
 'total_assets' as reported_metric,['total_liabilities','net_worth'] as term_metrics from roles r
 union all
 select r.*, 'cash_bridge' as kind,
 'ending_cash' as reported_metric,['beginning_cash','cfo','cfi','cff','cash_fx','cash_other'] as term_metrics from roles r
), diagnostic_terms as (
 select e.run_id,e.entity,e.period_role,e.kind,
 countif(f.status is null or f.status not in ('sourced','calculated')) as unavailable,
 max(if(pos=0,cast(f.value as bignumeric),null)) as reported_value,
 sum(if(pos>0,cast(f.value as bignumeric),cast(0 as bignumeric))) as calculated_value
 from equations e,unnest(array_concat([e.reported_metric],e.term_metrics)) metric with offset pos
 left join preferred_facts f
 on f.run_id=e.run_id and f.entity=e.entity and f.period_role=e.period_role and f.metric=metric
 group by e.run_id,e.entity,e.period_role,e.kind
), reviews as (
 select run_id,entity,json_value(payload,'$.kind') as kind,json_value(payload,'$.period_role') as period_role,
 record_id as review_id,json_value(payload,'$.status') as submitted_status,
 json_value(payload,'$.reported_fact_id') as reported_fact_id,
 json_query_array(payload,'$.terms') as terms,json_value_array(payload,'$.evidence_ids') as evidence_ids,
 safe_cast(coalesce(json_value(payload,'$.tolerance'),'0') as bignumeric) as tolerance,
 safe_cast(json_value(payload,'$.calculated_value') as bignumeric) as claimed_calculated,
 safe_cast(json_value(payload,'$.reported_value') as bignumeric) as claimed_reported,
 safe_cast(json_value(payload,'$.difference') as bignumeric) as claimed_difference,
 json_value(payload,'$.binding_hash') as binding_hash
 from {{ ref('stg_review_shadow_inputs') }} where record_kind='reconciliation_review'
), review_evidence as (
 select run_id,entity,record_id as evidence_id,json_value(payload,'$.scope') as scope,
 json_value(payload,'$.kind') as kind,json_value_array(payload,'$.period_roles') as period_roles,
 json_value(payload,'$.binding_hash') as binding_hash,
 cast(json_value(payload,'$.document_date') as date) as document_date
 from {{ ref('stg_review_shadow_inputs') }} where record_kind='review_evidence'
), reviewed_components as (
 select e.*,r.* except(run_id,entity,kind,period_role),
 array_length(e.term_metrics) as expected_terms,
 f.metric as actual_reported_metric,
 f.start as reported_start,f.end as reported_end,f.expected_start as reported_expected_start,f.expected_end as reported_expected_end,
 f.value as reported_value,f.status as reported_status,f.unit as reported_unit,
 f.currency as reported_currency,f.scope as reported_scope,f.period_role as reported_role,
 f.source_precision_bound as reported_bound,f.source_evidence_ids as reported_sources,
 -- Select explicit ordered IDs; never substitute a metric with a matching amount.
 array(
 select as struct json_value(t,'$.fact_id') as fact_id,
 safe_cast(json_value(t,'$.coefficient') as bignumeric) as coefficient,
 array_length(json_keys(parse_json(t),1))=2 and json_value(t,'$.fact_id') is not null and json_query(t,'$.coefficient') is not null as keys_valid,pos as position
 from unnest(r.terms) t with offset pos order by pos) as explicit_terms
 from equations e left join reviews r using(run_id,entity,kind,period_role)
 left join {{ ref('int_review_shadow_calculated') }} f
 on f.run_id=e.run_id and f.entity=e.entity and f.fact_id=r.reported_fact_id
), resolved_terms as (
 select c.run_id,c.entity,c.period_role,c.kind,
 array_agg(if(t.fact_id is null,null,struct(t.fact_id,t.coefficient,t.position,t.keys_valid,
   f.metric,f.start,f.end,f.expected_start,f.expected_end,f.period_role,f.scope,f.unit,f.currency,f.status,f.value,f.source_precision_bound,f.source_evidence_ids)) ignore nulls order by t.position) as components,
 count(distinct t.fact_id) as distinct_terms
 from reviewed_components c
 left join unnest(c.explicit_terms) t on true
 left join {{ ref('int_review_shadow_calculated') }} f on f.run_id=c.run_id and f.entity=c.entity and f.fact_id=t.fact_id
 group by c.run_id,c.entity,c.period_role,c.kind
), evidence_checks as (
 select c.run_id,c.entity,c.period_role,c.kind,
 countif(e.evidence_id is null or e.scope!=c.scope or c.period_role not in unnest(e.period_roles)
   or e.document_date is null or e.document_date>c.as_of) as bad_evidence,
 countif(e.kind='fact')>0 as has_source_fact,
 countif(e.kind in ('review','definition') and e.binding_hash=c.binding_hash)>0 as binding_matches,
 ifnull(array_agg(if(e.kind='definition' and e.binding_hash=c.binding_hash,e.evidence_id,null) ignore nulls order by e.evidence_id),array<string>[]) as cash_definition_ids
 from reviewed_components c left join unnest(c.evidence_ids) eid on true
 left join review_evidence e on e.run_id=c.run_id and e.entity=c.entity and e.evidence_id=eid
 group by c.run_id,c.entity,c.period_role,c.kind
), assessed as (
 select c.*,t.components,t.distinct_terms,ec.* except(run_id,entity,period_role,kind),
 (select sum(cast(x.value as bignumeric)) from unnest(t.components) x) as reviewed_calculated,
 c.reported_bound+(select sum(x.source_precision_bound) from unnest(t.components) x) as maximum_tolerance,
 array(select distinct eid from unnest(t.components) x,unnest(x.source_evidence_ids) eid) as required_sources
 from reviewed_components c join resolved_terms t using(run_id,entity,period_role,kind)
 join evidence_checks ec using(run_id,entity,period_role,kind)
), eligibility as (
 select a.*,
 coalesce(review_id is not null and submitted_status in ('matched','within_precision')
 and array_length(terms)=expected_terms and distinct_terms=expected_terms
 and reported_fact_id not in (select x.fact_id from unnest(components) x)
 and array_length(evidence_ids)=(select count(distinct eid) from unnest(evidence_ids) eid)
 and bad_evidence=0 and has_source_fact and binding_matches
 and actual_reported_metric=reported_metric
 and reported_start is not distinct from reported_expected_start and reported_end=reported_expected_end
 and reported_status in ('sourced','calculated') and reported_unit='money'
 and reported_scope=scope and reported_currency=currency and reported_role=period_role
 and tolerance>=0 and maximum_tolerance is not null and tolerance<=maximum_tolerance
 and not exists(select 1 from unnest(components) x
  where x.metric is distinct from term_metrics[safe_offset(x.position)]
  or x.status is null or x.status not in ('sourced','calculated') or x.unit!='money'
  or x.scope is distinct from a.scope or x.currency is distinct from a.currency
  or x.period_role is distinct from a.period_role or x.coefficient is distinct from cast(1 as bignumeric)
  or x.source_precision_bound is null or not x.keys_valid
  or x.start is distinct from x.expected_start or x.end is distinct from x.expected_end)
 and not exists(select 1 from unnest(array_concat(required_sources,reported_sources)) eid where eid not in unnest(evidence_ids))
 and claimed_calculated=reviewed_calculated and claimed_reported=cast(reported_value as bignumeric)
 and claimed_difference=reviewed_calculated-cast(reported_value as bignumeric),false) as eligible
 from assessed a
), results as (
 select *,
 case when review_id is null then 'not_calculable'
 when submitted_status not in ('matched','within_precision') then coalesce(submitted_status,'not_calculable')
 when not eligible then 'not_calculable'
 when reviewed_calculated=cast(reported_value as bignumeric) then 'matched'
 when abs(reviewed_calculated-cast(reported_value as bignumeric))<=tolerance then 'within_precision'
 else 'unexplained_difference' end as status
 from eligibility
)
select r.run_id,r.entity,r.scope,r.period_role,r.kind,r.status,
 r.eligible and r.status in ('matched','within_precision') as verified,
 if(r.eligible,r.reviewed_calculated,null) as calculated_value,
 if(r.eligible,cast(r.reported_value as bignumeric),null) as reported_value,
 if(r.eligible,r.reviewed_calculated-cast(r.reported_value as bignumeric),null) as difference,
 r.tolerance,r.maximum_tolerance,r.reported_fact_id,
 if(r.kind='cash_bridge',r.components[safe_offset(0)].fact_id,null) as beginning_fact_id,
 r.cash_definition_ids,
 d.unavailable,if(d.unavailable=0,d.calculated_value-d.reported_value,null) as diagnostic_difference,
 case when r.review_id is null then 'review_not_supplied' when not r.eligible then 'review_or_source_validation_failed'
 else 'reviewed_equation_recomputed' end as reason,
 false as publication_eligible
from results r join diagnostic_terms d using(run_id,entity,period_role,kind)
