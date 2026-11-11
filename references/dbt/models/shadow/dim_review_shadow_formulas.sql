{{ config(materialized='view', tags=['formal_review_shadow']) }}
-- Independent SQL business contract; never inferred from the Python plan.
select * from unnest([
 struct('CF-01' as formula_id,'current_ratio' as target_metric,['current_assets','current_liabilities'] as input_metrics,'percent' as target_unit,['money','money'] as input_units,false as prior_second),
 ('CF-02','quick_ratio',['quick_assets','current_liabilities'],'percent',['money','money'],false),
 ('CF-03','cash_flow_ratio',['cfo','current_liabilities'],'percent',['money','money'],false),
 ('CF-04','interest_coverage',['pretax_profit','interest_expense','capitalized_interest'],'multiple',['money','money','money'],false),
 ('CF-05','ebitda_interest',['pretax_profit','interest_expense','da','capitalized_interest'],'multiple',['money','money','money','money'],false),
 ('CF-06','debt_ratio',['total_liabilities','net_worth'],'percent',['money','money'],false),
 ('CF-09','revenue_growth',['revenue','revenue'],'percent',['money','money'],true),
 ('CF-10','gross_margin',['gross_profit','revenue'],'percent',['money','money'],false),
 ('CF-11','operating_margin',['operating_income','revenue'],'percent',['money','money'],false),
 ('CF-12','pretax_margin',['pretax_profit','revenue'],'percent',['money','money'],false),
 ('CF-16','operating_margin_change',['operating_margin','operating_margin'],'percentage_points',['percent','percent'],true),
 ('CASH-CHANGE-v1','cash_change',['ending_cash','beginning_cash'],'money',['money','money'],false),
 ('LEVERAGE-v1','total_leverage',['total_debt','ltm_ebitda'],'multiple',['money','money'],false),
 ('STANDARD-EBITDA-v1','ltm_ebitda',['net_income','interest_expense','income_tax','da'],'money',['money','money','money','money'],false),
 ('DER-01','gross_profit',['revenue','cost_of_revenue'],'money',['money','money'],false),
 ('DER-02','cost_of_revenue',['revenue','gross_profit'],'money',['money','money'],false),
 ('DER-03','operating_expense',['gross_profit','operating_income'],'money',['money','money'],false),
 ('DER-04','operating_income',['gross_profit','operating_expense'],'money',['money','money'],false),
 ('DER-05','pretax_profit',['net_income','income_tax'],'money',['money','money'],false),
 ('DER-06','net_income',['pretax_profit','income_tax'],'money',['money','money'],false)
])
union all
select 'COMMON-SIZE-v1',metric,[metric,'revenue'],'percent',['money','money'],false
from unnest(['revenue','cost_of_revenue','gross_profit','operating_expense','operating_income',
 'interest_expense','pretax_profit','income_tax','net_income']) metric
