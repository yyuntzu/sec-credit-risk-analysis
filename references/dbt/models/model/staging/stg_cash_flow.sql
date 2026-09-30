{{ config(materialized='view') }}

with source as (
    select * from {{ source('sec_raw', 'raw_cash_flow') }}
),

pivoted as (
    select
        ticker,
        filing_type,
        accession_number,
        filed_date,
        period_end,
        period_start,
        period_days,

        max(case when field_name = 'cfo'           then value end) / 1e6 as cfo_m,
        max(case when field_name = 'cfi'           then value end) / 1e6 as cfi_m,
        max(case when field_name = 'cff'           then value end) / 1e6 as cff_m,

        -- Capex 為負值，取絕對值
        abs(max(case when field_name = 'capex'     then value end)) / 1e6 as capex_m,

        max(case when field_name = 'dividends_paid' then value end) / 1e6 as dividends_paid_m,
        max(case when field_name = 'buybacks'       then value end) / 1e6 as buybacks_m,

        -- FCF = CFO - Capex
        (
            max(case when field_name = 'cfo'   then value end) -
            abs(max(case when field_name = 'capex' then value end))
        ) / 1e6                                                            as fcf_m,

        -- ⚠️ debt_repayment 缺失，DSCR 分母暫只用 interest_expense
        null                                                               as debt_repayment_m

    from source
    where filing_type in ('10-K', '10-Q')
    group by
        ticker, filing_type, accession_number,
        filed_date, period_end, period_start, period_days
),

deduped as (
    select
        *,
        row_number() over (
            partition by ticker, period_start, period_end, period_days
            order by filed_date desc
        ) as _row_num
    from pivoted
    where cfo_m is not null
)

select * except(_row_num)
from deduped
where _row_num = 1
