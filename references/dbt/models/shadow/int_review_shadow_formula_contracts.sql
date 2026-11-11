{{ config(materialized='table', tags=['formal_review_shadow']) }}
with periods as (
 select m.run_id,m.entity,json_value(m.payload,'$.request.mode') as mode,
 json_value(m.payload,'$.request.currency') as currency,
 cfg.formula_version,cfg.policy_version,
 json_value(p,'$.role') as role,json_value(p,'$.start') as start,
 json_value(p,'$.end') as `end`,json_value(p,'$.ltm_start') as ltm_start,pos,
 lag(json_value(p,'$.role')) over(partition by m.run_id,m.entity order by pos) as previous_role
 from {{ ref('stg_review_shadow_inputs') }} m,unnest(json_query_array(m.payload,'$.request.periods')) p with offset pos
 cross join {{ ref('dim_review_shadow_configuration') }} cfg
 where m.record_kind='metadata'
), declared as (
 select f.*,r.* except(formula_id),p.mode,p.currency as request_currency,
 p.formula_version as canonical_version,p.policy_version,
 p.role as canonical_role,{{ shadow_contract_start('f.metric','p') }} as canonical_start,
 {{ shadow_contract_end('f.metric','p') }} as canonical_end,
 if(p.mode='annual',coalesce(p.previous_role,'prior_period_not_in_report'),
    if(p.role='current_interim','prior_interim','prior_period_not_in_report')) as previous_role
 from {{ ref('stg_review_shadow_slots') }} f
 left join {{ ref('dim_review_shadow_formulas') }} r on r.formula_id=f.planned_formula and r.target_metric=f.metric
 left join periods p on p.run_id=f.run_id and p.entity=f.entity and p.role=f.period_role
), edges as (
 select f.run_id,f.entity,f.fact_id,
 countif(
   coalesce(i.metric,regexp_extract(iid,r'^(?:input:)?([^:]+):')) is distinct from f.input_metrics[safe_offset(pos)]
   or coalesce(i.period_role,regexp_extract(iid,r'^(?:input:)?[^:]+:(.+)$')) is distinct from
      if(f.prior_second and pos=1,f.previous_role,f.period_role)
   or i.fact_id is not null and (
     i.unit is distinct from f.input_units[safe_offset(pos)]
     or i.currency is distinct from if(i.unit='money',f.request_currency,null)
     or i.start is distinct from {{ shadow_contract_start('i.metric','ip') }}
     or i.end is distinct from {{ shadow_contract_end('i.metric','ip') }}
     or i.planned_formula is not null and i.depth>=f.depth)
 ) as invalid_edges
 from declared f left join unnest(f.planned_inputs) iid with offset pos on true
 left join {{ ref('stg_review_shadow_slots') }} i on i.run_id=f.run_id and i.entity=f.entity and i.fact_id=iid
 left join periods ip on ip.run_id=i.run_id and ip.entity=i.entity and ip.role=i.period_role
 where f.planned_formula is not null
 group by f.run_id,f.entity,f.fact_id
), assessed as (
 select f.run_id,f.entity,f.fact_id,
 coalesce(f.canonical_role is not null and f.start is not distinct from f.canonical_start and f.end is not distinct from f.canonical_end
 and f.declared_scale=f.scale and f.declared_report_scale=cfg.money_scale
 and f.declared_standard_basis=cfg.standard_basis
 and f.declared_formula_version=cfg.formula_version and f.declared_policy_version=cfg.policy_version
 and f.declared_precision_version=cfg.precision_version and f.declared_precision_approved='false'
 and mp.metric is not null
 and f.unit=if(f.planned_formula='COMMON-SIZE-v1','percent',mp.unit)
 and to_json_string(array(select d from unnest(f.pending) d order by d))=to_json_string(array(select d from unnest(mp.required_decisions) d order by d))
 and (mp.definition is null or f.planned_formula='COMMON-SIZE-v1' or f.definition=mp.definition)
 and f.currency is not distinct from if(f.unit='money',f.request_currency,null)
 and f.period_kind=if(f.metric in ('beginning_cash','ending_cash','current_assets','current_liabilities','quick_assets',
   'total_liabilities','net_worth','total_debt','total_assets','current_ratio','quick_ratio','debt_ratio'),'instant','duration')
 and case when f.planned_formula is null then
   f.metric not in ('current_ratio','quick_ratio','cash_flow_ratio','interest_coverage','ebitda_interest','debt_ratio',
     'revenue_growth','gross_margin','operating_margin','pretax_margin','operating_margin_change','cash_change','total_leverage','ltm_ebitda')
   and not contains_substr(f.fact_id,':pct:')
 else f.target_metric is not null and f.unit=f.target_unit
   and array_length(f.planned_inputs)=array_length(f.input_metrics)
   and f.depth between 1 and 4 and e.invalid_edges=0
   and (starts_with(f.planned_formula,'DER-') and nullif(trim(f.planned_version),'') is not null
     or f.planned_version=if(f.planned_formula='STANDARD-EBITDA-v1',f.policy_version,f.canonical_version))
   and f.source_allowed=(f.planned_formula='STANDARD-EBITDA-v1' or starts_with(f.planned_formula,'DER-'))
 end,false) as formula_contract_valid
 from declared f left join edges e using(run_id,entity,fact_id)
 left join {{ ref('dim_review_shadow_metric_policies') }} mp on mp.metric=f.metric
 cross join {{ ref('dim_review_shadow_configuration') }} cfg
)
select * from assessed
