{{ config(
    materialized='table',
    partition_by={'field': 'period_end', 'data_type': 'date'},
    cluster_by=['ticker']
) }}

with inc as (
    select * from {{ ref('stg_income_statement') }}
),
bal as (
    select * from {{ ref('stg_balance_sheet') }}
),
cf as (
    select * from {{ ref('stg_cash_flow') }}
),

joined as (
    select
        inc.ticker,
        inc.period_end,
        inc.period_start,
        inc.period_days,
        inc.filing_type,
        inc.filed_date,
        inc.accession_number,

        inc.revenue_m,
        inc.gross_profit_m,
        inc.operating_income_m,
        inc.ebit_m,
        inc.net_income_m,
        inc.eps_basic,
        inc.eps_diluted,
        inc.interest_expense_m,
        inc.da_m,
        inc.ebitda_m,

        bal.cash_m,
        bal.current_assets_m,
        bal.current_liabilities_m,
        bal.total_assets_m,
        bal.total_liabilities_m,
        bal.long_term_debt_m,
        bal.short_term_debt_m,
        bal.total_debt_m,
        bal.total_equity_m,
        bal.retained_earnings_m,

        cf.cfo_m,
        cf.cfi_m,
        cf.cff_m,
        cf.capex_m,
        cf.fcf_m,
        cf.dividends_paid_m,
        cf.buybacks_m,
        cf.debt_repayment_m

    from inc
    left join bal
        on inc.ticker      = bal.ticker
        and inc.period_end = bal.period_end
    left join cf
        on inc.ticker      = cf.ticker
        and inc.period_end = cf.period_end

    where inc.period_days is not null
),

-- ⚠️ 關鍵修正：JOIN 後再做一次 dedup
-- 同一個 ticker+period_end 只保留最新 filed_date
deduped as (
    select
        *,
        row_number() over (
            partition by ticker, period_end
            order by filed_date desc
        ) as _rn
    from joined
)

select * except(_rn)
from deduped
where _rn = 1