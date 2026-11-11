{{ config(materialized='table', tags=['formal_review_shadow']) }}
with initial as (select f.*,c.formula_contract_valid,cast(null as string) as precision_audit,[metric] as ancestor_metrics,if(status='sourced',evidence_ids,array<string>[]) as source_evidence_ids
 from {{ ref('int_review_shadow_adopted') }} f join {{ ref('int_review_shadow_formula_contracts') }} c using(run_id,entity,fact_id)),
-- Stage 0 has only sourced/unavailable facts; every stage depends on earlier values.
{% for stage in range(1,5) %}
args_{{ stage }} as (
 select f.run_id,f.entity,f.fact_id,
 array_agg(if(iid is null,null,struct(iid as id,d.metric,d.status,d.value,d.start,d.end,d.unit,d.currency,d.period_kind,d.period_role,d.basis,d.source_precision_bound,d.source_evidence_ids,d.ancestor_metrics)) ignore nulls order by pos) as args
 from {{ 'initial' if stage==1 else 'stage_' ~ (stage-1) }} f
 left join unnest(f.planned_inputs) iid with offset pos on true
 left join {{ 'initial' if stage==1 else 'stage_' ~ (stage-1) }} d on d.run_id=f.run_id and d.entity=f.entity and d.fact_id=iid
 group by f.run_id,f.entity,f.fact_id
), inputs_{{ stage }} as (
 select f.*,a.args from {{ 'initial' if stage==1 else 'stage_' ~ (stage-1) }} f
 join args_{{ stage }} a using(run_id,entity,fact_id)
), eligible_{{ stage }} as (
 select f.*,
 formula_contract_valid and depth={{ stage }} and status not in ('sourced','calculated','conflict','not_applicable')
 and planned_formula is not null and array_length(planned_inputs)>0
 and not exists(select 1 from unnest(pending) p where p='DEC-03')
 and not exists(select 1 from unnest(pending) p where p not in unnest(approved_decisions))
 and not exists(select 1 from unnest(args) a where a.status is null or a.status not in ('sourced','calculated') or a.value is null)
 and (planned_formula!='STANDARD-EBITDA-v1' or
     (start is not null and not exists(select 1 from unnest(args) a where a.start is distinct from f.start or a.end is distinct from f.`end`)))
 -- Cash identities require explicit reviewed bridges; shadow does not invent them.
 and planned_formula!='CASH-CHANGE-v1'
 and (not starts_with(planned_formula,'DER-') or {{ shadow_identity_eligible() }}) as can_calculate,
 array(select cast(a.value as bignumeric) from unnest(args) a where a.value is not null and a.unit!='text') as amounts
 from inputs_{{ stage }} f
), values_{{ stage }} as (
 select *,if(can_calculate,{{ shadow_financial_formula('planned_formula','amounts') }},cast(null as bignumeric)) as computed,
 if(can_calculate,{{ shadow_financial_formula('planned_formula','amounts',native=true) }},cast(null as bignumeric)) as native_computed,
 {{ shadow_division_operands('planned_formula','amounts') }} as division_operands
 from eligible_{{ stage }}
), stage_{{ stage }} as (
 select * except(args,can_calculate,amounts,computed,native_computed,division_operands,precision_audit,status,value,formula_id,formula_version,input_ids,basis,source_precision_bound,source_evidence_ids,evidence_ids,ancestor_metrics),
 if(computed is not null,to_json_string(struct(precision_version as policy,
   planned_formula not in ('CF-16','CASH-CHANGE-v1','STANDARD-EBITDA-v1','DER-01','DER-02','DER-03','DER-04','DER-05','DER-06') as division,
   cast(division_operands.numerator as string) as numerator,cast(division_operands.denominator as string) as denominator,
   cast(native_computed as string) as native_value,cast(computed as string) as canonical_value)),precision_audit) as precision_audit,
 if(computed is not null,array_concat([metric],array(select distinct m from unnest(args) a,unnest(a.ancestor_metrics) m order by m)),ancestor_metrics) as ancestor_metrics,
 if(computed is not null and starts_with(planned_formula,'DER-'),[json_value(identity_review,'$.evidence.id')],evidence_ids) as evidence_ids,
 case when depth={{ stage }} and planned_formula is not null and status not in ('sourced','calculated','conflict','not_applicable') then
      if(computed is null,'not_calculable','calculated') else status end as status,
 if(computed is not null,cast(computed as string),value) as value,
 if(computed is not null,planned_formula,formula_id) as formula_id,
 if(computed is not null,planned_version,formula_version) as formula_version,
 if(computed is not null,planned_inputs,input_ids) as input_ids,
 if(computed is not null,if(exists(select 1 from unnest(args) a where a.source_precision_bound is null),null,(select sum(a.source_precision_bound) from unnest(args) a)),source_precision_bound) as source_precision_bound,
 if(computed is not null,array(select distinct eid from unnest(args) a,unnest(a.source_evidence_ids) eid order by eid),source_evidence_ids) as source_evidence_ids,
 case when computed is not null and planned_formula='STANDARD-EBITDA-v1' then standard_basis
 when computed is not null and planned_formula='LEVERAGE-v1' then args[safe_offset(1)].basis else basis end as basis
 from values_{{ stage }}
),
{% endfor %}
basis_facts as (
 select f.* except(status,value,basis,evidence_ids,original_value),
 if(f.metric='ebitda_basis' and e.status='calculated' and f.status not in ('conflict','not_applicable'),'sourced',f.status) as status,
 if(f.metric='ebitda_basis' and e.status='calculated' and f.status not in ('conflict','not_applicable'),f.standard_basis,f.value) as value,
 if(f.metric='ebitda_basis' and e.status='calculated' and f.status not in ('conflict','not_applicable'),f.standard_basis,f.basis) as basis,
 if(f.metric='ebitda_basis' and e.status='calculated' and f.status not in ('conflict','not_applicable'),[concat('policy-basis:',f.period_role)],f.evidence_ids) as evidence_ids,
 if(f.metric='ebitda_basis' and e.status='calculated' and f.status not in ('conflict','not_applicable'),f.standard_basis,f.original_value) as original_value
 from stage_4 f left join stage_4 e
 on f.run_id=e.run_id and f.entity=e.entity and f.period_role=e.period_role and e.metric='ltm_ebitda' and not starts_with(e.fact_id,'input:')
)
select *,false as publication_eligible from basis_facts
