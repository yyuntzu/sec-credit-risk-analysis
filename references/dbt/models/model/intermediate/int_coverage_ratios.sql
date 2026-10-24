{{ config(materialized='view') }}

with base as (
    select * from {{ ref('int_ttm_metrics') }}
)

select
    ticker,
    period_end,
    filed_date,

    -- Interest Coverage = TTM EBITDA / TTM Interest Expense
    -- ⚠️ interest_expense_m 目前為 null → 比率為 null
    cast(null as float64) as interest_coverage_ratio, -- DEC-05; CF-04 is not EBITDA/interest

    -- Operating Income Coverage（interest_expense 缺失時的替代指標）
    safe_divide(ttm_operating_income_m, ttm_interest_expense_m) as ebit_coverage_ratio,

    -- DEC-03: no inferred principal or substitute DSCR definition.
    cast(null as float64) as dscr,

    -- CFO to Debt（替代覆蓋指標，不需要 interest 資料）
    -- 衡量現金流還清全部債務需幾年
    safe_divide(ttm_cfo_m, total_debt_m)                      as cfo_to_debt_ratio,

    -- FCF Coverage（替代指標）
    safe_divide(ttm_fcf_m, total_debt_m)                      as fcf_to_debt_ratio,

    -- Risk Flags
    'NO_DATA' as coverage_flag, -- CF-04/DEC-05 not verified in legacy dbt.


    case
        when ttm_cfo_m is null or total_debt_m is null then 'NO_DATA'
        when safe_divide(ttm_cfo_m, total_debt_m) < 0.05     then 'CRITICAL'
        when safe_divide(ttm_cfo_m, total_debt_m) < 0.10     then 'WARNING'
        else 'OK'
    end                                                        as cfo_to_debt_flag

from base