{{ config(materialized='view') }}

with base as (
    select * from {{ ref('int_ttm_metrics') }}
),

-- 計算 YoY 和 QoQ 成長率
with_growth as (
    select
        *,
        lag(ttm_revenue_m,    4) over (partition by ticker order by period_end)
                                                               as revenue_m_prior_year,
        lag(ttm_ebitda_m,     4) over (partition by ticker order by period_end)
                                                               as ebitda_m_prior_year,
        lag(ttm_net_income_m, 4) over (partition by ticker order by period_end)
                                                               as net_income_m_prior_year,
        lag(ttm_cfo_m,        4) over (partition by ticker order by period_end)
                                                               as cfo_m_prior_year,
        lag(ttm_fcf_m,        4) over (partition by ticker order by period_end)
                                                               as fcf_m_prior_year,

        -- QoQ（前一季）
        lag(ttm_revenue_m,    1) over (partition by ticker order by period_end)
                                                               as revenue_m_prior_quarter
    from base
)

select
    ticker,
    period_end,
    filed_date,

    -- TTM 現金流指標
    ttm_cfo_m,
    ttm_capex_m,
    ttm_fcf_m,

    -- Capex Intensity = Capex / Revenue
    safe_divide(ttm_capex_m, ttm_revenue_m)                   as capex_intensity,

    -- FCF Conversion = FCF / Net Income
    safe_divide(ttm_fcf_m, ttm_net_income_m)                  as fcf_conversion,

    -- FCF Yield = FCF / Total Assets（資產效率）
    safe_divide(ttm_fcf_m, total_assets_m)                    as fcf_yield,

    -- YoY 成長率
    safe_divide(
        ttm_revenue_m - revenue_m_prior_year,
        revenue_m_prior_year
    )                                                          as revenue_yoy_growth,

    safe_divide(
        ttm_ebitda_m - ebitda_m_prior_year,
        abs(ebitda_m_prior_year)
    )                                                          as ebitda_yoy_growth,

    safe_divide(
        ttm_cfo_m - cfo_m_prior_year,
        abs(cfo_m_prior_year)
    )                                                          as cfo_yoy_growth,

    -- Risk Flags
    case
        
        when safe_divide(ttm_revenue_m - revenue_m_prior_year,
                         revenue_m_prior_year) < -0.20   then 'CRITICAL'
        when safe_divide(ttm_revenue_m - revenue_m_prior_year,
                         revenue_m_prior_year) < -0.10   then 'WARNING'
        else 'OK'
    end                                                        as revenue_growth_flag,

    case
        when ttm_fcf_m < 0                                    then 'CRITICAL'
        when ttm_fcf_m < ttm_cfo_m * 0.3                     then 'WARNING'
        else 'OK'
    end                                                        as fcf_flag

from with_growth