{{ config(materialized='view', tags=['loan_review_sources']) }}

-- Block 2 candidate ledger. Never pivot, coalesce, sum alternate tags, select
-- latest filings, infer zeros, or collapse instant/YTD/quarter/annual intervals.
-- Rows without new audit metadata remain visible with lineage_status=unverified.
with candidates as (
    {% for statement in ['income_statement', 'balance_sheet', 'cash_flow'] %}
    select
        '{{ statement }}' as statement_type,
        fact_id, ticker, cik, scope, field_name, namespace, xbrl_tag,
        original_value, value, unit, period_kind, period_start, period_end,
        period_days, filing_type, accession_number, filed_date,
        source_version, source_url, document_url, source_locator,
        filing_fiscal_year, filing_fiscal_period, ingested_at
    from {{ source('sec_raw', 'raw_' ~ statement) }}
    {% if not loop.last %}union all{% endif %}
    {% endfor %}
)
select *,
    case when fact_id is null or cik is null or scope is null
           or source_version is null or source_url is null or source_locator is null
           or document_url is null or unit is null or period_kind is null
           or accession_number is null or filed_date is null or period_end is null
         then 'unverified' else 'traceable' end as lineage_status
from candidates
