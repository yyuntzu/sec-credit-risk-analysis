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

    -- CF-02 requires approved Quick Assets (DEC-01).
    -- 對 MSFT/AAPL 影響小（輕資產），WMT 有存貨需注意
    cast(null as float64) as quick_ratio, -- DEC-01: no current-ratio proxy

    -- Cash Ratio = 現金 / 流動負債（最嚴格）
    safe_divide(cash_m, current_liabilities_m)               as cash_ratio,

    -- Cash Flow Ratio = TTM CFO / 流動負債
    cast(null as float64) as cash_flow_ratio, -- CF-03 requires verified full FY CFO/year-end CL

    -- Risk Flags
    case
        when current_assets_m is null or current_liabilities_m is null or current_liabilities_m = 0 then 'NO_DATA'
        when safe_divide(current_assets_m, current_liabilities_m) < 1.0  then 'CRITICAL'
        when safe_divide(current_assets_m, current_liabilities_m) < 1.25 then 'WARNING'
        else 'OK'
    end                                                       as current_ratio_flag,

    'NO_DATA' as cash_flow_ratio_flag -- Verified FY CFO/year-end CL required.


from base