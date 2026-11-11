{% macro shadow_identity_eligible() -%}
(
 json_value(identity_review,'$.fact_id')=fact_id
 and json_value(identity_review,'$.formula_id')=planned_formula
 and json_value(identity_review,'$.formula_version')=planned_version
 and to_json_string(json_value_array(identity_review,'$.input_ids'))=to_json_string(planned_inputs)
 and json_value(identity_review,'$.evidence.kind')='definition'
 and json_value(identity_review,'$.evidence.entity')=entity
 and json_value(identity_review,'$.evidence.scope')=scope
 and json_value(identity_review,'$.evidence.id') is not null
 and cast(json_value(identity_review,'$.evidence.document_date') as date)<=as_of
 and period_role in unnest(json_value_array(identity_review,'$.evidence.period_roles'))
 and json_value(json_value(identity_review,'$.evidence.content'),'$.source_hash')=identity_source_hash
 and json_value(json_value(identity_review,'$.evidence.content'),'$.entity')=entity
 and json_value(json_value(identity_review,'$.evidence.content'),'$.scope')=scope
 and json_value(json_value(identity_review,'$.evidence.content'),'$.fact_id')=fact_id
 and json_value(json_value(identity_review,'$.evidence.content'),'$.formula_id')=planned_formula
 and json_value(json_value(identity_review,'$.evidence.content'),'$.formula_version')=planned_version
 and to_json_string(json_value_array(json_value(identity_review,'$.evidence.content'),'$.input_ids'))=to_json_string(planned_inputs)
 and json_value(json_value(identity_review,'$.evidence.content'),'$.period_role')=period_role
 and json_value(json_value(identity_review,'$.evidence.content'),'$.start')=start
 and json_value(json_value(identity_review,'$.evidence.content'),'$.end')=`end`
 and json_value(json_value(identity_review,'$.evidence.content'),'$.currency')=currency
 and json_value(json_value(identity_review,'$.evidence.content'),'$.unit')=unit
 and json_value(json_value(identity_review,'$.evidence.content'),'$.complete')='true'
 and array_length(args)=2
 and not exists(select 1 from unnest(args) a where a.period_role!=f.period_role
   or a.start is distinct from f.start or a.end is distinct from f.`end`
   or a.unit!=f.unit or a.currency is distinct from f.currency
   or a.period_kind!=f.period_kind or f.metric in unnest(a.ancestor_metrics))
 and case planned_formula
 when 'DER-01' then metric='gross_profit' and args[safe_offset(0)].metric='revenue' and args[safe_offset(1)].metric='cost_of_revenue'
 when 'DER-02' then metric='cost_of_revenue' and args[safe_offset(0)].metric='revenue' and args[safe_offset(1)].metric='gross_profit'
 when 'DER-03' then metric='operating_expense' and args[safe_offset(0)].metric='gross_profit' and args[safe_offset(1)].metric='operating_income'
 when 'DER-04' then metric='operating_income' and args[safe_offset(0)].metric='gross_profit' and args[safe_offset(1)].metric='operating_expense'
 when 'DER-05' then metric='pretax_profit' and args[safe_offset(0)].metric='net_income' and args[safe_offset(1)].metric='income_tax'
 when 'DER-06' then metric='net_income' and args[safe_offset(0)].metric='pretax_profit' and args[safe_offset(1)].metric='income_tax'
 else false end
)
{%- endmacro %}
