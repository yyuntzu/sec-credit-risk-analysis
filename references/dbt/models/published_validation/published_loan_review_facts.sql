{{ config(materialized='view', tags=['loan_review_published']) }}
with selected as (
 select s.* from {{ source('validated_publications','selection') }} s
 join {{ source('validated_publications','selection_events') }} e
 using(entity,scope,report_mode,publication_id,version)
 qualify count(*) over(partition by entity,scope,report_mode)=1
)
select f.*,s.version as selection_version from {{ ref('published_history_facts') }} f
join selected s using(entity,scope,report_mode,publication_id)
