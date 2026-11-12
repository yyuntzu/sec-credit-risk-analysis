{{ config(severity='error', tags=['loan_review_published']) }}
select table_publication_id as failure from {{ ref('int_publication_checks') }} where not publication_valid
union all
select publication_id from {{ ref('published_loan_review_facts') }} group by publication_id,fact_id having count(*)!=1
