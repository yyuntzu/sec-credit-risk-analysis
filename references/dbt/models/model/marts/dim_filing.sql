{{ config(materialized='table') }}

select
    ticker,
    period_end,
    period_start,
    period_days,
    filing_type,
    filed_date,
    accession_number,

    -- 年度和季度拆分（給 Looker filter 用）
    extract(year  from period_end)             as fiscal_year,
    extract(quarter from period_end)           as fiscal_quarter,

    -- 標籤（給 Looker 顯示用）
    cast(extract(year from period_end) as string)
        || ' Q'
        || cast(extract(quarter from period_end) as string)    as period_label,

    -- 申報時間差（申報延遲天數，越小越好）
    date_diff(filed_date, period_end, day)     as filing_lag_days,

    -- 10-K vs 10-Q
    case
        when filing_type = '10-K' then 'Annual'
        when filing_type = '10-Q' then 'Quarterly'
        else 'Other'
    end                                        as filing_period_type

from {{ ref('stg_income_statement') }}