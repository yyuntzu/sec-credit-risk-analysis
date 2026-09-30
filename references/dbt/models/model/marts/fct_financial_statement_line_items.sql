-- 這張表保留原始明細，供 Looker drill-through 用
{{ config(
    materialized='table',
    partition_by={'field': 'period_end', 'data_type': 'date'},
    cluster_by=['ticker']
) }}

with inc as (
    select
        ticker, period_end, filed_date, filing_type,
        'income_statement'  as statement_type,
        'revenue'           as line_item,
        revenue_m           as value_m
    from {{ ref('stg_income_statement') }}
    union all
    select ticker, period_end, filed_date, filing_type,
        'income_statement', 'gross_profit', gross_profit_m
    from {{ ref('stg_income_statement') }}
    union all
    select ticker, period_end, filed_date, filing_type,
        'income_statement', 'operating_income', operating_income_m
    from {{ ref('stg_income_statement') }}
    union all
    select ticker, period_end, filed_date, filing_type,
        'income_statement', 'net_income', net_income_m
    from {{ ref('stg_income_statement') }}
),

bal as (
    select ticker, period_end, filed_date, filing_type,
        'balance_sheet', 'cash', cash_m
    from {{ ref('stg_balance_sheet') }}
    union all
    select ticker, period_end, filed_date, filing_type,
        'balance_sheet', 'current_assets', current_assets_m
    from {{ ref('stg_balance_sheet') }}
    union all
    select ticker, period_end, filed_date, filing_type,
        'balance_sheet', 'total_assets', total_assets_m
    from {{ ref('stg_balance_sheet') }}
    union all
    select ticker, period_end, filed_date, filing_type,
        'balance_sheet', 'total_debt', total_debt_m
    from {{ ref('stg_balance_sheet') }}
    union all
    select ticker, period_end, filed_date, filing_type,
        'balance_sheet', 'total_equity', total_equity_m
    from {{ ref('stg_balance_sheet') }}
),

cf as (
    select ticker, period_end, filed_date, filing_type,
        'cash_flow', 'cfo', cfo_m
    from {{ ref('stg_cash_flow') }}
    union all
    select ticker, period_end, filed_date, filing_type,
        'cash_flow', 'capex', capex_m
    from {{ ref('stg_cash_flow') }}
    union all
    select ticker, period_end, filed_date, filing_type,
        'cash_flow', 'fcf', fcf_m
    from {{ ref('stg_cash_flow') }}
)

select * from inc
union all
select * from bal
union all
select * from cf