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
    safe_divide(ttm_ebitda_m, ttm_interest_expense_m)         as interest_coverage_ratio,

    -- Operating Income Coverage（interest_expense 缺失時的替代指標）
    safe_divide(ttm_operating_income_m, ttm_interest_expense_m) as ebit_coverage_ratio,

    -- DSCR = TTM CFO / (Interest + Debt Repayment)
    -- ⚠️ 兩個分母都缺失時，暫用 CFO / Interest 單項
    safe_divide(
        ttm_cfo_m,
        coalesce(ttm_interest_expense_m, 0) + coalesce(
            (select 0),  -- debt_repayment 缺失，暫為 0
            0
        )
    )                                                          as dscr,

    -- CFO to Debt（替代覆蓋指標，不需要 interest 資料）
    -- 衡量現金流還清全部債務需幾年
    safe_divide(ttm_cfo_m, total_debt_m)                      as cfo_to_debt_ratio,

    -- FCF Coverage（替代指標）
    safe_divide(ttm_fcf_m, total_debt_m)                      as fcf_to_debt_ratio,

    -- Risk Flags
    case
        when ttm_interest_expense_m is null                                        then 'NO_DATA'
        when safe_divide(ttm_ebitda_m, ttm_interest_expense_m) < 1.5              then 'CRITICAL'
        when safe_divide(ttm_ebitda_m, ttm_interest_expense_m) < 3.0              then 'WARNING'
        else 'OK'
    end                                                        as coverage_flag,

    case
        when safe_divide(ttm_cfo_m, total_debt_m) < 0.05     then 'CRITICAL'
        when safe_divide(ttm_cfo_m, total_debt_m) < 0.10     then 'WARNING'
        else 'OK'
    end                                                        as cfo_to_debt_flag

from base