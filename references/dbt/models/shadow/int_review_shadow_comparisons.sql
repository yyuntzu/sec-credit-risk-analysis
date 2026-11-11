{{ config(materialized='table', tags=['formal_review_shadow']) }}
with preferred as (
 select * from {{ ref('fct_review_shadow_facts') }}
 where unit!='text' and not contains_substr(fact_id,':pct:')
 qualify row_number() over(partition by run_id,entity,metric,period_role order by starts_with(fact_id,'input:'))=1
), metadata as (
 select run_id,entity,json_value(payload,'$.scope') as scope,
 json_value(payload,'$.source_hash') as source_hash,json_value(payload,'$.plan_hash') as plan_hash,
 json_value(payload,'$.precision_version') as precision_version,
 json_value(payload,'$.request.mode') as mode
 from {{ ref('stg_review_shadow_inputs') }} where record_kind='metadata'
), metrics as (select distinct run_id,entity,metric,unit from preferred), pairs as (
 select m.*,kind,
 if(mode='annual','fy_t_minus_1',if(kind='income','prior_interim','latest_fy_end')) as before_role,
 if(mode='annual','fy_t','current_interim') as after_role
 from metadata m,unnest(['income','balance']) kind
), endpoints as (
 select p.*,m.metric,m.unit,b.fact_id as before_fact_id,a.fact_id as after_fact_id,
 b.status as before_status,a.status as after_status,
 if(b.status in ('sourced','calculated'),cast(b.value as bignumeric),null) as before_value,
 if(a.status in ('sourced','calculated'),cast(a.value as bignumeric),null) as after_value
 from pairs p join metrics m using(run_id,entity)
 left join preferred b on b.run_id=p.run_id and b.entity=p.entity and b.metric=m.metric and b.period_role=p.before_role
 left join preferred a on a.run_id=p.run_id and a.entity=p.entity and a.metric=m.metric and a.period_role=p.after_role
), calculated as (
 select *,after_value-before_value as change,
 if(before_value>0,{{ shadow_checked_divide('after_value-before_value','before_value') }},null) as growth,
 if(before_value is null or after_value is null,'missing','available') as status,
 case when before_value is null or after_value is null then 'not_comparable'
 when after_value=before_value then 'unchanged' when after_value>before_value then 'increased' else 'decreased' end as direction
 from endpoints
)
select *,false as publication_eligible from calculated
