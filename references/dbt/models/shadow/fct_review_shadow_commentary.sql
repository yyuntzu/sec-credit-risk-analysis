{{ config(materialized='table', tags=['formal_review_shadow']) }}
with metadata as (
 select run_id,entity,json_value(payload,'$.scope') as scope,
 json_value(payload,'$.source_hash') as source_hash,json_value(payload,'$.plan_hash') as plan_hash,
 json_value(payload,'$.precision_version') as precision_version,
 json_value(payload,'$.request.currency') as currency,cast(json_value(payload,'$.request.as_of') as date) as as_of,
 json_value_array(payload,'$.excluded_observation_ids') as excluded_ids,
 if(json_value(payload,'$.request.mode')='annual','fy_t_minus_1','latest_fy_end') as before_role,
 if(json_value(payload,'$.request.mode')='annual','fy_t','current_interim') as after_role
 from {{ ref('stg_review_shadow_inputs') }} where record_kind='metadata'
), preferred as (
 select * from {{ ref('fct_review_shadow_facts') }} where not contains_substr(fact_id,':pct:')
 qualify row_number() over(partition by run_id,entity,metric,period_role order by starts_with(fact_id,'input:'))=1
), ratios as (
 select run_id,entity,record_id as metric,json_value(payload,'$.numerator') as numerator,
 json_value(payload,'$.denominator') as denominator
 from {{ ref('stg_review_shadow_inputs') }} where record_kind='commentary_ratio'
), ratio_rows as (
 select r.run_id,r.entity,'ratio' as record_kind,r.metric as record_id,
 to_json_string(struct(r.metric,
   cast(v.before_value as string) as before,cast(v.after_value as string) as after,
   cast(v.change as string) as change,cast(v.growth as string) as growth,v.status,
   array(select fid from unnest([if(v.before_value is not null,v.before_fact_id,null),if(v.after_value is not null,v.after_fact_id,null)]) fid where fid is not null) as fact_ids,
   struct(r.numerator as metric,{{ shadow_change_fields('n.before_value','n.after_value') }}) as numerator,
   struct(r.denominator as metric,{{ shadow_change_fields('d.before_value','d.after_value') }}) as denominator,
   coalesce(b.definition,a.definition,'') as definition,
   case when n.before_value>0 and n.after_value>0 and d.before_value>0 and d.after_value>0 then
     case when n.growth>d.growth then 'numerator_faster' when n.growth<d.growth then 'denominator_faster' else 'equal' end
   else 'not_comparable' end as relative_growth)) as payload
 from ratios r
 join {{ ref('int_review_shadow_comparisons') }} v on v.run_id=r.run_id and v.entity=r.entity and v.kind='balance' and v.metric=r.metric
 join {{ ref('int_review_shadow_comparisons') }} n on n.run_id=r.run_id and n.entity=r.entity and n.kind='balance' and n.metric=r.numerator
 join {{ ref('int_review_shadow_comparisons') }} d on d.run_id=r.run_id and d.entity=r.entity and d.kind='balance' and d.metric=r.denominator
 left join preferred b on b.run_id=r.run_id and b.entity=r.entity and b.fact_id=v.before_fact_id and b.status in ('sourced','calculated')
 left join preferred a on a.run_id=r.run_id and a.entity=r.entity and a.fact_id=v.after_fact_id and a.status in ('sourced','calculated')
), component_keys as (
 select distinct run_id,entity,concept,field_name,component_group from {{ ref('int_review_shadow_commentary_components') }} where component_group is not null
), component_pairs as (
 select k.*,b.value as before_value,a.value as after_value,
 if(b.signatures=1,to_json_string(b.sources),'[]') as before_sources_json,
 if(a.signatures=1,to_json_string(a.sources),'[]') as after_sources_json
 from component_keys k join metadata m using(run_id,entity)
 left join {{ ref('int_review_shadow_commentary_components') }} b on b.run_id=k.run_id and b.entity=k.entity and b.concept=k.concept and b.period_role=m.before_role
 left join {{ ref('int_review_shadow_commentary_components') }} a on a.run_id=k.run_id and a.entity=k.entity and a.concept=k.concept and a.period_role=m.after_role
), component_rows as (
 select run_id,entity,'component' as record_kind,concept as record_id,
 to_json_string(struct(concept,field_name,component_group as `group`,
 {{ shadow_change_fields('before_value','after_value') }},
 before_sources_json,after_sources_json,
 row_number() over(partition by run_id,entity order by (after_value-before_value) is null,abs(after_value-before_value) desc,concept) as position)) as payload
 from component_pairs
), total_keys as (
 select i.run_id,i.entity,json_value(i.payload,'$.total_metric') as metric,json_value(p,'$.role') as period_role
 from {{ ref('stg_review_shadow_inputs') }} i join metadata m using(run_id,entity)
 join {{ ref('stg_review_shadow_inputs') }} x on x.run_id=i.run_id and x.entity=i.entity and x.record_kind='metadata',
 unnest(json_query_array(x.payload,'$.request.periods')) p
 where i.record_kind='commentary_concept' and json_value(i.payload,'$.total_metric') is not null
 and json_value(p,'$.role') in (m.before_role,m.after_role)
), totals as (
 select k.*,s.value as source_value,if(f.status in ('sourced','calculated'),cast(f.value as bignumeric),null) as canonical_value,
 s.value-if(f.status in ('sourced','calculated'),cast(f.value as bignumeric),null) as difference
 from total_keys k
 left join {{ ref('int_review_shadow_commentary_components') }} s
 on s.run_id=k.run_id and s.entity=k.entity and s.period_role=k.period_role and s.total_metric=k.metric
 left join preferred f on f.run_id=k.run_id and f.entity=k.entity and f.metric=k.metric and f.period_role=k.period_role
), total_rows as (
 select run_id,entity,'total_check' as record_kind,concat(metric,':',period_role) as record_id,
 to_json_string(struct(metric,period_role,if(difference is null,'missing',if(difference=0,'matched','conflict')) as status,cast(difference as string) as difference)) as payload
 from totals
), report_groups as (
 select m.run_id,m.entity,g as component_group,role as period_role
 from metadata m,unnest(['current_assets','current_liabilities']) g,unnest([m.before_role,m.after_role]) role
), group_lines as (
 select g.*,ifnull(array_agg(s.concept ignore nulls order by s.concept),array<string>[]) as selected_concepts,
 count(s.concept) as line_count,sum(s.value) as selected_sum,
 countif(s.concept in ('PrepaidExpenseAndOtherAssetsCurrent','OtherAssetsCurrent'))=2 as overlapping
 from report_groups g left join {{ ref('int_review_shadow_commentary_components') }} s
 on s.run_id=g.run_id and s.entity=g.entity and s.period_role=g.period_role and s.component_group=g.component_group and s.signatures=1
 group by g.run_id,g.entity,g.component_group,g.period_role
), group_assessed as (
 select g.*,if(f.status in ('sourced','calculated'),cast(f.value as bignumeric),null) as canonical_total,
 if(g.line_count>0 and not g.overlapping,g.selected_sum,null) as amount,
 t.difference as total_difference
 from group_lines g left join preferred f
 on f.run_id=g.run_id and f.entity=g.entity and f.metric=g.component_group and f.period_role=g.period_role
 left join totals t on t.run_id=g.run_id and t.entity=g.entity and t.metric=g.component_group and t.period_role=g.period_role
), group_results as (
 select *,canonical_total-amount as residual,
 case when total_difference!=0 then 'conflict' when overlapping then 'overlapping_components'
 when canonical_total-amount=0 then 'matched_selected_lines' else 'partial_not_reconciled' end as status
 from group_assessed
), group_rows as (
 select run_id,entity,'component_reconciliation' as record_kind,concat(component_group,':',period_role) as record_id,
 to_json_string(struct(component_group as `group`,period_role,status,selected_concepts,
 cast(amount as string) as selected_sum,cast(canonical_total as string) as canonical_total,cast(residual as string) as unexplained_residual)) as payload
 from group_results
), coverage_rows as (
 select run_id,entity,'coverage' as record_kind,component_group as record_id,
 to_json_string(struct(if(countif(status='matched_selected_lines')=2,'matched_selected_lines','partial_not_reconciled') as status)) as payload
 from group_results group by run_id,entity,component_group
), limitations as (
 select run_id,entity,'limitation' as record_kind,record_id,json_value(payload,'$.text') as text
 from {{ ref('stg_review_shadow_inputs') }} where record_kind='commentary_limitation'
 union all
 select run_id,entity,'limitation',concat('conflict:',concept,':',period_role),'Conflicting source values: '||concept||'/'||period_role
 from {{ ref('int_review_shadow_commentary_components') }} where signatures>1
 union all
 select i.run_id,i.entity,'limitation','currency:'||i.record_id,'Component currency mismatch: '||json_value(i.payload,'$.tag')
 from {{ ref('stg_review_shadow_inputs') }} i join metadata m using(run_id,entity)
 join {{ ref('stg_review_shadow_inputs') }} c on c.run_id=i.run_id and c.entity=i.entity and c.record_kind='commentary_concept' and c.record_id=json_value(i.payload,'$.tag')
 where (i.record_kind='commentary_observation' or i.record_kind='observation' and json_value(i.payload,'$.origin')='sec' and i.record_id not in unnest(m.excluded_ids))
 and json_value(i.payload,'$.namespace')='us-gaap' and json_value(i.payload,'$.status')='sourced'
 and json_value(i.payload,'$.period_kind')='instant' and json_value(i.payload,'$.start') is null
 and json_value(i.payload,'$.scope')=m.scope and json_value(i.payload,'$.entity')=m.entity
 and cast(json_value(i.payload,'$.document_date') as date)<=m.as_of and json_value(i.payload,'$.unit')!=m.currency
), records as (
 select * from ratio_rows union all select * from component_rows union all select * from total_rows
 union all select * from group_rows union all select * from coverage_rows
 union all select run_id,entity,record_kind,record_id,to_json_string(struct(text)) as payload from limitations
 union all select run_id,entity,'comparison',concat(kind,':',metric),
 to_json_string(struct(kind,metric,unit,before_role,after_role,before_fact_id,after_fact_id,before_status,after_status,
 cast(before_value as string) as before,cast(after_value as string) as after,cast(change as string) as change,cast(growth as string) as growth,status,direction))
 from {{ ref('int_review_shadow_comparisons') }}
)
select m.run_id,m.entity,m.scope,m.source_hash,m.plan_hash,m.precision_version,r.record_kind,r.record_id,r.payload,
 false as publication_eligible
from records r join metadata m using(run_id,entity)
