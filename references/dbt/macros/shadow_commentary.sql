{% macro shadow_change_fields(before, after) -%}
cast({{ before }} as string) as before,cast({{ after }} as string) as after,
 cast(({{ after }})-({{ before }}) as string) as change,
 cast(if(({{ before }})>0,{{ shadow_checked_divide('(' ~ after ~ ')-(' ~ before ~ ')',before) }},null) as string) as growth,
 if(({{ before }}) is null or ({{ after }}) is null,'missing','available') as status
{%- endmacro %}
