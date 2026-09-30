{{ config(materialized='view') }}

select
    upper(trim(ticker))                         as ticker,
    trim(covenant_name)                         as covenant_name,
    lower(trim(covenant_type))                  as covenant_type,
    safe_cast(threshold_value as float64)       as threshold_value,
    trim(threshold_unit)                        as threshold_unit,
    trim(monitoring_frequency)                  as monitoring_frequency,
    trim(severity_level)                        as severity_level,
    trim(rationale)                             as rationale

from {{ source('sec_raw', 'raw_covenant_terms') }}
where ticker is not null
  and covenant_name is not null