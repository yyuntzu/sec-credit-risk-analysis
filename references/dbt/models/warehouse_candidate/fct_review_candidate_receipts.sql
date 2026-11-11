{{ config(materialized='view', tags=['formal_review_archive']) }}
select run_id,attempt_id,entity,scope,table_attempt_id,content_sha256,computed_content_sha256,commit_sha256,calculation_receipt_sha256,
 source_hash,plan_hash,precision_version,
 json_value(commit_payload,'$.bindings.code_hash') as calculation_code_hash,
 json_value(commit_payload,'$.bindings.formula_version') as formula_version,
 json_value(commit_payload,'$.bindings.policy_version') as policy_version,
 json_value(commit_payload,'$.archive_code_hash') as archive_code_hash,
 fact_count,evidence_count,input_bridge_count,evidence_bridge_count,source_evidence_bridge_count,
 row_count,archive_integrity_passed,false as precision_approved,false as publication_eligible
from {{ ref('int_review_candidate_checks') }}
