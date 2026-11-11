{{ config(materialized='table', tags=['formal_review_shadow']) }}
-- Reconciliation reads preliminary facts, so this reviewed adoption has no DAG cycle.
with assessed as (
 select f.*,r.cash_definition_ids,
 coalesce(f.formula_contract_valid and f.metric='cash_change' and f.planned_formula='CASH-CHANGE-v1'
   and f.start is not distinct from f.expected_start and f.end=f.expected_end
   and f.unit='money' and f.period_kind='duration'
   and f.status not in ('sourced','calculated','conflict','not_applicable')
   and r.verified and array_length(r.cash_definition_ids)>0
   and r.reported_fact_id=f.planned_inputs[safe_offset(0)]
   and r.beginning_fact_id=f.planned_inputs[safe_offset(1)]
   and ending.status in ('sourced','calculated') and beginning.status in ('sourced','calculated'),false) as cash_ready,
 ending.value as ending_amount,beginning.value as beginning_amount,
 ending.source_precision_bound+beginning.source_precision_bound as cash_bound,
 array(select distinct eid from unnest(array_concat(ending.source_evidence_ids,beginning.source_evidence_ids)) eid order by eid) as cash_sources
 from {{ ref('int_review_shadow_calculated') }} f
 left join {{ ref('fct_review_shadow_reconciliations') }} r
 on r.run_id=f.run_id and r.entity=f.entity and r.scope=f.scope and r.period_role=f.period_role and r.kind='cash_bridge'
 left join {{ ref('int_review_shadow_calculated') }} ending
 on ending.run_id=f.run_id and ending.entity=f.entity and ending.fact_id=r.reported_fact_id
 left join {{ ref('int_review_shadow_calculated') }} beginning
 on beginning.run_id=f.run_id and beginning.entity=f.entity and beginning.fact_id=r.beginning_fact_id
)
select * except(cash_ready,ending_amount,beginning_amount,cash_bound,cash_sources,cash_definition_ids,
 status,value,formula_id,formula_version,input_ids,evidence_ids,source_evidence_ids,source_precision_bound),
 if(cash_ready,'calculated',status) as status,
 if(cash_ready,cast(cast(ending_amount as bignumeric)-cast(beginning_amount as bignumeric) as string),value) as value,
 if(cash_ready,planned_formula,formula_id) as formula_id,
 if(cash_ready,planned_version,formula_version) as formula_version,
 if(cash_ready,planned_inputs,input_ids) as input_ids,
 if(cash_ready,cash_definition_ids,evidence_ids) as evidence_ids,
 if(cash_ready,cash_sources,source_evidence_ids) as source_evidence_ids,
 if(cash_ready,cash_bound,source_precision_bound) as source_precision_bound
from assessed
