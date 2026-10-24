{{ config(materialized='view') }}

with base as (
    select * from {{ ref('int_ttm_metrics') }}
)

select
    ticker,
    period_end,
    filed_date,

    -- CF-06 = Total Liabilities / approved Net Worth
    cast(null as float64) as debt_ratio, -- CF-06 requires approved Net Worth (DEC-02)

    -- Total Leverage = 總債務 / TTM EBITDA
    safe_divide(total_debt_m, ttm_ebitda_m)                   as total_leverage_ratio,

    -- Net Leverage = 淨債務 / TTM EBITDA
    safe_divide((total_debt_m - cash_m), ttm_ebitda_m)        as net_leverage_ratio,

    -- Debt to Equity
    safe_divide(total_debt_m, total_equity_m)                 as debt_to_equity,

    -- 金額
    total_debt_m,
    total_debt_m - cash_m                                     as net_debt_m,
    cash_m,

    -- Risk Flags
    'NO_DATA' as debt_ratio_flag, -- DEC-02 pending.


    case
        when total_debt_m is null or ttm_ebitda_m is null then 'NO_DATA'
        when safe_divide(total_debt_m, ttm_ebitda_m) > 6.0   then 'CRITICAL'
        when safe_divide(total_debt_m, ttm_ebitda_m) > 4.0   then 'WARNING'
        else 'OK'
    end                                                        as leverage_flag,

    -- 標記 EBITDA 為近似值時的可靠性
    case
        when ttm_ebitda_m is null then 'NO_DATA'
        else 'OK'
    end                                                        as ebitda_data_quality

from base