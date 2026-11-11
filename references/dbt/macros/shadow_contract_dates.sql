{% macro shadow_contract_start(metric,period) -%}
case when {{ metric }} in ('beginning_cash','ending_cash','current_assets','current_liabilities','quick_assets',
 'total_liabilities','net_worth','total_debt','total_assets','current_ratio','quick_ratio','debt_ratio') then cast(null as string)
 when {{ metric }} in ('ltm_ebitda','ebitda_basis','total_leverage') then {{ period }}.ltm_start
 else {{ period }}.start end
{%- endmacro %}

{% macro shadow_contract_end(metric,period) -%}
if({{ metric }}='beginning_cash',cast(date_sub(cast({{ period }}.start as date),interval 1 day) as string),{{ period }}.`end`)
{%- endmacro %}
