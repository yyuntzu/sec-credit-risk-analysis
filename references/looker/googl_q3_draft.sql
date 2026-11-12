-- User-authorized UNACCEPTED DRAFT. No writes to formal results/acceptance.
-- Existing BigQuery source bundle only; USD millions. Missing inputs remain NULL.
CREATE OR REPLACE VIEW `focus-heuristic-438521-v4.sec_raw.vw_googl_q3_draft_financials` AS
WITH records AS (
  SELECT record_kind,record_id,payload FROM `focus-heuristic-438521-v4.sec_raw.raw_review_sources`
  WHERE entity='GOOGL' AND run_id='353f7c1b63c542ef8592be3f27322562'
  QUALIFY ROW_NUMBER() OVER(PARTITION BY record_kind,record_id ORDER BY created_at DESC)=1
), periods AS (
  SELECT JSON_VALUE(p,'$.role') period_role,JSON_VALUE(p,'$.label') period_label,
    SAFE_CAST(JSON_VALUE(p,'$.start') AS DATE) period_start,
    SAFE_CAST(JSON_VALUE(p,'$.end') AS DATE) period_end
  FROM records,UNNEST(JSON_QUERY_ARRAY(payload,'$.request.periods')) p
  WHERE record_kind='metadata'
), observations AS (
  SELECT record_id,JSON_VALUE(payload,'$.field_name') field_name,
    SAFE_CAST(JSON_VALUE(payload,'$.start') AS DATE) start_date,
    SAFE_CAST(JSON_VALUE(payload,'$.end') AS DATE) end_date,
    SAFE_CAST(JSON_VALUE(payload,'$.value') AS BIGNUMERIC)*SAFE_CAST(JSON_VALUE(payload,'$.scale') AS BIGNUMERIC)/1000000 amount_m
  FROM records WHERE record_kind='evidence'
    AND JSON_VALUE(payload,'$.origin')='sec'
    AND JSON_VALUE(payload,'$.entity')='GOOGL'
    AND JSON_VALUE(payload,'$.scope')='entity-wide'
    AND JSON_VALUE(payload,'$.unit')='USD'
    AND JSON_VALUE(payload,'$.status')='sourced'
    AND SAFE_CAST(JSON_VALUE(payload,'$.document_date') AS DATE)<=DATE '2026-10-31'
  UNION ALL
  SELECT record_id,'interest_expense',
    SAFE_CAST(JSON_VALUE(payload,'$.start') AS DATE),
    SAFE_CAST(JSON_VALUE(payload,'$.end') AS DATE),
    SAFE_CAST(JSON_VALUE(payload,'$.value') AS BIGNUMERIC)*SAFE_CAST(JSON_VALUE(payload,'$.scale') AS BIGNUMERIC)/1000000
  FROM records WHERE record_kind='inputs'
    AND JSON_VALUE(payload,'$.metric')='interest_expense'
    AND JSON_VALUE(payload,'$.status')='sourced'
    AND JSON_VALUE(payload,'$.currency')='USD'
    AND NOT CONTAINS_SUBSTR(record_id,':pct:')
), grouped AS (
  SELECT p.period_role,IF(o.field_name='revenue_alt','revenue',o.field_name) metric,
    IF(COUNT(DISTINCT amount_m)=1 AND COUNTIF(amount_m IS NULL)=0,MAX(amount_m),NULL) amount_m,
    COUNT(DISTINCT amount_m)>1 conflict,
    STRING_AGG(DISTINCT record_id,',' ORDER BY record_id) source_ids
  FROM periods p JOIN observations o ON o.end_date=p.period_end
    AND (o.start_date IS NULL OR o.start_date=p.period_start)
  GROUP BY 1,2
), wide AS (
  SELECT p.*, max(if(metric='revenue', amount_m, null)) as revenue,
max(if(metric='cost_of_revenue', amount_m, null)) as cost_of_revenue,
max(if(metric='operating_income', amount_m, null)) as operating_income,
max(if(metric='net_income', amount_m, null)) as net_income,
max(if(metric='interest_expense', amount_m, null)) as interest_expense,
max(if(metric='income_tax_expense', amount_m, null)) as income_tax_expense,
max(if(metric='income_before_tax', amount_m, null)) as income_before_tax,
max(if(metric='cash', amount_m, null)) as cash,
max(if(metric='cfo', amount_m, null)) as cfo,
max(if(metric='cfi', amount_m, null)) as cfi,
max(if(metric='cff', amount_m, null)) as cff,
max(if(metric='total_assets', amount_m, null)) as total_assets,
max(if(metric='current_assets', amount_m, null)) as current_assets,
max(if(metric='current_liabilities', amount_m, null)) as current_liabilities,
max(if(metric='total_liabilities', amount_m, null)) as total_liabilities,
max(if(metric='stockholders_equity', amount_m, null)) as stockholders_equity,
max(if(metric='accounts_receivable_net', amount_m, null)) as accounts_receivable_net,
max(if(metric='accounts_payable', amount_m, null)) as accounts_payable,
max(if(metric='property_plant_equipment_net', amount_m, null)) as property_plant_equipment_net,
    COUNTIF(g.conflict) source_conflict_count,
    STRING_AGG(g.source_ids,',') source_ids
  FROM periods p LEFT JOIN grouped g USING(period_role)
  GROUP BY p.period_role,p.period_label,p.period_start,p.period_end
), derived AS (
  SELECT *,revenue-cost_of_revenue gross_profit,
    revenue-cost_of_revenue-operating_income operating_expenses,
    revenue-operating_income total_expenses,
    total_assets-current_assets noncurrent_assets,
    total_liabilities-current_liabilities noncurrent_liabilities,
    current_assets-cash other_current_assets_ex_cash,
    current_assets-cash-accounts_receivable_net other_current_assets_ex_cash_ar,
    total_assets-current_assets-property_plant_equipment_net other_noncurrent_assets_ex_ppe,
    current_liabilities-accounts_payable other_current_liabilities_ex_ap,
    SAFE_DIVIDE(revenue-cost_of_revenue,revenue) gross_margin,
    SAFE_DIVIDE(operating_income,revenue) operating_margin,
    SAFE_DIVIDE(net_income,revenue) net_margin,
    IF(period_role IN ('prior_interim','current_interim'),SAFE_DIVIDE(cfo,current_liabilities),NULL) cash_flow_ratio,
    CAST(NULL AS BIGNUMERIC) debt_ratio,
    SAFE_DIVIDE(total_liabilities,stockholders_equity) candidate_liabilities_to_equity,
    SAFE_DIVIDE(total_assets,stockholders_equity) assets_to_equity,
    SAFE_DIVIDE(total_liabilities,total_assets) liabilities_to_assets,
    total_assets-total_liabilities-stockholders_equity balance_sheet_residual,
    CAST(NULL AS BIGNUMERIC) beginning_cash,
    CAST(NULL AS BIGNUMERIC) ending_cash,
    CAST(NULL AS BIGNUMERIC) cash_fx,
    CAST(NULL AS BIGNUMERIC) cash_other,
    CAST(NULL AS BIGNUMERIC) cash_change
  FROM wide
)
SELECT *, 'GOOGL' entity,'Alphabet Inc.' entity_name,'353f7c1b63c542ef8592be3f27322562' source_run_id,
  'UNACCEPTED DRAFT' report_status,FALSE final_report_accepted,'USD millions' presentation_unit,
  period_role='current_interim' is_current,
  period_role IN ('prior_interim','current_interim') is_ytd,
  IF(period_role='current_interim',revenue,NULL) card_revenue,
  IF(period_role='current_interim',gross_profit,NULL) card_gross_profit,
  IF(period_role='current_interim',operating_income,NULL) card_operating_income,
  IF(period_role='current_interim',net_income,NULL) card_net_income,
  IF(period_role='current_interim',cash_flow_ratio,NULL) card_cash_flow_ratio,
  IF(period_role='current_interim',debt_ratio,NULL) card_debt_ratio,
  IF(period_role='current_interim',total_assets,NULL) card_total_assets,
  IF(period_role='current_interim',total_liabilities,NULL) card_total_liabilities,
  IF(period_role='current_interim',stockholders_equity,NULL) card_equity,
  IF(period_role='current_interim',assets_to_equity,NULL) card_assets_to_equity,
  IF(period_role='current_interim',liabilities_to_assets,NULL) card_liabilities_to_assets,
  'Draft derived values are not canonical accepted Report facts. CFO periods are YTD; equity uses source StockholdersEquity; Debt Ratio is NULL because net-worth equivalence is unapproved. CF beginning/ending cash and FX bridge unverified; AP/PPE may be missing.' limitations
