{{ config(
   materialized='table',
   partition_by={'field': 'period_end', 'data_type': 'date'},
   cluster_by=['ticker']
) }}
with base as (
   select * from {{ ref('int_financials_combined') }}
),
quarterly_raw as (
   select *
   from base
   where period_days between 70 and 105
),
-- ⚠️ 關鍵：確保 window function 輸入是唯一的
quarterly as (
   select *,
       row_number() over (
           partition by ticker, period_end
           order by filed_date desc
       ) as _rn
   from quarterly_raw
),
quarterly_clean as (
   select * except(_rn)
   from quarterly
   where _rn = 1
),
ttm as (
   select
       ticker,
       period_end,
       filed_date,
       filing_type,
       sum(revenue_m)          over w as ttm_revenue_m,
       sum(gross_profit_m)     over w as ttm_gross_profit_m,
       sum(operating_income_m) over w as ttm_operating_income_m,
       sum(ebit_m)             over w as ttm_ebit_m,
       sum(net_income_m)       over w as ttm_net_income_m,
       sum(cfo_m)              over w as ttm_cfo_m,
       sum(capex_m)            over w as ttm_capex_m,
       sum(fcf_m)              over w as ttm_fcf_m,
       sum(interest_expense_m) over w as ttm_interest_expense_m,
       sum(da_m)               over w as ttm_da_m,
       count(period_end)       over w as periods_available,
       -- DEC-06 and exact fiscal calendar approval are not available in legacy dbt.
       cast(null as float64) as ttm_ebitda_m,
       cash_m,
       current_assets_m,
       current_liabilities_m,
       total_assets_m,
       total_liabilities_m,
       total_debt_m,
       long_term_debt_m,
       total_equity_m,
       retained_earnings_m
   from quarterly_clean
   window w as (
       partition by ticker
       order by period_end
       rows between 3 preceding and current row
   )
)
select
   ticker,
   period_end,
   filed_date,
   filing_type,
   periods_available,
   ttm_revenue_m,
   ttm_gross_profit_m,
   ttm_operating_income_m,
   ttm_ebit_m,
   ttm_ebitda_m,
   ttm_net_income_m,
   ttm_interest_expense_m,
   ttm_da_m,
   ttm_cfo_m,
   ttm_capex_m,
   ttm_fcf_m,
   cash_m,
   current_assets_m,
   current_liabilities_m,
   total_assets_m,
   total_liabilities_m,
   total_debt_m,
   long_term_debt_m,
   total_equity_m,
   retained_earnings_m,
   total_debt_m - cash_m                          as net_debt_m,
   safe_divide(ttm_ebitda_m, ttm_revenue_m)       as ebitda_margin,
   safe_divide(ttm_gross_profit_m, ttm_revenue_m) as gross_margin,
   safe_divide(ttm_net_income_m, ttm_revenue_m)   as net_margin,
   false as is_full_ttm, -- Row count alone does not prove a fiscal LTM interval.
   'Not calculable: verified fiscal calendar and EBITDA basis required' as ebitda_calc_method
from ttm
