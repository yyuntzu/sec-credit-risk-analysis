{{ config(materialized='view', tags=['loan_review_published']) }}
select _TABLE_SUFFIX as table_publication_id,* from {{ source('validated_publications','batches') }}
