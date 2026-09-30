{{ config(
   materialized='table',
   partition_by={'field': 'period_end', 'data_type': 'date'},
   cluster_by=['ticker']
) }}
with ttm as (select * from {{ ref('int_ttm_metrics') }}),
    liq as (select * from {{ ref('int_liquidity_ratios') }}),
    lev as (select * from {{ ref('int_leverage_ratios') }}),
    cov as (select * from {{ ref('int_coverage_ratios') }}),
    cf  as (select * from {{ ref('int_cash_flow_metrics') }}),
joined as (
   select
       ttm.ticker,
       ttm.period_end,
       ttm.filed_date,
       ttm.filing_type,
       ttm.is_full_ttm,
       ttm.ebitda_calc_method,
       ttm.ttm_revenue_m,
       ttm.ttm_gross_profit_m,
       ttm.ttm_ebitda_m,
       ttm.ttm_ebit_m,
       ttm.ttm_net_income_m,
       ttm.ebitda_margin,
       ttm.gross_margin,
       ttm.net_margin,
       ttm.ttm_cfo_m,
       ttm.ttm_capex_m,
       ttm.ttm_fcf_m,
       ttm.total_debt_m,
       ttm.net_debt_m,
       ttm.cash_m,
       liq.current_ratio,
       liq.quick_ratio,
       liq.cash_ratio,
       liq.cash_flow_ratio,
       liq.current_ratio_flag,
       liq.cash_flow_ratio_flag,
       lev.debt_ratio,
       lev.total_leverage_ratio,
       lev.net_leverage_ratio,
       lev.debt_to_equity,
       lev.debt_ratio_flag,
       lev.leverage_flag,
       lev.ebitda_data_quality,
       cov.interest_coverage_ratio,
       cov.ebit_coverage_ratio,
       cov.dscr,
       cov.cfo_to_debt_ratio,
       cov.fcf_to_debt_ratio,
       cov.coverage_flag,
       cov.cfo_to_debt_flag,
       cf.capex_intensity,
       cf.fcf_conversion,
       cf.revenue_yoy_growth,
       cf.ebitda_yoy_growth,
       cf.cfo_yoy_growth,
       cf.revenue_growth_flag,
       cf.fcf_flag,
       case
           when 'CRITICAL' in (
               liq.current_ratio_flag,
               lev.leverage_flag,
               cov.coverage_flag,
               cf.revenue_growth_flag,
               cf.fcf_flag
           ) then 'CRITICAL'
           when 'WARNING' in (
               liq.current_ratio_flag,
               lev.leverage_flag,
               cov.coverage_flag,
               cf.revenue_growth_flag,
               cf.fcf_flag
           ) then 'WARNING'
           when 'NO_DATA' in (
               lev.ebitda_data_quality,
               cov.coverage_flag
           ) then 'INCOMPLETE'
           else 'OK'
       end as overall_risk_flag,
       -- ⚠️ dedup 用
       row_number() over (
           partition by ttm.ticker, ttm.period_end
           order by ttm.filed_date desc
       ) as _rn
   from ttm
   left join liq using (ticker, period_end)
   left join lev using (ticker, period_end)
   left join cov using (ticker, period_end)
   left join cf  using (ticker, period_end)
)
select * except(_rn)
from joined
where _rn = 1