{{ config(materialized='view', tags=['formal_review_shadow']) }}
{% set run_id = var('shadow_run_id', '00000000000000000000000000000000') %}
{% if run_id | length != 32 or modules.re.fullmatch('[a-f0-9]{32}', run_id) is none %}
  {{ exceptions.raise_compiler_error('Invalid shadow run ID') }}
{% endif %}
select *
from {{ source('review_shadow_raw', 'raw_review_shadow_inputs') }}
where run_id = '{{ run_id }}'
