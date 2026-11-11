{{ config(materialized='table', tags=['formal_review_shadow']) }}
-- Independent source selection: no Python inputs/value/status enter this model.
with observations as (
 select run_id, entity, record_id as observation_id,
 json_value(payload,'$.origin') as origin,
 json_value(payload,'$.scope') as scope,
 json_value(payload,'$.metric') as metric,
 json_value(payload,'$.field_name') as field_name,
 json_value(payload,'$.namespace') as namespace,
 json_value(payload,'$.tag') as tag,
 json_value(payload,'$.start') as start, json_value(payload,'$.end') as `end`,
 json_value(payload,'$.unit') as unit,
 cast(json_value(payload,'$.scale') as bignumeric) as original_scale,
 json_value(payload,'$.value') as original_value,
 cast(json_value(payload,'$.source_quantum') as bignumeric) as original_quantum,
 json_value(payload,'$.status') as source_status,
 json_value(payload,'$.definition') as definition,
 json_value(payload,'$.basis') as basis,
 cast(json_value(payload,'$.document_date') as date) as document_date,
 json_value(payload,'$.filing_type') as filing_type
 from {{ ref('stg_review_shadow_inputs') }} where record_kind='observation'
), matches as (
 select s.run_id,s.entity,s.fact_id,o.* except(run_id,entity),s.source_unit,s.scale,
 max(o.document_date) over(partition by s.run_id,s.entity,s.fact_id,o.origin,o.namespace,o.tag,o.definition,o.basis) as latest_date
 from {{ ref('stg_review_shadow_slots') }} s join observations o
 on s.run_id=o.run_id and s.entity=o.entity and s.scope=o.scope
 and s.start is not distinct from o.start and s.end=o.end
 and (o.metric=s.metric or o.origin='sec' and o.field_name in unnest(s.sec_fields))
 where s.source_allowed and o.document_date<=s.as_of
), amended as (
 select *, countif(document_date=latest_date and filing_type not in ('10-K/A','10-Q/A')) over(
 partition by run_id,entity,fact_id,origin,namespace,tag,definition,basis) as latest_not_amended
 from matches
), chosen as (
 select *, unit=source_unit and (origin!='sec' or latest_not_amended>0 or document_date=latest_date) as selected,
 if(unit='text',null,cast(original_value as bignumeric)*original_scale/scale) as normalized
 from amended
), summaries as (
 select run_id,entity,fact_id,
 array_agg(observation_id order by observation_id) as candidate_ids,
 countif(unit!=source_unit) as bad_units,
 count(distinct if(selected,to_json_string(struct(source_status,normalized,if(unit='text',original_value,null),basis,definition)),null)) as signatures,
 array_agg(if(selected,struct(observation_id,source_status,original_value,original_scale,normalized,basis,definition,original_quantum),null) ignore nulls order by observation_id) as selected,
 countif(selected and unit!='text' and original_value is not null and normalized*scale!=cast(original_value as bignumeric)*original_scale)>0 as normalization_loss
 from chosen group by run_id,entity,fact_id
)
select s.*,coalesce(c.candidate_ids,array<string>[]) as candidate_ids,
 coalesce(c.bad_units,0) as bad_units,coalesce(c.signatures,0) as signatures,
 coalesce(c.selected,array<struct<observation_id string,source_status string,original_value string,original_scale bignumeric,normalized bignumeric,basis string,definition string,original_quantum bignumeric>>[]) as selected,
 coalesce(c.normalization_loss,false) as normalization_loss
from {{ ref('stg_review_shadow_slots') }} s left join summaries c using(run_id,entity,fact_id)
