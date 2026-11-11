-- depends_on: {{ ref('dim_review_shadow_configuration') }}
{{ config(materialized='table', tags=['formal_review_shadow']) }}
with cases as (
 select run_id,entity,record_id as case_id,json_value(payload,'$.formula_id') as formula_id,
 array(select cast(x as bignumeric) from unnest(json_value_array(payload,'$.values')) x) as amounts,
 json_value(payload,'$.expected') as expected,
 json_value(payload,'$.expected_reason') as expected_reason
 from {{ ref('stg_review_shadow_inputs') }} where record_kind='kernel_case'
)
select *,{{ shadow_financial_formula('formula_id','amounts') }} as actual,
 {{ shadow_financial_formula('formula_id','amounts',native=true) }} as native_actual,
 {{ shadow_formula_arity('formula_id') }} as arity
from cases
