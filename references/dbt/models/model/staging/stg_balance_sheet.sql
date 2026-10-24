{{ config(materialized='view') }}

with source as (
    select * from {{ source('sec_raw', 'raw_balance_sheet') }}
),

pivoted as (
    select
        ticker,
        filing_type,
        accession_number,
        filed_date,
        period_end,

        max(case when field_name = 'cash'                then value end) / 1e6 as cash_m,
        max(case when field_name = 'current_assets'      then value end) / 1e6 as current_assets_m,
        max(case when field_name = 'current_liabilities' then value end) / 1e6 as current_liabilities_m,
        max(case when field_name = 'total_assets'        then value end) / 1e6 as total_assets_m,
        max(case when field_name = 'total_liabilities'   then value end) / 1e6 as total_liabilities_m,
        coalesce(
            max(case when field_name = 'long_term_liabilities'     then value end),
            max(case when field_name in ('long_term_liabilities_alt', 'long_term_liabilities_alt2') then value end),
            max(case when field_name = 'long_term_debt_aggregate'  then value end),
            max(case when field_name in ('long_term_debt_aggregate_alt', 'long_term_debt_aggregate_alt2', 'long_term_debt_aggregate_alt3') then value end)
        ) / 1e6 as long_term_debt_m,
        max(case when field_name = 'stockholders_equity' then value end) / 1e6 as total_equity_m,
        max(case when field_name = 'retained_earnings'   then value end) / 1e6 as retained_earnings_m,
        max(case when field_name = 'inventory'           then value end) / 1e6 as inventory_m,

        -- DEC-02: do not adopt incomplete debt components or a lease policy.
        cast(null as float64) as short_term_debt_m,
        cast(null as float64) as total_debt_m

    from source
    where filing_type in ('10-K', '10-Q')
    group by
        ticker, filing_type, accession_number,
        filed_date, period_end
),

deduped as (
    select
        *,
        row_number() over (
            partition by ticker, period_end
            order by filed_date desc
        ) as _row_num
    from pivoted
    where total_assets_m is not null
)

select * except(_row_num)
from deduped
where _row_num = 1
