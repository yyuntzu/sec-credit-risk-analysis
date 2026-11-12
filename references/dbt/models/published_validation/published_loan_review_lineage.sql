{{ config(materialized='view', tags=['loan_review_published']) }}
select r.publication_id,r.run_id,r.attempt_id,r.entity,r.scope,r.record_kind,r.record_id,r.payload
from {{ ref('stg_publication_records') }} r join {{ ref('int_publication_checks') }} c using(table_publication_id)
where c.publication_valid and r.record_kind in ('evidence','input_bridge','evidence_bridge','source_evidence_bridge','source_receipt','delivery_receipt','calculation_receipt')
