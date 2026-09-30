{{ config(materialized='table') }}

with covenants as (
    select * from {{ ref('stg_covenant_terms') }}
),

kpis as (
    select * from {{ ref('fct_credit_kpis') }}
),

-- 將 KPI 欄位對應到 covenant_name
covenant_actual as (
    select
        k.ticker,
        k.period_end,
        k.filed_date,
        c.covenant_name,
        c.covenant_type,
        c.threshold_value,
        c.threshold_unit,
        c.severity_level,
        c.rationale,

        -- 實際值對應
        case c.covenant_name
            when 'net_leverage_ratio'       then k.net_leverage_ratio
            when 'total_leverage_ratio'     then k.total_leverage_ratio
            when 'interest_coverage_ratio'  then k.interest_coverage_ratio
            when 'dscr'                     then k.dscr
            when 'current_ratio'            then k.current_ratio
            when 'debt_ratio'               then k.debt_ratio
            when 'cfo_to_debt_ratio'        then k.cfo_to_debt_ratio
        end                                                    as actual_value,

        -- 資料是否可用
        case c.covenant_name
            when 'interest_coverage_ratio'  then k.coverage_flag
            when 'dscr'                     then k.coverage_flag
            else 'OK'
        end                                                    as data_quality_flag

    from kpis k
    inner join covenants c
        on k.ticker = c.ticker
    where k.is_full_ttm = true   -- 只在 TTM 完整時評估 covenant
),

with_headroom as (
    select
        *,
        -- Headroom：距離門檻值的緩衝空間
        case
            when covenant_type = 'max'
            then threshold_value - actual_value
            when covenant_type = 'min'
            then actual_value - threshold_value
        end                                                    as headroom_absolute,

        -- Headroom %：相對緩衝空間
        case
            when covenant_type = 'max' and threshold_value != 0
            then safe_divide(threshold_value - actual_value, threshold_value)
            when covenant_type = 'min' and actual_value != 0
            then safe_divide(actual_value - threshold_value, actual_value)
        end                                                    as headroom_pct,

        -- 合規狀態
        case
            when actual_value is null                          then 'NO_DATA'
            when data_quality_flag = 'NO_DATA'                then 'NO_DATA'
            when covenant_type = 'max'
                 and actual_value <= threshold_value           then 'COMPLIANT'
            when covenant_type = 'min'
                 and actual_value >= threshold_value           then 'COMPLIANT'
            else 'BREACH'
        end                                                    as compliance_status

    from covenant_actual
)

select
    ticker,
    period_end,
    filed_date,
    covenant_name,
    covenant_type,
    threshold_value,
    threshold_unit,
    actual_value,
    headroom_absolute,
    headroom_pct,
    compliance_status,
    severity_level,
    rationale,

    -- Headroom 警示燈
    case
        when compliance_status = 'BREACH'   then 'BREACH'
        when compliance_status = 'NO_DATA'  then 'NO_DATA'
        when headroom_pct < 0.10            then 'CRITICAL'
        when headroom_pct < 0.20            then 'WARNING'
        else 'OK'
    end                                                        as headroom_flag,

    -- Looker 燈號顏色（直接給 Looker 用）
    case
        when compliance_status = 'BREACH'   then 'red'
        when compliance_status = 'NO_DATA'  then 'grey'
        when headroom_pct < 0.20            then 'yellow'
        else 'green'
    end                                                        as traffic_light

from with_headroom