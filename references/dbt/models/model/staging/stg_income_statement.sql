{{ config(materialized='view') }}

with source as (
    select * from {{ source('sec_raw', 'raw_income_statement') }}
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

        -- Revenue：優先用 revenue，沒有才用 revenue_alt
        coalesce(
            max(case when field_name = 'revenue'     then value end),
            max(case when field_name = 'revenue_alt' then value end)
        ) / 1e6                                                         as revenue_m,

        max(case when field_name = 'gross_profit'     then value end) / 1e6
                                                                        as gross_profit_m,
        max(case when field_name = 'operating_income' then value end) / 1e6
                                                                        as operating_income_m,
        max(case when field_name = 'net_income'       then value end) / 1e6
                                                                        as net_income_m,
        max(case when field_name = 'eps_basic'        then value end)  as eps_basic,
        max(case when field_name = 'eps_diluted'      then value end)  as eps_diluted,

        -- EBIT 用 operating_income 近似
        max(case when field_name = 'operating_income' then value end) / 1e6
                                                                        as ebit_m,
        -- Interest expense：優先用 interest_expense，沒有才用 interest_expense_alt
        -- (有些 filer 換過 tag，例如 AMZN：InterestExpense → InterestExpenseNonoperating)
        coalesce(
            max(case when field_name = 'interest_expense'     then value end),
            max(case when field_name = 'interest_expense_alt' then value end)
        ) / 1e6                                                         as interest_expense_m,
        max(case when field_name = 'da'                   then value end) / 1e6
                                                                        as da_m,
        max(case when field_name = 'income_before_tax'    then value end) / 1e6
                                                                        as income_before_tax_m,
        max(case when field_name = 'income_tax_expense'   then value end) / 1e6
                                                                        as income_tax_m,

        -- Cost of revenue：優先用 cost_of_revenue，沒有才用 cost_of_revenue_alt
        coalesce(
            max(case when field_name = 'cost_of_revenue'     then value end),
            max(case when field_name = 'cost_of_revenue_alt' then value end)
        ) / 1e6                                                         as cost_of_revenue_m,

        -- Operating expense（直接來自 us-gaap:OperatingExpenses）：只有沒有
        -- COGS/GrossProfit 這段的公司（如 Coinbase）才會標這個 tag。
        max(case when field_name = 'operating_expense_direct' then value end) / 1e6
                                                                        as operating_expense_direct_m,

        -- EBITDA = Operating income + D&A（D&A 缺失時退回 operating income）
        (
            max(case when field_name = 'operating_income' then value end)
            + coalesce(max(case when field_name = 'da' then value end), 0)
        ) / 1e6                                                         as ebitda_m

    from source
    -- 只取季度申報（10-Q 和 10-K）
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
    where revenue_m is not null
)

select * except(_row_num)
from deduped
where _row_num = 1
