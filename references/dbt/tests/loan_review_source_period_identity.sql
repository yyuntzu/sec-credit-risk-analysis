{{ config(severity='error', tags=['loan_review_sources']) }}

-- Do not erase incomplete legacy rows; they remain unverified and the Python
-- ingestion boundary rejects them. Traceable rows must have coherent periods.
select *
from {{ ref('stg_loan_review_sources') }}
where lineage_status = 'traceable'
  and (
    period_kind not in ('instant', 'duration')
    or (period_kind = 'instant' and period_start is not null)
    or (period_kind = 'duration' and (period_start is null or period_start > period_end))
  )
