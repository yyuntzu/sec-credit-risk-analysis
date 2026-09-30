{{ config(materialized='table') }}

with company as (
    select * from {{ ref('stg_company') }}
),

filing_stats as (
    select
        ticker,
        min(period_end)     as earliest_filing_date,
        max(period_end)     as latest_filing_date,
        count(distinct period_end) as total_quarters
    from {{ ref('stg_income_statement') }}
    group by ticker
)

select
    c.ticker,
    c.cik,
    c.company_name,
    c.sic_code,
    c.industry,
    c.state_of_incorporation,
    c.fiscal_year_end,
    c.exchanges,
    f.earliest_filing_date,
    f.latest_filing_date,
    f.total_quarters,

    -- Looker label（公司名稱 + ticker 合併顯示）
    c.company_name || ' (' || c.ticker || ')'  as company_label

from company c
left join filing_stats f using (ticker)