{{ config(materialized='view', tags=['formal_review_shadow']) }}
with metadata as (
 select run_id, entity, payload from {{ ref('stg_review_shadow_inputs') }} where record_kind='metadata'
)
select s.run_id, s.entity, s.record_id as fact_id,
 json_value(s.payload,'$.metric') as metric,
 json_value(s.payload,'$.period_role') as period_role,
 json_value(s.payload,'$.expected_start') as expected_start,
 json_value(s.payload,'$.expected_end') as expected_end,
 json_value(s.payload,'$.start') as start, json_value(s.payload,'$.end') as `end`,
 json_value(s.payload,'$.unit') as unit, json_value(s.payload,'$.currency') as currency,
 json_value(s.payload,'$.period_kind') as period_kind,
 json_value(s.payload,'$.definition') as definition,
 json_value(s.payload,'$.source_unit') as source_unit,
 cast(json_value(s.payload,'$.scale') as bignumeric) as declared_scale,
 if(json_value(s.payload,'$.unit')='money',cfg.money_scale,cast(1 as bignumeric)) as scale,
 json_value(s.payload,'$.formula_id') as planned_formula,
 json_value(s.payload,'$.formula_version') as planned_version,
 json_query(s.payload,'$.identity_review') as identity_review,
 json_value(m.payload,'$.identity_source_hash') as identity_source_hash,
 json_value_array(s.payload,'$.input_ids') as planned_inputs,
 json_value_array(s.payload,'$.sec_fields') as sec_fields,
 json_value_array(s.payload,'$.pending') as pending,
 json_value_array(m.payload,'$.decisions') as approved_decisions,
 cast(json_value(s.payload,'$.source_allowed') as bool) as source_allowed,
 cast(json_value(s.payload,'$.depth') as int64) as depth,
 json_value(m.payload,'$.scope') as scope,
 cast(json_value(m.payload,'$.request.as_of') as date) as as_of,
 json_query(m.payload,'$.approved_definitions') as approved_definitions,
 json_value(m.payload,'$.standard_ebitda_basis') as declared_standard_basis,
 cast(json_value(m.payload,'$.scale') as bignumeric) as declared_report_scale,
 json_value(m.payload,'$.formula_version') as declared_formula_version,
 json_value(m.payload,'$.policy_version') as declared_policy_version,
 json_value(m.payload,'$.precision_version') as declared_precision_version,
 json_value(m.payload,'$.precision_approved') as declared_precision_approved,
 cfg.standard_basis,
 json_value(m.payload,'$.source_hash') as source_hash,
 json_value(m.payload,'$.plan_hash') as plan_hash,
 cfg.precision_version
from {{ ref('stg_review_shadow_inputs') }} s
join metadata m using(run_id,entity)
cross join {{ ref('dim_review_shadow_configuration') }} cfg
where s.record_kind='slot'
