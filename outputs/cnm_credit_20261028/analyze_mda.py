import json,pathlib,sys
sys.path.insert(0,'scripts')
import agent_runner as r
p=pathlib.Path(__file__).parent
text=r._html_to_text((p/'2026-02-01.htm').read_text())
(p/'mda_input.txt').write_text(text)
metrics=['revenue','gross_profit','operating_income','interest_expense','pre_tax','current_assets','inventory','total_debt','ebitda','operating_cash']
result=r.generate_commentary(filing_text=text,metrics=metrics,company_name='Core & Main, Inc. (CNM), consolidated including NCI',period_label='FY2025 ended Feb 1 2026 (52 weeks), FY2024 ended Feb 2 2025 (53 weeks), FY2023 ended Jan 28 2024 (52 weeks); main comparison FY2025 versus FY2024; use Standard EBITDA (not Adjusted) when discussing leverage; as of Oct 28 2026')
(p/'commentary.json').write_text(json.dumps(result,indent=2))
print('MD&A model topics:',len(result))
