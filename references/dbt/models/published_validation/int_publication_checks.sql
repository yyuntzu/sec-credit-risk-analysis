{{ config(materialized='view', tags=['loan_review_published'], pre_hook=publication_raw_bundle_ddl()) }}
{% set kinds=['fact','evidence','input_bridge','evidence_bridge','source_evidence_bridge','reconciliation','acceptance','source_receipt','delivery_receipt','release_policy','calculation_receipt'] %}
with batches as (
 select table_publication_id,
 count(*)-count(distinct to_json_string(struct(record_kind,record_id))) as duplicates,
 countif(record_kind='commit') as commit_count,
 countif(payload_sha256 is distinct from lower(to_hex(sha256(payload)))) as bad_hashes,
 countif(publication_id is distinct from table_publication_id) as bad_table_id,
 countif(record_kind not in ('commit',{% for kind in kinds %}'{{ kind }}'{% if not loop.last %},{% endif %}{% endfor %})) as unknown_kinds,
 {% for kind in kinds %}countif(record_kind='{{ kind }}') as {{ kind }}_count,{% endfor %}
 max(if(record_kind='commit' and record_id='publication',payload,null)) as commit_payload,
 max(if(record_kind='acceptance',payload,null)) as acceptance_payload,
 max(if(record_kind='calculation_receipt',payload,null)) as calculation_payload,
 max(if(record_kind='source_receipt',payload,null)) as source_payload,
 max(if(record_kind='delivery_receipt',payload,null)) as delivery_payload,
 max(if(record_kind='release_policy',payload,null)) as policy_payload,
 lower(to_hex(sha256(string_agg(if(record_kind!='commit',concat(record_kind,':',record_id,':',payload_sha256),null),'\n' order by record_kind,record_id)))) as computed_content_sha256
 from {{ ref('stg_publication_records') }} group by table_publication_id
), identities as (
 select *,json_value(commit_payload,'$.run_id') as run_id,json_value(commit_payload,'$.attempt_id') as attempt_id,
 json_value(commit_payload,'$.entity') as entity,json_value(commit_payload,'$.scope') as scope,
 json_value(commit_payload,'$.report_mode') as report_mode,
 json_value(commit_payload,'$.bindings.source_hash') as source_hash,
 json_value(commit_payload,'$.bindings.plan_hash') as plan_hash,
 json_value(commit_payload,'$.bindings.code_hash') as code_hash,
 json_value(commit_payload,'$.bindings.precision_version') as precision_version
 from batches
), source_rows as (
 select _TABLE_SUFFIX as table_source_id,* from {{ source('immutable_publication_sources','envelopes') }}
), sources_checked as (
 select i.table_publication_id,count(s.source_id) as physical_sources,
 countif(s.source_id is null or s.source_id is distinct from s.table_source_id
    or s.payload_sha256 is distinct from lower(to_hex(sha256(s.payload))) or s.payload_sha256 is distinct from s.source_id
    or s.entity is distinct from i.entity or s.scope is distinct from i.scope
    or s.request_hash is distinct from json_value(i.commit_payload,'$.bindings.request_hash')
    or lower(to_hex(sha256(`{{ target.project }}.{{ target.schema }}.publication_raw_bundle_v1`(s.payload)))) is distinct from i.source_hash) as bad_sources
 from identities i left join source_rows s on s.source_id=json_value(i.commit_payload,'$.source_id')
 group by i.table_publication_id
), records_checked as (
 select i.table_publication_id,
 count(distinct if(r.record_kind='reconciliation',concat(json_value(r.payload,'$.kind'),':',json_value(r.payload,'$.period_role')),null)) as distinct_reconciliations,
 countif(r.run_id is distinct from i.run_id or r.entity is distinct from i.entity or r.scope is distinct from i.scope
    or r.attempt_id is distinct from i.attempt_id) as foreign_records,
 countif(r.record_kind='fact' and (
    json_value(r.payload,'$.run_id') is distinct from i.run_id or json_value(r.payload,'$.entity') is distinct from i.entity
    or json_value(r.payload,'$.scope') is distinct from i.scope or json_value(r.payload,'$.source_hash') is distinct from i.source_hash
    or json_value(r.payload,'$.plan_hash') is distinct from i.plan_hash or json_value(r.payload,'$.precision_version') is distinct from i.precision_version)) as foreign_facts,
 countif(r.record_kind='reconciliation' and (json_value(r.payload,'$.verified') is distinct from 'true'
    or json_value(r.payload,'$.status') not in ('matched','within_precision')
    or json_value(r.payload,'$.kind') not in ('balance_sheet_equation','cash_bridge')
    or json_value(r.payload,'$.period_role') not in unnest(json_value_array(i.commit_payload,'$.period_roles')))) as bad_reconciliations
 from identities i join {{ ref('stg_publication_records') }} r using(table_publication_id)
 group by i.table_publication_id
), required_checked as (
 select i.table_publication_id,countif(f.record_id is null or json_value(f.payload,'$.status') not in ('sourced','calculated')
    or json_value(f.payload,'$.value') is null) as missing_required
 from identities i,unnest(json_value_array(i.commit_payload,'$.required_fact_ids')) fid
 left join {{ ref('stg_publication_records') }} f on f.table_publication_id=i.table_publication_id and f.record_kind='fact' and f.record_id=fid
 group by i.table_publication_id
), expected_edges as (
 select f.table_publication_id,'input_bridge' as kind,f.record_id as output_id,cast(pos as string) as position,parent as target_id
 from {{ ref('stg_publication_records') }} f,unnest(json_value_array(f.payload,'$.input_ids')) parent with offset pos where f.record_kind='fact'
 union all
 select f.table_publication_id,'evidence_bridge',f.record_id,'',eid
 from {{ ref('stg_publication_records') }} f,unnest(json_value_array(f.payload,'$.evidence_ids')) eid where f.record_kind='fact'
 union all
 select f.table_publication_id,'source_evidence_bridge',f.record_id,'',eid
 from {{ ref('stg_publication_records') }} f,unnest(json_value_array(f.payload,'$.source_evidence_ids')) eid where f.record_kind='fact'
), edges_checked as (
 select e.table_publication_id,count(*) as expected_edges,countif(b.record_id is null or t.record_id is null) as missing_edges
 from expected_edges e left join {{ ref('stg_publication_records') }} b on b.table_publication_id=e.table_publication_id and b.record_kind=e.kind
 and if(e.kind='input_bridge',json_value(b.payload,'$.output_fact_id'),json_value(b.payload,'$.fact_id'))=e.output_id
 and if(e.kind='input_bridge',json_value(b.payload,'$.input_position'),'')=e.position
 and if(e.kind='input_bridge',json_value(b.payload,'$.input_fact_id'),json_value(b.payload,'$.evidence_id'))=e.target_id
 left join {{ ref('stg_publication_records') }} t on t.table_publication_id=e.table_publication_id
 and t.record_kind=if(e.kind='input_bridge','fact','evidence') and t.record_id=e.target_id
 group by e.table_publication_id
)
select i.*,r.foreign_records,r.foreign_facts,r.bad_reconciliations,q.missing_required,
 coalesce(i.commit_count=1 and i.duplicates=0 and i.bad_hashes=0 and i.bad_table_id=0 and i.unknown_kinds=0
 and r.foreign_records=0 and r.foreign_facts=0 and r.bad_reconciliations=0 and q.missing_required=0
 and sc.physical_sources=1 and sc.bad_sources=0
 and coalesce(ec.missing_edges,0)=0 and coalesce(ec.expected_edges,0)=i.input_bridge_count+i.evidence_bridge_count+i.source_evidence_bridge_count
 and i.fact_count>0 and i.acceptance_count=1 and i.source_receipt_count=1 and i.delivery_receipt_count=1
 and i.release_policy_count=1 and i.calculation_receipt_count=1
 and json_value(i.commit_payload,'$.format_version')='warehouse-publication-v1'
 and json_value(i.commit_payload,'$.deployment')='validation' and i.entity='SYNTHETIC-ONLY'
 and i.computed_content_sha256=json_value(i.commit_payload,'$.content_sha256')
 and json_value(i.commit_payload,'$.gates.source_verified')='true'
 and json_value(i.commit_payload,'$.gates.dbt_tests_passed')='true'
 and json_value(i.commit_payload,'$.gates.financial_accepted')='true'
 and json_value(i.commit_payload,'$.gates.delivery_success')='true'
 and json_value(i.commit_payload,'$.gates.release_authorized')='true'
 and json_value(i.acceptance_payload,'$.substantive_data_ready')='true'
 and array_length(json_value_array(i.acceptance_payload,'$.acceptance_blockers'))=0
 and array_length(json_value_array(i.commit_payload,'$.period_roles'))=4
 and i.reconciliation_count=8 and r.distinct_reconciliations=8
 and array_length(json_value_array(i.commit_payload,'$.required_fact_ids'))>0
 and to_json_string(json_value_array(i.commit_payload,'$.required_fact_ids'))=to_json_string(json_value_array(i.acceptance_payload,'$.required_fact_ids'))
 and lower(to_hex(sha256(i.calculation_payload)))=json_value(i.commit_payload,'$.calculation_receipt_content_sha256')
 and to_json_string(json_query(i.calculation_payload,'$.bindings'))=to_json_string(json_query(i.commit_payload,'$.bindings'))
 {% for key in ['run_id','entity','scope','source_hash','plan_hash','precision_version'] %}
 and json_value(i.acceptance_payload,'$.{{ key }}')=json_value(i.commit_payload,'$.bindings.{{ key }}')
 {% endfor %}
 and lower(to_hex(sha256(i.source_payload)))=json_value(i.commit_payload,'$.source_receipt_content_sha256')
 and json_value(i.source_payload,'$.source_id')=json_value(i.commit_payload,'$.source_id')
 and json_value(i.source_payload,'$.request_hash')=json_value(i.commit_payload,'$.bindings.request_hash')
 and json_value(i.source_payload,'$.entity')=i.entity and json_value(i.source_payload,'$.scope')=i.scope
 and lower(to_hex(sha256(i.delivery_payload)))=json_value(i.commit_payload,'$.delivery_receipt_content_sha256')
 and json_value(i.delivery_payload,'$.run_id')=i.run_id and json_value(i.delivery_payload,'$.archive_attempt_id')=i.attempt_id
 and lower(to_hex(sha256(i.policy_payload)))=json_value(i.commit_payload,'$.release_policy_content_sha256')
 and json_value(i.policy_payload,'$.deployment')='validation'
 and to_json_string(json_value_array(i.policy_payload,'$.entity_allowlist'))='["SYNTHETIC-ONLY"]'
 and json_value(i.policy_payload,'$.release_id')=json_value(i.commit_payload,'$.release_id')
 and json_value(i.policy_payload,'$.package_sha256')=json_value(i.commit_payload,'$.package_sha256')
 {% for key in ['code_hash','formula_version','policy_version','precision_version'] %}
 and json_value(i.policy_payload,'$.{{ key }}')=json_value(i.commit_payload,'$.bindings.{{ key }}')
 {% endfor %}
 {% for kind in kinds %}and i.{{ kind }}_count=coalesce(cast(json_value(i.commit_payload,'$.record_counts.{{ kind }}') as int64),0){% endfor %}
 ,false) as publication_valid
from identities i join records_checked r using(table_publication_id) left join required_checked q using(table_publication_id)
left join edges_checked ec using(table_publication_id)
join sources_checked sc using(table_publication_id)
