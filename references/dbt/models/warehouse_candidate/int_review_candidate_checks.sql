{{ config(materialized='view', tags=['formal_review_archive']) }}
{% set kinds = ['artifact','fact','evidence','reconciliation','acceptance','commentary','input_bridge','evidence_bridge','source_evidence_bridge'] %}
{% set files = ['source_bundle.json','shadow_inputs.json','reconciliation_reviews.json','warehouse_facts.json','warehouse_reconciliations.json','warehouse_acceptance.json','kernel_results.json','dbt/run_results_run.json','dbt/run_results_test.json','dbt/target/manifest.json','warehouse_commentary.json','commentary_documents.json','calculation_receipt.json'] %}
with summaries as (
 select table_attempt_id,count(*) as row_count,
 count(*)-count(distinct to_json_string(struct(record_kind,record_id))) as duplicate_records,
 countif(record_kind='commit') as commit_count,
 countif(payload_sha256 is distinct from lower(to_hex(sha256(payload)))) as bad_hashes,
 countif(attempt_id is distinct from table_attempt_id) as bad_table_identity,
 countif(record_kind not in ('commit',{% for kind in kinds %}'{{ kind }}'{% if not loop.last %},{% endif %}{% endfor %})) as unknown_kinds,
 max(if(record_kind='commit' and record_id='calculation',payload,null)) as commit_payload,
 max(if(record_kind='commit' and record_id='calculation',payload_sha256,null)) as commit_sha256,
 lower(to_hex(sha256(string_agg(if(record_kind!='commit',concat(record_kind,':',record_id,':',payload_sha256),null),'\n' order by record_kind,record_id)))) as computed_content_sha256,
 {% for kind in kinds %}countif(record_kind='{{ kind }}') as {{ kind }}_count,{% endfor %}
 max(if(record_kind='artifact' and record_id='calculation_receipt.json',payload_sha256,null)) as calculation_receipt_sha256
 from {{ ref('stg_review_candidate_records') }} group by table_attempt_id
), bound as (
 select *,json_value(commit_payload,'$.run_id') as run_id,json_value(commit_payload,'$.attempt_id') as attempt_id,
 json_value(commit_payload,'$.entity') as entity,json_value(commit_payload,'$.scope') as scope,
 json_value(commit_payload,'$.content_sha256') as content_sha256,
 json_value(commit_payload,'$.bindings.source_hash') as source_hash,json_value(commit_payload,'$.bindings.plan_hash') as plan_hash,
 json_value(commit_payload,'$.bindings.precision_version') as precision_version
 from summaries
), record_checks as (
 select b.table_attempt_id,
 countif(r.run_id is distinct from b.run_id or r.attempt_id is distinct from b.attempt_id
     or r.entity is distinct from b.entity or r.scope is distinct from b.scope) as bad_identity,
 countif(r.record_kind='artifact' and r.payload_sha256 is distinct from case r.record_id
 {% for file in files %}when '{{ file }}' then json_value(b.commit_payload,'$.artifact_hashes."{{ file }}"'){% endfor %}
 else null end) as bad_artifact_bindings
 from bound b join {{ ref('stg_review_candidate_records') }} r using(table_attempt_id)
 group by b.table_attempt_id
)
select b.*,r.bad_identity,r.bad_artifact_bindings,
 coalesce(b.commit_count=1 and b.duplicate_records=0 and b.bad_hashes=0 and b.bad_table_identity=0 and b.unknown_kinds=0
 and r.bad_identity=0 and r.bad_artifact_bindings=0
 and json_value(b.commit_payload,'$.format_version')='candidate-archive-v1'
 and json_value(b.commit_payload,'$.precision_approved')='false' and json_value(b.commit_payload,'$.publication_eligible')='false'
 and b.computed_content_sha256=b.content_sha256
 and b.calculation_receipt_sha256=json_value(b.commit_payload,'$.calculation_receipt_sha256')
 and b.artifact_count=array_length(json_keys(parse_json(b.commit_payload).artifact_hashes,1))
 and b.fact_count>0 and b.acceptance_count=1
 {% for kind in kinds %}and b.{{ kind }}_count=coalesce(cast(json_value(b.commit_payload,'$.record_counts.{{ kind }}') as int64),0){% endfor %}
 ,false) as archive_integrity_passed,
 false as precision_approved,false as publication_eligible
from bound b join record_checks r using(table_attempt_id)
