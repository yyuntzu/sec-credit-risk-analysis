{{ config(materialized='table', tags=['formal_review_shadow']) }}
with source_contract as (
 select s.*,p.required_decisions as canonical_pending,p.definition as canonical_definition
 from {{ ref('int_review_shadow_selection') }} s
 left join {{ ref('dim_review_shadow_metric_policies') }} p on p.metric=s.metric
), classified as (
 select c.*,
 case
 when not source_allowed then 'not_calculable'
 when `end` is null or (start is null and period_kind!='instant') then 'missing'
 when bad_units>0 or signatures>1 then if(array_length(candidate_ids)>1,'conflict','not_calculable')
 when array_length(selected)=0 then 'missing'
 when exists(select 1 from unnest(canonical_pending) d where d not in unnest(approved_decisions)) then 'not_calculable'
 when exists(select 1 from unnest(canonical_pending) d where d='DEC-03') then 'not_calculable'
 when selected[safe_offset(0)].source_status='sourced' and array_length(canonical_pending)>0
 and (exists(select 1 from unnest(selected) x where x.definition!=coalesce(c.canonical_definition,c.definition))
 or metric in ('ltm_ebitda','ebitda_basis') and selected[safe_offset(0)].basis!=standard_basis) then 'not_calculable'
 when selected[safe_offset(0)].source_status='not_disclosed' then 'missing'
 else selected[safe_offset(0)].source_status end as status
 from source_contract c
)
select * except(selected,definition),
 if(status='sourced' and unit='money',selected[safe_offset(0)].original_quantum*selected[safe_offset(0)].original_scale/scale/2,null) as source_precision_bound,
 if(status='sourced',selected[safe_offset(0)].definition,definition) as definition,
 if(status='sourced',if(unit='text',selected[safe_offset(0)].original_value,cast(selected[safe_offset(0)].normalized as string)),null) as value,
 if(status='sourced',coalesce(selected[safe_offset(0)].basis,''),'') as basis,
 if(status='conflict',candidate_ids,array(select x.observation_id from unnest(selected) x order by x.observation_id)) as evidence_ids,
 cast(null as string) as formula_id, cast(null as string) as formula_version,
 array<string>[] as input_ids,
 if(status='sourced',selected[safe_offset(0)].original_value,null) as original_value,
 if(status='sourced' and unit!='text',cast(selected[safe_offset(0)].original_scale as string),null) as original_scale
from classified
