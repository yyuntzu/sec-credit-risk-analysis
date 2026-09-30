{{ config(materialized='view') }}

select
    upper(trim(ticker))         as ticker,
    cast(cik as string)         as cik,
    trim(company_name)          as company_name,
    cast(sic as string)         as sic_code,
    trim(sic_desc)              as industry,
    trim(state_inc)             as state_of_incorporation,
    trim(fiscal_year_end)       as fiscal_year_end,
    trim(exchanges)             as exchanges,
    ingested_at

from {{ source('sec_raw', 'raw_company') }}
where ticker is not null