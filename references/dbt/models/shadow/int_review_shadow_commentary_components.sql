{{ config(materialized='table', tags=['formal_review_shadow']) }}
with metadata as (
 select run_id,entity,json_value(payload,'$.scope') as scope,
 json_value(payload,'$.request.currency') as currency,
 cast(json_value(payload,'$.request.as_of') as date) as as_of,
 cast(json_value(payload,'$.scale') as bignumeric) as report_scale,
 json_value_array(payload,'$.excluded_observation_ids') as excluded_ids,
 json_query_array(payload,'$.request.periods') as periods,
 if(json_value(payload,'$.request.mode')='annual','fy_t_minus_1','latest_fy_end') as before_role,
 if(json_value(payload,'$.request.mode')='annual','fy_t','current_interim') as after_role
 from {{ ref('stg_review_shadow_inputs') }} where record_kind='metadata'
), concepts as (
 select run_id,entity,record_id as concept,json_value(payload,'$.field_name') as field_name,
 json_value(payload,'$.group') as component_group,json_value(payload,'$.total_metric') as total_metric
 from {{ ref('stg_review_shadow_inputs') }} where record_kind='commentary_concept'
), observations as (
 select i.run_id,i.entity,i.record_id as observation_id,
 json_value(i.payload,'$.tag') as concept,json_value(i.payload,'$.unit') as unit,
 json_value(i.payload,'$.value') as original_value,cast(json_value(i.payload,'$.scale') as bignumeric) as original_scale,
 json_value(i.payload,'$.end') as endpoint,cast(json_value(i.payload,'$.document_date') as date) as document_date,
 json_value(i.payload,'$.filing_type') as filing_type,
 json_value(i.payload,'$.source_id') as source_id,json_value(i.payload,'$.version') as version,
 json_value(i.payload,'$.locator') as locator
 from {{ ref('stg_review_shadow_inputs') }} i join metadata m using(run_id,entity)
 where (i.record_kind='commentary_observation' or
        i.record_kind='observation' and json_value(i.payload,'$.origin')='sec' and i.record_id not in unnest(m.excluded_ids))
 and json_value(i.payload,'$.namespace')='us-gaap' and json_value(i.payload,'$.status')='sourced'
 and json_value(i.payload,'$.period_kind')='instant' and json_value(i.payload,'$.start') is null
 and json_value(i.payload,'$.scope')=m.scope and json_value(i.payload,'$.entity')=m.entity
 and cast(json_value(i.payload,'$.document_date') as date)<=m.as_of
), matching as (
 select o.*,c.* except(run_id,entity,concept),m.scope,m.report_scale,
 json_value(p,'$.role') as period_role,
 max(o.document_date) over(partition by o.run_id,o.entity,o.concept,json_value(p,'$.role')) as latest_date
 from observations o join metadata m using(run_id,entity) join concepts c using(run_id,entity,concept),unnest(m.periods) p
 where o.unit=m.currency and o.endpoint=json_value(p,'$.end')
 and json_value(p,'$.role') in (m.before_role,m.after_role)
), amendment as (
 select *,countif(document_date=latest_date and not coalesce(filing_type in ('10-K/A','10-Q/A'),false))
 over(partition by run_id,entity,concept,period_role) as latest_not_amended
 from matching
), chosen as (
 select *,cast(original_value as bignumeric)*original_scale/report_scale as normalized
 from amendment where latest_not_amended>0 or document_date=latest_date
), grouped as (
 select run_id,entity,scope,concept,field_name,component_group,total_metric,period_role,
 count(distinct normalized) as signatures,
 if(count(distinct normalized)=1,min(normalized),null) as value,
 countif(normalized*report_scale!=cast(original_value as bignumeric)*original_scale)>0 as normalization_loss,
 array_agg(struct(observation_id as id,source_id,version,locator,cast(document_date as string) as document_date) order by observation_id) as sources
 from chosen group by run_id,entity,scope,concept,field_name,component_group,total_metric,period_role
)
select * from grouped