FROM derived;

CREATE OR REPLACE VIEW `focus-heuristic-438521-v4.sec_raw.vw_googl_q3_draft_ytd` AS
SELECT * FROM `focus-heuristic-438521-v4.sec_raw.vw_googl_q3_draft_financials` WHERE is_ytd;

CREATE OR REPLACE VIEW `focus-heuristic-438521-v4.sec_raw.vw_googl_q3_draft_income` AS
SELECT f.entity,f.source_run_id,f.period_role,f.period_label,f.period_end,f.report_status,f.final_report_accepted,
  line.*,IF(line.amount_m IS NULL,'Missing / unverified','Draft source or derived') value_status
FROM `focus-heuristic-438521-v4.sec_raw.vw_googl_q3_draft_financials` f,
UNNEST([STRUCT(1 AS row_order,'Revenue' AS line_item,revenue AS amount_m),
STRUCT(2 AS row_order,'Cost of Revenue' AS line_item,cost_of_revenue AS amount_m),
STRUCT(3 AS row_order,'Gross Profit' AS line_item,gross_profit AS amount_m),
STRUCT(4 AS row_order,'Operating Expenses' AS line_item,operating_expenses AS amount_m),
STRUCT(5 AS row_order,'Operating Income' AS line_item,operating_income AS amount_m),
STRUCT(6 AS row_order,'Interest Expense' AS line_item,interest_expense AS amount_m),
STRUCT(7 AS row_order,'Pre-tax Income' AS line_item,income_before_tax AS amount_m),
STRUCT(8 AS row_order,'Income Tax' AS line_item,income_tax_expense AS amount_m),
STRUCT(9 AS row_order,'Net Income' AS line_item,net_income AS amount_m)]) line WHERE f.is_ytd;

