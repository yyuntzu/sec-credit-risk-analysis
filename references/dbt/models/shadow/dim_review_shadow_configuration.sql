{{ config(materialized='view', tags=['formal_review_shadow'], pre_hook=shadow_precision_ddl()) }}
-- Versioned SQL configuration. Editing producer metadata cannot approve policy.
select cast(1000000 as bignumeric) as money_scale,
 'Standard EBITDA: Net Income + Interest + Taxes + D&A' as standard_basis,
 'acceptance-v1.0-addendum-2026-10-23' as formula_version,
 'user-approved-2026-10-24' as policy_version,
 'bignumeric-q18-half-even-v1' as precision_version,
 true as precision_policy_implementation_approved,
 18 as division_decimal_places,
 'ROUND_HALF_EVEN' as division_rounding,
 false as precision_approved
