{{ config(materialized='view', tags=['formal_review_shadow']) }}
-- Approved domain requirements, independent of producer-supplied pending lists.
with units as (
 select metric,'money' as unit from unnest(['revenue','cost_of_revenue','gross_profit','operating_expense',
 'operating_income','interest_expense','pretax_profit','income_tax','net_income','beginning_cash','cfo','cfi','cff',
 'ending_cash','cash_change','total_debt','debt_service','ltm_ebitda','current_assets','current_liabilities',
 'quick_assets','total_liabilities','net_worth','capitalized_interest','da','total_assets','cash_fx','cash_other']) metric
 union all select metric,'percent' from unnest(['current_ratio','quick_ratio','cash_flow_ratio','debt_ratio',
 'revenue_growth','gross_margin','operating_margin','pretax_margin']) metric
 union all select metric,'multiple' from unnest(['interest_coverage','total_leverage','ebitda_interest','dscr']) metric
 union all select 'operating_margin_change','percentage_points'
 union all select 'ebitda_basis','text'
), requirements as (
 select * from unnest([
 struct('quick_ratio' as metric,['DEC-01'] as required_decisions,'Quick Assets / Current Liabilities' as definition),
 ('quick_assets',['DEC-01'],'Verified source Quick Assets'),
 ('debt_ratio',['DEC-02'],'Total Liabilities / Net Worth'),
 ('total_debt',['DEC-02'],'Consolidated interest-bearing borrowings, bonds and finance lease liabilities, including current portions once; exclude operating lease liabilities and trade payables'),
 ('net_worth',['DEC-02'],'Verified source Net Worth'),
 ('interest_expense',['DEC-05'],'Gross expensed interest without netting interest income; exclude separately capitalized interest'),
 ('capitalized_interest',['DEC-05'],'Verified source Capitalized Interest'),
 ('interest_coverage',['DEC-05'],'(Pre-tax Profit + Interest Expense) / (Interest Expense + Capitalized Interest)'),
 ('ebitda_interest',['DEC-05'],'(Pre-tax Profit + Interest Expense + D&A) / (Interest Expense + Capitalized Interest)'),
 ('ltm_ebitda',['DEC-06'],'Standard EBITDA: Net Income + Interest + Taxes + D&A'),
 ('ebitda_basis',['DEC-06'],'Source and actual EBITDA definition, including adjustments'),
 ('total_leverage',['DEC-02','DEC-06'],'Total debt / applicable LTM EBITDA'),
 ('debt_service',['DEC-03'],'Pending approved debt-service definition; no CapEx proxy'),
 ('dscr',['DEC-03'],'CFADS / Debt Service; CFADS and debt-service components pending confirmation')
 ])
)
select u.*,coalesce(r.required_decisions,array<string>[]) as required_decisions,r.definition
from units u left join requirements r using(metric)
