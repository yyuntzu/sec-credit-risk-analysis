{{ config(materialized='view', tags=['formal_review_archive']) }}
select _TABLE_SUFFIX as table_attempt_id,*
from {{ source('review_candidate_archive','snapshots') }}
