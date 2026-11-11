{% macro shadow_formula_arity(id) -%}
case {{ id }}
 when 'STANDARD-EBITDA-v1' then 4 when 'CF-05' then 4 when 'CF-04' then 3
 when 'CF-01' then 2 when 'CF-02' then 2 when 'CF-03' then 2 when 'CF-06' then 2
 when 'CF-09' then 2 when 'CF-10' then 2 when 'CF-11' then 2 when 'CF-12' then 2
 when 'CF-16' then 2 when 'COMMON-SIZE-v1' then 2 when 'CASH-CHANGE-v1' then 2
 when 'LEVERAGE-v1' then 2 when 'DER-01' then 2 when 'DER-02' then 2
 when 'DER-03' then 2 when 'DER-04' then 2 when 'DER-05' then 2 when 'DER-06' then 2
 else error('Unknown shadow financial formula') end
{%- endmacro %}

{% macro shadow_checked_divide(numerator, denominator, native=false) -%}
{# Only a zero divisor becomes NULL. Overflow must fail instead of hiding as missing. #}
{% if native %}
if(({{ denominator }})=0,cast(null as bignumeric),({{ numerator }})/({{ denominator }}))
{% else %}
cast(`{{ target.project }}.{{ target.schema }}.review_divide_q18_v1`(cast(({{ numerator }}) as string),cast(({{ denominator }}) as string)) as bignumeric)
{% endif %}
{%- endmacro %}

{% macro shadow_financial_formula(id, values, native=false) -%}
{% set a = values ~ '[safe_offset(0)]' %}
{% set b = values ~ '[safe_offset(1)]' %}
{% set c = values ~ '[safe_offset(2)]' %}
{% set d = values ~ '[safe_offset(3)]' %}
{# Exact q18 HALF_EVEN division; additions/subtractions remain BIGNUMERIC exact. #}
case {{ id }}
 when 'STANDARD-EBITDA-v1' then {{ values }}[safe_offset(0)] + {{ values }}[safe_offset(1)] + {{ values }}[safe_offset(2)] + {{ values }}[safe_offset(3)]
 when 'CF-04' then {{ shadow_checked_divide(a ~ '+' ~ b, b ~ '+' ~ c, native=native) }}
 when 'CF-05' then {{ shadow_checked_divide(a ~ '+' ~ b ~ '+' ~ c, b ~ '+' ~ d, native=native) }}
 when 'CF-09' then {{ shadow_checked_divide(a ~ '-' ~ b, b, native=native) }}
 when 'CF-16' then {{ values }}[safe_offset(0)] - {{ values }}[safe_offset(1)]
 when 'CASH-CHANGE-v1' then {{ values }}[safe_offset(0)] - {{ values }}[safe_offset(1)]
 when 'DER-01' then {{ values }}[safe_offset(0)] - {{ values }}[safe_offset(1)]
 when 'DER-02' then {{ values }}[safe_offset(0)] - {{ values }}[safe_offset(1)]
 when 'DER-03' then {{ values }}[safe_offset(0)] - {{ values }}[safe_offset(1)]
 when 'DER-04' then {{ values }}[safe_offset(0)] - {{ values }}[safe_offset(1)]
 when 'DER-05' then {{ values }}[safe_offset(0)] + {{ values }}[safe_offset(1)]
 when 'DER-06' then {{ values }}[safe_offset(0)] - {{ values }}[safe_offset(1)]
 when 'CF-01' then {{ shadow_checked_divide(a, b, native=native) }}
 when 'CF-02' then {{ shadow_checked_divide(a, b, native=native) }}
 when 'CF-03' then {{ shadow_checked_divide(a, b, native=native) }}
 when 'CF-06' then {{ shadow_checked_divide(a, b, native=native) }}
 when 'CF-10' then {{ shadow_checked_divide(a, b, native=native) }}
 when 'CF-11' then {{ shadow_checked_divide(a, b, native=native) }}
 when 'CF-12' then {{ shadow_checked_divide(a, b, native=native) }}
 when 'COMMON-SIZE-v1' then {{ shadow_checked_divide(a, b, native=native) }}
 when 'LEVERAGE-v1' then {{ shadow_checked_divide(a, b, native=native) }}
 else error('Unknown shadow financial formula') end
{%- endmacro %}
