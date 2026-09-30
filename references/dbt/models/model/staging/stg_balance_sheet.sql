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

        (
            coalesce(max(case when field_name = 'short_term_loans' then value end), 0)
            + coalesce(max(case when field_name = 'short_term_notes_payable' then value end), 0)
            + coalesce(
                max(case when field_name = 'current_maturities_ltd' then value end),
                max(case when field_name in ('current_maturities_ltd_alt', 'current_maturities_ltd_alt2') then value end),
                0
            )
        ) / 1e6 as short_term_debt_m,

        -- Total Debt = short-term loans/notes + current maturities +
        -- noncurrent long-term liabilities. DebtCurrent and aggregate
        -- LongTermDebt are mutually exclusive fallbacks to prevent overlap.
        case
            when coalesce(
                max(case when field_name = 'long_term_liabilities' then value end),
                max(case when field_name in ('long_term_liabilities_alt', 'long_term_liabilities_alt2') then value end)
            ) is not null then (
                coalesce(max(case when field_name = 'short_term_loans' then value end), 0)
                + coalesce(max(case when field_name = 'short_term_notes_payable' then value end), 0)
                + coalesce(
                    max(case when field_name = 'current_maturities_ltd' then value end),
                    max(case when field_name in ('current_maturities_ltd_alt', 'current_maturities_ltd_alt2') then value end),
                    case when max(case when field_name = 'short_term_loans' then value end) is null
                           and max(case when field_name = 'short_term_notes_payable' then value end) is null
                         then max(case when field_name = 'debt_current_fallback' then value end)
                         else 0 end,
                    0
                )
                + coalesce(
                    max(case when field_name = 'long_term_liabilities' then value end),
                    max(case when field_name in ('long_term_liabilities_alt', 'long_term_liabilities_alt2') then value end)
                )
            )
            else coalesce(
                max(case when field_name = 'long_term_debt_aggregate' then value end),
                max(case when field_name in ('long_term_debt_aggregate_alt', 'long_term_debt_aggregate_alt2', 'long_term_debt_aggregate_alt3') then value end)
            )
        end / 1e6 as total_debt_m

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
