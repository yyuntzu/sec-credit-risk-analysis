{{ config(severity='error', tags=['formal_review_shadow']) }}
with failures as (
 select 'configuration_count' as key from (select count(*) as n from {{ ref('dim_review_shadow_configuration') }}) where n!=1
 union all
 select fact_id as key from {{ ref('int_review_shadow_formula_contracts') }} where not formula_contract_valid
 union all
 select formula_id from {{ ref('dim_review_shadow_formulas') }}
 where array_length(input_metrics)!=array_length(input_units) or array_length(input_metrics)!={{ shadow_formula_arity('formula_id') }}
 union all
 select 'metadata_count' as key from (select countif(record_kind='metadata') as n from {{ ref('stg_review_shadow_inputs') }}) where n!=1
 union all
 select record_id as key from {{ ref('stg_review_shadow_inputs') }} group by run_id,entity,record_kind,record_id having count(*)!=1
 union all
 select fact_id from {{ ref('fct_review_shadow_facts') }} group by run_id,entity,fact_id having count(*)!=1
 union all
 select fact_id from {{ ref('fct_review_shadow_facts') }}
 where normalization_loss or publication_eligible or status not in ('sourced','calculated','missing','not_calculable','conflict','not_applicable')
 or (status not in ('sourced','calculated') and value is not null)
 or (status in ('sourced','calculated') and value is null)
 or (status in ('sourced','calculated') and unit!='text' and safe_cast(value as bignumeric) is null)
 or (status='sourced' and unit='money' and (source_precision_bound is null or source_precision_bound<=0))
 union all
 select f.fact_id from {{ ref('fct_review_shadow_facts') }} f,unnest(f.input_ids) iid
 left join {{ ref('fct_review_shadow_facts') }} i on f.run_id=i.run_id and f.entity=i.entity and i.fact_id=iid
 where i.fact_id is null or i.status not in ('sourced','calculated')
 union all
 select f.fact_id from {{ ref('stg_review_shadow_slots') }} f,unnest(f.planned_inputs) iid
 left join {{ ref('stg_review_shadow_slots') }} i on f.run_id=i.run_id and f.entity=i.entity and i.fact_id=iid
 where starts_with(f.planned_formula,'DER-') and (i.fact_id is null or i.depth>=f.depth or f.depth not between 1 and 4)
 union all
 select fact_id from {{ ref('fct_review_shadow_facts') }}
 where starts_with(formula_id,'DER-') and (status!='calculated' or array_length(input_ids)!=2
   or to_json_string(evidence_ids)!=to_json_string([json_value(identity_review,'$.evidence.id')]))
 union all
 select f.fact_id from {{ ref('fct_review_shadow_facts') }} f
 left join {{ ref('fct_review_shadow_reconciliations') }} r
 on r.run_id=f.run_id and r.entity=f.entity and r.period_role=f.period_role and r.kind='cash_bridge'
 where f.formula_id='CASH-CHANGE-v1' and (r.verified is not true
   or array_length(r.cash_definition_ids)=0 or to_json_string(f.evidence_ids)!=to_json_string(r.cash_definition_ids)
   or to_json_string(f.input_ids)!=to_json_string([r.reported_fact_id,r.beginning_fact_id]))
 union all
 select concat(kind,':',period_role) from {{ ref('fct_review_shadow_reconciliations') }}
 where publication_eligible or (unavailable>0 and diagnostic_difference is not null)
 or (verified and (status not in ('matched','within_precision') or difference is null or tolerance<0 or tolerance>maximum_tolerance))
 or (not verified and status in ('matched','within_precision'))
 union all
 select run_id from {{ ref('fct_review_shadow_acceptance') }}
 where publication_eligible or precision_approved or final_report_accepted
 or substantive_data_ready != (array_length(acceptance_blockers)=0)
 or array_length(required_fact_ids)=0
 or array_length(required_fact_ids)!=(select count(distinct fid) from unnest(required_fact_ids) fid)
 union all
 select concat(concept,':',period_role) from {{ ref('int_review_shadow_commentary_components') }} where normalization_loss
 union all
 select concat(kind,':',metric) from {{ ref('int_review_shadow_comparisons') }}
 where publication_eligible or (status='missing' and (change is not null or growth is not null))
 union all
 select record_id from {{ ref('fct_review_shadow_commentary') }}
 group by run_id,entity,record_kind,record_id having count(*)!=1
 union all
 select record_id from {{ ref('fct_review_shadow_commentary') }} where publication_eligible or safe.parse_json(payload) is null
 union all
 select case_id from {{ ref('fct_review_shadow_kernels') }}
 where array_length(amounts)!=arity or
 (expected is null and actual is not null) or
 (expected is not null and (actual is null or actual!=cast(expected as bignumeric)))
)
select * from failures
