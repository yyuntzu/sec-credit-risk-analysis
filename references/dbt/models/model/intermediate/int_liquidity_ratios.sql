{{ config(materialized='view') }}

with base as (
    select * from {{ ref('int_ttm_metrics') }}
)

select
    ticker,
    period_end,
    filed_date,

    -- Current Ratio = 流動資產 / 流動負債
    -- 健康標準：> 1.5x；警戒：< 1.0x
    safe_divide(current_assets_m, current_liabilities_m)     as current_ratio,

    -- Quick Ratio = 流動資產 / 流動負債（近似，缺 inventory 資料）
    -- 對 MSFT/AAPL 影響小（輕資產），WMT 有存貨需注意
    safe_divide(current_assets_m, current_liabilities_m)     as quick_ratio,

    -- Cash Ratio = 現金 / 流動負債（最嚴格）
    safe_divide(cash_m, current_liabilities_m)               as cash_ratio,

    -- Cash Flow Ratio = TTM CFO / 流動負債
    safe_divide(ttm_cfo_m, current_liabilities_m)            as cash_flow_ratio,

    -- Risk Flags
    case
        when safe_divide(current_assets_m, current_liabilities_m) < 1.0  then 'CRITICAL'
        when safe_divide(current_assets_m, current_liabilities_m) < 1.25 then 'WARNING'
        else 'OK'
    end                                                       as current_ratio_flag,

    case
        when safe_divide(ttm_cfo_m, current_liabilities_m) < 0.3 then 'CRITICAL'
        when safe_divide(ttm_cfo_m, current_liabilities_m) < 0.5 then 'WARNING'
        else 'OK'
    end                                                       as cash_flow_ratio_flag

from base