CREATE OR REPLACE VIEW `focus-heuristic-438521-v4.sec_raw.vw_googl_q3_draft_cash_flow` AS
SELECT f.entity,f.source_run_id,f.period_role,f.period_label,f.period_end,f.report_status,f.final_report_accepted,
  line.*,IF(line.amount_m IS NULL,'Missing / unverified','Draft source or derived') value_status
FROM `focus-heuristic-438521-v4.sec_raw.vw_googl_q3_draft_financials` f,
UNNEST([STRUCT(1 AS row_order,'Beginning Cash (unverified)' AS line_item,beginning_cash AS amount_m),
STRUCT(2 AS row_order,'Operating Cash Flow' AS line_item,cfo AS amount_m),
STRUCT(3 AS row_order,'Investing Cash Flow' AS line_item,cfi AS amount_m),
STRUCT(4 AS row_order,'Financing Cash Flow' AS line_item,cff AS amount_m),
STRUCT(5 AS row_order,'FX Effect (unverified)' AS line_item,cash_fx AS amount_m),
STRUCT(6 AS row_order,'Other Adjustments (unverified)' AS line_item,cash_other AS amount_m),
STRUCT(7 AS row_order,'Cash Change (unverified)' AS line_item,cash_change AS amount_m),
STRUCT(8 AS row_order,'Ending Cash (unverified)' AS line_item,ending_cash AS amount_m)]) line WHERE f.is_ytd;

