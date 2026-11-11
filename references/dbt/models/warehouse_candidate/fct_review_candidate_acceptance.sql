{{ config(materialized='view', tags=['formal_review_archive']) }}
select r.run_id,r.attempt_id,r.entity,r.scope,c.content_sha256,c.calculation_receipt_sha256,c.archive_integrity_passed,
 cast(json_value(r.payload,'$.substantive_data_ready') as bool) as substantive_data_ready,
 json_value_array(r.payload,'$.acceptance_blockers') as acceptance_blockers,
 json_value_array(r.payload,'$.unavailable_fact_ids') as unavailable_fact_ids,
 cast(json_value(r.payload,'$.verified_reconciliations') as int64) as verified_reconciliations,
 r.payload as frozen_acceptance_payload,false as precision_approved,false as final_report_accepted,false as publication_eligible
from {{ ref('stg_review_candidate_records') }} r join {{ ref('int_review_candidate_checks') }} c using(table_attempt_id)
where r.record_kind='acceptance' and r.record_id='financial'
