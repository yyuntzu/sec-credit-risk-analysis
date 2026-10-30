import json,pathlib,sys
sys.path.insert(0,'scripts')
import agent_runner as r
p=pathlib.Path(__file__).parent
text=r._html_to_text((p/'2026-06-30.htm').read_text())
(p/'mda_input.txt').write_text(text)
metrics=['revenue','gross_profit','operating_income','interest_expense','pre_tax','current_assets','total_debt','operating_cash']
result=r.generate_commentary(filing_text=text,metrics=metrics,company_name='CDW Corporation',period_label='10-Q for six months ended June 30, 2026 versus June 30, 2025; balance sheets June 30, 2026 versus December 31, 2025; as of October 27, 2026')
(p/'commentary.json').write_text(json.dumps(result,indent=2))
print('MD&A explanations returned:',len(result))