CREATE OR REPLACE VIEW `focus-heuristic-438521-v4.sec_raw.vw_googl_q3_draft_balance_sheet` AS
SELECT f.entity,f.source_run_id,f.period_role,f.period_label,f.period_end,f.report_status,f.final_report_accepted,
  line.*,IF(line.amount_m IS NULL,'Missing / unverified','Draft source or derived') value_status
FROM `focus-heuristic-438521-v4.sec_raw.vw_googl_q3_draft_financials` f,
UNNEST([STRUCT(1 AS row_order,'Cash and Cash Equivalents' AS line_item,cash AS amount_m),
STRUCT(2 AS row_order,'Accounts Receivable Net' AS line_item,accounts_receivable_net AS amount_m),
STRUCT(3 AS row_order,'Other Current Assets ex Cash/AR' AS line_item,other_current_assets_ex_cash_ar AS amount_m),
STRUCT(4 AS row_order,'Total Current Assets' AS line_item,current_assets AS amount_m),
STRUCT(5 AS row_order,'PPE Net (source unavailable)' AS line_item,property_plant_equipment_net AS amount_m),
STRUCT(6 AS row_order,'Other Non-current Assets ex PPE' AS line_item,other_noncurrent_assets_ex_ppe AS amount_m),
STRUCT(7 AS row_order,'Total Assets' AS line_item,total_assets AS amount_m),
STRUCT(8 AS row_order,'Accounts Payable (source unavailable)' AS line_item,accounts_payable AS amount_m),
STRUCT(9 AS row_order,'Other Current Liabilities ex AP' AS line_item,other_current_liabilities_ex_ap AS amount_m),
STRUCT(10 AS row_order,'Total Current Liabilities' AS line_item,current_liabilities AS amount_m),
STRUCT(11 AS row_order,'Non-current Liabilities' AS line_item,noncurrent_liabilities AS amount_m),
STRUCT(12 AS row_order,'Total Liabilities' AS line_item,total_liabilities AS amount_m),
STRUCT(13 AS row_order,'Equity (source StockholdersEquity)' AS line_item,stockholders_equity AS amount_m),
STRUCT(14 AS row_order,'Total Liabilities and Equity' AS line_item,total_liabilities+stockholders_equity AS amount_m)]) line ;

CREATE OR REPLACE VIEW `focus-heuristic-438521-v4.sec_raw.vw_googl_q3_draft_components_prior` AS
SELECT f.entity,f.source_run_id,f.period_label,f.period_end,f.report_status,line.*
FROM `focus-heuristic-438521-v4.sec_raw.vw_googl_q3_draft_financials` f,
UNNEST([
STRUCT('Assets' AS balance_side,'Cash' AS component,cash AS amount_m),
STRUCT('Assets','Other Current Assets',other_current_assets_ex_cash),
STRUCT('Assets','Non-current Assets',noncurrent_assets),
STRUCT('Liabilities and Equity','Current Liabilities',current_liabilities),
STRUCT('Liabilities and Equity','Non-current Liabilities',noncurrent_liabilities),
STRUCT('Liabilities and Equity','Equity',stockholders_equity)
]) line WHERE period_role='prior_interim';

CREATE OR REPLACE VIEW `focus-heuristic-438521-v4.sec_raw.vw_googl_q3_draft_components_current` AS
SELECT f.entity,f.source_run_id,f.period_label,f.period_end,f.report_status,line.*
FROM `focus-heuristic-438521-v4.sec_raw.vw_googl_q3_draft_financials` f,
UNNEST([
STRUCT('Assets' AS balance_side,'Cash' AS component,cash AS amount_m),
STRUCT('Assets','Other Current Assets',other_current_assets_ex_cash),
STRUCT('Assets','Non-current Assets',noncurrent_assets),
STRUCT('Liabilities and Equity','Current Liabilities',current_liabilities),
STRUCT('Liabilities and Equity','Non-current Liabilities',noncurrent_liabilities),
STRUCT('Liabilities and Equity','Equity',stockholders_equity)
]) line WHERE period_role='current_interim';
