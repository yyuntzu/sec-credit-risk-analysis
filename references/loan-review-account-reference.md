# AI 財務資料擷取：逐科目參考索引

日期：2026-10-23。此索引與[共通擷取準則](loan-review-extraction-reference.md)一起使用。305組原文／位置／子項情境完整涵蓋1,836筆原檔出現紀錄，並非305個已核准標準科目。原始字串與各來源均保留於[JSON參考資料](loan-review-account-reference.json)。

所有項目繼承G01–G10、F01–F07及E01；名稱、包含及排除項目均是查找／核對候選，須以當期申報確認。沒有正式METRICS代碼的項目不新增代碼、不塞入其他metric，也不作為現有supplement可接收的資料。標題不搜尋數值。

## 查閱索引

| 原始名稱／子項 | 報表／名稱行 | 沿用契約候選 | 既有tag候選 | 查閱 |
|---|---|---|---|---|
| Current Assets | BS / 10 | current_assets | 1 | [查看](#or01-report1-a10) |
| Cash & Cash Equivalents | BS / 11 | 未登錄／非契約科目 | 1 | [查看](#or01-report1-a11) |
| Financial Assets - Current | BS / 12 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a12) |
| Receivables | BS / 13 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a13) |
| Notes & Accounts Receivable | BS / 14 | 未登錄／非契約科目 | 1 | [查看](#or01-report1-a14) |
| Notes & Accounts Receivable - Related Party | BS / 15 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a15) |
| Other receivable | BS / 16 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a16) |
| Inventory | BS / 17 | 未登錄／非契約科目 | 1 | [查看](#or01-report1-a17) |
| Prepayments | BS / 18 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a18) |
| Other Current Assets | BS / 23 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a23) |
| Funds & Investments | BS / 24 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a24) |
| Fixed Assets | BS / 26 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a26) |
| Land | BS / 27 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a27) |
| Buildings | BS / 28 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a28) |
| Machinery Equipment | BS / 29 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a29) |
| Transport Equipment | BS / 30 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a30) |
| Other Fixed Assets | BS / 31 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a31) |
| Less: Accumulated Depreciation & Fixed Asset Impairment | BS / 32 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a32) |
| Uncompleted Constructions & Prepayments For Equipment Purchases | BS / 33 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a33) |
| Studio and transmission equipment | BS / 34 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a34) |
| Intangible Assets | BS / 35 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a35) |
| Intangible Assets | BS / 36 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a36) |
| Goodwill | BS / 37 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a37) |
| Other Assets | BS / 38 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a38) |
| Total Assets | BS / 39 | 未登錄／非契約科目 | 1 | [查看](#or01-report1-a39) |
| Current Liabilities | BS / 40 | current_liabilities | 1 | [查看](#or01-report1-a40) |
| Short Term Loans (including short term notes payable) | BS / 41 | 未登錄／非契約科目 | 3 | [查看](#or01-report1-a41) |
| Long Term Liabilities Maturing Within One Year | BS / 43 | 未登錄／非契約科目 | 3 | [查看](#or01-report1-a43) |
| Payables | BS / 44 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a44) |
| Notes & Accounts Payable | BS / 45 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a45) |
| Notes & Accounts Payable - Related Party | BS / 46 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a46) |
| Accrued Expenses | BS / 47 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a47) |
| Advance Receipts | BS / 48 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a48) |
| Amount Owed To/From Shareholders | BS / 49 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a49) |
| Other Current Liabilities | BS / 53 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a53) |
| Long Term Liabilities | BS / 54 | 未登錄／非契約科目 | 3 | [查看](#or01-report1-a54) |
| Long Term Bank Loans | BS / 55 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a55) |
| Corporate Bond Payable | BS / 56 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a56) |
| Provisions | BS / 58 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a58) |
| Deferred tax liabilities | BS / 59 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a59) |
| Other Liabilities | BS / 61 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a61) |
| Total Liabilities | BS / 62 | total_liabilities | 1 | [查看](#or01-report1-a62) |
| Share Capital / Paid-up Capital | BS / 63 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a63) |
| Additional paid-in capital | BS / 65 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a65) |
| Retained Earnings | BS / 66 | 未登錄／非契約科目 | 1 | [查看](#or01-report1-a66) |
| Adjustments To Shareholders' Equity | BS / 67 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a67) |
| Less: Treasury Stock | BS / 68 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a68) |
| Minority Interest | BS / 69 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a69) |
| Total Net Worth | BS / 70 | net_worth | 1 | [查看](#or01-report1-a70) |
| Total Liabilities & Net Worth | BS / 71 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a71) |
| Allowance For Inventory Devaluation | BS / 72 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a72) |
| Bad Debt Loss | BS / 73 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a73) |
| Revenues | IS / 80 | revenue | 2 | [查看](#or01-report1-a80) |
| Net Sales | IS / 81 | revenue | 2 | [查看](#or01-report1-a81) |
| Other Revenues | IS / 82 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a82) |
| Operating Cost | IS / 86 | cost_of_revenue | 2 | [查看](#or01-report1-a86) |
| Cost Of Goods Sold | IS / 87 | cost_of_revenue | 2 | [查看](#or01-report1-a87) |
| Other Operating Costs | IS / 88 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a88) |
| Realized Gains On Associated Companies | IS / 92 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a92) |
| Unrealized Gains On Associated Companies | IS / 93 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a93) |
| Gross Profit | IS / 94 | gross_profit | 1 | [查看](#or01-report1-a94) |
| Bad Debt Expense | IS / 95 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a95) |
| Operating Expense | IS / 96 | operating_expense | 1 | [查看](#or01-report1-a96) |
| Operating Profit | IS / 97 | operating_income | 1 | [查看](#or01-report1-a97) |
| Non-operating Revenues & Expenses - Net | IS / 98 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a98) |
| Non-operating Revenues | IS / 99 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a99) |
| Interest Income | IS / 100 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a100) |
| Investment Gains | IS / 101 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a101) |
| Gain On Fixed Asset Disposal | IS / 102 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a102) |
| Gain On Investment Disposal | IS / 103 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a103) |
| Other Income | IS / 104 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a104) |
| Non-operating Expenses | IS / 105 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a105) |
| Interest Expense | IS / 106 | interest_expense | 2 | [查看](#or01-report1-a106) |
| Investment Loss | IS / 107 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a107) |
| Loss on extinguishment of debt | IS / 108 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a108) |
| Loss On Investment Disposal | IS / 109 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a109) |
| Other Expenses | IS / 110 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a110) |
| Pre-tax Profit (Loss) | IS / 111 | pretax_profit | 1 | [查看](#or01-report1-a111) |
| Income Tax Expense(Credit) | IS / 112 | income_tax | 1 | [查看](#or01-report1-a112) |
| Profit (Loss) From Discontinued Operations | IS / 113 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a113) |
| Extraordinary Profit (Loss) | IS / 114 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a114) |
| Cumulative Effects Of Changes In Accounting Policies | IS / 115 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a115) |
| Other Adjustments | IS / 116 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a116) |
| After-tax Net Profit (Loss) | IS / 117 | net_income | 1 | [查看](#or01-report1-a117) |
| Sales To Related Parties | IS / 118 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a118) |
| % Of Related Party Sales To Total Sales | IS / 119 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a119) |
| Capitalized Interest | IS / 120 | capitalized_interest | 1 | [查看](#or01-report1-a120) |
| Depreciation & Amortization | IS / 121 | da | 1 | [查看](#or01-report1-a121) |
| Prepayments To Related Parties | IS / 122 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a122) |
| (operating income) Rental income from properties | IS / 123 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a123) |
| (non-operating income) Rental income from properties | IS / 125 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a125) |
| Cash and cash equivalents - beginning of period | CF / 129 | beginning_cash | 1 | [查看](#or01-report1-a129) |
| Cash Flow From Operating Activities | CF / 130 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a130) |
| Net profit (loss) after tax | CF / 131 | net_income | 1 | [查看](#or01-report1-a131) |
| Income and loss items that do not affect cash flow from operating activities | CF / 132 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a132) |
| Depreciation & Amortization | CF / 133 | da | 1 | [查看](#or01-report1-a133) |
| Other Adjustment items | CF / 134 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a134) |
| Dividend and interest income | CF / 135 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a135) |
| Loss (gain) on valuation of financial assets | CF / 136 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a136) |
| Investment loss (gain) recognized under equity method | CF / 137 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a137) |
| Loss (gain on reversal) of bad debts | CF / 138 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a138) |
| Allowance (reversal) for inventory valuation and obsolescence loss | CF / 139 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a139) |
| Loss (gain) on disposal of investments | CF / 140 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a140) |
| Loss (gain) on disposal of property, equipment and plant | CF / 141 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a141) |
| Unrealized foreign exchange loss (gain) ,net | CF / 142 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a142) |
| Payment for broadcast rights | CF / 143 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a143) |
| Changes in assets/liabilities associated with operating activities | CF / 144 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a144) |
| Decrease (Increase) In Accounts Receivable | CF / 145 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a145) |
| Other receivables | CF / 146 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a146) |
| Decrease (Increase) In Other noncurrent assets | CF / 147 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a147) |
| Prepayments | CF / 148 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a148) |
| Increase (Decrease) In Accrued expenses and other current liabilities | CF / 149 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a149) |
| Increase (Decrease) In Accounts Payable | CF / 150 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a150) |
| Expense payable | CF / 151 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a151) |
| Unearned receipts | CF / 152 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a152) |
| Increase (Decrease) In Other noncurrent Liabilities | CF / 153 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a153) |
| Income tax payable | CF / 154 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a154) |
| Interest paid | CF / 155 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a155) |
| Interest received | CF / 156 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a156) |
| Dividends received | CF / 157 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a157) |
| Other | CF / 158 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a158) |
| Net cash generated by (used in) operating activities | CF / 159 | cfo | 1 | [查看](#or01-report1-a159) |
| Cash Flow From Investing Activities | CF / 160 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a160) |
| Financial assets - current | CF / 161 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a161) |
| Financial assets - non-current | CF / 162 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a162) |
| Investments accounted for using equity method | CF / 163 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a163) |
| Proceeds from disposals of property and equipment | CF / 164 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a164) |
| Intangible assets | CF / 165 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a165) |
| Dviidends and interest received | CF / 166 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a166) |
| Purchases of property and equipment | CF / 167 | 未登錄／非契約科目 | 1 | [查看](#or01-report1-a167) |
| Proceeds from sale of stations | CF / 168 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a168) |
| Payment for acquisition | CF / 169 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a169) |
| Proceeds from disposal of an investment | CF / 170 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a170) |
| Proceeds received from life insurance policies | CF / 171 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a171) |
| Other | CF / 172 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a172) |
| Net cash generated by (used in) investing activities | CF / 173 | cfi | 1 | [查看](#or01-report1-a173) |
| Cash flow from financing activities | CF / 174 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a174) |
| Repayments of long-term debt | CF / 175 | 未登錄／非契約科目 | 2 | [查看](#or01-report1-a175) |
| Proceeds from long-term debt, including debt premium and discounts | CF / 176 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a176) |
| Payables-related parties | CF / 177 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a177) |
| Issuances of bonds payable | CF / 178 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a178) |
| Repayments of bonds payable | CF / 179 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a179) |
| Payments for debt financing costs | CF / 180 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a180) |
| Premium paid on debt extinguishment | CF / 181 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a181) |
| Common stock dividends paid | CF / 182 | 未登錄／非契約科目 | 1 | [查看](#or01-report1-a182) |
| Purchase of treasury stock | CF / 183 | 未登錄／非契約科目 | 1 | [查看](#or01-report1-a183) |
| Cash paid for shares withheld for taxes | CF / 184 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a184) |
| Other | CF / 188 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a188) |
| Net cash generated by (used in) financing activities | CF / 189 | cff | 1 | [查看](#or01-report1-a189) |
| Effects Of Exchange Rate Variation | CF / 190 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a190) |
| Net Cash Inflow (outflow) for current period | CF / 191 | cash_change | 0 | [查看](#or01-report1-a191) |
| Cash and cash equivalents - end of period | CF / 194 | ending_cash | 1 | [查看](#or01-report1-a194) |
| Liquidity | RATIO / 196 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a196) |
| Current Ratio | RATIO / 197 | current_ratio | 0 | [查看](#or01-report1-a197) |
| Quick Ratio | RATIO / 198 | quick_ratio | 0 | [查看](#or01-report1-a198) |
| Cash Flow Ratio | RATIO / 199 | cash_flow_ratio | 0 | [查看](#or01-report1-a199) |
| Interest Coverage Ratio | RATIO / 200 | interest_coverage | 0 | [查看](#or01-report1-a200) |
| EBITDA / Interest Expenses | RATIO / 201 | ebitda_interest | 0 | [查看](#or01-report1-a201) |
| Financial Structure | RATIO / 202 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a202) |
| Debt Ratio | RATIO / 203 | debt_ratio | 0 | [查看](#or01-report1-a203) |
| Fixed Asset To Net Worth Ratio | RATIO / 204 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a204) |
| Fixed Assets To Long Term Capital Ratio | RATIO / 205 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a205) |
| Profitability | RATIO / 206 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a206) |
| Revenue Growth Rate | RATIO / 207 | revenue_growth | 0 | [查看](#or01-report1-a207) |
| Gross Profit Margin | RATIO / 208 | gross_margin | 0 | [查看](#or01-report1-a208) |
| Operating Profit Margin | RATIO / 209 | operating_margin | 0 | [查看](#or01-report1-a209) |
| Pre-tax Profit Margin | RATIO / 210 | pretax_margin | 0 | [查看](#or01-report1-a210) |
| Return On Net Worth | RATIO / 211 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a211) |
| Return On Asset | RATIO / 212 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a212) |
| Financial Expense Ratio | RATIO / 213 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a213) |
| Change In Operating Profit Margin | RATIO / 214 | operating_margin_change | 0 | [查看](#or01-report1-a214) |
| Business Management | RATIO / 215 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a215) |
| Accounts Receivable Turnover / 次數 | RATIO / 217 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a217-次數) |
| Accounts Receivable Turnover / 天數 | RATIO / 217 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a217-天數) |
| Accounts Payable Turnover / 次數 | RATIO / 221 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a221-次數) |
| Accounts Payable Turnover / 天數 | RATIO / 221 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a221-天數) |
| Inventory Turnover / 次數 | RATIO / 225 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a225-次數) |
| Inventory Turnover / 天數 | RATIO / 225 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a225-天數) |
| Fixed Asset Turnover / 次數 | RATIO / 229 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a229-次數) |
| Fixed Asset Turnover / 天數 | RATIO / 229 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a229-天數) |
| Total Asset Turnover / 次數 | RATIO / 232 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a232-次數) |
| Total Asset Turnover / 天數 | RATIO / 232 | 未登錄／非契約科目 | 0 | [查看](#or01-report1-a232-天數) |
| Payments for broadcast rights | CF / 143 | 未登錄／非契約科目 | 0 | [查看](#or02-report1-a143) |
| Payments for acquisitions | CF / 169 | 未登錄／非契約科目 | 0 | [查看](#or02-report1-a169) |
| Income Taxes Receivable | BS / 19 | 未登錄／非契約科目 | 0 | [查看](#or03-report1-a19) |
| Income Taxes Payable | BS / 50 | 未登錄／非契約科目 | 0 | [查看](#or03-report1-a50) |
| Long-Term Income Taxes Payable | BS / 59 | 未登錄／非契約科目 | 0 | [查看](#or03-report1-a59) |
| Long-Term Operating Lease Liabilities | BS / 60 | 未登錄／非契約科目 | 0 | [查看](#or03-report1-a60) |
| Asset impairments | IS / 108 | 未登錄／非契約科目 | 0 | [查看](#or03-report1-a108) |
| Depreciation and amortization expenses | CF / 133 | da | 1 | [查看](#or03-report1-a133) |
| Operating lease cost | CF / 134 | 未登錄／非契約科目 | 0 | [查看](#or03-report1-a134) |
| Inventory donations | CF / 135 | 未登錄／非契約科目 | 0 | [查看](#or03-report1-a135) |
| Provision (recovery) for doubtful accounts, net | CF / 136 | 未登錄／非契約科目 | 0 | [查看](#or03-report1-a136) |
| Share-based compensation | CF / 137 | 未登錄／非契約科目 | 0 | [查看](#or03-report1-a137) |
| Asset impairments | CF / 138 | 未登錄／非契約科目 | 0 | [查看](#or03-report1-a138) |
| Deferred taxes | CF / 139 | 未登錄／非契約科目 | 0 | [查看](#or03-report1-a139) |
| Loss on disposal of assets | CF / 140 | 未登錄／非契約科目 | 0 | [查看](#or03-report1-a140) |
| Other non-cash items | CF / 143 | 未登錄／非契約科目 | 0 | [查看](#or03-report1-a143) |
| Accounts receivable, net of allowances | CF / 145 | 未登錄／非契約科目 | 0 | [查看](#or03-report1-a145) |
| Inventories | CF / 146 | 未登錄／非契約科目 | 0 | [查看](#or03-report1-a146) |
| Prepaid expenses and other assets | CF / 147 | 未登錄／非契約科目 | 0 | [查看](#or03-report1-a147) |
| Accounts payable | CF / 148 | 未登錄／非契約科目 | 0 | [查看](#or03-report1-a148) |
| Accrued expenses and other liabilities | CF / 149 | 未登錄／非契約科目 | 0 | [查看](#or03-report1-a149) |
| Right-of-use assets and operating lease liabilities | CF / 150 | 未登錄／非契約科目 | 0 | [查看](#or03-report1-a150) |
| Income taxes | CF / 151 | 未登錄／非契約科目 | 0 | [查看](#or03-report1-a151) |
| Others | CF / 158 | 未登錄／非契約科目 | 0 | [查看](#or03-report1-a158) |
| Purchases of property, equipment, and software | CF / 161 | 未登錄／非契約科目 | 1 | [查看](#or03-report1-a161) |
| Proceeds from disposal of property and equipment | CF / 162 | 未登錄／非契約科目 | 0 | [查看](#or03-report1-a162) |
| Acquisition of HEYDUDE, net of cash acquired | CF / 163 | 未登錄／非契約科目 | 0 | [查看](#or03-report1-a163) |
| Others | CF / 172 | 未登錄／非契約科目 | 0 | [查看](#or03-report1-a172) |
| Proceeds from notes issuance | CF / 175 | 未登錄／非契約科目 | 0 | [查看](#or03-report1-a175) |
| Proceeds from bank borrowings | CF / 176 | 未登錄／非契約科目 | 0 | [查看](#or03-report1-a176) |
| Repayments of bank borrowings | CF / 177 | 未登錄／非契約科目 | 2 | [查看](#or03-report1-a177) |
| Deferred debt issuance costs | CF / 178 | 未登錄／非契約科目 | 0 | [查看](#or03-report1-a178) |
| Repurchases of common stock | CF / 179 | 未登錄／非契約科目 | 1 | [查看](#or03-report1-a179) |
| Repurchases of common stock for tax withholding | CF / 180 | 未登錄／非契約科目 | 1 | [查看](#or03-report1-a180) |
| Others | CF / 188 | 未登錄／非契約科目 | 0 | [查看](#or03-report1-a188) |
| Effect of exchange rate changes | CF / 190 | 未登錄／非契約科目 | 0 | [查看](#or03-report1-a190) |
| Prepaid expenses and other current assets | BS / 19 | 未登錄／非契約科目 | 0 | [查看](#or04-report1-a19) |
| Accrued Expenses - Related Party | BS / 48 | 未登錄／非契約科目 | 0 | [查看](#or04-report1-a48) |
| Other | BS / 57 | 未登錄／非契約科目 | 0 | [查看](#or04-report1-a57) |
| Revenue from related party | IS / 83 | 未登錄／非契約科目 | 0 | [查看](#or04-report1-a83) |
| Loss On Fixed Asset Disposal | IS / 108 | 未登錄／非契約科目 | 0 | [查看](#or04-report1-a108) |
| Income tax benefit (expense) | IS / 113 | income_tax | 1 | [查看](#or04-report1-a113) |
| Stock-based compensation expense | CF / 134 | 未登錄／非契約科目 | 0 | [查看](#or04-report1-a134) |
| Deferred income taxes | CF / 135 | 未登錄／非契約科目 | 0 | [查看](#or04-report1-a135) |
| Non-cash interest expense | CF / 136 | 未登錄／非契約科目 | 0 | [查看](#or04-report1-a136) |
| Loss on extinguishment of convertible debt | CF / 137 | 未登錄／非契約科目 | 0 | [查看](#or04-report1-a137) |
| Provision for credit losses | CF / 138 | 未登錄／非契約科目 | 0 | [查看](#or04-report1-a138) |
| Unrealized loss (gain) on investments | CF / 139 | 未登錄／非契約科目 | 0 | [查看](#or04-report1-a139) |
| Others | CF / 143 | 未登錄／非契約科目 | 0 | [查看](#or04-report1-a143) |
| Accounts receivable | CF / 145 | 未登錄／非契約科目 | 0 | [查看](#or04-report1-a145) |
| Accounts receivable — related party | CF / 146 | 未登錄／非契約科目 | 0 | [查看](#or04-report1-a146) |
| Inventories | CF / 147 | 未登錄／非契約科目 | 0 | [查看](#or04-report1-a147) |
| Prepaid expenses and other assets | CF / 148 | 未登錄／非契約科目 | 0 | [查看](#or04-report1-a148) |
| Other current assets | CF / 149 | 未登錄／非契約科目 | 0 | [查看](#or04-report1-a149) |
| Accounts payable | CF / 150 | 未登錄／非契約科目 | 0 | [查看](#or04-report1-a150) |
| Accrued expenses and other liabilities | CF / 151 | 未登錄／非契約科目 | 0 | [查看](#or04-report1-a151) |
| Accrued expenses and other liabilities — related party | CF / 152 | 未登錄／非契約科目 | 0 | [查看](#or04-report1-a152) |
| Other current liabilities | CF / 153 | 未登錄／非契約科目 | 0 | [查看](#or04-report1-a153) |
| Capital expenditures | CF / 161 | 未登錄／非契約科目 | 1 | [查看](#or04-report1-a161) |
| Investments in developed software | CF / 162 | 未登錄／非契約科目 | 0 | [查看](#or04-report1-a162) |
| Cash paid for investments | CF / 163 | 未登錄／非契約科目 | 0 | [查看](#or04-report1-a163) |
| Acquisition of other intangible assets | CF / 164 | 未登錄／非契約科目 | 0 | [查看](#or04-report1-a164) |
| Acquisition of a business | CF / 165 | 未登錄／非契約科目 | 0 | [查看](#or04-report1-a165) |
| Proceeds from issuance of term loan, net of issuance costs | CF / 175 | 未登錄／非契約科目 | 0 | [查看](#or04-report1-a175) |
| Repayment of term loan | CF / 176 | 未登錄／非契約科目 | 2 | [查看](#or04-report1-a176) |
| Repayment of equipment financings | CF / 177 | 未登錄／非契約科目 | 0 | [查看](#or04-report1-a177) |
| Financing lease payments | CF / 178 | 未登錄／非契約科目 | 0 | [查看](#or04-report1-a178) |
| Repayment of mortgage | CF / 179 | 未登錄／非契約科目 | 2 | [查看](#or04-report1-a179) |
| Proceeds from secured borrowing (Note 6) | CF / 180 | 未登錄／非契約科目 | 0 | [查看](#or04-report1-a180) |
| Repayment of secured borrowing (Note 6) | CF / 181 | 未登錄／非契約科目 | 2 | [查看](#or04-report1-a181) |
| Proceeds from exercise of stock options | CF / 182 | 未登錄／非契約科目 | 0 | [查看](#or04-report1-a182) |
| Proceeds from issuance of common stock under employee stock purchase plan | CF / 183 | 未登錄／非契約科目 | 0 | [查看](#or04-report1-a183) |
| Payment of withholding taxes in connection with vesting of restricted stock units | CF / 184 | 未登錄／非契約科目 | 0 | [查看](#or04-report1-a184) |
| Repayment of convertible debt | CF / 185 | 未登錄／非契約科目 | 2 | [查看](#or04-report1-a185) |
| Proceeds from issuance of senior unsecured notes, net of issuance costs | CF / 186 | 未登錄／非契約科目 | 0 | [查看](#or04-report1-a186) |
| Repurchase of common stock | CF / 187 | 未登錄／非契約科目 | 1 | [查看](#or04-report1-a187) |
| Depreciation and amortization | CF / 133 | da | 1 | [查看](#or05-report1-a133) |
| Loss on repayment of loans | CF / 134 | 未登錄／非契約科目 | 2 | [查看](#or05-report1-a134) |
| Deferred taxes | CF / 135 | 未登錄／非契約科目 | 0 | [查看](#or05-report1-a135) |
| Stock-based compensation | CF / 136 | 未登錄／非契約科目 | 0 | [查看](#or05-report1-a136) |
| Other | CF / 143 | 未登錄／非契約科目 | 0 | [查看](#or05-report1-a143) |
| Trade accounts receivable | CF / 145 | 未登錄／非契約科目 | 0 | [查看](#or05-report1-a145) |
| Other current and long-term assets | CF / 146 | 未登錄／非契約科目 | 0 | [查看](#or05-report1-a146) |
| Trade accounts payable | CF / 147 | 未登錄／非契約科目 | 0 | [查看](#or05-report1-a147) |
| Other current and long-term liabilities | CF / 148 | 未登錄／非契約科目 | 0 | [查看](#or05-report1-a148) |
| Proceeds from sale/maturities of other investments | CF / 162 | 未登錄／非契約科目 | 0 | [查看](#or05-report1-a162) |
| Investments in nonconsolidated affiliates and notes receivable | CF / 163 | 未登錄／非契約科目 | 0 | [查看](#or05-report1-a163) |
| Proceeds from term loans | CF / 175 | 未登錄／非契約科目 | 0 | [查看](#or05-report1-a175) |
| Repayments of term loans | CF / 176 | 未登錄／非契約科目 | 2 | [查看](#or05-report1-a176) |
| Repayments of debt | CF / 177 | 未登錄／非契約科目 | 2 | [查看](#or05-report1-a177) |
| Debt financing fees | CF / 178 | 未登錄／非契約科目 | 0 | [查看](#or05-report1-a178) |
| Dividends to shareholders | CF / 179 | 未登錄／非契約科目 | 1 | [查看](#or05-report1-a179) |
| Proceeds from issuance of common stock | CF / 180 | 未登錄／非契約科目 | 0 | [查看](#or05-report1-a180) |
| Employee taxes paid on restricted stock units recorded as treasury stock | CF / 181 | 未登錄／非契約科目 | 1 | [查看](#or05-report1-a181) |
| Repurchase of common stock | CF / 182 | 未登錄／非契約科目 | 1 | [查看](#or05-report1-a182) |
| Proceeds from revolving credit facility | CF / 183 | 未登錄／非契約科目 | 0 | [查看](#or05-report1-a183) |
| Impairment of an equity method investment | IS / 108 | 未登錄／非契約科目 | 0 | [查看](#or07-report1-a108) |
| Impairment of an equity method investment | CF / 142 | 未登錄／非契約科目 | 0 | [查看](#or07-report1-a142) |
| Income tax paid | CF / 154 | 未登錄／非契約科目 | 0 | [查看](#or07-report1-a154) |
| Current assets of discontinued operations | BS / 22 | 未登錄／非契約科目 | 0 | [查看](#or08-report1-a22) |
| Current Liabilities of discontinued operations | BS / 52 | 未登錄／非契約科目 | 0 | [查看](#or08-report1-a52) |
| Other Long Term Debt | BS / 57 | 未登錄／非契約科目 | 0 | [查看](#or08-report1-a57) |
| Purchased transportation | IS / 89 | 未登錄／非契約科目 | 0 | [查看](#or08-report1-a89) |
| Fuel, operating expenses and supplies | IS / 90 | 未登錄／非契約科目 | 0 | [查看](#or08-report1-a90) |
| Depreciation and amortization expense | IS / 91 | 未登錄／非契約科目 | 0 | [查看](#or08-report1-a91) |
| Gain On Sale of Fixed Asset | IS / 102 | 未登錄／非契約科目 | 0 | [查看](#or08-report1-a102) |
| Depreciation and Amortization | CF / 133 | da | 1 | [查看](#or08-report1-a133) |
| Stock compensation expense | CF / 134 | 未登錄／非契約科目 | 0 | [查看](#or08-report1-a134) |
| Accretion of debt | CF / 135 | 未登錄／非契約科目 | 0 | [查看](#or08-report1-a135) |
| Deferred tax expense | CF / 136 | 未登錄／非契約科目 | 0 | [查看](#or08-report1-a136) |
| Gains on sales of property and equipment | CF / 137 | 未登錄／非契約科目 | 0 | [查看](#or08-report1-a137) |
| Accounts payable | CF / 146 | 未登錄／非契約科目 | 0 | [查看](#or08-report1-a146) |
| Accrued expenses and other liabilities | CF / 147 | 未登錄／非契約科目 | 0 | [查看](#or08-report1-a147) |
| Payment for purchases of property and equipment | CF / 161 | 未登錄／非契約科目 | 1 | [查看](#or08-report1-a161) |
| Proceeds from sale of property and equipment | CF / 162 | 未登錄／非契約科目 | 0 | [查看](#or08-report1-a162) |
| Repayment of debt and finance leases | CF / 175 | 未登錄／非契約科目 | 2 | [查看](#or08-report1-a175) |
| Payment for debt issuance costs | CF / 176 | 未登錄／非契約科目 | 0 | [查看](#or08-report1-a176) |
| Repurchase of common stock | CF / 177 | 未登錄／非契約科目 | 1 | [查看](#or08-report1-a177) |
| Change in bank overdrafts | CF / 178 | 未登錄／非契約科目 | 0 | [查看](#or08-report1-a178) |
| Payment for tax withholdings for restricted shares | CF / 179 | 未登錄／非契約科目 | 0 | [查看](#or08-report1-a179) |
| Repurchase of debt | CF / 180 | 未登錄／非契約科目 | 0 | [查看](#or08-report1-a180) |
| Distribution from RXO and GXO spins, net | CF / 181 | 未登錄／非契約科目 | 0 | [查看](#or08-report1-a181) |
| Net cash provided by (used in) discontinued operations | CF / 192 | 未登錄／非契約科目 | 0 | [查看](#or08-report1-a192) |

## OR01-Report1-A10

原始英文：`Current Assets`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | BS 名稱行10；OR01/Nexstar/Quarter/Report1!A10 → 數值行10; OR02/Nexstar/Quarter/Report1!A10 → 數值行10; OR03/CROX/Quarter/Report1!A10 → 數值行10; OR04/Insulet/Quarter/Report1!A10 → 數值行10; OR05/TransUnion/Quarter/Report1!A10 → 數值行10; OR06/TransUnion/Quarter/Report1!A10 → 數值行10; OR07/Nexstar/Year/Report1!A10 → 數值行10; OR08/XPO/Year/Report1!A10 → 數值行10; OR09/CROX/Year/Report1!A10 → 數值行10; OR10/Insulet/Year/Report1!A10 → 數值行10; OR11/TransUnion/Year/Report1!A10 → 數值行10 |
| 意義候選 | 來源列示的流動資產總額 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 流動分類之資產 |
| 排除與不可替代項 | 非流動資產；總額與其明細不可重複加總 |
| 既有代碼 | METRICS候選：current_assets；raw候選：current_assets。兩者不可互換。 |
| SEC查找位置 | Consolidated Balance Sheets；資產負債表；該資產／負債／權益附註 |
| 候選XBRL tags | us-gaap:AssetsCurrent → raw.current_assets |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：DER-07。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=instant；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A11

原始英文：`Cash & Cash Equivalents`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | BS 名稱行11；OR01/Nexstar/Quarter/Report1!A11 → 數值行11; OR02/Nexstar/Quarter/Report1!A11 → 數值行11; OR03/CROX/Quarter/Report1!A11 → 數值行11; OR04/Insulet/Quarter/Report1!A11 → 數值行11; OR05/TransUnion/Quarter/Report1!A11 → 數值行11; OR06/TransUnion/Quarter/Report1!A11 → 數值行11; OR07/Nexstar/Year/Report1!A11 → 數值行11; OR08/XPO/Year/Report1!A11 → 數值行11; OR09/CROX/Year/Report1!A11 → 數值行11; OR10/Insulet/Year/Report1!A11 → 數值行11; OR11/TransUnion/Year/Report1!A11 → 數值行11 |
| 意義候選 | 現金及約當現金餘額；須確認受限制現金是否另列 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 經核實的現金及約當現金 |
| 排除與不可替代項 | 受限制現金不得未核定即併入；不自動等同CF期末現金 |
| 既有代碼 | METRICS候選：無；raw候選：cash。兩者不可互換。 |
| SEC查找位置 | Consolidated Balance Sheets；資產負債表；該資產／負債／權益附註 |
| 候選XBRL tags | us-gaap:CashAndCashEquivalentsAtCarryingValue → raw.cash |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：DER-08。 |
| 核准公式／推導條件引用 | DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=instant；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A12

原始英文：`Financial Assets - Current`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | BS 名稱行12；OR01/Nexstar/Quarter/Report1!A12 → 數值行12; OR02/Nexstar/Quarter/Report1!A12 → 數值行12; OR03/CROX/Quarter/Report1!A12 → 數值行12; OR04/Insulet/Quarter/Report1!A12 → 數值行12; OR05/TransUnion/Quarter/Report1!A12 → 數值行12; OR06/TransUnion/Quarter/Report1!A12 → 數值行12; OR07/Nexstar/Year/Report1!A12 → 數值行12; OR08/XPO/Year/Report1!A12 → 數值行12; OR09/CROX/Year/Report1!A12 → 數值行12; OR10/Insulet/Year/Report1!A12 → 數值行12; OR11/TransUnion/Year/Report1!A12 → 數值行12 |
| 意義候選 | 流動金融資產；須辨識金融工具種類與淨額 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源列示之流動金融資產 |
| 排除與不可替代項 | 非流動投資；不自動視為Quick Assets |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Balance Sheets；資產負債表；該資產／負債／權益附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=instant；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | DEC-01；另見全部84項盤點待確認清單。 |

## OR01-Report1-A13

原始英文：`Receivables`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | BS 名稱行13；OR01/Nexstar/Quarter/Report1!A13 → 數值行13; OR02/Nexstar/Quarter/Report1!A13 → 數值行13; OR03/CROX/Quarter/Report1!A13 → 數值行13; OR04/Insulet/Quarter/Report1!A13 → 數值行13; OR05/TransUnion/Quarter/Report1!A13 → 數值行13; OR06/TransUnion/Quarter/Report1!A13 → 數值行13; OR07/Nexstar/Year/Report1!A13 → 數值行13; OR08/XPO/Year/Report1!A13 → 數值行13; OR09/CROX/Year/Report1!A13 → 數值行13; OR10/Insulet/Year/Report1!A13 → 數值行13; OR11/TransUnion/Year/Report1!A13 → 數值行13 |
| 意義候選 | 應收款項小計，涵蓋範圍尚待附註確認 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源小計明列之票據／帳款或其他組成 |
| 排除與不可替代項 | 不預設其他應收款已含或未含；不預設淨額加備抵為同一指標 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Balance Sheets；資產負債表；該資產／負債／權益附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=instant；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A14

原始英文：`Notes & Accounts Receivable`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | BS 名稱行14；OR01/Nexstar/Quarter/Report1!A14 → 數值行14; OR02/Nexstar/Quarter/Report1!A14 → 數值行14; OR03/CROX/Quarter/Report1!A14 → 數值行14; OR04/Insulet/Quarter/Report1!A14 → 數值行14; OR05/TransUnion/Quarter/Report1!A14 → 數值行14; OR06/TransUnion/Quarter/Report1!A14 → 數值行14; OR07/Nexstar/Year/Report1!A14 → 數值行14; OR08/XPO/Year/Report1!A14 → 數值行14; OR09/CROX/Year/Report1!A14 → 數值行14; OR10/Insulet/Year/Report1!A14 → 數值行14; OR11/TransUnion/Year/Report1!A14 → 數值行14 |
| 意義候選 | 應收票據及帳款；須區分帳面淨額、總額與關係人 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源該行明列之票據及帳款 |
| 排除與不可替代項 | 淨應收帳款tag未必涵蓋票據；不能直接與Receivables小計相加 |
| 既有代碼 | METRICS候選：無；raw候選：accounts_receivable_net。兩者不可互換。 |
| SEC查找位置 | Consolidated Balance Sheets；資產負債表；該資產／負債／權益附註 |
| 候選XBRL tags | us-gaap:AccountsReceivableNetCurrent → raw.accounts_receivable_net |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=instant；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | DEC-04；另見全部84項盤點待確認清單。 |

## OR01-Report1-A15

原始英文：`Notes & Accounts Receivable - Related Party`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | BS 名稱行15；OR01/Nexstar/Quarter/Report1!A15 → 數值行15; OR02/Nexstar/Quarter/Report1!A15 → 數值行15; OR03/CROX/Quarter/Report1!A15 → 數值行15; OR04/Insulet/Quarter/Report1!A15 → 數值行15; OR05/TransUnion/Quarter/Report1!A15 → 數值行15; OR06/TransUnion/Quarter/Report1!A15 → 數值行15; OR07/Nexstar/Year/Report1!A15 → 數值行15; OR08/XPO/Year/Report1!A15 → 數值行15; OR09/CROX/Year/Report1!A15 → 數值行15; OR10/Insulet/Year/Report1!A15 → 數值行15; OR11/TransUnion/Year/Report1!A15 → 數值行15 |
| 意義候選 | 對關係人的應收票據及帳款 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 經關係人附註核對的應收餘額 |
| 排除與不可替代項 | 不能混入非關係人、未沖銷集團內部往來或關係人收入 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Balance Sheets；資產負債表；該資產／負債／權益附註；Related-party transactions／關係人交易附註；核對交易對手及合併沖銷 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=instant；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A16

原始英文：`Other receivable`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | BS 名稱行16；OR01/Nexstar/Quarter/Report1!A16 → 數值行16; OR02/Nexstar/Quarter/Report1!A16 → 數值行16; OR03/CROX/Quarter/Report1!A16 → 數值行16; OR04/Insulet/Quarter/Report1!A16 → 數值行16; OR05/TransUnion/Quarter/Report1!A16 → 數值行16; OR06/TransUnion/Quarter/Report1!A16 → 數值行16; OR07/Nexstar/Year/Report1!A16 → 數值行16; OR08/XPO/Year/Report1!A16 → 數值行16; OR09/CROX/Year/Report1!A16 → 數值行16; OR10/Insulet/Year/Report1!A16 → 數值行16; OR11/TransUnion/Year/Report1!A16 → 數值行16 |
| 意義候選 | 其他應收款；組成及流動分類待核 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源其他應收款組成 |
| 排除與不可替代項 | 不可直接用全部應收帳款或其他流動資產替代 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Balance Sheets；資產負債表；該資產／負債／權益附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=instant；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A17

原始英文：`Inventory`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | BS 名稱行17；OR01/Nexstar/Quarter/Report1!A17 → 數值行17; OR02/Nexstar/Quarter/Report1!A17 → 數值行17; OR03/CROX/Quarter/Report1!A17 → 數值行17; OR04/Insulet/Quarter/Report1!A17 → 數值行17; OR05/TransUnion/Quarter/Report1!A17 → 數值行17; OR06/TransUnion/Quarter/Report1!A17 → 數值行17; OR07/Nexstar/Year/Report1!A17 → 數值行17; OR08/XPO/Year/Report1!A17 → 數值行17; OR09/CROX/Year/Report1!A17 → 數值行17; OR10/Insulet/Year/Report1!A17 → 數值行17; OR11/TransUnion/Year/Report1!A17 → 數值行17 |
| 意義候選 | 存貨餘額；須區分淨額、總額與跌價備抵 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源存貨範圍 |
| 排除與不可替代項 | 不將未取得備抵當0；不自動批准週轉率分母 |
| 既有代碼 | METRICS候選：無；raw候選：inventory。兩者不可互換。 |
| SEC查找位置 | Consolidated Balance Sheets；資產負債表；該資產／負債／權益附註 |
| 候選XBRL tags | us-gaap:InventoryNet → raw.inventory |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=instant；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | DEC-04；ISS-065。 |

## OR01-Report1-A18

原始英文：`Prepayments`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | BS 名稱行18；OR01/Nexstar/Quarter/Report1!A18 → 數值行18; OR02/Nexstar/Quarter/Report1!A18 → 數值行18; OR03/CROX/Quarter/Report1!A18 → 數值行18; OR04/Insulet/Quarter/Report1!A18 → 數值行18; OR05/TransUnion/Quarter/Report1!A18 → 數值行18; OR06/TransUnion/Quarter/Report1!A18 → 數值行18; OR07/Nexstar/Year/Report1!A18 → 數值行18; OR08/XPO/Year/Report1!A18 → 數值行18; OR09/CROX/Year/Report1!A18 → 數值行18; OR10/Insulet/Year/Report1!A18 → 數值行18; OR11/TransUnion/Year/Report1!A18 → 數值行18 |
| 意義候選 | 預付款項／預付費用餘額 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源列示的預付項目 |
| 排除與不可替代項 | 不等同所有其他流動資產；現金付款不等同資產餘額 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Balance Sheets；資產負債表；該資產／負債／權益附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=instant；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A23

原始英文：`Other Current Assets`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | BS 名稱行23；OR01/Nexstar/Quarter/Report1!A23 → 數值行23; OR02/Nexstar/Quarter/Report1!A23 → 數值行23; OR03/CROX/Quarter/Report1!A23 → 數值行23; OR04/Insulet/Quarter/Report1!A23 → 數值行23; OR05/TransUnion/Quarter/Report1!A23 → 數值行23; OR06/TransUnion/Quarter/Report1!A23 → 數值行23; OR07/Nexstar/Year/Report1!A23 → 數值行23; OR08/XPO/Year/Report1!A23 → 數值行23; OR09/CROX/Year/Report1!A23 → 數值行23; OR10/Insulet/Year/Report1!A23 → 數值行23; OR11/TransUnion/Year/Report1!A23 → 數值行23 |
| 意義候選 | 其他流動資產；須查看組成附註 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源該行明列項目 |
| 排除與不可替代項 | 不把缺少的其他科目或勾稽差額塞入此行 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Balance Sheets；資產負債表；該資產／負債／權益附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=instant；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A24

原始英文：`Funds & Investments`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | BS 名稱行24；OR01/Nexstar/Quarter/Report1!A24 → 數值行24; OR02/Nexstar/Quarter/Report1!A24 → 數值行24; OR03/CROX/Quarter/Report1!A24 → 數值行24; OR04/Insulet/Quarter/Report1!A24 → 數值行24; OR05/TransUnion/Quarter/Report1!A24 → 數值行24; OR06/TransUnion/Quarter/Report1!A24 → 數值行24; OR07/Nexstar/Year/Report1!A24 → 數值行24; OR08/XPO/Year/Report1!A24 → 數值行24; OR09/CROX/Year/Report1!A24 → 數值行24; OR10/Insulet/Year/Report1!A24 → 數值行24; OR11/TransUnion/Year/Report1!A24 → 數值行24 |
| 意義候選 | 基金及投資，包含項目與流動分類須核實 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源列示之基金／投資 |
| 排除與不可替代項 | 不預設包含全部金融資產或權益法投資；不與流動金融資產重複 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Balance Sheets；資產負債表；該資產／負債／權益附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：CF-08。 |
| 核准公式／推導條件引用 | CF-08: (Fixed Assets + Funds & Investments) / (Net Worth + Long Term Liabilities) |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=instant；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A26

原始英文：`Fixed Assets`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | BS 名稱行26；OR01/Nexstar/Quarter/Report1!A26 → 數值行26; OR02/Nexstar/Quarter/Report1!A26 → 數值行26; OR03/CROX/Quarter/Report1!A26 → 數值行26; OR04/Insulet/Quarter/Report1!A26 → 數值行26; OR05/TransUnion/Quarter/Report1!A26 → 數值行26; OR06/TransUnion/Quarter/Report1!A26 → 數值行26; OR07/Nexstar/Year/Report1!A26 → 數值行26; OR08/XPO/Year/Report1!A26 → 數值行26; OR09/CROX/Year/Report1!A26 → 數值行26; OR10/Insulet/Year/Report1!A26 → 數值行26; OR11/TransUnion/Year/Report1!A26 → 數值行26 |
| 意義候選 | 固定資產／不動產廠房設備；總額與淨額待核 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源支持的土地、建物、設備等組成 |
| 排除與不可替代項 | 不可與已包含的明細再次加總；折舊減項不可重複扣除 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Balance Sheets；資產負債表；該資產／負債／權益附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：DER-07, CF-07, CF-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；CF-07: Fixed Assets / Net Worth；CF-08: (Fixed Assets + Funds & Investments) / (Net Worth + Long Term Liabilities) |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=instant；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A27

原始英文：`Land`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | BS 名稱行27；OR01/Nexstar/Quarter/Report1!A27 → 數值行27; OR02/Nexstar/Quarter/Report1!A27 → 數值行27; OR03/CROX/Quarter/Report1!A27 → 數值行27; OR04/Insulet/Quarter/Report1!A27 → 數值行27; OR05/TransUnion/Quarter/Report1!A27 → 數值行27; OR06/TransUnion/Quarter/Report1!A27 → 數值行27; OR07/Nexstar/Year/Report1!A27 → 數值行27; OR08/XPO/Year/Report1!A27 → 數值行27; OR09/CROX/Year/Report1!A27 → 數值行27; OR10/Insulet/Year/Report1!A27 → 數值行27; OR11/TransUnion/Year/Report1!A27 → 數值行27 |
| 意義候選 | 固定資產中的土地 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源土地帳面價值 |
| 排除與不可替代項 | 不動產投資、使用權資產及租賃土地須分辨 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Balance Sheets；資產負債表；該資產／負債／權益附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=instant；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A28

原始英文：`Buildings`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | BS 名稱行28；OR01/Nexstar/Quarter/Report1!A28 → 數值行28; OR02/Nexstar/Quarter/Report1!A28 → 數值行28; OR03/CROX/Quarter/Report1!A28 → 數值行28; OR04/Insulet/Quarter/Report1!A28 → 數值行28; OR05/TransUnion/Quarter/Report1!A28 → 數值行28; OR06/TransUnion/Quarter/Report1!A28 → 數值行28; OR07/Nexstar/Year/Report1!A28 → 數值行28; OR08/XPO/Year/Report1!A28 → 數值行28; OR09/CROX/Year/Report1!A28 → 數值行28; OR10/Insulet/Year/Report1!A28 → 數值行28; OR11/TransUnion/Year/Report1!A28 → 數值行28 |
| 意義候選 | 房屋及建築物 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源建物項目 |
| 排除與不可替代項 | 不與土地或已合併列報的不動產總額重複 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Balance Sheets；資產負債表；該資產／負債／權益附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=instant；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A29

原始英文：`Machinery Equipment`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | BS 名稱行29；OR01/Nexstar/Quarter/Report1!A29 → 數值行29; OR02/Nexstar/Quarter/Report1!A29 → 數值行29; OR03/CROX/Quarter/Report1!A29 → 數值行29; OR04/Insulet/Quarter/Report1!A29 → 數值行29; OR05/TransUnion/Quarter/Report1!A29 → 數值行29; OR06/TransUnion/Quarter/Report1!A29 → 數值行29; OR07/Nexstar/Year/Report1!A29 → 數值行29; OR08/XPO/Year/Report1!A29 → 數值行29; OR09/CROX/Year/Report1!A29 → 數值行29; OR10/Insulet/Year/Report1!A29 → 數值行29; OR11/TransUnion/Year/Report1!A29 → 數值行29 |
| 意義候選 | 機器設備 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源機器設備項目 |
| 排除與不可替代項 | 不預設包含所有運輸、資訊或播映設備 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Balance Sheets；資產負債表；該資產／負債／權益附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=instant；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A30

原始英文：`Transport Equipment`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | BS 名稱行30；OR01/Nexstar/Quarter/Report1!A30 → 數值行30; OR02/Nexstar/Quarter/Report1!A30 → 數值行30; OR03/CROX/Quarter/Report1!A30 → 數值行30; OR04/Insulet/Quarter/Report1!A30 → 數值行30; OR05/TransUnion/Quarter/Report1!A30 → 數值行30; OR06/TransUnion/Quarter/Report1!A30 → 數值行30; OR07/Nexstar/Year/Report1!A30 → 數值行30; OR08/XPO/Year/Report1!A30 → 數值行30; OR09/CROX/Year/Report1!A30 → 數值行30; OR10/Insulet/Year/Report1!A30 → 數值行30; OR11/TransUnion/Year/Report1!A30 → 數值行30 |
| 意義候選 | 運輸設備 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源車輛及其他運輸設備 |
| 排除與不可替代項 | 不可由公司產業名稱判定其設備範圍 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Balance Sheets；資產負債表；該資產／負債／權益附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=instant；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A31

原始英文：`Other Fixed Assets`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | BS 名稱行31；OR01/Nexstar/Quarter/Report1!A31 → 數值行31; OR02/Nexstar/Quarter/Report1!A31 → 數值行31; OR03/CROX/Quarter/Report1!A31 → 數值行31; OR04/Insulet/Quarter/Report1!A31 → 數值行31; OR05/TransUnion/Quarter/Report1!A31 → 數值行31; OR06/TransUnion/Quarter/Report1!A31 → 數值行31; OR07/Nexstar/Year/Report1!A31 → 數值行31; OR08/XPO/Year/Report1!A31 → 數值行31; OR09/CROX/Year/Report1!A31 → 數值行31; OR10/Insulet/Year/Report1!A31 → 數值行31; OR11/TransUnion/Year/Report1!A31 → 數值行31 |
| 意義候選 | 其他固定資產；可能是未拆分的淨額，須核附註 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源該行所涵蓋設備 |
| 排除與不可替代項 | 不直接與固定資產總額相加；不可預設為總額或淨額 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Balance Sheets；資產負債表；該資產／負債／權益附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=instant；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A32

原始英文：`Less: Accumulated Depreciation & Fixed Asset Impairment`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | BS 名稱行32；OR01/Nexstar/Quarter/Report1!A32 → 數值行32; OR02/Nexstar/Quarter/Report1!A32 → 數值行32; OR03/CROX/Quarter/Report1!A32 → 數值行32; OR04/Insulet/Quarter/Report1!A32 → 數值行32; OR05/TransUnion/Quarter/Report1!A32 → 數值行32; OR06/TransUnion/Quarter/Report1!A32 → 數值行32; OR07/Nexstar/Year/Report1!A32 → 數值行32; OR08/XPO/Year/Report1!A32 → 數值行32; OR09/CROX/Year/Report1!A32 → 數值行32; OR10/Insulet/Year/Report1!A32 → 數值行32; OR11/TransUnion/Year/Report1!A32 → 數值行32 |
| 意義候選 | 固定資產累計折舊及減損之減項 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源對應資產之累計減項 |
| 排除與不可替代項 | 不等同當期折舊費用；符號需核對來源 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Balance Sheets；資產負債表；該資產／負債／權益附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：DER-07。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=instant；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A33

原始英文：`Uncompleted Constructions & Prepayments For Equipment Purchases`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | BS 名稱行33；OR01/Nexstar/Quarter/Report1!A33 → 數值行33; OR02/Nexstar/Quarter/Report1!A33 → 數值行33; OR03/CROX/Quarter/Report1!A33 → 數值行33; OR04/Insulet/Quarter/Report1!A33 → 數值行33; OR05/TransUnion/Quarter/Report1!A33 → 數值行33; OR06/TransUnion/Quarter/Report1!A33 → 數值行33; OR07/Nexstar/Year/Report1!A33 → 數值行33; OR08/XPO/Year/Report1!A33 → 數值行33; OR09/CROX/Year/Report1!A33 → 數值行33; OR10/Insulet/Year/Report1!A33 → 數值行33; OR11/TransUnion/Year/Report1!A33 → 數值行33 |
| 意義候選 | 未完工程及預付設備款 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源工程及設備預付款 |
| 排除與不可替代項 | 不與已轉列固定資產的金額重複 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Balance Sheets；資產負債表；該資產／負債／權益附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=instant；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A34

原始英文：`Studio and transmission equipment`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | BS 名稱行34；OR01/Nexstar/Quarter/Report1!A34 → 數值行34; OR02/Nexstar/Quarter/Report1!A34 → 數值行34; OR07/Nexstar/Year/Report1!A34 → 數值行34 |
| 意義候選 | 攝影棚及傳輸設備 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源設備分類 |
| 排除與不可替代項 | 不將其他公司的相同行號設備當成此類資產 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Balance Sheets；資產負債表；該資產／負債／權益附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=instant；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A35

原始英文：`Intangible Assets`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | BS 名稱行35；OR01/Nexstar/Quarter/Report1!A35 → 數值行35; OR02/Nexstar/Quarter/Report1!A35 → 數值行35; OR03/CROX/Quarter/Report1!A35 → 數值行35; OR04/Insulet/Quarter/Report1!A35 → 數值行35; OR05/TransUnion/Quarter/Report1!A35 → 數值行35; OR06/TransUnion/Quarter/Report1!A35 → 數值行35; OR07/Nexstar/Year/Report1!A35 → 數值行35; OR08/XPO/Year/Report1!A35 → 數值行35; OR09/CROX/Year/Report1!A35 → 數值行35; OR10/Insulet/Year/Report1!A35 → 數值行35; OR11/TransUnion/Year/Report1!A35 → 數值行35 |
| 意義候選 | 第一列Intangible Assets，可能為含商譽的小計；尚待核實 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 只有來源證實的小計組成 |
| 排除與不可替代項 | 不因同名合併第36列；商譽是否包含須核定 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Balance Sheets；資產負債表；該資產／負債／權益附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：DER-07。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=instant；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-050。 |

## OR01-Report1-A36

原始英文：`Intangible Assets`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | BS 名稱行36；OR01/Nexstar/Quarter/Report1!A36 → 數值行36; OR02/Nexstar/Quarter/Report1!A36 → 數值行36; OR03/CROX/Quarter/Report1!A36 → 數值行36; OR04/Insulet/Quarter/Report1!A36 → 數值行36; OR05/TransUnion/Quarter/Report1!A36 → 數值行36; OR06/TransUnion/Quarter/Report1!A36 → 數值行36; OR07/Nexstar/Year/Report1!A36 → 數值行36; OR08/XPO/Year/Report1!A36 → 數值行36; OR09/CROX/Year/Report1!A36 → 數值行36; OR10/Insulet/Year/Report1!A36 → 數值行36; OR11/TransUnion/Year/Report1!A36 → 數值行36 |
| 意義候選 | 第二列Intangible Assets，可能為不含商譽之無形資產；尚待核實 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源該列之有限／無限年限資產 |
| 排除與不可替代項 | 不直接視為第一列的重複值；不預設含商譽 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Balance Sheets；資產負債表；該資產／負債／權益附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=instant；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-050。 |

## OR01-Report1-A37

原始英文：`Goodwill`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | BS 名稱行37；OR01/Nexstar/Quarter/Report1!A37 → 數值行37; OR02/Nexstar/Quarter/Report1!A37 → 數值行37; OR03/CROX/Quarter/Report1!A37 → 數值行37; OR04/Insulet/Quarter/Report1!A37 → 數值行37; OR05/TransUnion/Quarter/Report1!A37 → 數值行37; OR06/TransUnion/Quarter/Report1!A37 → 數值行37; OR07/Nexstar/Year/Report1!A37 → 數值行37; OR08/XPO/Year/Report1!A37 → 數值行37; OR09/CROX/Year/Report1!A37 → 數值行37; OR10/Insulet/Year/Report1!A37 → 數值行37; OR11/TransUnion/Year/Report1!A37 → 數值行37 |
| 意義候選 | 商譽帳面餘額 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源商譽項目 |
| 排除與不可替代項 | 不等同可辨認無形資產；減損損失不是期末餘額 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Balance Sheets；資產負債表；該資產／負債／權益附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=instant；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A38

原始英文：`Other Assets`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | BS 名稱行38；OR01/Nexstar/Quarter/Report1!A38 → 數值行38; OR02/Nexstar/Quarter/Report1!A38 → 數值行38; OR03/CROX/Quarter/Report1!A38 → 數值行38; OR04/Insulet/Quarter/Report1!A38 → 數值行38; OR05/TransUnion/Quarter/Report1!A38 → 數值行38; OR06/TransUnion/Quarter/Report1!A38 → 數值行38; OR07/Nexstar/Year/Report1!A38 → 數值行38; OR08/XPO/Year/Report1!A38 → 數值行38; OR09/CROX/Year/Report1!A38 → 數值行38; OR10/Insulet/Year/Report1!A38 → 數值行38; OR11/TransUnion/Year/Report1!A38 → 數值行38 |
| 意義候選 | 其他資產；流動／非流動及組成待核 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源該行明列項目 |
| 排除與不可替代項 | 不以資產勾稽差額回填 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Balance Sheets；資產負債表；該資產／負債／權益附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=instant；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A39

原始英文：`Total Assets`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | BS 名稱行39；OR01/Nexstar/Quarter/Report1!A39 → 數值行39; OR02/Nexstar/Quarter/Report1!A39 → 數值行39; OR03/CROX/Quarter/Report1!A39 → 數值行39; OR04/Insulet/Quarter/Report1!A39 → 數值行39; OR05/TransUnion/Quarter/Report1!A39 → 數值行39; OR06/TransUnion/Quarter/Report1!A39 → 數值行39; OR07/Nexstar/Year/Report1!A39 → 數值行39; OR08/XPO/Year/Report1!A39 → 數值行39; OR09/CROX/Year/Report1!A39 → 數值行39; OR10/Insulet/Year/Report1!A39 → 數值行39; OR11/TransUnion/Year/Report1!A39 → 數值行39 |
| 意義候選 | 來源列示資產總額 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 同一申報範圍的全部資產 |
| 排除與不可替代項 | 不混用母公司與合併數；不加重複小計 |
| 既有代碼 | METRICS候選：無；raw候選：total_assets。兩者不可互換。 |
| SEC查找位置 | Consolidated Balance Sheets；資產負債表；該資產／負債／權益附註 |
| 候選XBRL tags | us-gaap:Assets → raw.total_assets |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：REC-01, DER-07。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=instant；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A40

原始英文：`Current Liabilities`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | BS 名稱行40；OR01/Nexstar/Quarter/Report1!A40 → 數值行40; OR02/Nexstar/Quarter/Report1!A40 → 數值行40; OR03/CROX/Quarter/Report1!A40 → 數值行40; OR04/Insulet/Quarter/Report1!A40 → 數值行40; OR05/TransUnion/Quarter/Report1!A40 → 數值行40; OR06/TransUnion/Quarter/Report1!A40 → 數值行40; OR07/Nexstar/Year/Report1!A40 → 數值行40; OR08/XPO/Year/Report1!A40 → 數值行40; OR09/CROX/Year/Report1!A40 → 數值行40; OR10/Insulet/Year/Report1!A40 → 數值行40; OR11/TransUnion/Year/Report1!A40 → 數值行40 |
| 意義候選 | 來源列示流動負債總額 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 流動分類負債 |
| 排除與不可替代項 | 不得以DebtCurrent替代全部流動負債 |
| 既有代碼 | METRICS候選：current_liabilities；raw候選：current_liabilities。兩者不可互換。 |
| SEC查找位置 | Consolidated Balance Sheets；資產負債表；該資產／負債／權益附註 |
| 候選XBRL tags | us-gaap:LiabilitiesCurrent → raw.current_liabilities |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：DER-07。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=instant；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A41

原始英文：`Short Term Loans (including short term notes payable)`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | BS 名稱行41；OR01/Nexstar/Quarter/Report1!A41 → 數值行41; OR02/Nexstar/Quarter/Report1!A41 → 數值行41; OR03/CROX/Quarter/Report1!A41 → 數值行41; OR04/Insulet/Quarter/Report1!A41 → 數值行41; OR05/TransUnion/Quarter/Report1!A41 → 數值行41; OR06/TransUnion/Quarter/Report1!A41 → 數值行41; OR07/Nexstar/Year/Report1!A41 → 數值行41; OR08/XPO/Year/Report1!A41 → 數值行41; OR09/CROX/Year/Report1!A41 → 數值行41; OR10/Insulet/Year/Report1!A41 → 數值行41; OR11/TransUnion/Year/Report1!A41 → 數值行41 |
| 意義候選 | 短期借款及短期應付票券 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 經來源核對且不重疊之短期借款、票券 |
| 排除與不可替代項 | DebtCurrent可能已含一年內到期長債；不得全部相加 |
| 既有代碼 | METRICS候選：無；raw候選：short_term_loans, short_term_notes_payable, debt_current_fallback。兩者不可互換。 |
| SEC查找位置 | Consolidated Balance Sheets；資產負債表；該資產／負債／權益附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | us-gaap:ShortTermBorrowings → raw.short_term_loans; us-gaap:ShortTermNotesPayable → raw.short_term_notes_payable; us-gaap:DebtCurrent → raw.debt_current_fallback |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=instant；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | DEC-02；另見全部84項盤點待確認清單。 |

## OR01-Report1-A43

原始英文：`Long Term Liabilities Maturing Within One Year`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | BS 名稱行43；OR01/Nexstar/Quarter/Report1!A43 → 數值行43; OR02/Nexstar/Quarter/Report1!A43 → 數值行43; OR03/CROX/Quarter/Report1!A43 → 數值行43; OR04/Insulet/Quarter/Report1!A43 → 數值行43; OR05/TransUnion/Quarter/Report1!A43 → 數值行43; OR06/TransUnion/Quarter/Report1!A43 → 數值行43; OR07/Nexstar/Year/Report1!A43 → 數值行43; OR08/XPO/Year/Report1!A43 → 數值行43; OR09/CROX/Year/Report1!A43 → 數值行43; OR10/Insulet/Year/Report1!A43 → 數值行43; OR11/TransUnion/Year/Report1!A43 → 數值行43 |
| 意義候選 | 一年內到期長期負債／債務 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 當期到期部分；租賃是否涵蓋待核 |
| 排除與不可替代項 | 不與已含流動部分的DebtCurrent或長債總額重複 |
| 既有代碼 | METRICS候選：無；raw候選：current_maturities_ltd, current_maturities_ltd_alt, current_maturities_ltd_alt2。兩者不可互換。 |
| SEC查找位置 | Consolidated Balance Sheets；資產負債表；該資產／負債／權益附註 |
| 候選XBRL tags | us-gaap:LongTermDebtCurrent → raw.current_maturities_ltd; us-gaap:LongTermDebtAndFinanceLeaseObligationsCurrent → raw.current_maturities_ltd_alt; us-gaap:LongTermDebtAndCapitalLeaseObligationsCurrent → raw.current_maturities_ltd_alt2 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=instant；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | DEC-02；另見全部84項盤點待確認清單。 |

## OR01-Report1-A44

原始英文：`Payables`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | BS 名稱行44；OR01/Nexstar/Quarter/Report1!A44 → 數值行44; OR02/Nexstar/Quarter/Report1!A44 → 數值行44; OR03/CROX/Quarter/Report1!A44 → 數值行44; OR04/Insulet/Quarter/Report1!A44 → 數值行44; OR05/TransUnion/Quarter/Report1!A44 → 數值行44; OR06/TransUnion/Quarter/Report1!A44 → 數值行44; OR07/Nexstar/Year/Report1!A44 → 數值行44; OR08/XPO/Year/Report1!A44 → 數值行44; OR09/CROX/Year/Report1!A44 → 數值行44; OR10/Insulet/Year/Report1!A44 → 數值行44; OR11/TransUnion/Year/Report1!A44 → 數值行44 |
| 意義候選 | 應付款項小計；組成待核 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源應付票據、帳款等核實組成 |
| 排除與不可替代項 | 不能與其明細重複；不預設包含應計費用 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Balance Sheets；資產負債表；該資產／負債／權益附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=instant；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A45

原始英文：`Notes & Accounts Payable`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | BS 名稱行45；OR01/Nexstar/Quarter/Report1!A45 → 數值行45; OR02/Nexstar/Quarter/Report1!A45 → 數值行45; OR03/CROX/Quarter/Report1!A45 → 數值行45; OR04/Insulet/Quarter/Report1!A45 → 數值行45; OR05/TransUnion/Quarter/Report1!A45 → 數值行45; OR06/TransUnion/Quarter/Report1!A45 → 數值行45; OR07/Nexstar/Year/Report1!A45 → 數值行45; OR08/XPO/Year/Report1!A45 → 數值行45; OR09/CROX/Year/Report1!A45 → 數值行45; OR10/Insulet/Year/Report1!A45 → 數值行45; OR11/TransUnion/Year/Report1!A45 → 數值行45 |
| 意義候選 | 應付票據及帳款 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源該行之票據及營業帳款 |
| 排除與不可替代項 | 純Accounts Payable不一定含票據；不可由名稱近似直接接受 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Balance Sheets；資產負債表；該資產／負債／權益附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=instant；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A46

原始英文：`Notes & Accounts Payable - Related Party`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | BS 名稱行46；OR01/Nexstar/Quarter/Report1!A46 → 數值行46; OR02/Nexstar/Quarter/Report1!A46 → 數值行46; OR03/CROX/Quarter/Report1!A46 → 數值行46; OR04/Insulet/Quarter/Report1!A46 → 數值行46; OR05/TransUnion/Quarter/Report1!A46 → 數值行46; OR06/TransUnion/Quarter/Report1!A46 → 數值行46; OR07/Nexstar/Year/Report1!A46 → 數值行46; OR08/XPO/Year/Report1!A46 → 數值行46; OR09/CROX/Year/Report1!A46 → 數值行46; OR10/Insulet/Year/Report1!A46 → 數值行46; OR11/TransUnion/Year/Report1!A46 → 數值行46 |
| 意義候選 | 應付關係人票據及帳款 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 關係人附註支持的應付款 |
| 排除與不可替代項 | 不與非關係人、集團內部已沖銷金額混用 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Balance Sheets；資產負債表；該資產／負債／權益附註；Related-party transactions／關係人交易附註；核對交易對手及合併沖銷 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=instant；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A47

原始英文：`Accrued Expenses`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | BS 名稱行47；OR01/Nexstar/Quarter/Report1!A47 → 數值行47; OR02/Nexstar/Quarter/Report1!A47 → 數值行47; OR03/CROX/Quarter/Report1!A47 → 數值行47; OR04/Insulet/Quarter/Report1!A47 → 數值行47; OR05/TransUnion/Quarter/Report1!A47 → 數值行47; OR06/TransUnion/Quarter/Report1!A47 → 數值行47; OR07/Nexstar/Year/Report1!A47 → 數值行47; OR08/XPO/Year/Report1!A47 → 數值行47; OR09/CROX/Year/Report1!A47 → 數值行47; OR10/Insulet/Year/Report1!A47 → 數值行47; OR11/TransUnion/Year/Report1!A47 → 數值行47 |
| 意義候選 | 應計費用餘額 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源已發生未支付之費用 |
| 排除與不可替代項 | 不等同現金支付費用或CF應計費用變動 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Balance Sheets；資產負債表；該資產／負債／權益附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=instant；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A48

原始英文：`Advance Receipts`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | BS 名稱行48；OR01/Nexstar/Quarter/Report1!A48 → 數值行48; OR02/Nexstar/Quarter/Report1!A48 → 數值行48; OR03/CROX/Quarter/Report1!A48 → 數值行48; OR05/TransUnion/Quarter/Report1!A48 → 數值行48; OR06/TransUnion/Quarter/Report1!A48 → 數值行48; OR07/Nexstar/Year/Report1!A48 → 數值行48; OR08/XPO/Year/Report1!A48 → 數值行48; OR09/CROX/Year/Report1!A48 → 數值行48; OR11/TransUnion/Year/Report1!A48 → 數值行48 |
| 意義候選 | 預收款項 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 依關係人／合約負債附註核對 |
| 排除與不可替代項 | 應計費用與預收款不是同義；不能依行號替代 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Balance Sheets；資產負債表；該資產／負債／權益附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=instant；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-004。 |

## OR01-Report1-A49

原始英文：`Amount Owed To/From Shareholders`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | BS 名稱行49；OR01/Nexstar/Quarter/Report1!A49 → 數值行49; OR02/Nexstar/Quarter/Report1!A49 → 數值行49; OR03/CROX/Quarter/Report1!A49 → 數值行49; OR04/Insulet/Quarter/Report1!A49 → 數值行49; OR07/Nexstar/Year/Report1!A49 → 數值行49; OR10/Insulet/Year/Report1!A49 → 數值行49 |
| 意義候選 | 股東往來應收／應付款 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源股東往來的實際方向 |
| 排除與不可替代項 | 不得不分借貸方向取絕對值；須核資產／負債分類 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Balance Sheets；資產負債表；該資產／負債／權益附註；Related-party transactions／關係人交易附註；核對交易對手及合併沖銷 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=instant；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A53

原始英文：`Other Current Liabilities`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | BS 名稱行53；OR01/Nexstar/Quarter/Report1!A53 → 數值行53; OR02/Nexstar/Quarter/Report1!A53 → 數值行53; OR03/CROX/Quarter/Report1!A53 → 數值行53; OR04/Insulet/Quarter/Report1!A53 → 數值行53; OR05/TransUnion/Quarter/Report1!A53 → 數值行53; OR06/TransUnion/Quarter/Report1!A53 → 數值行53; OR07/Nexstar/Year/Report1!A53 → 數值行53; OR08/XPO/Year/Report1!A53 → 數值行53; OR09/CROX/Year/Report1!A53 → 數值行53; OR10/Insulet/Year/Report1!A53 → 數值行53; OR11/TransUnion/Year/Report1!A53 → 數值行53 |
| 意義候選 | 其他流動負債 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源該行核實組成 |
| 排除與不可替代項 | 不能用流動負債減不完整明細的差額任意補值 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Balance Sheets；資產負債表；該資產／負債／權益附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=instant；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A54

原始英文：`Long Term Liabilities`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | BS 名稱行54；OR01/Nexstar/Quarter/Report1!A54 → 數值行54; OR02/Nexstar/Quarter/Report1!A54 → 數值行54; OR03/CROX/Quarter/Report1!A54 → 數值行54; OR04/Insulet/Quarter/Report1!A54 → 數值行54; OR05/TransUnion/Quarter/Report1!A54 → 數值行54; OR06/TransUnion/Quarter/Report1!A54 → 數值行54; OR07/Nexstar/Year/Report1!A54 → 數值行54; OR08/XPO/Year/Report1!A54 → 數值行54; OR09/CROX/Year/Report1!A54 → 數值行54; OR10/Insulet/Year/Report1!A54 → 數值行54; OR11/TransUnion/Year/Report1!A54 → 數值行54 |
| 意義候選 | Long Term Liabilities小計；債務或全部非流動負債涵蓋範圍須確認 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源明列的長期借款／債券等組成 |
| 排除與不可替代項 | LongTermDebtNoncurrent只代表債務概念，不能默認代表所有非流動負債 |
| 既有代碼 | METRICS候選：無；raw候選：long_term_liabilities, long_term_liabilities_alt, long_term_liabilities_alt2。兩者不可互換。 |
| SEC查找位置 | Consolidated Balance Sheets；資產負債表；該資產／負債／權益附註 |
| 候選XBRL tags | us-gaap:LongTermDebtNoncurrent → raw.long_term_liabilities; us-gaap:LongTermDebtAndFinanceLeaseObligationsNoncurrent → raw.long_term_liabilities_alt; us-gaap:LongTermDebtAndCapitalLeaseObligations → raw.long_term_liabilities_alt2 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：CF-08, DER-07。 |
| 核准公式／推導條件引用 | CF-08: (Fixed Assets + Funds & Investments) / (Net Worth + Long Term Liabilities)；DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=instant；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | DEC-02；另見全部84項盤點待確認清單。 |

## OR01-Report1-A55

原始英文：`Long Term Bank Loans`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | BS 名稱行55；OR01/Nexstar/Quarter/Report1!A55 → 數值行55; OR02/Nexstar/Quarter/Report1!A55 → 數值行55; OR03/CROX/Quarter/Report1!A55 → 數值行55; OR04/Insulet/Quarter/Report1!A55 → 數值行55; OR05/TransUnion/Quarter/Report1!A55 → 數值行55; OR06/TransUnion/Quarter/Report1!A55 → 數值行55; OR07/Nexstar/Year/Report1!A55 → 數值行55; OR08/XPO/Year/Report1!A55 → 數值行55; OR09/CROX/Year/Report1!A55 → 數值行55; OR10/Insulet/Year/Report1!A55 → 數值行55; OR11/TransUnion/Year/Report1!A55 → 數值行55 |
| 意義候選 | 長期銀行借款 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源銀行借款之非流動部分 |
| 排除與不可替代項 | 既有長債tag可能包含債券等，不是銀行借款的直接證明 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Balance Sheets；資產負債表；該資產／負債／權益附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=instant；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | DEC-02；另見全部84項盤點待確認清單。 |

## OR01-Report1-A56

原始英文：`Corporate Bond Payable`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | BS 名稱行56；OR01/Nexstar/Quarter/Report1!A56 → 數值行56; OR02/Nexstar/Quarter/Report1!A56 → 數值行56; OR03/CROX/Quarter/Report1!A56 → 數值行56; OR04/Insulet/Quarter/Report1!A56 → 數值行56; OR05/TransUnion/Quarter/Report1!A56 → 數值行56; OR06/TransUnion/Quarter/Report1!A56 → 數值行56; OR07/Nexstar/Year/Report1!A56 → 數值行56; OR08/XPO/Year/Report1!A56 → 數值行56; OR09/CROX/Year/Report1!A56 → 數值行56; OR10/Insulet/Year/Report1!A56 → 數值行56; OR11/TransUnion/Year/Report1!A56 → 數值行56 |
| 意義候選 | 應付公司債 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源公司債餘額及溢折價口徑 |
| 排除與不可替代項 | 不得以全部長期債務tag直接代替 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Balance Sheets；資產負債表；該資產／負債／權益附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=instant；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | DEC-02；另見全部84項盤點待確認清單。 |

## OR01-Report1-A58

原始英文：`Provisions`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | BS 名稱行58；OR01/Nexstar/Quarter/Report1!A58 → 數值行58; OR02/Nexstar/Quarter/Report1!A58 → 數值行58; OR03/CROX/Quarter/Report1!A58 → 數值行58; OR04/Insulet/Quarter/Report1!A58 → 數值行58; OR05/TransUnion/Quarter/Report1!A58 → 數值行58; OR06/TransUnion/Quarter/Report1!A58 → 數值行58; OR07/Nexstar/Year/Report1!A58 → 數值行58; OR08/XPO/Year/Report1!A58 → 數值行58; OR09/CROX/Year/Report1!A58 → 數值行58; OR10/Insulet/Year/Report1!A58 → 數值行58; OR11/TransUnion/Year/Report1!A58 → 數值行58 |
| 意義候選 | 負債準備 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源準備種類、流動分類及認列範圍 |
| 排除與不可替代項 | 不等同所有其他負債；不與應計費用任意合併 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Balance Sheets；資產負債表；該資產／負債／權益附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=instant；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A59

原始英文：`Deferred tax liabilities`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | BS 名稱行59；OR01/Nexstar/Quarter/Report1!A59 → 數值行59; OR02/Nexstar/Quarter/Report1!A59 → 數值行59; OR07/Nexstar/Year/Report1!A59 → 數值行59 |
| 意義候選 | 遞延所得稅負債 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源明列之遞延稅或長期應付稅負債 |
| 排除與不可替代項 | 兩者不是同義；均非當期所得稅費用或支付所得稅 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Balance Sheets；資產負債表；該資產／負債／權益附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=instant；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-006。 |

## OR01-Report1-A61

原始英文：`Other Liabilities`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | BS 名稱行61；OR01/Nexstar/Quarter/Report1!A61 → 數值行61; OR02/Nexstar/Quarter/Report1!A61 → 數值行61; OR03/CROX/Quarter/Report1!A61 → 數值行61; OR04/Insulet/Quarter/Report1!A61 → 數值行61; OR05/TransUnion/Quarter/Report1!A61 → 數值行61; OR06/TransUnion/Quarter/Report1!A61 → 數值行61; OR07/Nexstar/Year/Report1!A61 → 數值行61; OR08/XPO/Year/Report1!A61 → 數值行61; OR09/CROX/Year/Report1!A61 → 數值行61; OR10/Insulet/Year/Report1!A61 → 數值行61; OR11/TransUnion/Year/Report1!A61 → 數值行61 |
| 意義候選 | 其他負債 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源其他負債組成與分類 |
| 排除與不可替代項 | 不作為勾稽差額承接科目 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Balance Sheets；資產負債表；該資產／負債／權益附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=instant；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A62

原始英文：`Total Liabilities`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | BS 名稱行62；OR01/Nexstar/Quarter/Report1!A62 → 數值行62; OR02/Nexstar/Quarter/Report1!A62 → 數值行62; OR03/CROX/Quarter/Report1!A62 → 數值行62; OR04/Insulet/Quarter/Report1!A62 → 數值行62; OR05/TransUnion/Quarter/Report1!A62 → 數值行62; OR06/TransUnion/Quarter/Report1!A62 → 數值行62; OR07/Nexstar/Year/Report1!A62 → 數值行62; OR08/XPO/Year/Report1!A62 → 數值行62; OR09/CROX/Year/Report1!A62 → 數值行62; OR10/Insulet/Year/Report1!A62 → 數值行62; OR11/TransUnion/Year/Report1!A62 → 數值行62 |
| 意義候選 | 來源負債總額 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 同一範圍的全部負債 |
| 排除與不可替代項 | Total Debt是有息債務概念，不可直接等同負債總額 |
| 既有代碼 | METRICS候選：total_liabilities；raw候選：total_liabilities。兩者不可互換。 |
| SEC查找位置 | Consolidated Balance Sheets；資產負債表；該資產／負債／權益附註 |
| 候選XBRL tags | us-gaap:Liabilities → raw.total_liabilities |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：REC-01, DER-07。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=instant；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A63

原始英文：`Share Capital / Paid-up Capital`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | BS 名稱行63；OR01/Nexstar/Quarter/Report1!A63 → 數值行63; OR02/Nexstar/Quarter/Report1!A63 → 數值行63; OR03/CROX/Quarter/Report1!A63 → 數值行63; OR04/Insulet/Quarter/Report1!A63 → 數值行63; OR05/TransUnion/Quarter/Report1!A63 → 數值行63; OR06/TransUnion/Quarter/Report1!A63 → 數值行63; OR07/Nexstar/Year/Report1!A63 → 數值行63; OR08/XPO/Year/Report1!A63 → 數值行63; OR09/CROX/Year/Report1!A63 → 數值行63; OR10/Insulet/Year/Report1!A63 → 數值行63; OR11/TransUnion/Year/Report1!A63 → 數值行63 |
| 意義候選 | 股本／實收資本額 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源股本、面額及實收資本定義 |
| 排除與不可替代項 | 不等同Additional Paid-in Capital或權益總額 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Balance Sheets；資產負債表；該資產／負債／權益附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=instant；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A65

原始英文：`Additional paid-in capital`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | BS 名稱行65；OR01/Nexstar/Quarter/Report1!A65 → 數值行65; OR02/Nexstar/Quarter/Report1!A65 → 數值行65; OR03/CROX/Quarter/Report1!A65 → 數值行65; OR04/Insulet/Quarter/Report1!A65 → 數值行65; OR05/TransUnion/Quarter/Report1!A65 → 數值行65; OR06/TransUnion/Quarter/Report1!A65 → 數值行65; OR07/Nexstar/Year/Report1!A65 → 數值行65; OR08/XPO/Year/Report1!A65 → 數值行65; OR09/CROX/Year/Report1!A65 → 數值行65; OR10/Insulet/Year/Report1!A65 → 數值行65; OR11/TransUnion/Year/Report1!A65 → 數值行65 |
| 意義候選 | 額外實收資本／資本公積 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源資本公積組成 |
| 排除與不可替代項 | 不與股本或全部權益重複 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Balance Sheets；資產負債表；該資產／負債／權益附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=instant；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A66

原始英文：`Retained Earnings`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | BS 名稱行66；OR01/Nexstar/Quarter/Report1!A66 → 數值行66; OR02/Nexstar/Quarter/Report1!A66 → 數值行66; OR03/CROX/Quarter/Report1!A66 → 數值行66; OR04/Insulet/Quarter/Report1!A66 → 數值行66; OR05/TransUnion/Quarter/Report1!A66 → 數值行66; OR06/TransUnion/Quarter/Report1!A66 → 數值行66; OR07/Nexstar/Year/Report1!A66 → 數值行66; OR08/XPO/Year/Report1!A66 → 數值行66; OR09/CROX/Year/Report1!A66 → 數值行66; OR10/Insulet/Year/Report1!A66 → 數值行66; OR11/TransUnion/Year/Report1!A66 → 數值行66 |
| 意義候選 | 保留盈餘或累積虧損 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源累積盈餘／虧損，保留正負號 |
| 排除與不可替代項 | 不是當期淨利；不能自行用淨利推完整期末保留盈餘 |
| 既有代碼 | METRICS候選：無；raw候選：retained_earnings。兩者不可互換。 |
| SEC查找位置 | Consolidated Balance Sheets；資產負債表；該資產／負債／權益附註 |
| 候選XBRL tags | us-gaap:RetainedEarningsAccumulatedDeficit → raw.retained_earnings |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=instant；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A67

原始英文：`Adjustments To Shareholders' Equity`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | BS 名稱行67；OR01/Nexstar/Quarter/Report1!A67 → 數值行67; OR02/Nexstar/Quarter/Report1!A67 → 數值行67; OR03/CROX/Quarter/Report1!A67 → 數值行67; OR04/Insulet/Quarter/Report1!A67 → 數值行67; OR05/TransUnion/Quarter/Report1!A67 → 數值行67; OR06/TransUnion/Quarter/Report1!A67 → 數值行67; OR07/Nexstar/Year/Report1!A67 → 數值行67; OR08/XPO/Year/Report1!A67 → 數值行67; OR09/CROX/Year/Report1!A67 → 數值行67; OR10/Insulet/Year/Report1!A67 → 數值行67; OR11/TransUnion/Year/Report1!A67 → 數值行67 |
| 意義候選 | 股東權益調整項目 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源明列之調整，例如累積其他綜合損益 |
| 排除與不可替代項 | 不以平衡權益為目的回填未知項 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Balance Sheets；資產負債表；該資產／負債／權益附註；Related-party transactions／關係人交易附註；核對交易對手及合併沖銷 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=instant；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A68

原始英文：`Less: Treasury Stock`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | BS 名稱行68；OR01/Nexstar/Quarter/Report1!A68 → 數值行68; OR02/Nexstar/Quarter/Report1!A68 → 數值行68; OR03/CROX/Quarter/Report1!A68 → 數值行68; OR04/Insulet/Quarter/Report1!A68 → 數值行68; OR05/TransUnion/Quarter/Report1!A68 → 數值行68; OR06/TransUnion/Quarter/Report1!A68 → 數值行68; OR07/Nexstar/Year/Report1!A68 → 數值行68; OR08/XPO/Year/Report1!A68 → 數值行68; OR09/CROX/Year/Report1!A68 → 數值行68; OR10/Insulet/Year/Report1!A68 → 數值行68; OR11/TransUnion/Year/Report1!A68 → 數值行68 |
| 意義候選 | 庫藏股票減項 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源庫藏股帳面餘額及符號 |
| 排除與不可替代項 | 買回現金流不等同期末庫藏股；不得任意取絕對值 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Balance Sheets；資產負債表；該資產／負債／權益附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=instant；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A69

原始英文：`Minority Interest`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | BS 名稱行69；OR01/Nexstar/Quarter/Report1!A69 → 數值行69; OR02/Nexstar/Quarter/Report1!A69 → 數值行69; OR03/CROX/Quarter/Report1!A69 → 數值行69; OR04/Insulet/Quarter/Report1!A69 → 數值行69; OR05/TransUnion/Quarter/Report1!A69 → 數值行69; OR06/TransUnion/Quarter/Report1!A69 → 數值行69; OR07/Nexstar/Year/Report1!A69 → 數值行69; OR08/XPO/Year/Report1!A69 → 數值行69; OR09/CROX/Year/Report1!A69 → 數值行69; OR10/Insulet/Year/Report1!A69 → 數值行69; OR11/TransUnion/Year/Report1!A69 → 數值行69 |
| 意義候選 | 非控制權益 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源非控制權益；可能另列可贖回權益 |
| 排除與不可替代項 | 不默認含於或排除於Net Worth |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Balance Sheets；資產負債表；該資產／負債／權益附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=instant；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | DEC-02；另見全部84項盤點待確認清單。 |

## OR01-Report1-A70

原始英文：`Total Net Worth`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | BS 名稱行70；OR01/Nexstar/Quarter/Report1!A70 → 數值行70; OR02/Nexstar/Quarter/Report1!A70 → 數值行70; OR03/CROX/Quarter/Report1!A70 → 數值行70; OR04/Insulet/Quarter/Report1!A70 → 數值行70; OR05/TransUnion/Quarter/Report1!A70 → 數值行70; OR06/TransUnion/Quarter/Report1!A70 → 數值行70; OR07/Nexstar/Year/Report1!A70 → 數值行70; OR08/XPO/Year/Report1!A70 → 數值行70; OR09/CROX/Year/Report1!A70 → 數值行70; OR10/Insulet/Year/Report1!A70 → 數值行70; OR11/TransUnion/Year/Report1!A70 → 數值行70 |
| 意義候選 | Net Worth／權益總額，母公司與非控制權益範圍待決 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 依已核准Net Worth定義選取來源組成 |
| 排除與不可替代項 | StockholdersEquity不可未經確認就當Net Worth；不以資產減不完整負債替代 |
| 既有代碼 | METRICS候選：net_worth；raw候選：stockholders_equity。兩者不可互換。 |
| SEC查找位置 | Consolidated Balance Sheets；資產負債表；該資產／負債／權益附註 |
| 候選XBRL tags | us-gaap:StockholdersEquity → raw.stockholders_equity |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：REC-01。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=instant；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | DEC-02；另見全部84項盤點待確認清單。 |

## OR01-Report1-A71

原始英文：`Total Liabilities & Net Worth`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | BS 名稱行71；OR01/Nexstar/Quarter/Report1!A71 → 數值行71; OR02/Nexstar/Quarter/Report1!A71 → 數值行71; OR03/CROX/Quarter/Report1!A71 → 數值行71; OR04/Insulet/Quarter/Report1!A71 → 數值行71; OR05/TransUnion/Quarter/Report1!A71 → 數值行71; OR06/TransUnion/Quarter/Report1!A71 → 數值行71; OR07/Nexstar/Year/Report1!A71 → 數值行71; OR08/XPO/Year/Report1!A71 → 數值行71; OR09/CROX/Year/Report1!A71 → 數值行71; OR10/Insulet/Year/Report1!A71 → 數值行71; OR11/TransUnion/Year/Report1!A71 → 數值行71 |
| 意義候選 | 負債及權益合計 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 同口徑負債與權益 |
| 排除與不可替代項 | 不得用總資產直接覆寫以掩蓋未勾稽 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Balance Sheets；資產負債表；該資產／負債／權益附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：REC-01, DER-07。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=instant；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A72

原始英文：`Allowance For Inventory Devaluation`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | BS 名稱行72；OR01/Nexstar/Quarter/Report1!A72 → 數值行72; OR02/Nexstar/Quarter/Report1!A72 → 數值行72; OR03/CROX/Quarter/Report1!A72 → 數值行72; OR04/Insulet/Quarter/Report1!A72 → 數值行72; OR05/TransUnion/Quarter/Report1!A72 → 數值行72; OR06/TransUnion/Quarter/Report1!A72 → 數值行72; OR07/Nexstar/Year/Report1!A72 → 數值行72; OR08/XPO/Year/Report1!A72 → 數值行72; OR09/CROX/Year/Report1!A72 → 數值行72; OR10/Insulet/Year/Report1!A72 → 數值行72; OR11/TransUnion/Year/Report1!A72 → 數值行72 |
| 意義候選 | 備抵存貨跌價損失／存貨評價備抵 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源備抵餘額及符號 |
| 排除與不可替代項 | 當期跌價費用不是備抵餘額；缺值不可當0 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Balance Sheets；資產負債表；該資產／負債／權益附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=instant；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | DEC-04；另見全部84項盤點待確認清單。 |

## OR01-Report1-A73

原始英文：`Bad Debt Loss`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | BS 名稱行73；OR01/Nexstar/Quarter/Report1!A73 → 數值行73; OR02/Nexstar/Quarter/Report1!A73 → 數值行73; OR03/CROX/Quarter/Report1!A73 → 數值行73; OR04/Insulet/Quarter/Report1!A73 → 數值行73; OR05/TransUnion/Quarter/Report1!A73 → 數值行73; OR06/TransUnion/Quarter/Report1!A73 → 數值行73; OR07/Nexstar/Year/Report1!A73 → 數值行73; OR08/XPO/Year/Report1!A73 → 數值行73; OR09/CROX/Year/Report1!A73 → 數值行73; OR10/Insulet/Year/Report1!A73 → 數值行73; OR11/TransUnion/Year/Report1!A73 → 數值行73 |
| 意義候選 | Bad Debt Loss，屬損失費用或備抵餘額尚待確認 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源實際定義及期間 |
| 排除與不可替代項 | 不能直接當CF-17的呆帳備抵；不能只憑名稱選資產負債或損益期間 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Balance Sheets；資產負債表；該資產／負債／權益附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=source_definition_required；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | DEC-04；另見全部84項盤點待確認清單。 |

## OR01-Report1-A80

原始英文：`Revenues`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | IS 名稱行80；OR01/Nexstar/Quarter/Report1!A80 → 數值行80; OR02/Nexstar/Quarter/Report1!A80 → 數值行80; OR03/CROX/Quarter/Report1!A80 → 數值行80; OR04/Insulet/Quarter/Report1!A80 → 數值行80; OR05/TransUnion/Quarter/Report1!A80 → 數值行80; OR06/TransUnion/Quarter/Report1!A80 → 數值行80; OR07/Nexstar/Year/Report1!A80 → 數值行80; OR08/XPO/Year/Report1!A80 → 數值行80; OR09/CROX/Year/Report1!A80 → 數值行80; OR10/Insulet/Year/Report1!A80 → 數值行80; OR11/TransUnion/Year/Report1!A80 → 數值行80 |
| 意義候選 | 營業收入合計 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 同範圍主要營業收入 |
| 排除與不可替代項 | 不與Net Sales及已含關係人收入重複 |
| 既有代碼 | METRICS候選：revenue；raw候選：revenue, revenue_alt。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Operations / Income；損益表；該收入／成本／費用及稅項附註 |
| 候選XBRL tags | us-gaap:Revenues → raw.revenue; us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax → raw.revenue_alt |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：DER-07。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A81

原始英文：`Net Sales`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | IS 名稱行81；OR01/Nexstar/Quarter/Report1!A81 → 數值行81; OR02/Nexstar/Quarter/Report1!A81 → 數值行81; OR03/CROX/Quarter/Report1!A81 → 數值行81; OR04/Insulet/Quarter/Report1!A81 → 數值行81; OR05/TransUnion/Quarter/Report1!A81 → 數值行81; OR06/TransUnion/Quarter/Report1!A81 → 數值行81; OR07/Nexstar/Year/Report1!A81 → 數值行81; OR08/XPO/Year/Report1!A81 → 數值行81; OR09/CROX/Year/Report1!A81 → 數值行81; OR10/Insulet/Year/Report1!A81 → 數值行81; OR11/TransUnion/Year/Report1!A81 → 數值行81 |
| 意義候選 | 銷貨收入淨額，可能與總營收不同 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源扣除退回／折讓等後收入 |
| 排除與不可替代項 | 需核是否排除服務、其他或關係人收入；不可直接當全部營收 |
| 既有代碼 | METRICS候選：revenue；raw候選：revenue, revenue_alt。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Operations / Income；損益表；該收入／成本／費用及稅項附註 |
| 候選XBRL tags | us-gaap:Revenues → raw.revenue; us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax → raw.revenue_alt |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A82

原始英文：`Other Revenues`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | IS 名稱行82；OR01/Nexstar/Quarter/Report1!A82 → 數值行82; OR02/Nexstar/Quarter/Report1!A82 → 數值行82; OR03/CROX/Quarter/Report1!A82 → 數值行82; OR04/Insulet/Quarter/Report1!A82 → 數值行82; OR05/TransUnion/Quarter/Report1!A82 → 數值行82; OR06/TransUnion/Quarter/Report1!A82 → 數值行82; OR07/Nexstar/Year/Report1!A82 → 數值行82; OR08/XPO/Year/Report1!A82 → 數值行82; OR09/CROX/Year/Report1!A82 → 數值行82; OR10/Insulet/Year/Report1!A82 → 數值行82; OR11/TransUnion/Year/Report1!A82 → 數值行82 |
| 意義候選 | 其他營業收入 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源其他營業收入組成 |
| 排除與不可替代項 | 不等同營業外Other Income |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Operations / Income；損益表；該收入／成本／費用及稅項附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A86

原始英文：`Operating Cost`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | IS 名稱行86；OR01/Nexstar/Quarter/Report1!A86 → 數值行86; OR02/Nexstar/Quarter/Report1!A86 → 數值行86; OR03/CROX/Quarter/Report1!A86 → 數值行86; OR04/Insulet/Quarter/Report1!A86 → 數值行86; OR05/TransUnion/Quarter/Report1!A86 → 數值行86; OR06/TransUnion/Quarter/Report1!A86 → 數值行86; OR07/Nexstar/Year/Report1!A86 → 數值行86; OR08/XPO/Year/Report1!A86 → 數值行86; OR09/CROX/Year/Report1!A86 → 數值行86; OR10/Insulet/Year/Report1!A86 → 數值行86; OR11/TransUnion/Year/Report1!A86 → 數值行86 |
| 意義候選 | 營收成本合計 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 對應同期間營收的成本 |
| 排除與不可替代項 | 包含全部營業費用的CostsAndExpenses不是等價概念 |
| 既有代碼 | METRICS候選：cost_of_revenue；raw候選：cost_of_revenue, cost_of_revenue_alt。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Operations / Income；損益表；該收入／成本／費用及稅項附註 |
| 候選XBRL tags | us-gaap:CostOfRevenue → raw.cost_of_revenue; us-gaap:CostOfGoodsAndServicesSold → raw.cost_of_revenue_alt |
| 計算輸入tag候選 | revenue: us-gaap:Revenues, us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax; gross_profit: us-gaap:GrossProfit |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：DER-02, DER-07。 |
| 核准公式／推導條件引用 | DER-02: Revenues − Gross Profit；僅在直接成本未取得、毛利有獨立來源且 DER-01 的會計結構成立時使用。不得同時以未知成本推毛利，再以該毛利反推成本。；DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。 |
| 必要輸入與版本 | revenue, gross_profit；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A87

原始英文：`Cost Of Goods Sold`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | IS 名稱行87；OR01/Nexstar/Quarter/Report1!A87 → 數值行87; OR02/Nexstar/Quarter/Report1!A87 → 數值行87; OR03/CROX/Quarter/Report1!A87 → 數值行87; OR04/Insulet/Quarter/Report1!A87 → 數值行87; OR05/TransUnion/Quarter/Report1!A87 → 數值行87; OR06/TransUnion/Quarter/Report1!A87 → 數值行87; OR07/Nexstar/Year/Report1!A87 → 數值行87; OR08/XPO/Year/Report1!A87 → 數值行87; OR09/CROX/Year/Report1!A87 → 數值行87; OR10/Insulet/Year/Report1!A87 → 數值行87; OR11/TransUnion/Year/Report1!A87 → 數值行87 |
| 意義候選 | 銷貨成本 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源商品／服務成本之適用範圍 |
| 排除與不可替代項 | 不自動涵蓋全部營收成本；折舊可能已含 |
| 既有代碼 | METRICS候選：cost_of_revenue；raw候選：cost_of_revenue, cost_of_revenue_alt。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Operations / Income；損益表；該收入／成本／費用及稅項附註 |
| 候選XBRL tags | us-gaap:CostOfRevenue → raw.cost_of_revenue; us-gaap:CostOfGoodsAndServicesSold → raw.cost_of_revenue_alt |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：DER-02。 |
| 核准公式／推導條件引用 | DER-02: Revenues − Gross Profit；僅在直接成本未取得、毛利有獨立來源且 DER-01 的會計結構成立時使用。不得同時以未知成本推毛利，再以該毛利反推成本。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A88

原始英文：`Other Operating Costs`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | IS 名稱行88；OR01/Nexstar/Quarter/Report1!A88 → 數值行88; OR02/Nexstar/Quarter/Report1!A88 → 數值行88; OR03/CROX/Quarter/Report1!A88 → 數值行88; OR04/Insulet/Quarter/Report1!A88 → 數值行88; OR05/TransUnion/Quarter/Report1!A88 → 數值行88; OR06/TransUnion/Quarter/Report1!A88 → 數值行88; OR07/Nexstar/Year/Report1!A88 → 數值行88; OR08/XPO/Year/Report1!A88 → 數值行88; OR09/CROX/Year/Report1!A88 → 數值行88; OR10/Insulet/Year/Report1!A88 → 數值行88; OR11/TransUnion/Year/Report1!A88 → 數值行88 |
| 意義候選 | 其他營業成本 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源營收成本之其他組成 |
| 排除與不可替代項 | 不得與Operating Expense或已列明細重複 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Operations / Income；損益表；該收入／成本／費用及稅項附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A92

原始英文：`Realized Gains On Associated Companies`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | IS 名稱行92；OR01/Nexstar/Quarter/Report1!A92 → 數值行92; OR02/Nexstar/Quarter/Report1!A92 → 數值行92; OR03/CROX/Quarter/Report1!A92 → 數值行92; OR04/Insulet/Quarter/Report1!A92 → 數值行92; OR05/TransUnion/Quarter/Report1!A92 → 數值行92; OR06/TransUnion/Quarter/Report1!A92 → 數值行92; OR07/Nexstar/Year/Report1!A92 → 數值行92; OR08/XPO/Year/Report1!A92 → 數值行92; OR09/CROX/Year/Report1!A92 → 數值行92; OR10/Insulet/Year/Report1!A92 → 數值行92; OR11/TransUnion/Year/Report1!A92 → 數值行92 |
| 意義候選 | 關聯企業已實現利益 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源列報之已實現利益及損益分類 |
| 排除與不可替代項 | 不預設等同全部權益法投資收益 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Operations / Income；損益表；該收入／成本／費用及稅項附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A93

原始英文：`Unrealized Gains On Associated Companies`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | IS 名稱行93；OR01/Nexstar/Quarter/Report1!A93 → 數值行93; OR02/Nexstar/Quarter/Report1!A93 → 數值行93; OR03/CROX/Quarter/Report1!A93 → 數值行93; OR04/Insulet/Quarter/Report1!A93 → 數值行93; OR05/TransUnion/Quarter/Report1!A93 → 數值行93; OR06/TransUnion/Quarter/Report1!A93 → 數值行93; OR07/Nexstar/Year/Report1!A93 → 數值行93; OR08/XPO/Year/Report1!A93 → 數值行93; OR09/CROX/Year/Report1!A93 → 數值行93; OR10/Insulet/Year/Report1!A93 → 數值行93; OR11/TransUnion/Year/Report1!A93 → 數值行93 |
| 意義候選 | 關聯企業未實現利益 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源未實現利益與列報符號 |
| 排除與不可替代項 | 不自行套正負號或當作現金流入 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Operations / Income；損益表；該收入／成本／費用及稅項附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A94

原始英文：`Gross Profit`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | IS 名稱行94；OR01/Nexstar/Quarter/Report1!A94 → 數值行94; OR02/Nexstar/Quarter/Report1!A94 → 數值行94; OR03/CROX/Quarter/Report1!A94 → 數值行94; OR04/Insulet/Quarter/Report1!A94 → 數值行94; OR05/TransUnion/Quarter/Report1!A94 → 數值行94; OR06/TransUnion/Quarter/Report1!A94 → 數值行94; OR07/Nexstar/Year/Report1!A94 → 數值行94; OR08/XPO/Year/Report1!A94 → 數值行94; OR09/CROX/Year/Report1!A94 → 數值行94; OR10/Insulet/Year/Report1!A94 → 數值行94; OR11/TransUnion/Year/Report1!A94 → 數值行94 |
| 意義候選 | 毛利金額 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 對應營收及營收成本後之毛利 |
| 排除與不可替代項 | 毛利率不是金額；其他毛利橋接項須核實 |
| 既有代碼 | METRICS候選：gross_profit；raw候選：gross_profit。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Operations / Income；損益表；該收入／成本／費用及稅項附註 |
| 候選XBRL tags | us-gaap:GrossProfit → raw.gross_profit |
| 計算輸入tag候選 | revenue: us-gaap:Revenues, us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax; cost_of_revenue: us-gaap:CostOfRevenue, us-gaap:CostOfGoodsAndServicesSold |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接揭露與DER-01條件式推導分別保留；不一致時列conflict，不以推導覆寫來源；規則：DER-01。 |
| 核准公式／推導條件引用 | DER-01: Revenues − Cost of Revenue；優先保留適用的直接揭露毛利；推導時營收與成本必須同期間、同範圍，且成本為對應營收成本，不是包含其他營業費用的總費用。若主表另有影響毛利的項目，須先確認完整恆等式。 |
| 必要輸入與版本 | revenue, cost_of_revenue；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A95

原始英文：`Bad Debt Expense`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | IS 名稱行95；OR01/Nexstar/Quarter/Report1!A95 → 數值行95; OR02/Nexstar/Quarter/Report1!A95 → 數值行95; OR03/CROX/Quarter/Report1!A95 → 數值行95; OR04/Insulet/Quarter/Report1!A95 → 數值行95; OR05/TransUnion/Quarter/Report1!A95 → 數值行95; OR06/TransUnion/Quarter/Report1!A95 → 數值行95; OR07/Nexstar/Year/Report1!A95 → 數值行95; OR08/XPO/Year/Report1!A95 → 數值行95; OR09/CROX/Year/Report1!A95 → 數值行95; OR10/Insulet/Year/Report1!A95 → 數值行95; OR11/TransUnion/Year/Report1!A95 → 數值行95 |
| 意義候選 | 呆帳費用 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源當期信用損失費用及列報位置 |
| 排除與不可替代項 | 不是應收款備抵餘額；不得與Operating Expense重複扣除 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Operations / Income；損益表；該收入／成本／費用及稅項附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A96

原始英文：`Operating Expense`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | IS 名稱行96；OR01/Nexstar/Quarter/Report1!A96 → 數值行96; OR02/Nexstar/Quarter/Report1!A96 → 數值行96; OR03/CROX/Quarter/Report1!A96 → 數值行96; OR04/Insulet/Quarter/Report1!A96 → 數值行96; OR05/TransUnion/Quarter/Report1!A96 → 數值行96; OR06/TransUnion/Quarter/Report1!A96 → 數值行96; OR07/Nexstar/Year/Report1!A96 → 數值行96; OR08/XPO/Year/Report1!A96 → 數值行96; OR09/CROX/Year/Report1!A96 → 數值行96; OR10/Insulet/Year/Report1!A96 → 數值行96; OR11/TransUnion/Year/Report1!A96 → 數值行96 |
| 意義候選 | 不含營收成本之營業費用 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源SG&A、研發等經確認不重疊組成 |
| 排除與不可替代項 | 不可把含COGS的CostsAndExpenses直接採用 |
| 既有代碼 | METRICS候選：operating_expense；raw候選：operating_expense_direct。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Operations / Income；損益表；該收入／成本／費用及稅項附註 |
| 候選XBRL tags | us-gaap:OperatingExpenses → raw.operating_expense_direct |
| 計算輸入tag候選 | gross_profit: us-gaap:GrossProfit; operating_income: us-gaap:OperatingIncomeLoss |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：DER-03。 |
| 核准公式／推導條件引用 | DER-03: Gross Profit − Operating Income；僅適用於兩者之間完全由該類營業費用構成的列報。若另有營業收益、重組、減損或其他獨立調整，須確認其歸屬及符號後使用完整橋接式。不得不加核對地將 `CostsAndExpenses` 當成不含 COGS 的費用。 |
| 必要輸入與版本 | gross_profit, operating_income；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A97

原始英文：`Operating Profit`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | IS 名稱行97；OR01/Nexstar/Quarter/Report1!A97 → 數值行97; OR02/Nexstar/Quarter/Report1!A97 → 數值行97; OR03/CROX/Quarter/Report1!A97 → 數值行97; OR04/Insulet/Quarter/Report1!A97 → 數值行97; OR05/TransUnion/Quarter/Report1!A97 → 數值行97; OR06/TransUnion/Quarter/Report1!A97 → 數值行97; OR07/Nexstar/Year/Report1!A97 → 數值行97; OR08/XPO/Year/Report1!A97 → 數值行97; OR09/CROX/Year/Report1!A97 → 數值行97; OR10/Insulet/Year/Report1!A97 → 數值行97; OR11/TransUnion/Year/Report1!A97 → 數值行97 |
| 意義候選 | 營業利益 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源營業損益；或完整營業費用橋接 |
| 排除與不可替代項 | 營業外損益、EBITDA及其他調整利益不可互換 |
| 既有代碼 | METRICS候選：operating_income；raw候選：operating_income。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Operations / Income；損益表；該收入／成本／費用及稅項附註 |
| 候選XBRL tags | us-gaap:OperatingIncomeLoss → raw.operating_income |
| 計算輸入tag候選 | gross_profit: us-gaap:GrossProfit; operating_expense: us-gaap:OperatingExpenses |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：DER-04。 |
| 核准公式／推導條件引用 | DER-04: Gross Profit − Operating Expense；與 DER-03 相同的完整橋接條件；不得重複扣除已含在成本中的折舊、攤銷或其他費用。 |
| 必要輸入與版本 | gross_profit, operating_expense；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A98

原始英文：`Non-operating Revenues & Expenses - Net`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | IS 名稱行98；OR01/Nexstar/Quarter/Report1!A98 → 數值行98; OR02/Nexstar/Quarter/Report1!A98 → 數值行98; OR03/CROX/Quarter/Report1!A98 → 數值行98; OR04/Insulet/Quarter/Report1!A98 → 數值行98; OR05/TransUnion/Quarter/Report1!A98 → 數值行98; OR06/TransUnion/Quarter/Report1!A98 → 數值行98; OR07/Nexstar/Year/Report1!A98 → 數值行98; OR08/XPO/Year/Report1!A98 → 數值行98; OR09/CROX/Year/Report1!A98 → 數值行98; OR10/Insulet/Year/Report1!A98 → 數值行98; OR11/TransUnion/Year/Report1!A98 → 數值行98 |
| 意義候選 | 營業外收入及費用淨額 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源確認之營業外收益與費用 |
| 排除與不可替代項 | 不預設利息是唯一營業外項目 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Operations / Income；損益表；該收入／成本／費用及稅項附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：DER-07。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A99

原始英文：`Non-operating Revenues`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | IS 名稱行99；OR01/Nexstar/Quarter/Report1!A99 → 數值行99; OR02/Nexstar/Quarter/Report1!A99 → 數值行99; OR03/CROX/Quarter/Report1!A99 → 數值行99; OR04/Insulet/Quarter/Report1!A99 → 數值行99; OR05/TransUnion/Quarter/Report1!A99 → 數值行99; OR06/TransUnion/Quarter/Report1!A99 → 數值行99; OR07/Nexstar/Year/Report1!A99 → 數值行99; OR08/XPO/Year/Report1!A99 → 數值行99; OR09/CROX/Year/Report1!A99 → 數值行99; OR10/Insulet/Year/Report1!A99 → 數值行99; OR11/TransUnion/Year/Report1!A99 → 數值行99 |
| 意義候選 | 營業外收入小計 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源營業外收益組成 |
| 排除與不可替代項 | 不得同時加總小計及投資／利息等明細 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Operations / Income；損益表；該收入／成本／費用及稅項附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：DER-07。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A100

原始英文：`Interest Income`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | IS 名稱行100；OR01/Nexstar/Quarter/Report1!A100 → 數值行100; OR02/Nexstar/Quarter/Report1!A100 → 數值行100; OR03/CROX/Quarter/Report1!A100 → 數值行100; OR04/Insulet/Quarter/Report1!A100 → 數值行100; OR05/TransUnion/Quarter/Report1!A100 → 數值行100; OR06/TransUnion/Quarter/Report1!A100 → 數值行100; OR07/Nexstar/Year/Report1!A100 → 數值行100; OR08/XPO/Year/Report1!A100 → 數值行100; OR09/CROX/Year/Report1!A100 → 數值行100; OR10/Insulet/Year/Report1!A100 → 數值行100; OR11/TransUnion/Year/Report1!A100 → 數值行100 |
| 意義候選 | 利息收入 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源利息收入及分類 |
| 排除與不可替代項 | 不把淨利息費用拆成未揭露之毛額利息收入 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Operations / Income；損益表；該收入／成本／費用及稅項附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A101

原始英文：`Investment Gains`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | IS 名稱行101；OR01/Nexstar/Quarter/Report1!A101 → 數值行101; OR02/Nexstar/Quarter/Report1!A101 → 數值行101; OR03/CROX/Quarter/Report1!A101 → 數值行101; OR04/Insulet/Quarter/Report1!A101 → 數值行101; OR05/TransUnion/Quarter/Report1!A101 → 數值行101; OR06/TransUnion/Quarter/Report1!A101 → 數值行101; OR07/Nexstar/Year/Report1!A101 → 數值行101; OR08/XPO/Year/Report1!A101 → 數值行101; OR09/CROX/Year/Report1!A101 → 數值行101; OR10/Insulet/Year/Report1!A101 → 數值行101; OR11/TransUnion/Year/Report1!A101 → 數值行101 |
| 意義候選 | 投資利益 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源投資收益範圍 |
| 排除與不可替代項 | 已實現、未實現、權益法及處分利益須區別 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Operations / Income；損益表；該收入／成本／費用及稅項附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A102

原始英文：`Gain On Fixed Asset Disposal`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | IS 名稱行102；OR01/Nexstar/Quarter/Report1!A102 → 數值行102; OR02/Nexstar/Quarter/Report1!A102 → 數值行102; OR03/CROX/Quarter/Report1!A102 → 數值行102; OR04/Insulet/Quarter/Report1!A102 → 數值行102; OR05/TransUnion/Quarter/Report1!A102 → 數值行102; OR06/TransUnion/Quarter/Report1!A102 → 數值行102; OR07/Nexstar/Year/Report1!A102 → 數值行102; OR09/CROX/Year/Report1!A102 → 數值行102; OR10/Insulet/Year/Report1!A102 → 數值行102; OR11/TransUnion/Year/Report1!A102 → 數值行102 |
| 意義候選 | 處分固定資產利益 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源資產處分損益 |
| 排除與不可替代項 | 出售現金收款不是處分利益 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Operations / Income；損益表；該收入／成本／費用及稅項附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-047。 |

## OR01-Report1-A103

原始英文：`Gain On Investment Disposal`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | IS 名稱行103；OR01/Nexstar/Quarter/Report1!A103 → 數值行103; OR02/Nexstar/Quarter/Report1!A103 → 數值行103; OR03/CROX/Quarter/Report1!A103 → 數值行103; OR04/Insulet/Quarter/Report1!A103 → 數值行103; OR05/TransUnion/Quarter/Report1!A103 → 數值行103; OR06/TransUnion/Quarter/Report1!A103 → 數值行103; OR07/Nexstar/Year/Report1!A103 → 數值行103; OR08/XPO/Year/Report1!A103 → 數值行103; OR09/CROX/Year/Report1!A103 → 數值行103; OR10/Insulet/Year/Report1!A103 → 數值行103; OR11/TransUnion/Year/Report1!A103 → 數值行103 |
| 意義候選 | 處分投資利益 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源投資處分利益 |
| 排除與不可替代項 | 不以投資出售收款替代 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Operations / Income；損益表；該收入／成本／費用及稅項附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A104

原始英文：`Other Income`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | IS 名稱行104；OR01/Nexstar/Quarter/Report1!A104 → 數值行104; OR02/Nexstar/Quarter/Report1!A104 → 數值行104; OR03/CROX/Quarter/Report1!A104 → 數值行104; OR04/Insulet/Quarter/Report1!A104 → 數值行104; OR05/TransUnion/Quarter/Report1!A104 → 數值行104; OR06/TransUnion/Quarter/Report1!A104 → 數值行104; OR07/Nexstar/Year/Report1!A104 → 數值行104; OR08/XPO/Year/Report1!A104 → 數值行104; OR09/CROX/Year/Report1!A104 → 數值行104; OR10/Insulet/Year/Report1!A104 → 數值行104; OR11/TransUnion/Year/Report1!A104 → 數值行104 |
| 意義候選 | 其他營業外收入 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源其他收入組成 |
| 排除與不可替代項 | 不等同Other Revenues或所有不明收益 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Operations / Income；損益表；該收入／成本／費用及稅項附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A105

原始英文：`Non-operating Expenses`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | IS 名稱行105；OR01/Nexstar/Quarter/Report1!A105 → 數值行105; OR02/Nexstar/Quarter/Report1!A105 → 數值行105; OR03/CROX/Quarter/Report1!A105 → 數值行105; OR04/Insulet/Quarter/Report1!A105 → 數值行105; OR05/TransUnion/Quarter/Report1!A105 → 數值行105; OR06/TransUnion/Quarter/Report1!A105 → 數值行105; OR07/Nexstar/Year/Report1!A105 → 數值行105; OR08/XPO/Year/Report1!A105 → 數值行105; OR09/CROX/Year/Report1!A105 → 數值行105; OR10/Insulet/Year/Report1!A105 → 數值行105; OR11/TransUnion/Year/Report1!A105 → 數值行105 |
| 意義候選 | 營業外費用小計 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源營業外費用組成 |
| 排除與不可替代項 | 不與利息、投資損失等明細重複 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Operations / Income；損益表；該收入／成本／費用及稅項附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：DER-07。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A106

原始英文：`Interest Expense`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | IS 名稱行106；OR01/Nexstar/Quarter/Report1!A106 → 數值行106; OR02/Nexstar/Quarter/Report1!A106 → 數值行106; OR03/CROX/Quarter/Report1!A106 → 數值行106; OR04/Insulet/Quarter/Report1!A106 → 數值行106; OR05/TransUnion/Quarter/Report1!A106 → 數值行106; OR06/TransUnion/Quarter/Report1!A106 → 數值行106; OR07/Nexstar/Year/Report1!A106 → 數值行106; OR08/XPO/Year/Report1!A106 → 數值行106; OR09/CROX/Year/Report1!A106 → 數值行106; OR10/Insulet/Year/Report1!A106 → 數值行106; OR11/TransUnion/Year/Report1!A106 → 數值行106 |
| 意義候選 | 利息費用，毛額／淨額定義待確認 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源適用利息費用 |
| 排除與不可替代項 | 利息收入、支付利息、資本化利息不能任意互換 |
| 既有代碼 | METRICS候選：interest_expense；raw候選：interest_expense, interest_expense_alt。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Operations / Income；損益表；該收入／成本／費用及稅項附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | us-gaap:InterestExpense → raw.interest_expense; us-gaap:InterestExpenseNonoperating → raw.interest_expense_alt |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | DEC-05；另見全部84項盤點待確認清單。 |

## OR01-Report1-A107

原始英文：`Investment Loss`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | IS 名稱行107；OR01/Nexstar/Quarter/Report1!A107 → 數值行107; OR02/Nexstar/Quarter/Report1!A107 → 數值行107; OR03/CROX/Quarter/Report1!A107 → 數值行107; OR04/Insulet/Quarter/Report1!A107 → 數值行107; OR05/TransUnion/Quarter/Report1!A107 → 數值行107; OR06/TransUnion/Quarter/Report1!A107 → 數值行107; OR07/Nexstar/Year/Report1!A107 → 數值行107; OR08/XPO/Year/Report1!A107 → 數值行107; OR09/CROX/Year/Report1!A107 → 數值行107; OR10/Insulet/Year/Report1!A107 → 數值行107; OR11/TransUnion/Year/Report1!A107 → 數值行107 |
| 意義候選 | 投資損失 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源投資損失及損益分類 |
| 排除與不可替代項 | 已實現、未實現、權益法、減損及處分損失不可僅因都稱投資而合併 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Operations / Income；損益表；該收入／成本／費用及稅項附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A108

原始英文：`Loss on extinguishment of debt`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | IS 名稱行108；OR01/Nexstar/Quarter/Report1!A108 → 數值行108; OR02/Nexstar/Quarter/Report1!A108 → 數值行108 |
| 意義候選 | 債務清償損失 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 該公司該期該名稱實際損失 |
| 排除與不可替代項 | 不能將本行跨公司或跨檔固定為一種損失；CF回加數另核 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Operations / Income；損益表；該收入／成本／費用及稅項附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-048。 |

## OR01-Report1-A109

原始英文：`Loss On Investment Disposal`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | IS 名稱行109；OR01/Nexstar/Quarter/Report1!A109 → 數值行109; OR02/Nexstar/Quarter/Report1!A109 → 數值行109; OR03/CROX/Quarter/Report1!A109 → 數值行109; OR04/Insulet/Quarter/Report1!A109 → 數值行109; OR05/TransUnion/Quarter/Report1!A109 → 數值行109; OR06/TransUnion/Quarter/Report1!A109 → 數值行109; OR07/Nexstar/Year/Report1!A109 → 數值行109; OR08/XPO/Year/Report1!A109 → 數值行109; OR09/CROX/Year/Report1!A109 → 數值行109; OR10/Insulet/Year/Report1!A109 → 數值行109; OR11/TransUnion/Year/Report1!A109 → 數值行109 |
| 意義候選 | 處分投資損失 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源投資處分損失 |
| 排除與不可替代項 | 投資出售現金流與評價損失不是同一概念 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Operations / Income；損益表；該收入／成本／費用及稅項附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A110

原始英文：`Other Expenses`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | IS 名稱行110；OR01/Nexstar/Quarter/Report1!A110 → 數值行110; OR02/Nexstar/Quarter/Report1!A110 → 數值行110; OR03/CROX/Quarter/Report1!A110 → 數值行110; OR04/Insulet/Quarter/Report1!A110 → 數值行110; OR05/TransUnion/Quarter/Report1!A110 → 數值行110; OR06/TransUnion/Quarter/Report1!A110 → 數值行110; OR07/Nexstar/Year/Report1!A110 → 數值行110; OR08/XPO/Year/Report1!A110 → 數值行110; OR09/CROX/Year/Report1!A110 → 數值行110; OR10/Insulet/Year/Report1!A110 → 數值行110; OR11/TransUnion/Year/Report1!A110 → 數值行110 |
| 意義候選 | 其他營業外費用 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源該行明細 |
| 排除與不可替代項 | 不以缺項或勾稽差額補入 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Operations / Income；損益表；該收入／成本／費用及稅項附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A111

原始英文：`Pre-tax Profit (Loss)`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | IS 名稱行111；OR01/Nexstar/Quarter/Report1!A111 → 數值行111; OR02/Nexstar/Quarter/Report1!A111 → 數值行111; OR03/CROX/Quarter/Report1!A111 → 數值行111; OR04/Insulet/Quarter/Report1!A111 → 數值行111; OR05/TransUnion/Quarter/Report1!A111 → 數值行111; OR06/TransUnion/Quarter/Report1!A111 → 數值行111; OR07/Nexstar/Year/Report1!A111 → 數值行111; OR08/XPO/Year/Report1!A111 → 數值行111; OR09/CROX/Year/Report1!A111 → 數值行111; OR10/Insulet/Year/Report1!A111 → 數值行111; OR11/TransUnion/Year/Report1!A111 → 數值行111 |
| 意義候選 | 稅前利益或損失 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 同一損益範圍之稅前結果 |
| 排除與不可替代項 | 不得混用繼續營業、母公司與合併範圍 |
| 既有代碼 | METRICS候選：pretax_profit；raw候選：income_before_tax。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Operations / Income；損益表；該收入／成本／費用及稅項附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | us-gaap:IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest → raw.income_before_tax |
| 計算輸入tag候選 | net_income: us-gaap:NetIncomeLoss; income_tax: us-gaap:IncomeTaxExpenseBenefit |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：DER-05。 |
| 核准公式／推導條件引用 | DER-05: Net Income + signed Income Tax Expense；只限淨利與所得稅對應同一稅前損益範圍，且沒有未處理的停業單位、非控制權益或其他橋接項。所得稅費用為正、利益為負；不得使用 `abs(tax)`。若有橋接項，須有來源及經確認的完整公式。 |
| 必要輸入與版本 | net_income, income_tax；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A112

原始英文：`Income Tax Expense(Credit)`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | IS 名稱行112；OR01/Nexstar/Quarter/Report1!A112 → 數值行112; OR02/Nexstar/Quarter/Report1!A112 → 數值行112; OR03/CROX/Quarter/Report1!A112 → 數值行112; OR04/Insulet/Quarter/Report1!A112 → 數值行112; OR05/TransUnion/Quarter/Report1!A112 → 數值行112; OR06/TransUnion/Quarter/Report1!A112 → 數值行112; OR07/Nexstar/Year/Report1!A112 → 數值行112; OR08/XPO/Year/Report1!A112 → 數值行112; OR09/CROX/Year/Report1!A112 → 數值行112; OR10/Insulet/Year/Report1!A112 → 數值行112; OR11/TransUnion/Year/Report1!A112 → 數值行112 |
| 意義候選 | 所得稅費用或利益，保留來源符號 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 當期及遞延稅之費用／利益組成 |
| 排除與不可替代項 | 現金付稅、應付稅額及遞延稅負債不是所得稅費用 |
| 既有代碼 | METRICS候選：income_tax；raw候選：income_tax_expense。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Operations / Income；損益表；該收入／成本／費用及稅項附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | us-gaap:IncomeTaxExpenseBenefit → raw.income_tax_expense |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：DER-05, DER-06。 |
| 核准公式／推導條件引用 | DER-05: Net Income + signed Income Tax Expense；只限淨利與所得稅對應同一稅前損益範圍，且沒有未處理的停業單位、非控制權益或其他橋接項。所得稅費用為正、利益為負；不得使用 `abs(tax)`。若有橋接項，須有來源及經確認的完整公式。；DER-06: Pre-tax Profit − signed Income Tax Expense；與 DER-05 相同的適用條件；不得把 continuing operations、歸屬母公司淨利與合併淨利直接互換。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A113

原始英文：`Profit (Loss) From Discontinued Operations`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | IS 名稱行113；OR01/Nexstar/Quarter/Report1!A113 → 數值行113; OR02/Nexstar/Quarter/Report1!A113 → 數值行113; OR03/CROX/Quarter/Report1!A113 → 數值行113; OR05/TransUnion/Quarter/Report1!A113 → 數值行113; OR06/TransUnion/Quarter/Report1!A113 → 數值行113; OR07/Nexstar/Year/Report1!A113 → 數值行113; OR08/XPO/Year/Report1!A113 → 數值行113; OR09/CROX/Year/Report1!A113 → 數值行113; OR11/TransUnion/Year/Report1!A113 → 數值行113 |
| 意義候選 | 停業單位損益；稅前／稅後與範圍須確認 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源停業單位損益 |
| 排除與不可替代項 | 不可當成稅益；不能未經核實直接加到合併淨利橋接 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Operations / Income；損益表；該收入／成本／費用及稅項附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-049。 |

## OR01-Report1-A114

原始英文：`Extraordinary Profit (Loss)`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | IS 名稱行114；OR01/Nexstar/Quarter/Report1!A114 → 數值行114; OR02/Nexstar/Quarter/Report1!A114 → 數值行114; OR03/CROX/Quarter/Report1!A114 → 數值行114; OR04/Insulet/Quarter/Report1!A114 → 數值行114; OR05/TransUnion/Quarter/Report1!A114 → 數值行114; OR06/TransUnion/Quarter/Report1!A114 → 數值行114; OR07/Nexstar/Year/Report1!A114 → 數值行114; OR08/XPO/Year/Report1!A114 → 數值行114; OR09/CROX/Year/Report1!A114 → 數值行114; OR10/Insulet/Year/Report1!A114 → 數值行114; OR11/TransUnion/Year/Report1!A114 → 數值行114 |
| 意義候選 | Extraordinary損益，需核當期列報制度與來源 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源實際獨立揭露項目 |
| 排除與不可替代項 | 歷史範本欄位存在不代表當期有此會計分類 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Operations / Income；損益表；該收入／成本／費用及稅項附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A115

原始英文：`Cumulative Effects Of Changes In Accounting Policies`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | IS 名稱行115；OR01/Nexstar/Quarter/Report1!A115 → 數值行115; OR02/Nexstar/Quarter/Report1!A115 → 數值行115; OR03/CROX/Quarter/Report1!A115 → 數值行115; OR04/Insulet/Quarter/Report1!A115 → 數值行115; OR05/TransUnion/Quarter/Report1!A115 → 數值行115; OR06/TransUnion/Quarter/Report1!A115 → 數值行115; OR07/Nexstar/Year/Report1!A115 → 數值行115; OR08/XPO/Year/Report1!A115 → 數值行115; OR09/CROX/Year/Report1!A115 → 數值行115; OR10/Insulet/Year/Report1!A115 → 數值行115; OR11/TransUnion/Year/Report1!A115 → 數值行115 |
| 意義候選 | 會計政策變動累積影響數 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源實際變動與列報位置 |
| 排除與不可替代項 | 不自行當作當期稅後損益調整 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Operations / Income；損益表；該收入／成本／費用及稅項附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A116

原始英文：`Other Adjustments`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | IS 名稱行116；OR01/Nexstar/Quarter/Report1!A116 → 數值行116; OR02/Nexstar/Quarter/Report1!A116 → 數值行116; OR03/CROX/Quarter/Report1!A116 → 數值行116; OR04/Insulet/Quarter/Report1!A116 → 數值行116; OR05/TransUnion/Quarter/Report1!A116 → 數值行116; OR06/TransUnion/Quarter/Report1!A116 → 數值行116; OR07/Nexstar/Year/Report1!A116 → 數值行116; OR08/XPO/Year/Report1!A116 → 數值行116; OR09/CROX/Year/Report1!A116 → 數值行116; OR10/Insulet/Year/Report1!A116 → 數值行116; OR11/TransUnion/Year/Report1!A116 → 數值行116 |
| 意義候選 | 其他損益調整 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源逐項定義 |
| 排除與不可替代項 | 不是可任意放入差額的欄位 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Operations / Income；損益表；該收入／成本／費用及稅項附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A117

原始英文：`After-tax Net Profit (Loss)`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | IS 名稱行117；OR01/Nexstar/Quarter/Report1!A117 → 數值行117; OR02/Nexstar/Quarter/Report1!A117 → 數值行117; OR03/CROX/Quarter/Report1!A117 → 數值行117; OR04/Insulet/Quarter/Report1!A117 → 數值行117; OR05/TransUnion/Quarter/Report1!A117 → 數值行117; OR06/TransUnion/Quarter/Report1!A117 → 數值行117; OR07/Nexstar/Year/Report1!A117 → 數值行117; OR08/XPO/Year/Report1!A117 → 數值行117; OR09/CROX/Year/Report1!A117 → 數值行117; OR10/Insulet/Year/Report1!A117 → 數值行117; OR11/TransUnion/Year/Report1!A117 → 數值行117 |
| 意義候選 | 稅後淨利／淨損 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源淨利範圍及非控制權益處理 |
| 排除與不可替代項 | 母公司淨利、合併淨利及繼續營業淨利不可互換 |
| 既有代碼 | METRICS候選：net_income；raw候選：net_income。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Operations / Income；損益表；該收入／成本／費用及稅項附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | us-gaap:NetIncomeLoss → raw.net_income |
| 計算輸入tag候選 | pretax_profit: us-gaap:IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest; income_tax: us-gaap:IncomeTaxExpenseBenefit |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：DER-06。 |
| 核准公式／推導條件引用 | DER-06: Pre-tax Profit − signed Income Tax Expense；與 DER-05 相同的適用條件；不得把 continuing operations、歸屬母公司淨利與合併淨利直接互換。 |
| 必要輸入與版本 | pretax_profit, income_tax；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A118

原始英文：`Sales To Related Parties`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | IS 名稱行118；OR01/Nexstar/Quarter/Report1!A118 → 數值行118; OR02/Nexstar/Quarter/Report1!A118 → 數值行118; OR03/CROX/Quarter/Report1!A118 → 數值行118; OR04/Insulet/Quarter/Report1!A118 → 數值行118; OR05/TransUnion/Quarter/Report1!A118 → 數值行118; OR06/TransUnion/Quarter/Report1!A118 → 數值行118; OR07/Nexstar/Year/Report1!A118 → 數值行118; OR08/XPO/Year/Report1!A118 → 數值行118; OR09/CROX/Year/Report1!A118 → 數值行118; OR10/Insulet/Year/Report1!A118 → 數值行118; OR11/TransUnion/Year/Report1!A118 → 數值行118 |
| 意義候選 | 對關係人銷貨補充揭露 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源關係人交易收入 |
| 排除與不可替代項 | 不與主表營收重複加總；未披露不代表0 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Operations / Income；損益表；該收入／成本／費用及稅項附註；Related-party transactions／關係人交易附註；核對交易對手及合併沖銷 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=source_definition_required；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A119

原始英文：`% Of Related Party Sales To Total Sales`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | IS 名稱行119；OR01/Nexstar/Quarter/Report1!A119 → 數值行119; OR02/Nexstar/Quarter/Report1!A119 → 數值行119; OR03/CROX/Quarter/Report1!A119 → 數值行119; OR04/Insulet/Quarter/Report1!A119 → 數值行119; OR05/TransUnion/Quarter/Report1!A119 → 數值行119; OR06/TransUnion/Quarter/Report1!A119 → 數值行119; OR07/Nexstar/Year/Report1!A119 → 數值行119; OR08/XPO/Year/Report1!A119 → 數值行119; OR09/CROX/Year/Report1!A119 → 數值行119; OR10/Insulet/Year/Report1!A119 → 數值行119; OR11/TransUnion/Year/Report1!A119 → 數值行119 |
| 意義候選 | 關係人銷貨占總銷貨比率 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 經核實關係人銷貨及一致分母 |
| 排除與不可替代項 | 主表總營收或Net Sales何者為分母仍須查證 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Operations / Income；損益表；該收入／成本／費用及稅項附註；Related-party transactions／關係人交易附註；核對交易對手及合併沖銷 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 原檔比率僅作比較；分子與分母定義核定前不自行註冊正式公式；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=percent（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A120

原始英文：`Capitalized Interest`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | IS 名稱行120；OR01/Nexstar/Quarter/Report1!A120 → 數值行120; OR02/Nexstar/Quarter/Report1!A120 → 數值行120; OR03/CROX/Quarter/Report1!A120 → 數值行120; OR04/Insulet/Quarter/Report1!A120 → 數值行120; OR05/TransUnion/Quarter/Report1!A120 → 數值行120; OR06/TransUnion/Quarter/Report1!A120 → 數值行120; OR07/Nexstar/Year/Report1!A120 → 數值行120; OR08/XPO/Year/Report1!A120 → 數值行120; OR09/CROX/Year/Report1!A120 → 數值行120; OR10/Insulet/Year/Report1!A120 → 數值行120; OR11/TransUnion/Year/Report1!A120 → 數值行120 |
| 意義候選 | 資本化利息，來源映射待核 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源本期間資本化利息 |
| 排除與不可替代項 | 支付利息、利息費用及未披露金額不可替代 |
| 既有代碼 | METRICS候選：capitalized_interest；raw候選：capitalized_interest。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Operations / Income；損益表；該收入／成本／費用及稅項附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | us-gaap:InterestCostsCapitalized → raw.capitalized_interest |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：CF-04, CF-05。 |
| 核准公式／推導條件引用 | CF-04: (Pre-tax Profit + Interest Expense) / (Interest Expense + Capitalized Interest)；CF-05: (Pre-tax Profit + Interest Expense + Depreciation & Amortization) / (Interest Expense + Capitalized Interest) |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=source_definition_required；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | DEC-05；另見全部84項盤點待確認清單。 |

## OR01-Report1-A121

原始英文：`Depreciation & Amortization`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | IS 名稱行121；OR01/Nexstar/Quarter/Report1!A121 → 數值行121; OR02/Nexstar/Quarter/Report1!A121 → 數值行121; OR03/CROX/Quarter/Report1!A121 → 數值行121; OR04/Insulet/Quarter/Report1!A121 → 數值行121; OR05/TransUnion/Quarter/Report1!A121 → 數值行121; OR06/TransUnion/Quarter/Report1!A121 → 數值行121; OR07/Nexstar/Year/Report1!A121 → 數值行121; OR08/XPO/Year/Report1!A121 → 數值行121; OR09/CROX/Year/Report1!A121 → 數值行121; OR10/Insulet/Year/Report1!A121 → 數值行121; OR11/TransUnion/Year/Report1!A121 → 數值行121 |
| 意義候選 | 折舊及攤銷補充揭露 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源全範圍D&A與單位期間 |
| 排除與不可替代項 | 不把單一成本中的D&A等同全公司；CF回加數可能口徑不同 |
| 既有代碼 | METRICS候選：da；raw候選：da。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Operations / Income；損益表；該收入／成本／費用及稅項附註 |
| 候選XBRL tags | us-gaap:DepreciationDepletionAndAmortization → raw.da |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | DEC-06；ISS-059。 |

## OR01-Report1-A122

原始英文：`Prepayments To Related Parties`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | IS 名稱行122；OR01/Nexstar/Quarter/Report1!A122 → 數值行122; OR02/Nexstar/Quarter/Report1!A122 → 數值行122; OR03/CROX/Quarter/Report1!A122 → 數值行122; OR04/Insulet/Quarter/Report1!A122 → 數值行122; OR05/TransUnion/Quarter/Report1!A122 → 數值行122; OR06/TransUnion/Quarter/Report1!A122 → 數值行122; OR07/Nexstar/Year/Report1!A122 → 數值行122; OR08/XPO/Year/Report1!A122 → 數值行122; OR09/CROX/Year/Report1!A122 → 數值行122; OR10/Insulet/Year/Report1!A122 → 數值行122; OR11/TransUnion/Year/Report1!A122 → 數值行122 |
| 意義候選 | 預付關係人款項補充資料 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源關係人餘額／交易及期間 |
| 排除與不可替代項 | 不能僅因位於損益區就判為當期費用 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Operations / Income；損益表；該收入／成本／費用及稅項附註；Related-party transactions／關係人交易附註；核對交易對手及合併沖銷 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=source_definition_required；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A123

原始英文：`(operating income) Rental income from properties`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | IS 名稱行123；OR01/Nexstar/Quarter/Report1!A123 → 數值行123; OR02/Nexstar/Quarter/Report1!A123 → 數值行123; OR03/CROX/Quarter/Report1!A123 → 數值行123; OR04/Insulet/Quarter/Report1!A123 → 數值行123; OR05/TransUnion/Quarter/Report1!A123 → 數值行123; OR06/TransUnion/Quarter/Report1!A123 → 數值行123; OR07/Nexstar/Year/Report1!A123 → 數值行123; OR08/XPO/Year/Report1!A123 → 數值行123; OR09/CROX/Year/Report1!A123 → 數值行123; OR10/Insulet/Year/Report1!A123 → 數值行123; OR11/TransUnion/Year/Report1!A123 → 數值行123 |
| 意義候選 | 不動產租金收入，列為營業收入 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源列報為營業之租金收入 |
| 排除與不可替代項 | 不與總營收重複；原檔填0指示不具指令權限 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Operations / Income；損益表；該收入／成本／費用及稅項附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A125

原始英文：`(non-operating income) Rental income from properties`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | IS 名稱行125；OR01/Nexstar/Quarter/Report1!A125 → 數值行125; OR02/Nexstar/Quarter/Report1!A125 → 數值行125; OR03/CROX/Quarter/Report1!A125 → 數值行125; OR04/Insulet/Quarter/Report1!A125 → 數值行125; OR05/TransUnion/Quarter/Report1!A125 → 數值行125; OR06/TransUnion/Quarter/Report1!A125 → 數值行125; OR07/Nexstar/Year/Report1!A125 → 數值行125; OR08/XPO/Year/Report1!A125 → 數值行125; OR09/CROX/Year/Report1!A125 → 數值行125; OR10/Insulet/Year/Report1!A125 → 數值行125; OR11/TransUnion/Year/Report1!A125 → 數值行125 |
| 意義候選 | 不動產租金收入，列為營業外收入 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源列報為營業外之租金收入 |
| 排除與不可替代項 | 不與Other Income小計重複；原檔空白不得默認0 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Operations / Income；損益表；該收入／成本／費用及稅項附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A129

原始英文：`Cash and cash equivalents - beginning of period`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行129；OR01/Nexstar/Quarter/Report1!A129 → 數值行129; OR02/Nexstar/Quarter/Report1!A129 → 數值行129; OR03/CROX/Quarter/Report1!A129 → 數值行129; OR04/Insulet/Quarter/Report1!A129 → 數值行129; OR05/TransUnion/Quarter/Report1!A129 → 數值行129; OR06/TransUnion/Quarter/Report1!A129 → 數值行129; OR07/Nexstar/Year/Report1!A129 → 數值行129; OR08/XPO/Year/Report1!A129 → 數值行129; OR09/CROX/Year/Report1!A129 → 數值行129; OR10/Insulet/Year/Report1!A129 → 數值行129; OR11/TransUnion/Year/Report1!A129 → 數值行129 |
| 意義候選 | 期初現金；須與期末採相同現金定義 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源CF期初現金及必要調節 |
| 排除與不可替代項 | 不得以期末減不完整三類活動反推 |
| 既有代碼 | METRICS候選：beginning_cash；raw候選：cash。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | us-gaap:CashAndCashEquivalentsAtCarryingValue → raw.cash |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：DER-08, DER-10。 |
| 核准公式／推導條件引用 | DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。；DER-10: 同口徑 Ending Cash − Beginning Cash。另以 DER-08 核對橋接；不可直接將 CFO＋CFI＋CFF 視為所有情況下的完整變動。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=opening；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A130

原始英文：`Cash Flow From Operating Activities`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行130；OR01/Nexstar/Quarter/Report1!A130 → 數值行130; OR02/Nexstar/Quarter/Report1!A130 → 數值行130; OR03/CROX/Quarter/Report1!A130 → 數值行130; OR04/Insulet/Quarter/Report1!A130 → 數值行130; OR05/TransUnion/Quarter/Report1!A130 → 數值行130; OR06/TransUnion/Quarter/Report1!A130 → 數值行130; OR07/Nexstar/Year/Report1!A130 → 數值行130; OR08/XPO/Year/Report1!A130 → 數值行130; OR09/CROX/Year/Report1!A130 → 數值行130; OR10/Insulet/Year/Report1!A130 → 數值行130; OR11/TransUnion/Year/Report1!A130 → 數值行130 |
| 意義候選 | 報表分組標題，不是可取數的金融事實 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 非數值標題／須核原文 |
| 排除與不可替代項 | 不搜尋或填入金額；不註冊metric |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 僅保留版面／分組；無取值、加總或公式；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=not_a_fact（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=not_a_fact；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A131

原始英文：`　　Net profit (loss) after tax`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行131；OR01/Nexstar/Quarter/Report1!A131 → 數值行131; OR02/Nexstar/Quarter/Report1!A131 → 數值行131; OR03/CROX/Quarter/Report1!A131 → 數值行131; OR04/Insulet/Quarter/Report1!A131 → 數值行131; OR05/TransUnion/Quarter/Report1!A131 → 數值行131; OR06/TransUnion/Quarter/Report1!A131 → 數值行131; OR07/Nexstar/Year/Report1!A131 → 數值行131; OR08/XPO/Year/Report1!A131 → 數值行131; OR09/CROX/Year/Report1!A131 → 數值行131; OR10/Insulet/Year/Report1!A131 → 數值行131; OR11/TransUnion/Year/Report1!A131 → 數值行131 |
| 意義候選 | 間接法CF起點之淨利／淨損 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源CF實際採用的淨利範圍 |
| 排除與不可替代項 | 可能與IS不同；不得自動連結後以未知調整補差 |
| 既有代碼 | METRICS候選：net_income；raw候選：net_income。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | us-gaap:NetIncomeLoss → raw.net_income |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：DER-06, DER-08。 |
| 核准公式／推導條件引用 | DER-06: Pre-tax Profit − signed Income Tax Expense；與 DER-05 相同的適用條件；不得把 continuing operations、歸屬母公司淨利與合併淨利直接互換。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A132

原始英文：`Income and loss items that do not affect cash flow from operating activities`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行132；OR01/Nexstar/Quarter/Report1!A132 → 數值行132; OR02/Nexstar/Quarter/Report1!A132 → 數值行132; OR03/CROX/Quarter/Report1!A132 → 數值行132; OR04/Insulet/Quarter/Report1!A132 → 數值行132; OR05/TransUnion/Quarter/Report1!A132 → 數值行132; OR06/TransUnion/Quarter/Report1!A132 → 數值行132; OR07/Nexstar/Year/Report1!A132 → 數值行132; OR08/XPO/Year/Report1!A132 → 數值行132; OR09/CROX/Year/Report1!A132 → 數值行132; OR10/Insulet/Year/Report1!A132 → 數值行132; OR11/TransUnion/Year/Report1!A132 → 數值行132 |
| 意義候選 | 報表分組標題，不是可取數的金融事實 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 非數值標題／須核原文 |
| 排除與不可替代項 | 不搜尋或填入金額；不註冊metric |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 僅保留版面／分組；無取值、加總或公式；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=not_a_fact（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=not_a_fact；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A133

原始英文：`　　Depreciation & Amortization`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行133；OR01/Nexstar/Quarter/Report1!A133 → 數值行133; OR02/Nexstar/Quarter/Report1!A133 → 數值行133; OR07/Nexstar/Year/Report1!A133 → 數值行133 |
| 意義候選 | 營業現金流中的非現金折舊攤銷調整 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源間接法明列之調整 |
| 排除與不可替代項 | 不預設等同IS補充D&A或全公司EBITDA輸入；不得重複回加 |
| 既有代碼 | METRICS候選：da；raw候選：da。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | us-gaap:DepreciationDepletionAndAmortization → raw.da |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：DER-07。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-007, ISS-059。 |

## OR01-Report1-A134

原始英文：`　　Other Adjustment items`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行134；OR01/Nexstar/Quarter/Report1!A134 → 數值行134; OR02/Nexstar/Quarter/Report1!A134 → 數值行134; OR07/Nexstar/Year/Report1!A134 → 數值行134 |
| 意義候選 | 來源該活動分類的其他調整／流量；必須取得組成 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 不能作為現金不勾稽的補差欄或從其他公司挪用 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-008。 |

## OR01-Report1-A135

原始英文：`　　Dividend and interest income`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行135；OR01/Nexstar/Quarter/Report1!A135 → 數值行135; OR02/Nexstar/Quarter/Report1!A135 → 數值行135; OR07/Nexstar/Year/Report1!A135 → 數值行135 |
| 意義候選 | 來源所列股利／利息收入調整或實收現金，依活動位置確認 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 間接法沖回的收益與實收現金不可混用或重複計入 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-009。 |

## OR01-Report1-A136

原始英文：`　　Loss (gain) on valuation of financial assets`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行136；OR01/Nexstar/Quarter/Report1!A136 → 數值行136; OR02/Nexstar/Quarter/Report1!A136 → 數值行136; OR07/Nexstar/Year/Report1!A136 → 數值行136 |
| 意義候選 | 來源間接法中的非現金損益／費用調整 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 損益表金額不必然等於CF回加；須核範圍、符號及是否已在其他調整中包含 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-010。 |

## OR01-Report1-A137

原始英文：`　　Investment loss (gain) recognized under equity method`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行137；OR01/Nexstar/Quarter/Report1!A137 → 數值行137; OR02/Nexstar/Quarter/Report1!A137 → 數值行137; OR07/Nexstar/Year/Report1!A137 → 數值行137 |
| 意義候選 | 來源間接法中的非現金損益／費用調整 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 損益表金額不必然等於CF回加；須核範圍、符號及是否已在其他調整中包含 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-011。 |

## OR01-Report1-A138

原始英文：`　　Loss (gain on reversal) of bad debts`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行138；OR01/Nexstar/Quarter/Report1!A138 → 數值行138; OR02/Nexstar/Quarter/Report1!A138 → 數值行138; OR07/Nexstar/Year/Report1!A138 → 數值行138 |
| 意義候選 | 來源間接法中的非現金損益／費用調整 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 損益表金額不必然等於CF回加；須核範圍、符號及是否已在其他調整中包含 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-012。 |

## OR01-Report1-A139

原始英文：`　　Allowance (reversal) for inventory valuation and obsolescence loss`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行139；OR01/Nexstar/Quarter/Report1!A139 → 數值行139; OR02/Nexstar/Quarter/Report1!A139 → 數值行139; OR07/Nexstar/Year/Report1!A139 → 數值行139 |
| 意義候選 | 營業相關資產負債變動或其他CF調整；必須核實是變動而非餘額 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | BS時點餘額tag不適用此處流量；不以兩期餘額差代替完整CF調整，除非已核非現金與合併變動 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-013。 |

## OR01-Report1-A140

原始英文：`　　Loss (gain) on disposal of investments`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行140；OR01/Nexstar/Quarter/Report1!A140 → 數值行140; OR02/Nexstar/Quarter/Report1!A140 → 數值行140; OR07/Nexstar/Year/Report1!A140 → 數值行140 |
| 意義候選 | 來源間接法中的非現金損益／費用調整 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 損益表金額不必然等於CF回加；須核範圍、符號及是否已在其他調整中包含 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-014。 |

## OR01-Report1-A141

原始英文：`　　Loss (gain) on disposal of property, equipment and plant`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行141；OR01/Nexstar/Quarter/Report1!A141 → 數值行141; OR02/Nexstar/Quarter/Report1!A141 → 數值行141; OR07/Nexstar/Year/Report1!A141 → 數值行141 |
| 意義候選 | 來源間接法中的非現金損益／費用調整 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 損益表金額不必然等於CF回加；須核範圍、符號及是否已在其他調整中包含 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A142

原始英文：`　　Unrealized foreign exchange loss (gain) ,net`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行142；OR01/Nexstar/Quarter/Report1!A142 → 數值行142; OR02/Nexstar/Quarter/Report1!A142 → 數值行142 |
| 意義候選 | 匯率變動對現金之影響或未實現兌換損益調整，須依位置與附註區別 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 影響現金餘額的匯率效果與非現金損益回加不是同一概念 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-015。 |

## OR01-Report1-A143

原始英文：`　　Payment for broadcast rights`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行143；OR01/Nexstar/Quarter/Report1!A143 → 數值行143 |
| 意義候選 | 來源所列收購、資產取得或播映權付款 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 扣除取得現金與否、業務併購及資產購置須分開；不得套用全部CapEx |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-016, ISS-061。 |

## OR01-Report1-A144

原始英文：`Changes in assets/liabilities associated with operating activities`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行144；OR01/Nexstar/Quarter/Report1!A144 → 數值行144; OR02/Nexstar/Quarter/Report1!A144 → 數值行144; OR03/CROX/Quarter/Report1!A144 → 數值行144; OR04/Insulet/Quarter/Report1!A144 → 數值行144; OR05/TransUnion/Quarter/Report1!A144 → 數值行144; OR06/TransUnion/Quarter/Report1!A144 → 數值行144; OR07/Nexstar/Year/Report1!A144 → 數值行144; OR08/XPO/Year/Report1!A144 → 數值行144; OR09/CROX/Year/Report1!A144 → 數值行144; OR10/Insulet/Year/Report1!A144 → 數值行144; OR11/TransUnion/Year/Report1!A144 → 數值行144 |
| 意義候選 | 報表分組標題，不是可取數的金融事實 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 非數值標題／須核原文 |
| 排除與不可替代項 | 不搜尋或填入金額；不註冊metric |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 僅保留版面／分組；無取值、加總或公式；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=not_a_fact（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=not_a_fact；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A145

原始英文：`　　Decrease (Increase) In Accounts Receivable`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行145；OR01/Nexstar/Quarter/Report1!A145 → 數值行145; OR02/Nexstar/Quarter/Report1!A145 → 數值行145; OR07/Nexstar/Year/Report1!A145 → 數值行145 |
| 意義候選 | 營業相關資產負債變動或其他CF調整；必須核實是變動而非餘額 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | BS時點餘額tag不適用此處流量；不以兩期餘額差代替完整CF調整，除非已核非現金與合併變動 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-017, ISS-066。 |

## OR01-Report1-A146

原始英文：`　　Other receivables`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行146；OR01/Nexstar/Quarter/Report1!A146 → 數值行146; OR02/Nexstar/Quarter/Report1!A146 → 數值行146; OR07/Nexstar/Year/Report1!A146 → 數值行146 |
| 意義候選 | 營業相關資產負債變動或其他CF調整；必須核實是變動而非餘額 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | BS時點餘額tag不適用此處流量；不以兩期餘額差代替完整CF調整，除非已核非現金與合併變動 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-018。 |

## OR01-Report1-A147

原始英文：`　　Decrease (Increase) In Other noncurrent assets`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行147；OR01/Nexstar/Quarter/Report1!A147 → 數值行147; OR02/Nexstar/Quarter/Report1!A147 → 數值行147; OR07/Nexstar/Year/Report1!A147 → 數值行147 |
| 意義候選 | 營業相關資產負債變動或其他CF調整；必須核實是變動而非餘額 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | BS時點餘額tag不適用此處流量；不以兩期餘額差代替完整CF調整，除非已核非現金與合併變動 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-019。 |

## OR01-Report1-A148

原始英文：`　　Prepayments`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行148；OR01/Nexstar/Quarter/Report1!A148 → 數值行148; OR02/Nexstar/Quarter/Report1!A148 → 數值行148; OR07/Nexstar/Year/Report1!A148 → 數值行148 |
| 意義候選 | 償還融資現金流；須逐項辨識本金、借款種類及費用 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 廣義還債tag不證明是該項特定借款；不等同debt service，亦不預設包含利息或融資租賃 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-020。 |

## OR01-Report1-A149

原始英文：`　　Increase (Decrease) In Accrued expenses and other current liabilities`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行149；OR01/Nexstar/Quarter/Report1!A149 → 數值行149; OR02/Nexstar/Quarter/Report1!A149 → 數值行149; OR07/Nexstar/Year/Report1!A149 → 數值行149 |
| 意義候選 | 營業相關資產負債變動或其他CF調整；必須核實是變動而非餘額 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | BS時點餘額tag不適用此處流量；不以兩期餘額差代替完整CF調整，除非已核非現金與合併變動 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-021。 |

## OR01-Report1-A150

原始英文：`　　Increase (Decrease) In Accounts Payable`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行150；OR01/Nexstar/Quarter/Report1!A150 → 數值行150; OR02/Nexstar/Quarter/Report1!A150 → 數值行150; OR07/Nexstar/Year/Report1!A150 → 數值行150 |
| 意義候選 | 營業相關資產負債變動或其他CF調整；必須核實是變動而非餘額 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | BS時點餘額tag不適用此處流量；不以兩期餘額差代替完整CF調整，除非已核非現金與合併變動 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-022。 |

## OR01-Report1-A151

原始英文：`　　Expense payable`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行151；OR01/Nexstar/Quarter/Report1!A151 → 數值行151; OR02/Nexstar/Quarter/Report1!A151 → 數值行151; OR07/Nexstar/Year/Report1!A151 → 數值行151 |
| 意義候選 | 營業相關資產負債變動或其他CF調整；必須核實是變動而非餘額 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | BS時點餘額tag不適用此處流量；不以兩期餘額差代替完整CF調整，除非已核非現金與合併變動 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-023。 |

## OR01-Report1-A152

原始英文：`　　Unearned receipts`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行152；OR01/Nexstar/Quarter/Report1!A152 → 數值行152; OR02/Nexstar/Quarter/Report1!A152 → 數值行152; OR07/Nexstar/Year/Report1!A152 → 數值行152 |
| 意義候選 | 營業相關資產負債變動或其他CF調整；必須核實是變動而非餘額 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | BS時點餘額tag不適用此處流量；不以兩期餘額差代替完整CF調整，除非已核非現金與合併變動 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-024。 |

## OR01-Report1-A153

原始英文：`　　Increase (Decrease) In Other noncurrent Liabilities`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行153；OR01/Nexstar/Quarter/Report1!A153 → 數值行153; OR02/Nexstar/Quarter/Report1!A153 → 數值行153; OR07/Nexstar/Year/Report1!A153 → 數值行153 |
| 意義候選 | 營業相關資產負債變動或其他CF調整；必須核實是變動而非餘額 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | BS時點餘額tag不適用此處流量；不以兩期餘額差代替完整CF調整，除非已核非現金與合併變動 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-025。 |

## OR01-Report1-A154

原始英文：`　　Income tax payable`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行154；OR01/Nexstar/Quarter/Report1!A154 → 數值行154; OR02/Nexstar/Quarter/Report1!A154 → 數值行154 |
| 意義候選 | 來源CF中的稅款支付、稅項變動或遞延稅調整，依原文確認 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | Income tax payable、Income tax paid及Deferred taxes不可互換；不能套用所得稅費用tag |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-026。 |

## OR01-Report1-A155

原始英文：`　　Interest paid`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行155；OR01/Nexstar/Quarter/Report1!A155 → 數值行155; OR02/Nexstar/Quarter/Report1!A155 → 數值行155; OR07/Nexstar/Year/Report1!A155 → 數值行155 |
| 意義候選 | 實際支付利息現金 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 不等同權責制利息費用或資本化利息 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A156

原始英文：`　　Interest received`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行156；OR01/Nexstar/Quarter/Report1!A156 → 數值行156; OR02/Nexstar/Quarter/Report1!A156 → 數值行156; OR07/Nexstar/Year/Report1!A156 → 數值行156 |
| 意義候選 | 來源所列股利／利息收入調整或實收現金，依活動位置確認 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 間接法沖回的收益與實收現金不可混用或重複計入 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A157

原始英文：`　　Dividends received`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行157；OR01/Nexstar/Quarter/Report1!A157 → 數值行157; OR02/Nexstar/Quarter/Report1!A157 → 數值行157; OR07/Nexstar/Year/Report1!A157 → 數值行157 |
| 意義候選 | 來源所列股利／利息收入調整或實收現金，依活動位置確認 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 間接法沖回的收益與實收現金不可混用或重複計入 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A158

原始英文：`　　Other`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行158；OR01/Nexstar/Quarter/Report1!A158 → 數值行158; OR02/Nexstar/Quarter/Report1!A158 → 數值行158; OR05/TransUnion/Quarter/Report1!A158 → 數值行158; OR06/TransUnion/Quarter/Report1!A158 → 數值行158; OR07/Nexstar/Year/Report1!A158 → 數值行158; OR08/XPO/Year/Report1!A158 → 數值行158; OR11/TransUnion/Year/Report1!A158 → 數值行158 |
| 意義候選 | 來源該活動分類的其他調整／流量；必須取得組成 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 不能作為現金不勾稽的補差欄或從其他公司挪用 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-027, ISS-055, ISS-064。 |

## OR01-Report1-A159

原始英文：`Net cash generated by (used in) operating activities`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行159；OR01/Nexstar/Quarter/Report1!A159 → 數值行159; OR02/Nexstar/Quarter/Report1!A159 → 數值行159; OR03/CROX/Quarter/Report1!A159 → 數值行159; OR04/Insulet/Quarter/Report1!A159 → 數值行159; OR05/TransUnion/Quarter/Report1!A159 → 數值行159; OR06/TransUnion/Quarter/Report1!A159 → 數值行159; OR07/Nexstar/Year/Report1!A159 → 數值行159; OR08/XPO/Year/Report1!A159 → 數值行159; OR09/CROX/Year/Report1!A159 → 數值行159; OR10/Insulet/Year/Report1!A159 → 數值行159; OR11/TransUnion/Year/Report1!A159 → 數值行159 |
| 意義候選 | 來源列示的營業活動淨現金流 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 該類活動全部淨流量 |
| 排除與不可替代項 | 不與明細再次加總；不混用總流入或總流出 |
| 既有代碼 | METRICS候選：cfo；raw候選：cfo。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | us-gaap:NetCashProvidedByUsedInOperatingActivities → raw.cfo |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A160

原始英文：`Cash Flow From Investing Activities`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行160；OR01/Nexstar/Quarter/Report1!A160 → 數值行160; OR02/Nexstar/Quarter/Report1!A160 → 數值行160; OR03/CROX/Quarter/Report1!A160 → 數值行160; OR04/Insulet/Quarter/Report1!A160 → 數值行160; OR05/TransUnion/Quarter/Report1!A160 → 數值行160; OR06/TransUnion/Quarter/Report1!A160 → 數值行160; OR07/Nexstar/Year/Report1!A160 → 數值行160; OR08/XPO/Year/Report1!A160 → 數值行160; OR09/CROX/Year/Report1!A160 → 數值行160; OR10/Insulet/Year/Report1!A160 → 數值行160; OR11/TransUnion/Year/Report1!A160 → 數值行160 |
| 意義候選 | 報表分組標題，不是可取數的金融事實 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 非數值標題／須核原文 |
| 排除與不可替代項 | 不搜尋或填入金額；不註冊metric |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 僅保留版面／分組；無取值、加總或公式；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=not_a_fact（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=not_a_fact；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A161

原始英文：`　　Financial assets - current`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行161；OR01/Nexstar/Quarter/Report1!A161 → 數值行161; OR02/Nexstar/Quarter/Report1!A161 → 數值行161; OR07/Nexstar/Year/Report1!A161 → 數值行161 |
| 意義候選 | 投資活動中金融／權益法／無形資產相關現金流；買入、出售或其他變動待核 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 不是BS時點餘額；原文只寫資產名稱時不得猜付款或收款方向 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-028。 |

## OR01-Report1-A162

原始英文：`　　Financial assets - non-current`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行162；OR01/Nexstar/Quarter/Report1!A162 → 數值行162; OR02/Nexstar/Quarter/Report1!A162 → 數值行162; OR07/Nexstar/Year/Report1!A162 → 數值行162 |
| 意義候選 | 投資活動中金融／權益法／無形資產相關現金流；買入、出售或其他變動待核 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 不是BS時點餘額；原文只寫資產名稱時不得猜付款或收款方向 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-029。 |

## OR01-Report1-A163

原始英文：`　　Investments accounted for using equity method`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行163；OR01/Nexstar/Quarter/Report1!A163 → 數值行163; OR02/Nexstar/Quarter/Report1!A163 → 數值行163; OR07/Nexstar/Year/Report1!A163 → 數值行163 |
| 意義候選 | 投資活動中金融／權益法／無形資產相關現金流；買入、出售或其他變動待核 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 不是BS時點餘額；原文只寫資產名稱時不得猜付款或收款方向 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-030。 |

## OR01-Report1-A164

原始英文：`　　Proceeds from disposals of property and equipment`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行164；OR01/Nexstar/Quarter/Report1!A164 → 數值行164; OR02/Nexstar/Quarter/Report1!A164 → 數值行164; OR07/Nexstar/Year/Report1!A164 → 數值行164 |
| 意義候選 | 資產／投資出售、到期或其他處分收款 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 借款流入、發股流入與資產出售收款不是同義；不使用同一行號跨公司取數 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-031。 |

## OR01-Report1-A165

原始英文：`　　Intangible assets`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行165；OR01/Nexstar/Quarter/Report1!A165 → 數值行165; OR02/Nexstar/Quarter/Report1!A165 → 數值行165; OR07/Nexstar/Year/Report1!A165 → 數值行165 |
| 意義候選 | 投資活動中金融／權益法／無形資產相關現金流；買入、出售或其他變動待核 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 不是BS時點餘額；原文只寫資產名稱時不得猜付款或收款方向 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-032。 |

## OR01-Report1-A166

原始英文：`　　Dviidends and interest received`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行166；OR01/Nexstar/Quarter/Report1!A166 → 數值行166; OR02/Nexstar/Quarter/Report1!A166 → 數值行166; OR07/Nexstar/Year/Report1!A166 → 數值行166 |
| 意義候選 | 來源所列股利／利息收入調整或實收現金，依活動位置確認 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 間接法沖回的收益與實收現金不可混用或重複計入 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A167

原始英文：`　　Purchases of property and equipment`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行167；OR01/Nexstar/Quarter/Report1!A167 → 數值行167; OR02/Nexstar/Quarter/Report1!A167 → 數值行167; OR07/Nexstar/Year/Report1!A167 → 數值行167 |
| 意義候選 | 購置資本資產付款 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 軟體、租賃或併購可能另列；不可把CapEx當作償還本金 |
| 既有代碼 | METRICS候選：無；raw候選：capex。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | us-gaap:PaymentsToAcquirePropertyPlantAndEquipment → raw.capex |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A168

原始英文：`　　Proceeds from sale of stations`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行168；OR01/Nexstar/Quarter/Report1!A168 → 數值行168; OR02/Nexstar/Quarter/Report1!A168 → 數值行168; OR07/Nexstar/Year/Report1!A168 → 數值行168 |
| 意義候選 | 資產／投資出售、到期或其他處分收款 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 借款流入、發股流入與資產出售收款不是同義；不使用同一行號跨公司取數 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A169

原始英文：`　　Payment for acquisition`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行169；OR01/Nexstar/Quarter/Report1!A169 → 數值行169; OR07/Nexstar/Year/Report1!A169 → 數值行169 |
| 意義候選 | 來源所列收購、資產取得或播映權付款 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 扣除取得現金與否、業務併購及資產購置須分開；不得套用全部CapEx |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-033, ISS-060。 |

## OR01-Report1-A170

原始英文：`　　Proceeds from disposal of an investment`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行170；OR01/Nexstar/Quarter/Report1!A170 → 數值行170; OR02/Nexstar/Quarter/Report1!A170 → 數值行170 |
| 意義候選 | 資產／投資出售、到期或其他處分收款 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 借款流入、發股流入與資產出售收款不是同義；不使用同一行號跨公司取數 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A171

原始英文：`　　Proceeds received from life insurance policies`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行171；OR01/Nexstar/Quarter/Report1!A171 → 數值行171 |
| 意義候選 | 來源CF原文所指之現金流或調整項，須逐項核附註 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 不只依名稱、行號或金額相同判定其經濟內容 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A172

原始英文：`　　Other`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行172；OR01/Nexstar/Quarter/Report1!A172 → 數值行172; OR02/Nexstar/Quarter/Report1!A172 → 數值行172; OR05/TransUnion/Quarter/Report1!A172 → 數值行172; OR06/TransUnion/Quarter/Report1!A172 → 數值行172; OR07/Nexstar/Year/Report1!A172 → 數值行172; OR08/XPO/Year/Report1!A172 → 數值行172; OR11/TransUnion/Year/Report1!A172 → 數值行172 |
| 意義候選 | 來源該活動分類的其他調整／流量；必須取得組成 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 不能作為現金不勾稽的補差欄或從其他公司挪用 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-034, ISS-055, ISS-064。 |

## OR01-Report1-A173

原始英文：`Net cash generated by (used in) investing activities`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行173；OR01/Nexstar/Quarter/Report1!A173 → 數值行173; OR02/Nexstar/Quarter/Report1!A173 → 數值行173; OR03/CROX/Quarter/Report1!A173 → 數值行173; OR04/Insulet/Quarter/Report1!A173 → 數值行173; OR05/TransUnion/Quarter/Report1!A173 → 數值行173; OR06/TransUnion/Quarter/Report1!A173 → 數值行173; OR07/Nexstar/Year/Report1!A173 → 數值行173; OR08/XPO/Year/Report1!A173 → 數值行173; OR09/CROX/Year/Report1!A173 → 數值行173; OR10/Insulet/Year/Report1!A173 → 數值行173; OR11/TransUnion/Year/Report1!A173 → 數值行173 |
| 意義候選 | 來源列示的投資活動淨現金流 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 該類活動全部淨流量 |
| 排除與不可替代項 | 不與明細再次加總；不混用總流入或總流出 |
| 既有代碼 | METRICS候選：cfi；raw候選：cfi。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | us-gaap:NetCashProvidedByUsedInInvestingActivities → raw.cfi |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A174

原始英文：`Cash flow from financing activities`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行174；OR01/Nexstar/Quarter/Report1!A174 → 數值行174; OR02/Nexstar/Quarter/Report1!A174 → 數值行174; OR03/CROX/Quarter/Report1!A174 → 數值行174; OR04/Insulet/Quarter/Report1!A174 → 數值行174; OR05/TransUnion/Quarter/Report1!A174 → 數值行174; OR06/TransUnion/Quarter/Report1!A174 → 數值行174; OR07/Nexstar/Year/Report1!A174 → 數值行174; OR08/XPO/Year/Report1!A174 → 數值行174; OR09/CROX/Year/Report1!A174 → 數值行174; OR10/Insulet/Year/Report1!A174 → 數值行174; OR11/TransUnion/Year/Report1!A174 → 數值行174 |
| 意義候選 | 報表分組標題，不是可取數的金融事實 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 非數值標題／須核原文 |
| 排除與不可替代項 | 不搜尋或填入金額；不註冊metric |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 僅保留版面／分組；無取值、加總或公式；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=not_a_fact（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=not_a_fact；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A175

原始英文：`　　Repayments of long-term debt`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行175；OR01/Nexstar/Quarter/Report1!A175 → 數值行175; OR02/Nexstar/Quarter/Report1!A175 → 數值行175; OR07/Nexstar/Year/Report1!A175 → 數值行175 |
| 意義候選 | 償還融資現金流；須逐項辨識本金、借款種類及費用 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 廣義還債tag不證明是該項特定借款；不等同debt service，亦不預設包含利息或融資租賃 |
| 既有代碼 | METRICS候選：無；raw候選：debt_repayment, debt_repayment_lt。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | us-gaap:RepaymentsOfDebt → raw.debt_repayment; us-gaap:RepaymentsOfLongTermDebt → raw.debt_repayment_lt |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-035。 |

## OR01-Report1-A176

原始英文：`　　Proceeds from long-term debt, including debt premium and discounts`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行176；OR01/Nexstar/Quarter/Report1!A176 → 數值行176; OR02/Nexstar/Quarter/Report1!A176 → 數值行176; OR07/Nexstar/Year/Report1!A176 → 數值行176 |
| 意義候選 | 原文所列交易之現金收款；須核交易種類 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 借款流入、發股流入與資產出售收款不是同義；不使用同一行號跨公司取數 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-036。 |

## OR01-Report1-A177

原始英文：`　　Payables-related parties`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行177；OR01/Nexstar/Quarter/Report1!A177 → 數值行177; OR02/Nexstar/Quarter/Report1!A177 → 數值行177; OR07/Nexstar/Year/Report1!A177 → 數值行177 |
| 意義候選 | 營業相關資產負債變動或其他CF調整；必須核實是變動而非餘額 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | BS時點餘額tag不適用此處流量；不以兩期餘額差代替完整CF調整，除非已核非現金與合併變動 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註；Related-party transactions／關係人交易附註；核對交易對手及合併沖銷 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-037。 |

## OR01-Report1-A178

原始英文：`　　Issuances of bonds payable`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行178；OR01/Nexstar/Quarter/Report1!A178 → 數值行178; OR02/Nexstar/Quarter/Report1!A178 → 數值行178; OR07/Nexstar/Year/Report1!A178 → 數值行178 |
| 意義候選 | 借款／發債取得之現金 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 借款流入、發股流入與資產出售收款不是同義；不使用同一行號跨公司取數 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-038。 |

## OR01-Report1-A179

原始英文：`　　Repayments of bonds payable`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行179；OR01/Nexstar/Quarter/Report1!A179 → 數值行179; OR02/Nexstar/Quarter/Report1!A179 → 數值行179; OR07/Nexstar/Year/Report1!A179 → 數值行179 |
| 意義候選 | 償還融資現金流；須逐項辨識本金、借款種類及費用 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 廣義還債tag不證明是該項特定借款；不等同debt service，亦不預設包含利息或融資租賃 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-039。 |

## OR01-Report1-A180

原始英文：`　　Payments for debt financing costs`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行180；OR01/Nexstar/Quarter/Report1!A180 → 數值行180; OR02/Nexstar/Quarter/Report1!A180 → 數值行180; OR07/Nexstar/Year/Report1!A180 → 數值行180 |
| 意義候選 | 支付或遞延處理的債務發行／融資成本 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 費用認列、實付現金與借款淨收款須區分；不可直接當償還本金 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-040。 |

## OR01-Report1-A181

原始英文：`　　Premium paid on debt extinguishment`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行181；OR01/Nexstar/Quarter/Report1!A181 → 數值行181; OR02/Nexstar/Quarter/Report1!A181 → 數值行181; OR07/Nexstar/Year/Report1!A181 → 數值行181 |
| 意義候選 | 來源CF原文所指之現金流或調整項，須逐項核附註 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 不只依名稱、行號或金額相同判定其經濟內容 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-041。 |

## OR01-Report1-A182

原始英文：`　　Common stock dividends paid`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行182；OR01/Nexstar/Quarter/Report1!A182 → 數值行182; OR02/Nexstar/Quarter/Report1!A182 → 數值行182; OR07/Nexstar/Year/Report1!A182 → 數值行182 |
| 意義候選 | 股利支付現金 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 不等同宣告股利、應付股利或收取股利 |
| 既有代碼 | METRICS候選：無；raw候選：dividends_paid。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | us-gaap:PaymentsOfDividendsCommonStock → raw.dividends_paid |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-042。 |

## OR01-Report1-A183

原始英文：`　　Purchase of treasury stock`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行183；OR01/Nexstar/Quarter/Report1!A183 → 數值行183; OR02/Nexstar/Quarter/Report1!A183 → 數值行183; OR07/Nexstar/Year/Report1!A183 → 數值行183 |
| 意義候選 | 股份買回相關付款，需辨識普通股、庫藏股或代扣稅 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 員工代扣稅款與普通股買回的涵蓋範圍須另核 |
| 既有代碼 | METRICS候選：無；raw候選：buybacks。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | us-gaap:PaymentsForRepurchaseOfCommonStock → raw.buybacks |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-043。 |

## OR01-Report1-A184

原始英文：`　　Cash paid for shares withheld for taxes`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行184；OR01/Nexstar/Quarter/Report1!A184 → 數值行184 |
| 意義候選 | 股權薪酬相關員工代扣稅款之付款 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 不是企業所得稅費用；與買回股份或融資費用的涵蓋範圍須核對 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-044。 |

## OR01-Report1-A188

原始英文：`　　Other`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行188；OR01/Nexstar/Quarter/Report1!A188 → 數值行188; OR02/Nexstar/Quarter/Report1!A188 → 數值行188; OR05/TransUnion/Quarter/Report1!A188 → 數值行188; OR06/TransUnion/Quarter/Report1!A188 → 數值行188; OR07/Nexstar/Year/Report1!A188 → 數值行188; OR08/XPO/Year/Report1!A188 → 數值行188; OR11/TransUnion/Year/Report1!A188 → 數值行188 |
| 意義候選 | 來源該活動分類的其他調整／流量；必須取得組成 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 不能作為現金不勾稽的補差欄或從其他公司挪用 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-045, ISS-055, ISS-064。 |

## OR01-Report1-A189

原始英文：`Net cash generated by (used in) financing activities`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行189；OR01/Nexstar/Quarter/Report1!A189 → 數值行189; OR02/Nexstar/Quarter/Report1!A189 → 數值行189; OR03/CROX/Quarter/Report1!A189 → 數值行189; OR04/Insulet/Quarter/Report1!A189 → 數值行189; OR05/TransUnion/Quarter/Report1!A189 → 數值行189; OR06/TransUnion/Quarter/Report1!A189 → 數值行189; OR07/Nexstar/Year/Report1!A189 → 數值行189; OR08/XPO/Year/Report1!A189 → 數值行189; OR09/CROX/Year/Report1!A189 → 數值行189; OR10/Insulet/Year/Report1!A189 → 數值行189; OR11/TransUnion/Year/Report1!A189 → 數值行189 |
| 意義候選 | 來源列示的籌資活動淨現金流 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 該類活動全部淨流量 |
| 排除與不可替代項 | 不與明細再次加總；不混用總流入或總流出 |
| 既有代碼 | METRICS候選：cff；raw候選：cff。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | us-gaap:NetCashProvidedByUsedInFinancingActivities → raw.cff |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A190

原始英文：`Effects Of Exchange Rate Variation`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行190；OR01/Nexstar/Quarter/Report1!A190 → 數值行190; OR02/Nexstar/Quarter/Report1!A190 → 數值行190; OR05/TransUnion/Quarter/Report1!A190 → 數值行190; OR06/TransUnion/Quarter/Report1!A190 → 數值行190; OR07/Nexstar/Year/Report1!A190 → 數值行190; OR08/XPO/Year/Report1!A190 → 數值行190; OR11/TransUnion/Year/Report1!A190 → 數值行190 |
| 意義候選 | 匯率變動對現金之影響或未實現兌換損益調整，須依位置與附註區別 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 影響現金餘額的匯率效果與非現金損益回加不是同一概念 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-046, ISS-063。 |

## OR01-Report1-A191

原始英文：`Net Cash Inflow (outflow) for current period`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行191；OR01/Nexstar/Quarter/Report1!A191 → 數值行191; OR02/Nexstar/Quarter/Report1!A191 → 數值行191; OR03/CROX/Quarter/Report1!A191 → 數值行191; OR04/Insulet/Quarter/Report1!A191 → 數值行191; OR05/TransUnion/Quarter/Report1!A191 → 數值行191; OR06/TransUnion/Quarter/Report1!A191 → 數值行191; OR07/Nexstar/Year/Report1!A191 → 數值行191; OR08/XPO/Year/Report1!A191 → 數值行191; OR09/CROX/Year/Report1!A191 → 數值行191; OR10/Insulet/Year/Report1!A191 → 數值行191; OR11/TransUnion/Year/Report1!A191 → 數值行191 |
| 意義候選 | 來源稱本期現金淨變動；FX及停業單位是否包含須核對 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 已核實完整現金定義之變動 |
| 排除與不可替代項 | 不自動將此行當成ending-beginning；不預設僅含三類活動 |
| 既有代碼 | METRICS候選：cash_change；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | ending_cash: us-gaap:CashAndCashEquivalentsAtCarryingValue; beginning_cash: us-gaap:CashAndCashEquivalentsAtCarryingValue |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：DER-08, DER-10。 |
| 核准公式／推導條件引用 | DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。；DER-10: 同口徑 Ending Cash − Beginning Cash。另以 DER-08 核對橋接；不可直接將 CFO＋CFI＋CFF 視為所有情況下的完整變動。 |
| 必要輸入與版本 | ending_cash, beginning_cash；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A194

原始英文：`Cash and cash equivalents - end of period`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行194；OR01/Nexstar/Quarter/Report1!A194 → 數值行194; OR02/Nexstar/Quarter/Report1!A194 → 數值行194; OR03/CROX/Quarter/Report1!A194 → 數值行194; OR04/Insulet/Quarter/Report1!A194 → 數值行194; OR05/TransUnion/Quarter/Report1!A194 → 數值行194; OR06/TransUnion/Quarter/Report1!A194 → 數值行194; OR07/Nexstar/Year/Report1!A194 → 數值行194; OR08/XPO/Year/Report1!A194 → 數值行194; OR09/CROX/Year/Report1!A194 → 數值行194; OR10/Insulet/Year/Report1!A194 → 數值行194; OR11/TransUnion/Year/Report1!A194 → 數值行194 |
| 意義候選 | 期末現金；須核對是否含受限制現金 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源CF期末餘額及現金附註 |
| 排除與不可替代項 | BS Cash tag只是候選；不以不完整橋接覆寫直接揭露 |
| 既有代碼 | METRICS候選：ending_cash；raw候選：cash。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | us-gaap:CashAndCashEquivalentsAtCarryingValue → raw.cash |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：DER-08, DER-10。 |
| 核准公式／推導條件引用 | DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。；DER-10: 同口徑 Ending Cash − Beginning Cash。另以 DER-08 核對橋接；不可直接將 CFO＋CFI＋CFF 視為所有情況下的完整變動。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=instant；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A196

原始英文：`Liquidity`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | RATIO 名稱行196；OR01/Nexstar/Quarter/Report1!A196 → 數值行196; OR02/Nexstar/Quarter/Report1!A196 → 數值行196; OR03/CROX/Quarter/Report1!A196 → 數值行196; OR04/Insulet/Quarter/Report1!A196 → 數值行196; OR05/TransUnion/Quarter/Report1!A196 → 數值行196; OR06/TransUnion/Quarter/Report1!A196 → 數值行196; OR07/Nexstar/Year/Report1!A196 → 數值行196; OR08/XPO/Year/Report1!A196 → 數值行196; OR09/CROX/Year/Report1!A196 → 數值行196; OR10/Insulet/Year/Report1!A196 → 數值行196; OR11/TransUnion/Year/Report1!A196 → 數值行196 |
| 意義候選 | 報表分組標題，不是可取數的金融事實 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 非數值標題／須核原文 |
| 排除與不可替代項 | 不搜尋或填入金額；不註冊metric |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | 核准公式的各輸入所屬主表／附註；管理層或貸款文件比率僅作定義與比對證據 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 僅保留版面／分組；無取值、加總或公式；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=not_a_fact（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=not_a_fact；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A197

原始英文：`Current Ratio`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | RATIO 名稱行197；OR01/Nexstar/Quarter/Report1!A197 → 數值行197; OR02/Nexstar/Quarter/Report1!A197 → 數值行197; OR03/CROX/Quarter/Report1!A197 → 數值行197; OR04/Insulet/Quarter/Report1!A197 → 數值行197; OR05/TransUnion/Quarter/Report1!A197 → 數值行197; OR06/TransUnion/Quarter/Report1!A197 → 數值行197; OR07/Nexstar/Year/Report1!A197 → 數值行197; OR08/XPO/Year/Report1!A197 → 數值行197; OR09/CROX/Year/Report1!A197 → 數值行197; OR10/Insulet/Year/Report1!A197 → 數值行197; OR11/TransUnion/Year/Report1!A197 → 數值行197 |
| 意義候選 | 已核准公式所定義的Current Ratio |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅核准公式所需且同口徑之輸入 |
| 排除與不可替代項 | 來源公布比率只是比對資料；不得反推缺失分子／分母 |
| 既有代碼 | METRICS候選：current_ratio；raw候選：無。兩者不可互換。 |
| SEC查找位置 | 核准公式的各輸入所屬主表／附註；管理層或貸款文件比率僅作定義與比對證據 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | current_assets: us-gaap:AssetsCurrent; current_liabilities: us-gaap:LiabilitiesCurrent |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源階段保留輸入候選及原比率證據，輸出仍為not_calculable；後續計算階段才以核准公式產生calculated；規則：CF-01。 |
| 核准公式／推導條件引用 | CF-01: Current Assets / Current Liabilities |
| 必要輸入與版本 | current_assets, current_liabilities；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=percent（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=mixed_formula_inputs；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A198

原始英文：`Quick Ratio`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | RATIO 名稱行198；OR01/Nexstar/Quarter/Report1!A198 → 數值行198; OR02/Nexstar/Quarter/Report1!A198 → 數值行198; OR03/CROX/Quarter/Report1!A198 → 數值行198; OR04/Insulet/Quarter/Report1!A198 → 數值行198; OR05/TransUnion/Quarter/Report1!A198 → 數值行198; OR06/TransUnion/Quarter/Report1!A198 → 數值行198; OR07/Nexstar/Year/Report1!A198 → 數值行198; OR08/XPO/Year/Report1!A198 → 數值行198; OR09/CROX/Year/Report1!A198 → 數值行198; OR10/Insulet/Year/Report1!A198 → 數值行198; OR11/TransUnion/Year/Report1!A198 → 數值行198 |
| 意義候選 | 已核准公式所定義的Quick Ratio |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅核准公式所需且同口徑之輸入 |
| 排除與不可替代項 | 來源公布比率只是比對資料；不得反推缺失分子／分母 |
| 既有代碼 | METRICS候選：quick_ratio；raw候選：無。兩者不可互換。 |
| SEC查找位置 | 核准公式的各輸入所屬主表／附註；管理層或貸款文件比率僅作定義與比對證據 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | quick_assets: 現有來源層無已登錄對應，須核定／補查; current_liabilities: us-gaap:LiabilitiesCurrent |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源階段保留輸入候選及原比率證據，輸出仍為not_calculable；後續計算階段才以核准公式產生calculated；規則：CF-02。 |
| 核准公式／推導條件引用 | CF-02: Quick Assets / Current Liabilities |
| 必要輸入與版本 | quick_assets, current_liabilities；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=percent（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=mixed_formula_inputs；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | DEC-01；另見全部84項盤點待確認清單。 |

## OR01-Report1-A199

原始英文：`Cash Flow Ratio`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | RATIO 名稱行199；OR01/Nexstar/Quarter/Report1!A199 → 數值行199; OR02/Nexstar/Quarter/Report1!A199 → 數值行199; OR03/CROX/Quarter/Report1!A199 → 數值行199; OR04/Insulet/Quarter/Report1!A199 → 數值行199; OR05/TransUnion/Quarter/Report1!A199 → 數值行199; OR06/TransUnion/Quarter/Report1!A199 → 數值行199; OR07/Nexstar/Year/Report1!A199 → 數值行199; OR08/XPO/Year/Report1!A199 → 數值行199; OR09/CROX/Year/Report1!A199 → 數值行199; OR10/Insulet/Year/Report1!A199 → 數值行199; OR11/TransUnion/Year/Report1!A199 → 數值行199 |
| 意義候選 | 已核准公式所定義的Cash Flow Ratio |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅核准公式所需且同口徑之輸入 |
| 排除與不可替代項 | 來源公布比率只是比對資料；不得反推缺失分子／分母 |
| 既有代碼 | METRICS候選：cash_flow_ratio；raw候選：無。兩者不可互換。 |
| SEC查找位置 | 核准公式的各輸入所屬主表／附註；管理層或貸款文件比率僅作定義與比對證據 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | cfo: us-gaap:NetCashProvidedByUsedInOperatingActivities; current_liabilities: us-gaap:LiabilitiesCurrent |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源階段保留輸入候選及原比率證據，輸出仍為not_calculable；後續計算階段才以核准公式產生calculated；規則：CF-03。 |
| 核准公式／推導條件引用 | CF-03: Net Cash Inflow (Outflow) From Operating Activities / Current Liabilities |
| 必要輸入與版本 | cfo, current_liabilities；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=percent（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=mixed_formula_inputs；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A200

原始英文：`Interest Coverage Ratio`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | RATIO 名稱行200；OR01/Nexstar/Quarter/Report1!A200 → 數值行200; OR02/Nexstar/Quarter/Report1!A200 → 數值行200; OR03/CROX/Quarter/Report1!A200 → 數值行200; OR04/Insulet/Quarter/Report1!A200 → 數值行200; OR05/TransUnion/Quarter/Report1!A200 → 數值行200; OR06/TransUnion/Quarter/Report1!A200 → 數值行200; OR07/Nexstar/Year/Report1!A200 → 數值行200; OR08/XPO/Year/Report1!A200 → 數值行200; OR09/CROX/Year/Report1!A200 → 數值行200; OR10/Insulet/Year/Report1!A200 → 數值行200; OR11/TransUnion/Year/Report1!A200 → 數值行200 |
| 意義候選 | 已核准公式所定義的Interest Coverage Ratio |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅核准公式所需且同口徑之輸入 |
| 排除與不可替代項 | 來源公布比率只是比對資料；不得反推缺失分子／分母 |
| 既有代碼 | METRICS候選：interest_coverage；raw候選：無。兩者不可互換。 |
| SEC查找位置 | 核准公式的各輸入所屬主表／附註；管理層或貸款文件比率僅作定義與比對證據；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | pretax_profit: us-gaap:IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest; interest_expense: us-gaap:InterestExpense, us-gaap:InterestExpenseNonoperating; capitalized_interest: us-gaap:InterestCostsCapitalized |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源階段保留輸入候選及原比率證據，輸出仍為not_calculable；後續計算階段才以核准公式產生calculated；規則：CF-04。 |
| 核准公式／推導條件引用 | CF-04: (Pre-tax Profit + Interest Expense) / (Interest Expense + Capitalized Interest) |
| 必要輸入與版本 | pretax_profit, interest_expense, capitalized_interest；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=multiple（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=mixed_formula_inputs；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | DEC-05；另見全部84項盤點待確認清單。 |

## OR01-Report1-A201

原始英文：`EBITDA / Interest Expenses`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | RATIO 名稱行201；OR01/Nexstar/Quarter/Report1!A201 → 數值行201; OR02/Nexstar/Quarter/Report1!A201 → 數值行201; OR03/CROX/Quarter/Report1!A201 → 數值行201; OR04/Insulet/Quarter/Report1!A201 → 數值行201; OR05/TransUnion/Quarter/Report1!A201 → 數值行201; OR06/TransUnion/Quarter/Report1!A201 → 數值行201; OR07/Nexstar/Year/Report1!A201 → 數值行201; OR08/XPO/Year/Report1!A201 → 數值行201; OR09/CROX/Year/Report1!A201 → 數值行201; OR10/Insulet/Year/Report1!A201 → 數值行201; OR11/TransUnion/Year/Report1!A201 → 數值行201 |
| 意義候選 | 已核准公式所定義的EBITDA / Interest Expenses |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅核准公式所需且同口徑之輸入 |
| 排除與不可替代項 | 來源公布比率只是比對資料；不得反推缺失分子／分母 |
| 既有代碼 | METRICS候選：ebitda_interest；raw候選：無。兩者不可互換。 |
| SEC查找位置 | 核准公式的各輸入所屬主表／附註；管理層或貸款文件比率僅作定義與比對證據；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | pretax_profit: us-gaap:IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest; interest_expense: us-gaap:InterestExpense, us-gaap:InterestExpenseNonoperating; da: us-gaap:DepreciationDepletionAndAmortization; capitalized_interest: us-gaap:InterestCostsCapitalized |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源階段保留輸入候選及原比率證據，輸出仍為not_calculable；後續計算階段才以核准公式產生calculated；規則：CF-05。 |
| 核准公式／推導條件引用 | CF-05: (Pre-tax Profit + Interest Expense + Depreciation & Amortization) / (Interest Expense + Capitalized Interest) |
| 必要輸入與版本 | pretax_profit, interest_expense, da, capitalized_interest；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=multiple（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=mixed_formula_inputs；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | DEC-05；另見全部84項盤點待確認清單。 |

## OR01-Report1-A202

原始英文：`Financial Structure`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | RATIO 名稱行202；OR01/Nexstar/Quarter/Report1!A202 → 數值行202; OR02/Nexstar/Quarter/Report1!A202 → 數值行202; OR03/CROX/Quarter/Report1!A202 → 數值行202; OR04/Insulet/Quarter/Report1!A202 → 數值行202; OR05/TransUnion/Quarter/Report1!A202 → 數值行202; OR06/TransUnion/Quarter/Report1!A202 → 數值行202; OR07/Nexstar/Year/Report1!A202 → 數值行202; OR08/XPO/Year/Report1!A202 → 數值行202; OR09/CROX/Year/Report1!A202 → 數值行202; OR10/Insulet/Year/Report1!A202 → 數值行202; OR11/TransUnion/Year/Report1!A202 → 數值行202 |
| 意義候選 | 報表分組標題，不是可取數的金融事實 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 非數值標題／須核原文 |
| 排除與不可替代項 | 不搜尋或填入金額；不註冊metric |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | 核准公式的各輸入所屬主表／附註；管理層或貸款文件比率僅作定義與比對證據 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 僅保留版面／分組；無取值、加總或公式；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=not_a_fact（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=not_a_fact；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A203

原始英文：`Debt Ratio`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | RATIO 名稱行203；OR01/Nexstar/Quarter/Report1!A203 → 數值行203; OR02/Nexstar/Quarter/Report1!A203 → 數值行203; OR03/CROX/Quarter/Report1!A203 → 數值行203; OR04/Insulet/Quarter/Report1!A203 → 數值行203; OR05/TransUnion/Quarter/Report1!A203 → 數值行203; OR06/TransUnion/Quarter/Report1!A203 → 數值行203; OR07/Nexstar/Year/Report1!A203 → 數值行203; OR08/XPO/Year/Report1!A203 → 數值行203; OR09/CROX/Year/Report1!A203 → 數值行203; OR10/Insulet/Year/Report1!A203 → 數值行203; OR11/TransUnion/Year/Report1!A203 → 數值行203 |
| 意義候選 | 已核准公式所定義的Debt Ratio |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅核准公式所需且同口徑之輸入 |
| 排除與不可替代項 | 來源公布比率只是比對資料；不得反推缺失分子／分母 |
| 既有代碼 | METRICS候選：debt_ratio；raw候選：無。兩者不可互換。 |
| SEC查找位置 | 核准公式的各輸入所屬主表／附註；管理層或貸款文件比率僅作定義與比對證據；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | total_liabilities: us-gaap:Liabilities; net_worth: 現有來源層無已登錄對應，須核定／補查 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源階段保留輸入候選及原比率證據，輸出仍為not_calculable；後續計算階段才以核准公式產生calculated；規則：CF-06。 |
| 核准公式／推導條件引用 | CF-06: Total Liabilities / Net Worth |
| 必要輸入與版本 | total_liabilities, net_worth；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=percent（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=mixed_formula_inputs；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | DEC-02；另見全部84項盤點待確認清單。 |

## OR01-Report1-A204

原始英文：`Fixed Asset To Net Worth Ratio`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | RATIO 名稱行204；OR01/Nexstar/Quarter/Report1!A204 → 數值行204; OR02/Nexstar/Quarter/Report1!A204 → 數值行204; OR03/CROX/Quarter/Report1!A204 → 數值行204; OR04/Insulet/Quarter/Report1!A204 → 數值行204; OR05/TransUnion/Quarter/Report1!A204 → 數值行204; OR06/TransUnion/Quarter/Report1!A204 → 數值行204; OR07/Nexstar/Year/Report1!A204 → 數值行204; OR08/XPO/Year/Report1!A204 → 數值行204; OR09/CROX/Year/Report1!A204 → 數值行204; OR10/Insulet/Year/Report1!A204 → 數值行204; OR11/TransUnion/Year/Report1!A204 → 數值行204 |
| 意義候選 | 已核准公式所定義的Fixed Asset To Net Worth Ratio |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅核准公式所需且同口徑之輸入 |
| 排除與不可替代項 | 來源公布比率只是比對資料；不得反推缺失分子／分母 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | 核准公式的各輸入所屬主表／附註；管理層或貸款文件比率僅作定義與比對證據 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源階段保留輸入候選及原比率證據，輸出仍為not_calculable；後續計算階段才以核准公式產生calculated；規則：CF-07。 |
| 核准公式／推導條件引用 | CF-07: Fixed Assets / Net Worth |
| 必要輸入與版本 | Fixed Assets, Net Worth；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=percent（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=mixed_formula_inputs；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | DEC-02；另見全部84項盤點待確認清單。 |

## OR01-Report1-A205

原始英文：`Fixed Assets To Long Term Capital Ratio`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | RATIO 名稱行205；OR01/Nexstar/Quarter/Report1!A205 → 數值行205; OR02/Nexstar/Quarter/Report1!A205 → 數值行205; OR03/CROX/Quarter/Report1!A205 → 數值行205; OR04/Insulet/Quarter/Report1!A205 → 數值行205; OR05/TransUnion/Quarter/Report1!A205 → 數值行205; OR06/TransUnion/Quarter/Report1!A205 → 數值行205; OR07/Nexstar/Year/Report1!A205 → 數值行205; OR08/XPO/Year/Report1!A205 → 數值行205; OR09/CROX/Year/Report1!A205 → 數值行205; OR10/Insulet/Year/Report1!A205 → 數值行205; OR11/TransUnion/Year/Report1!A205 → 數值行205 |
| 意義候選 | 已核准公式所定義的Fixed Assets To Long Term Capital Ratio |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅核准公式所需且同口徑之輸入 |
| 排除與不可替代項 | 來源公布比率只是比對資料；不得反推缺失分子／分母 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | 核准公式的各輸入所屬主表／附註；管理層或貸款文件比率僅作定義與比對證據 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源階段保留輸入候選及原比率證據，輸出仍為not_calculable；後續計算階段才以核准公式產生calculated；規則：CF-08。 |
| 核准公式／推導條件引用 | CF-08: (Fixed Assets + Funds & Investments) / (Net Worth + Long Term Liabilities) |
| 必要輸入與版本 | Fixed Assets, Funds & Investments, Net Worth, Long Term Liabilities；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=percent（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=mixed_formula_inputs；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | DEC-02；另見全部84項盤點待確認清單。 |

## OR01-Report1-A206

原始英文：`Profitability`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | RATIO 名稱行206；OR01/Nexstar/Quarter/Report1!A206 → 數值行206; OR02/Nexstar/Quarter/Report1!A206 → 數值行206; OR03/CROX/Quarter/Report1!A206 → 數值行206; OR04/Insulet/Quarter/Report1!A206 → 數值行206; OR05/TransUnion/Quarter/Report1!A206 → 數值行206; OR06/TransUnion/Quarter/Report1!A206 → 數值行206; OR07/Nexstar/Year/Report1!A206 → 數值行206; OR08/XPO/Year/Report1!A206 → 數值行206; OR09/CROX/Year/Report1!A206 → 數值行206; OR10/Insulet/Year/Report1!A206 → 數值行206; OR11/TransUnion/Year/Report1!A206 → 數值行206 |
| 意義候選 | 報表分組標題，不是可取數的金融事實 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 非數值標題／須核原文 |
| 排除與不可替代項 | 不搜尋或填入金額；不註冊metric |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | 核准公式的各輸入所屬主表／附註；管理層或貸款文件比率僅作定義與比對證據 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 僅保留版面／分組；無取值、加總或公式；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=not_a_fact（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=not_a_fact；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A207

原始英文：`Revenue Growth Rate`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | RATIO 名稱行207；OR01/Nexstar/Quarter/Report1!A207 → 數值行207; OR02/Nexstar/Quarter/Report1!A207 → 數值行207; OR03/CROX/Quarter/Report1!A207 → 數值行207; OR04/Insulet/Quarter/Report1!A207 → 數值行207; OR05/TransUnion/Quarter/Report1!A207 → 數值行207; OR06/TransUnion/Quarter/Report1!A207 → 數值行207; OR07/Nexstar/Year/Report1!A207 → 數值行207; OR08/XPO/Year/Report1!A207 → 數值行207; OR09/CROX/Year/Report1!A207 → 數值行207; OR10/Insulet/Year/Report1!A207 → 數值行207; OR11/TransUnion/Year/Report1!A207 → 數值行207 |
| 意義候選 | 已核准公式所定義的Revenue Growth Rate |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅核准公式所需且同口徑之輸入 |
| 排除與不可替代項 | 來源公布比率只是比對資料；不得反推缺失分子／分母 |
| 既有代碼 | METRICS候選：revenue_growth；raw候選：無。兩者不可互換。 |
| SEC查找位置 | 核准公式的各輸入所屬主表／附註；管理層或貸款文件比率僅作定義與比對證據 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | revenue: us-gaap:Revenues, us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源階段保留輸入候選及原比率證據，輸出仍為not_calculable；後續計算階段才以核准公式產生calculated；規則：CF-09。 |
| 核准公式／推導條件引用 | CF-09: (Current Year Revenues − Previous Year Revenues) / Previous Year Revenues |
| 必要輸入與版本 | revenue, revenue；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=percent（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=mixed_formula_inputs；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A208

原始英文：`Gross Profit Margin`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | RATIO 名稱行208；OR01/Nexstar/Quarter/Report1!A208 → 數值行208; OR02/Nexstar/Quarter/Report1!A208 → 數值行208; OR03/CROX/Quarter/Report1!A208 → 數值行208; OR04/Insulet/Quarter/Report1!A208 → 數值行208; OR05/TransUnion/Quarter/Report1!A208 → 數值行208; OR06/TransUnion/Quarter/Report1!A208 → 數值行208; OR07/Nexstar/Year/Report1!A208 → 數值行208; OR08/XPO/Year/Report1!A208 → 數值行208; OR09/CROX/Year/Report1!A208 → 數值行208; OR10/Insulet/Year/Report1!A208 → 數值行208; OR11/TransUnion/Year/Report1!A208 → 數值行208 |
| 意義候選 | 已核准公式所定義的Gross Profit Margin |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅核准公式所需且同口徑之輸入 |
| 排除與不可替代項 | 來源公布比率只是比對資料；不得反推缺失分子／分母 |
| 既有代碼 | METRICS候選：gross_margin；raw候選：無。兩者不可互換。 |
| SEC查找位置 | 核准公式的各輸入所屬主表／附註；管理層或貸款文件比率僅作定義與比對證據 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | gross_profit: us-gaap:GrossProfit; revenue: us-gaap:Revenues, us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源階段保留輸入候選及原比率證據，輸出仍為not_calculable；後續計算階段才以核准公式產生calculated；規則：CF-10。 |
| 核准公式／推導條件引用 | CF-10: Gross Profit / Revenues |
| 必要輸入與版本 | gross_profit, revenue；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=percent（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=mixed_formula_inputs；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A209

原始英文：`Operating Profit Margin`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | RATIO 名稱行209；OR01/Nexstar/Quarter/Report1!A209 → 數值行209; OR02/Nexstar/Quarter/Report1!A209 → 數值行209; OR03/CROX/Quarter/Report1!A209 → 數值行209; OR04/Insulet/Quarter/Report1!A209 → 數值行209; OR05/TransUnion/Quarter/Report1!A209 → 數值行209; OR06/TransUnion/Quarter/Report1!A209 → 數值行209; OR07/Nexstar/Year/Report1!A209 → 數值行209; OR08/XPO/Year/Report1!A209 → 數值行209; OR09/CROX/Year/Report1!A209 → 數值行209; OR10/Insulet/Year/Report1!A209 → 數值行209; OR11/TransUnion/Year/Report1!A209 → 數值行209 |
| 意義候選 | 已核准公式所定義的Operating Profit Margin |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅核准公式所需且同口徑之輸入 |
| 排除與不可替代項 | 來源公布比率只是比對資料；不得反推缺失分子／分母 |
| 既有代碼 | METRICS候選：operating_margin；raw候選：無。兩者不可互換。 |
| SEC查找位置 | 核准公式的各輸入所屬主表／附註；管理層或貸款文件比率僅作定義與比對證據 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | operating_income: us-gaap:OperatingIncomeLoss; revenue: us-gaap:Revenues, us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源階段保留輸入候選及原比率證據，輸出仍為not_calculable；後續計算階段才以核准公式產生calculated；規則：CF-11。 |
| 核准公式／推導條件引用 | CF-11: Operating Profit / Revenues |
| 必要輸入與版本 | operating_income, revenue；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=percent（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=mixed_formula_inputs；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A210

原始英文：`Pre-tax Profit Margin`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | RATIO 名稱行210；OR01/Nexstar/Quarter/Report1!A210 → 數值行210; OR02/Nexstar/Quarter/Report1!A210 → 數值行210; OR03/CROX/Quarter/Report1!A210 → 數值行210; OR04/Insulet/Quarter/Report1!A210 → 數值行210; OR05/TransUnion/Quarter/Report1!A210 → 數值行210; OR06/TransUnion/Quarter/Report1!A210 → 數值行210; OR07/Nexstar/Year/Report1!A210 → 數值行210; OR08/XPO/Year/Report1!A210 → 數值行210; OR09/CROX/Year/Report1!A210 → 數值行210; OR10/Insulet/Year/Report1!A210 → 數值行210; OR11/TransUnion/Year/Report1!A210 → 數值行210 |
| 意義候選 | 已核准公式所定義的Pre-tax Profit Margin |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅核准公式所需且同口徑之輸入 |
| 排除與不可替代項 | 來源公布比率只是比對資料；不得反推缺失分子／分母 |
| 既有代碼 | METRICS候選：pretax_margin；raw候選：無。兩者不可互換。 |
| SEC查找位置 | 核准公式的各輸入所屬主表／附註；管理層或貸款文件比率僅作定義與比對證據；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | pretax_profit: us-gaap:IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest; revenue: us-gaap:Revenues, us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源階段保留輸入候選及原比率證據，輸出仍為not_calculable；後續計算階段才以核准公式產生calculated；規則：CF-12。 |
| 核准公式／推導條件引用 | CF-12: Pre-tax Profit / Revenues |
| 必要輸入與版本 | pretax_profit, revenue；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=percent（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=mixed_formula_inputs；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A211

原始英文：`Return On Net Worth`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | RATIO 名稱行211；OR01/Nexstar/Quarter/Report1!A211 → 數值行211; OR02/Nexstar/Quarter/Report1!A211 → 數值行211; OR03/CROX/Quarter/Report1!A211 → 數值行211; OR04/Insulet/Quarter/Report1!A211 → 數值行211; OR05/TransUnion/Quarter/Report1!A211 → 數值行211; OR06/TransUnion/Quarter/Report1!A211 → 數值行211; OR07/Nexstar/Year/Report1!A211 → 數值行211; OR08/XPO/Year/Report1!A211 → 數值行211; OR09/CROX/Year/Report1!A211 → 數值行211; OR10/Insulet/Year/Report1!A211 → 數值行211; OR11/TransUnion/Year/Report1!A211 → 數值行211 |
| 意義候選 | 已核准公式所定義的Return On Net Worth |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅核准公式所需且同口徑之輸入 |
| 排除與不可替代項 | 來源公布比率只是比對資料；不得反推缺失分子／分母 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | 核准公式的各輸入所屬主表／附註；管理層或貸款文件比率僅作定義與比對證據 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源階段保留輸入候選及原比率證據，輸出仍為not_calculable；後續計算階段才以核准公式產生calculated；規則：CF-13。 |
| 核准公式／推導條件引用 | CF-13: ((Pre-tax Profit / Months) × 12) / Average Net Worth |
| 必要輸入與版本 | Pre-tax Profit, verified Months, Average Net Worth；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=percent（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=mixed_formula_inputs；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | DEC-02, DEC-04；另見全部84項盤點待確認清單。 |

## OR01-Report1-A212

原始英文：`Return On Asset`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | RATIO 名稱行212；OR01/Nexstar/Quarter/Report1!A212 → 數值行212; OR02/Nexstar/Quarter/Report1!A212 → 數值行212; OR03/CROX/Quarter/Report1!A212 → 數值行212; OR04/Insulet/Quarter/Report1!A212 → 數值行212; OR05/TransUnion/Quarter/Report1!A212 → 數值行212; OR06/TransUnion/Quarter/Report1!A212 → 數值行212; OR07/Nexstar/Year/Report1!A212 → 數值行212; OR08/XPO/Year/Report1!A212 → 數值行212; OR09/CROX/Year/Report1!A212 → 數值行212; OR10/Insulet/Year/Report1!A212 → 數值行212; OR11/TransUnion/Year/Report1!A212 → 數值行212 |
| 意義候選 | 已核准公式所定義的Return On Asset |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅核准公式所需且同口徑之輸入 |
| 排除與不可替代項 | 來源公布比率只是比對資料；不得反推缺失分子／分母 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | 核准公式的各輸入所屬主表／附註；管理層或貸款文件比率僅作定義與比對證據 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源階段保留輸入候選及原比率證據，輸出仍為not_calculable；後續計算階段才以核准公式產生calculated；規則：CF-14。 |
| 核准公式／推導條件引用 | CF-14: ((Pre-tax Profit / Months) × 12) / Average Total Assets |
| 必要輸入與版本 | Pre-tax Profit, verified Months, Average Total Assets；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=percent（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=mixed_formula_inputs；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | DEC-04；另見全部84項盤點待確認清單。 |

## OR01-Report1-A213

原始英文：`Financial Expense Ratio`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | RATIO 名稱行213；OR01/Nexstar/Quarter/Report1!A213 → 數值行213; OR02/Nexstar/Quarter/Report1!A213 → 數值行213; OR03/CROX/Quarter/Report1!A213 → 數值行213; OR04/Insulet/Quarter/Report1!A213 → 數值行213; OR05/TransUnion/Quarter/Report1!A213 → 數值行213; OR06/TransUnion/Quarter/Report1!A213 → 數值行213; OR07/Nexstar/Year/Report1!A213 → 數值行213; OR08/XPO/Year/Report1!A213 → 數值行213; OR09/CROX/Year/Report1!A213 → 數值行213; OR10/Insulet/Year/Report1!A213 → 數值行213; OR11/TransUnion/Year/Report1!A213 → 數值行213 |
| 意義候選 | 已核准公式所定義的Financial Expense Ratio |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅核准公式所需且同口徑之輸入 |
| 排除與不可替代項 | 來源公布比率只是比對資料；不得反推缺失分子／分母 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | 核准公式的各輸入所屬主表／附註；管理層或貸款文件比率僅作定義與比對證據 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源階段保留輸入候選及原比率證據，輸出仍為not_calculable；後續計算階段才以核准公式產生calculated；規則：CF-15。 |
| 核准公式／推導條件引用 | CF-15: Interest Expense / Revenues |
| 必要輸入與版本 | Interest Expense, Revenues；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=percent（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=mixed_formula_inputs；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A214

原始英文：`Change In Operating Profit Margin`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | RATIO 名稱行214；OR01/Nexstar/Quarter/Report1!A214 → 數值行214; OR02/Nexstar/Quarter/Report1!A214 → 數值行214; OR03/CROX/Quarter/Report1!A214 → 數值行214; OR04/Insulet/Quarter/Report1!A214 → 數值行214; OR05/TransUnion/Quarter/Report1!A214 → 數值行214; OR06/TransUnion/Quarter/Report1!A214 → 數值行214; OR07/Nexstar/Year/Report1!A214 → 數值行214; OR08/XPO/Year/Report1!A214 → 數值行214; OR09/CROX/Year/Report1!A214 → 數值行214; OR10/Insulet/Year/Report1!A214 → 數值行214; OR11/TransUnion/Year/Report1!A214 → 數值行214 |
| 意義候選 | 已核准公式所定義的Change In Operating Profit Margin |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅核准公式所需且同口徑之輸入 |
| 排除與不可替代項 | 來源公布比率只是比對資料；不得反推缺失分子／分母 |
| 既有代碼 | METRICS候選：operating_margin_change；raw候選：無。兩者不可互換。 |
| SEC查找位置 | 核准公式的各輸入所屬主表／附註；管理層或貸款文件比率僅作定義與比對證據 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | operating_margin: 現有來源層無已登錄對應，須核定／補查 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源階段保留輸入候選及原比率證據，輸出仍為not_calculable；後續計算階段才以核准公式產生calculated；規則：CF-16。 |
| 核准公式／推導條件引用 | CF-16: Current Operating Profit Margin − Previous Operating Profit Margin |
| 必要輸入與版本 | operating_margin, operating_margin；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=percentage_points（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=mixed_formula_inputs；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A215

原始英文：`Business Management`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | RATIO 名稱行215；OR01/Nexstar/Quarter/Report1!A215 → 數值行215; OR02/Nexstar/Quarter/Report1!A215 → 數值行215; OR03/CROX/Quarter/Report1!A215 → 數值行215; OR04/Insulet/Quarter/Report1!A215 → 數值行215; OR05/TransUnion/Quarter/Report1!A215 → 數值行215; OR06/TransUnion/Quarter/Report1!A215 → 數值行215; OR07/Nexstar/Year/Report1!A215 → 數值行215; OR08/XPO/Year/Report1!A215 → 數值行215; OR09/CROX/Year/Report1!A215 → 數值行215; OR10/Insulet/Year/Report1!A215 → 數值行215; OR11/TransUnion/Year/Report1!A215 → 數值行215 |
| 意義候選 | 報表分組標題，不是可取數的金融事實 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 非數值標題／須核原文 |
| 排除與不可替代項 | 不搜尋或填入金額；不註冊metric |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | 核准公式的各輸入所屬主表／附註；管理層或貸款文件比率僅作定義與比對證據 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 僅保留版面／分組；無取值、加總或公式；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=not_a_fact（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=not_a_fact；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR01-Report1-A217-次數

原始英文：`Accounts Receivable Turnover`；子項：次數

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | RATIO 名稱行217；OR01/Nexstar/Quarter/Report1!A217 → 數值行216; OR02/Nexstar/Quarter/Report1!A217 → 數值行216; OR03/CROX/Quarter/Report1!A217 → 數值行216; OR04/Insulet/Quarter/Report1!A217 → 數值行216; OR05/TransUnion/Quarter/Report1!A217 → 數值行216; OR06/TransUnion/Quarter/Report1!A217 → 數值行216; OR07/Nexstar/Year/Report1!A217 → 數值行216; OR08/XPO/Year/Report1!A217 → 數值行216; OR09/CROX/Year/Report1!A217 → 數值行216; OR10/Insulet/Year/Report1!A217 → 數值行216; OR11/TransUnion/Year/Report1!A217 → 數值行216 |
| 意義候選 | 已核准公式所定義的Accounts Receivable Turnover／次數 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅核准公式所需且同口徑之輸入 |
| 排除與不可替代項 | 來源公布比率只是比對資料；不得反推缺失分子／分母 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | 核准公式的各輸入所屬主表／附註；管理層或貸款文件比率僅作定義與比對證據 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源階段保留輸入候選及原比率證據，輸出仍為not_calculable；後續計算階段才以核准公式產生calculated；規則：CF-17。 |
| 核准公式／推導條件引用 | CF-17: (Revenues / Months × 12) / Average (Accounts Receivable + Bad Debt Allowance)；365 / Times |
| 必要輸入與版本 | Revenues, verified Months, Average (Accounts Receivable + Bad Debt Allowance), verified allowance sign；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=multiple（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=mixed_formula_inputs；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | DEC-04；另見全部84項盤點待確認清單。 |

## OR01-Report1-A217-天數

原始英文：`Accounts Receivable Turnover`；子項：天數

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | RATIO 名稱行217；OR01/Nexstar/Quarter/Report1!A217 → 數值行218; OR02/Nexstar/Quarter/Report1!A217 → 數值行218; OR03/CROX/Quarter/Report1!A217 → 數值行218; OR04/Insulet/Quarter/Report1!A217 → 數值行218; OR05/TransUnion/Quarter/Report1!A217 → 數值行218; OR06/TransUnion/Quarter/Report1!A217 → 數值行218; OR07/Nexstar/Year/Report1!A217 → 數值行218; OR08/XPO/Year/Report1!A217 → 數值行218; OR09/CROX/Year/Report1!A217 → 數值行218; OR10/Insulet/Year/Report1!A217 → 數值行218; OR11/TransUnion/Year/Report1!A217 → 數值行218 |
| 意義候選 | 已核准公式所定義的Accounts Receivable Turnover／天數 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅核准公式所需且同口徑之輸入 |
| 排除與不可替代項 | 來源公布比率只是比對資料；不得反推缺失分子／分母 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | 核准公式的各輸入所屬主表／附註；管理層或貸款文件比率僅作定義與比對證據 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源階段保留輸入候選及原比率證據，輸出仍為not_calculable；後續計算階段才以核准公式產生calculated；規則：CF-17。 |
| 核准公式／推導條件引用 | CF-17: (Revenues / Months × 12) / Average (Accounts Receivable + Bad Debt Allowance)；365 / Times |
| 必要輸入與版本 | Revenues, verified Months, Average (Accounts Receivable + Bad Debt Allowance), verified allowance sign；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=day（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=mixed_formula_inputs；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | DEC-04；另見全部84項盤點待確認清單。 |

## OR01-Report1-A221-次數

原始英文：`Accounts Payable Turnover`；子項：次數

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | RATIO 名稱行221；OR01/Nexstar/Quarter/Report1!A221 → 數值行219; OR02/Nexstar/Quarter/Report1!A221 → 數值行219; OR03/CROX/Quarter/Report1!A221 → 數值行219; OR04/Insulet/Quarter/Report1!A221 → 數值行219; OR05/TransUnion/Quarter/Report1!A221 → 數值行219; OR06/TransUnion/Quarter/Report1!A221 → 數值行219; OR07/Nexstar/Year/Report1!A221 → 數值行219; OR08/XPO/Year/Report1!A221 → 數值行219; OR09/CROX/Year/Report1!A221 → 數值行219; OR10/Insulet/Year/Report1!A221 → 數值行219; OR11/TransUnion/Year/Report1!A221 → 數值行219 |
| 意義候選 | 已核准公式所定義的Accounts Payable Turnover／次數 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅核准公式所需且同口徑之輸入 |
| 排除與不可替代項 | 來源公布比率只是比對資料；不得反推缺失分子／分母 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | 核准公式的各輸入所屬主表／附註；管理層或貸款文件比率僅作定義與比對證據 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源階段保留輸入候選及原比率證據，輸出仍為not_calculable；後續計算階段才以核准公式產生calculated；規則：CF-18。 |
| 核准公式／推導條件引用 | CF-18: (Operating Costs / Months × 12) / Average Accounts Payable；365 / Times |
| 必要輸入與版本 | Operating Costs, verified Months, Average Accounts Payable；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=multiple（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=mixed_formula_inputs；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | DEC-04；另見全部84項盤點待確認清單。 |

## OR01-Report1-A221-天數

原始英文：`Accounts Payable Turnover`；子項：天數

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | RATIO 名稱行221；OR01/Nexstar/Quarter/Report1!A221 → 數值行222; OR02/Nexstar/Quarter/Report1!A221 → 數值行222; OR03/CROX/Quarter/Report1!A221 → 數值行222; OR04/Insulet/Quarter/Report1!A221 → 數值行222; OR05/TransUnion/Quarter/Report1!A221 → 數值行222; OR06/TransUnion/Quarter/Report1!A221 → 數值行222; OR07/Nexstar/Year/Report1!A221 → 數值行222; OR08/XPO/Year/Report1!A221 → 數值行222; OR09/CROX/Year/Report1!A221 → 數值行222; OR10/Insulet/Year/Report1!A221 → 數值行222; OR11/TransUnion/Year/Report1!A221 → 數值行222 |
| 意義候選 | 已核准公式所定義的Accounts Payable Turnover／天數 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅核准公式所需且同口徑之輸入 |
| 排除與不可替代項 | 來源公布比率只是比對資料；不得反推缺失分子／分母 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | 核准公式的各輸入所屬主表／附註；管理層或貸款文件比率僅作定義與比對證據 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源階段保留輸入候選及原比率證據，輸出仍為not_calculable；後續計算階段才以核准公式產生calculated；規則：CF-18。 |
| 核准公式／推導條件引用 | CF-18: (Operating Costs / Months × 12) / Average Accounts Payable；365 / Times |
| 必要輸入與版本 | Operating Costs, verified Months, Average Accounts Payable；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=day（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=mixed_formula_inputs；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | DEC-04；另見全部84項盤點待確認清單。 |

## OR01-Report1-A225-次數

原始英文：`Inventory Turnover`；子項：次數

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | RATIO 名稱行225；OR01/Nexstar/Quarter/Report1!A225 → 數值行223; OR02/Nexstar/Quarter/Report1!A225 → 數值行223; OR03/CROX/Quarter/Report1!A225 → 數值行223; OR04/Insulet/Quarter/Report1!A225 → 數值行223; OR05/TransUnion/Quarter/Report1!A225 → 數值行223; OR06/TransUnion/Quarter/Report1!A225 → 數值行223; OR07/Nexstar/Year/Report1!A225 → 數值行223; OR08/XPO/Year/Report1!A225 → 數值行223; OR09/CROX/Year/Report1!A225 → 數值行223; OR10/Insulet/Year/Report1!A225 → 數值行223; OR11/TransUnion/Year/Report1!A225 → 數值行223 |
| 意義候選 | 已核准公式所定義的Inventory Turnover／次數 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅核准公式所需且同口徑之輸入 |
| 排除與不可替代項 | 來源公布比率只是比對資料；不得反推缺失分子／分母 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | 核准公式的各輸入所屬主表／附註；管理層或貸款文件比率僅作定義與比對證據 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源階段保留輸入候選及原比率證據，輸出仍為not_calculable；後續計算階段才以核准公式產生calculated；規則：CF-19。 |
| 核准公式／推導條件引用 | CF-19: (Operating Costs / Months × 12) / Average (Inventory + Provision For Inventory Devaluation)；365 / Times |
| 必要輸入與版本 | Operating Costs, verified Months, Average (Inventory + Provision For Inventory Devaluation), verified provision sign；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=multiple（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=mixed_formula_inputs；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | DEC-04；另見全部84項盤點待確認清單。 |

## OR01-Report1-A225-天數

原始英文：`Inventory Turnover`；子項：天數

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | RATIO 名稱行225；OR01/Nexstar/Quarter/Report1!A225 → 數值行226; OR02/Nexstar/Quarter/Report1!A225 → 數值行226; OR03/CROX/Quarter/Report1!A225 → 數值行226; OR04/Insulet/Quarter/Report1!A225 → 數值行226; OR05/TransUnion/Quarter/Report1!A225 → 數值行226; OR06/TransUnion/Quarter/Report1!A225 → 數值行226; OR07/Nexstar/Year/Report1!A225 → 數值行226; OR08/XPO/Year/Report1!A225 → 數值行226; OR09/CROX/Year/Report1!A225 → 數值行226; OR10/Insulet/Year/Report1!A225 → 數值行226; OR11/TransUnion/Year/Report1!A225 → 數值行226 |
| 意義候選 | 已核准公式所定義的Inventory Turnover／天數 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅核准公式所需且同口徑之輸入 |
| 排除與不可替代項 | 來源公布比率只是比對資料；不得反推缺失分子／分母 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | 核准公式的各輸入所屬主表／附註；管理層或貸款文件比率僅作定義與比對證據 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源階段保留輸入候選及原比率證據，輸出仍為not_calculable；後續計算階段才以核准公式產生calculated；規則：CF-19。 |
| 核准公式／推導條件引用 | CF-19: (Operating Costs / Months × 12) / Average (Inventory + Provision For Inventory Devaluation)；365 / Times |
| 必要輸入與版本 | Operating Costs, verified Months, Average (Inventory + Provision For Inventory Devaluation), verified provision sign；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=day（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=mixed_formula_inputs；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | DEC-04；另見全部84項盤點待確認清單。 |

## OR01-Report1-A229-次數

原始英文：`Fixed Asset Turnover`；子項：次數

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | RATIO 名稱行229；OR01/Nexstar/Quarter/Report1!A229 → 數值行227; OR02/Nexstar/Quarter/Report1!A229 → 數值行227; OR03/CROX/Quarter/Report1!A229 → 數值行227; OR04/Insulet/Quarter/Report1!A229 → 數值行227; OR05/TransUnion/Quarter/Report1!A229 → 數值行227; OR06/TransUnion/Quarter/Report1!A229 → 數值行227; OR07/Nexstar/Year/Report1!A229 → 數值行227; OR08/XPO/Year/Report1!A229 → 數值行227; OR09/CROX/Year/Report1!A229 → 數值行227; OR10/Insulet/Year/Report1!A229 → 數值行227; OR11/TransUnion/Year/Report1!A229 → 數值行227 |
| 意義候選 | 已核准公式所定義的Fixed Asset Turnover／次數 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅核准公式所需且同口徑之輸入 |
| 排除與不可替代項 | 來源公布比率只是比對資料；不得反推缺失分子／分母 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | 核准公式的各輸入所屬主表／附註；管理層或貸款文件比率僅作定義與比對證據 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源階段保留輸入候選及原比率證據，輸出仍為not_calculable；後續計算階段才以核准公式產生calculated；規則：CF-20。 |
| 核准公式／推導條件引用 | CF-20: (Revenues / Months × 12) / Average Fixed Assets；365 / Times |
| 必要輸入與版本 | Revenues, verified Months, Average Fixed Assets；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=multiple（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=mixed_formula_inputs；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | DEC-04；另見全部84項盤點待確認清單。 |

## OR01-Report1-A229-天數

原始英文：`Fixed Asset Turnover`；子項：天數

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | RATIO 名稱行229；OR01/Nexstar/Quarter/Report1!A229 → 數值行230; OR02/Nexstar/Quarter/Report1!A229 → 數值行230; OR03/CROX/Quarter/Report1!A229 → 數值行230; OR04/Insulet/Quarter/Report1!A229 → 數值行230; OR05/TransUnion/Quarter/Report1!A229 → 數值行230; OR06/TransUnion/Quarter/Report1!A229 → 數值行230; OR07/Nexstar/Year/Report1!A229 → 數值行230; OR08/XPO/Year/Report1!A229 → 數值行230; OR09/CROX/Year/Report1!A229 → 數值行230; OR10/Insulet/Year/Report1!A229 → 數值行230; OR11/TransUnion/Year/Report1!A229 → 數值行230 |
| 意義候選 | 已核准公式所定義的Fixed Asset Turnover／天數 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅核准公式所需且同口徑之輸入 |
| 排除與不可替代項 | 來源公布比率只是比對資料；不得反推缺失分子／分母 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | 核准公式的各輸入所屬主表／附註；管理層或貸款文件比率僅作定義與比對證據 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源階段保留輸入候選及原比率證據，輸出仍為not_calculable；後續計算階段才以核准公式產生calculated；規則：CF-20。 |
| 核准公式／推導條件引用 | CF-20: (Revenues / Months × 12) / Average Fixed Assets；365 / Times |
| 必要輸入與版本 | Revenues, verified Months, Average Fixed Assets；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=day（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=mixed_formula_inputs；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | DEC-04；另見全部84項盤點待確認清單。 |

## OR01-Report1-A232-次數

原始英文：`Total Asset Turnover`；子項：次數

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | RATIO 名稱行232；OR01/Nexstar/Quarter/Report1!A232 → 數值行231; OR02/Nexstar/Quarter/Report1!A232 → 數值行231; OR03/CROX/Quarter/Report1!A232 → 數值行231; OR04/Insulet/Quarter/Report1!A232 → 數值行231; OR05/TransUnion/Quarter/Report1!A232 → 數值行231; OR06/TransUnion/Quarter/Report1!A232 → 數值行231; OR07/Nexstar/Year/Report1!A232 → 數值行231; OR08/XPO/Year/Report1!A232 → 數值行231; OR09/CROX/Year/Report1!A232 → 數值行231; OR10/Insulet/Year/Report1!A232 → 數值行231; OR11/TransUnion/Year/Report1!A232 → 數值行231 |
| 意義候選 | 已核准公式所定義的Total Asset Turnover／次數 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅核准公式所需且同口徑之輸入 |
| 排除與不可替代項 | 來源公布比率只是比對資料；不得反推缺失分子／分母 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | 核准公式的各輸入所屬主表／附註；管理層或貸款文件比率僅作定義與比對證據 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源階段保留輸入候選及原比率證據，輸出仍為not_calculable；後續計算階段才以核准公式產生calculated；規則：CF-21。 |
| 核准公式／推導條件引用 | CF-21: (Revenues / Months × 12) / Average Total Assets；365 / Times |
| 必要輸入與版本 | Revenues, verified Months, Average Total Assets；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=multiple（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=mixed_formula_inputs；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | DEC-04；另見全部84項盤點待確認清單。 |

## OR01-Report1-A232-天數

原始英文：`Total Asset Turnover`；子項：天數

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | RATIO 名稱行232；OR01/Nexstar/Quarter/Report1!A232 → 數值行233; OR02/Nexstar/Quarter/Report1!A232 → 數值行233; OR03/CROX/Quarter/Report1!A232 → 數值行233; OR04/Insulet/Quarter/Report1!A232 → 數值行233; OR05/TransUnion/Quarter/Report1!A232 → 數值行233; OR06/TransUnion/Quarter/Report1!A232 → 數值行233; OR07/Nexstar/Year/Report1!A232 → 數值行233; OR08/XPO/Year/Report1!A232 → 數值行233; OR09/CROX/Year/Report1!A232 → 數值行233; OR10/Insulet/Year/Report1!A232 → 數值行233; OR11/TransUnion/Year/Report1!A232 → 數值行233 |
| 意義候選 | 已核准公式所定義的Total Asset Turnover／天數 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅核准公式所需且同口徑之輸入 |
| 排除與不可替代項 | 來源公布比率只是比對資料；不得反推缺失分子／分母 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | 核准公式的各輸入所屬主表／附註；管理層或貸款文件比率僅作定義與比對證據 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源階段保留輸入候選及原比率證據，輸出仍為not_calculable；後續計算階段才以核准公式產生calculated；規則：CF-21。 |
| 核准公式／推導條件引用 | CF-21: (Revenues / Months × 12) / Average Total Assets；365 / Times |
| 必要輸入與版本 | Revenues, verified Months, Average Total Assets；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=day（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=mixed_formula_inputs；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | DEC-04；另見全部84項盤點待確認清單。 |

## OR02-Report1-A143

原始英文：`　　Payments for broadcast rights`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行143；OR02/Nexstar/Quarter/Report1!A143 → 數值行143; OR07/Nexstar/Year/Report1!A143 → 數值行143 |
| 意義候選 | 來源所列收購、資產取得或播映權付款 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 扣除取得現金與否、業務併購及資產購置須分開；不得套用全部CapEx |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-016, ISS-061。 |

## OR02-Report1-A169

原始英文：`　　Payments for acquisitions`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行169；OR02/Nexstar/Quarter/Report1!A169 → 數值行169 |
| 意義候選 | 來源所列收購、資產取得或播映權付款 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 扣除取得現金與否、業務併購及資產購置須分開；不得套用全部CapEx |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-033, ISS-060。 |

## OR03-Report1-A19

原始英文：`Income Taxes Receivable`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | BS 名稱行19；OR03/CROX/Quarter/Report1!A19 → 數值行19; OR09/CROX/Year/Report1!A19 → 數值行19 |
| 意義候選 | 應收所得稅 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅該原文實際涵蓋項目 |
| 排除與不可替代項 | 同一行號的稅款與預付資產不是同義；不可固定映射 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Balance Sheets；資產負債表；該資產／負債／權益附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=instant；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-003。 |

## OR03-Report1-A50

原始英文：`Income Taxes Payable`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | BS 名稱行50；OR03/CROX/Quarter/Report1!A50 → 數值行50; OR09/CROX/Year/Report1!A50 → 數值行50 |
| 意義候選 | 應付所得稅餘額 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源流動應付稅款 |
| 排除與不可替代項 | 不等同所得稅費用、遞延所得稅或現金納稅 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Balance Sheets；資產負債表；該資產／負債／權益附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=instant；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR03-Report1-A59

原始英文：`Long-Term Income Taxes Payable`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | BS 名稱行59；OR03/CROX/Quarter/Report1!A59 → 數值行59; OR09/CROX/Year/Report1!A59 → 數值行59 |
| 意義候選 | 長期應付所得稅 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源明列之遞延稅或長期應付稅負債 |
| 排除與不可替代項 | 兩者不是同義；均非當期所得稅費用或支付所得稅 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Balance Sheets；資產負債表；該資產／負債／權益附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=instant；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-006。 |

## OR03-Report1-A60

原始英文：`Long-Term Operating Lease Liabilities`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | BS 名稱行60；OR03/CROX/Quarter/Report1!A60 → 數值行60; OR09/CROX/Year/Report1!A60 → 數值行60 |
| 意義候選 | 長期營業租賃負債 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源營業租賃之非流動部分 |
| 排除與不可替代項 | 融資租賃、全部長期債務與流動部分須分開 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Balance Sheets；資產負債表；該資產／負債／權益附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=instant；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | DEC-02；另見全部84項盤點待確認清單。 |

## OR03-Report1-A108

原始英文：`Asset impairments`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | IS 名稱行108；OR03/CROX/Quarter/Report1!A108 → 數值行108; OR09/CROX/Year/Report1!A108 → 數值行108 |
| 意義候選 | 資產減損損失 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 該公司該期該名稱實際損失 |
| 排除與不可替代項 | 不能將本行跨公司或跨檔固定為一種損失；CF回加數另核 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Operations / Income；損益表；該收入／成本／費用及稅項附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-048。 |

## OR03-Report1-A133

原始英文：`　　Depreciation and amortization expenses`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行133；OR03/CROX/Quarter/Report1!A133 → 數值行133; OR04/Insulet/Quarter/Report1!A133 → 數值行133; OR09/CROX/Year/Report1!A133 → 數值行133; OR10/Insulet/Year/Report1!A133 → 數值行133 |
| 意義候選 | 營業現金流中的非現金折舊攤銷調整 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源間接法明列之調整 |
| 排除與不可替代項 | 不預設等同IS補充D&A或全公司EBITDA輸入；不得重複回加 |
| 既有代碼 | METRICS候選：da；raw候選：da。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | us-gaap:DepreciationDepletionAndAmortization → raw.da |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：DER-07。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-007, ISS-059。 |

## OR03-Report1-A134

原始英文：`　　Operating lease cost`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行134；OR03/CROX/Quarter/Report1!A134 → 數值行134; OR09/CROX/Year/Report1!A134 → 數值行134 |
| 意義候選 | 來源間接法中的非現金損益／費用調整 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 損益表金額不必然等於CF回加；須核範圍、符號及是否已在其他調整中包含 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-008。 |

## OR03-Report1-A135

原始英文：`　　Inventory donations`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行135；OR03/CROX/Quarter/Report1!A135 → 數值行135; OR09/CROX/Year/Report1!A135 → 數值行135 |
| 意義候選 | 營業相關資產負債變動或其他CF調整；必須核實是變動而非餘額 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | BS時點餘額tag不適用此處流量；不以兩期餘額差代替完整CF調整，除非已核非現金與合併變動 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-009。 |

## OR03-Report1-A136

原始英文：`　　Provision (recovery) for doubtful accounts, net`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行136；OR03/CROX/Quarter/Report1!A136 → 數值行136; OR09/CROX/Year/Report1!A136 → 數值行136 |
| 意義候選 | 來源CF原文所指之現金流或調整項，須逐項核附註 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 不只依名稱、行號或金額相同判定其經濟內容 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-010。 |

## OR03-Report1-A137

原始英文：`　　Share-based compensation`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行137；OR03/CROX/Quarter/Report1!A137 → 數值行137; OR09/CROX/Year/Report1!A137 → 數值行137 |
| 意義候選 | 來源間接法中的非現金損益／費用調整 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 損益表金額不必然等於CF回加；須核範圍、符號及是否已在其他調整中包含 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-011。 |

## OR03-Report1-A138

原始英文：`　　Asset impairments`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行138；OR03/CROX/Quarter/Report1!A138 → 數值行138; OR09/CROX/Year/Report1!A138 → 數值行138 |
| 意義候選 | 來源間接法中的非現金損益／費用調整 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 損益表金額不必然等於CF回加；須核範圍、符號及是否已在其他調整中包含 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-012。 |

## OR03-Report1-A139

原始英文：`　　Deferred taxes`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行139；OR03/CROX/Quarter/Report1!A139 → 數值行139; OR09/CROX/Year/Report1!A139 → 數值行139 |
| 意義候選 | 來源CF原文所指之現金流或調整項，須逐項核附註 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 不只依名稱、行號或金額相同判定其經濟內容 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-013, ISS-053。 |

## OR03-Report1-A140

原始英文：`　　Loss on disposal of assets`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行140；OR03/CROX/Quarter/Report1!A140 → 數值行140; OR09/CROX/Year/Report1!A140 → 數值行140 |
| 意義候選 | 來源間接法中的非現金損益／費用調整 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 損益表金額不必然等於CF回加；須核範圍、符號及是否已在其他調整中包含 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-014。 |

## OR03-Report1-A143

原始英文：`　　Other non-cash items`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行143；OR03/CROX/Quarter/Report1!A143 → 數值行143; OR09/CROX/Year/Report1!A143 → 數值行143 |
| 意義候選 | 來源間接法中的非現金損益／費用調整 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 損益表金額不必然等於CF回加；須核範圍、符號及是否已在其他調整中包含 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-016。 |

## OR03-Report1-A145

原始英文：`　　Accounts receivable, net of allowances`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行145；OR03/CROX/Quarter/Report1!A145 → 數值行145; OR09/CROX/Year/Report1!A145 → 數值行145 |
| 意義候選 | 營業相關資產負債變動或其他CF調整；必須核實是變動而非餘額 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | BS時點餘額tag不適用此處流量；不以兩期餘額差代替完整CF調整，除非已核非現金與合併變動 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-017, ISS-066。 |

## OR03-Report1-A146

原始英文：`　　Inventories`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行146；OR03/CROX/Quarter/Report1!A146 → 數值行146; OR09/CROX/Year/Report1!A146 → 數值行146 |
| 意義候選 | 營業相關資產負債變動或其他CF調整；必須核實是變動而非餘額 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | BS時點餘額tag不適用此處流量；不以兩期餘額差代替完整CF調整，除非已核非現金與合併變動 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-018, ISS-054, ISS-065。 |

## OR03-Report1-A147

原始英文：`　　Prepaid expenses and other assets`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行147；OR03/CROX/Quarter/Report1!A147 → 數值行147; OR09/CROX/Year/Report1!A147 → 數值行147 |
| 意義候選 | 來源CF原文所指之現金流或調整項，須逐項核附註 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 不只依名稱、行號或金額相同判定其經濟內容 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-019, ISS-057。 |

## OR03-Report1-A148

原始英文：`　　Accounts payable`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行148；OR03/CROX/Quarter/Report1!A148 → 數值行148; OR09/CROX/Year/Report1!A148 → 數值行148 |
| 意義候選 | 營業相關資產負債變動或其他CF調整；必須核實是變動而非餘額 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | BS時點餘額tag不適用此處流量；不以兩期餘額差代替完整CF調整，除非已核非現金與合併變動 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-020, ISS-051。 |

## OR03-Report1-A149

原始英文：`　　Accrued expenses and other liabilities`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行149；OR03/CROX/Quarter/Report1!A149 → 數值行149; OR09/CROX/Year/Report1!A149 → 數值行149 |
| 意義候選 | 營業相關資產負債變動或其他CF調整；必須核實是變動而非餘額 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | BS時點餘額tag不適用此處流量；不以兩期餘額差代替完整CF調整，除非已核非現金與合併變動 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-021, ISS-052。 |

## OR03-Report1-A150

原始英文：`　　Right-of-use assets and operating lease liabilities`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行150；OR03/CROX/Quarter/Report1!A150 → 數值行150; OR09/CROX/Year/Report1!A150 → 數值行150 |
| 意義候選 | 營業相關資產負債變動或其他CF調整；必須核實是變動而非餘額 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | BS時點餘額tag不適用此處流量；不以兩期餘額差代替完整CF調整，除非已核非現金與合併變動 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-022。 |

## OR03-Report1-A151

原始英文：`　　Income taxes`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行151；OR03/CROX/Quarter/Report1!A151 → 數值行151; OR09/CROX/Year/Report1!A151 → 數值行151 |
| 意義候選 | 來源CF中的稅款支付、稅項變動或遞延稅調整，依原文確認 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | Income tax payable、Income tax paid及Deferred taxes不可互換；不能套用所得稅費用tag |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-023。 |

## OR03-Report1-A158

原始英文：`　　Others`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行158；OR03/CROX/Quarter/Report1!A158 → 數值行158; OR04/Insulet/Quarter/Report1!A158 → 數值行158; OR09/CROX/Year/Report1!A158 → 數值行158; OR10/Insulet/Year/Report1!A158 → 數值行158 |
| 意義候選 | 來源該活動分類的其他調整／流量；必須取得組成 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 不能作為現金不勾稽的補差欄或從其他公司挪用 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-027, ISS-056, ISS-064。 |

## OR03-Report1-A161

原始英文：`　　Purchases of property, equipment, and software`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行161；OR03/CROX/Quarter/Report1!A161 → 數值行161; OR09/CROX/Year/Report1!A161 → 數值行161 |
| 意義候選 | 購置資本資產付款 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 軟體、租賃或併購可能另列；不可把CapEx當作償還本金 |
| 既有代碼 | METRICS候選：無；raw候選：capex。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | us-gaap:PaymentsToAcquirePropertyPlantAndEquipment → raw.capex |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-028。 |

## OR03-Report1-A162

原始英文：`　　Proceeds from disposal of property and equipment`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行162；OR03/CROX/Quarter/Report1!A162 → 數值行162; OR09/CROX/Year/Report1!A162 → 數值行162 |
| 意義候選 | 資產／投資出售、到期或其他處分收款 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 借款流入、發股流入與資產出售收款不是同義；不使用同一行號跨公司取數 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-029。 |

## OR03-Report1-A163

原始英文：`　　Acquisition of HEYDUDE, net of cash acquired`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行163；OR03/CROX/Quarter/Report1!A163 → 數值行163; OR09/CROX/Year/Report1!A163 → 數值行163 |
| 意義候選 | 來源所列收購、資產取得或播映權付款 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 扣除取得現金與否、業務併購及資產購置須分開；不得套用全部CapEx |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-030。 |

## OR03-Report1-A172

原始英文：`　　Others`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行172；OR03/CROX/Quarter/Report1!A172 → 數值行172; OR04/Insulet/Quarter/Report1!A172 → 數值行172; OR09/CROX/Year/Report1!A172 → 數值行172; OR10/Insulet/Year/Report1!A172 → 數值行172 |
| 意義候選 | 來源該活動分類的其他調整／流量；必須取得組成 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 不能作為現金不勾稽的補差欄或從其他公司挪用 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-034, ISS-056, ISS-064。 |

## OR03-Report1-A175

原始英文：`　　Proceeds from notes issuance`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行175；OR03/CROX/Quarter/Report1!A175 → 數值行175; OR09/CROX/Year/Report1!A175 → 數值行175 |
| 意義候選 | 借款／發債取得之現金 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 借款流入、發股流入與資產出售收款不是同義；不使用同一行號跨公司取數 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-035。 |

## OR03-Report1-A176

原始英文：`　　Proceeds from bank borrowings`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行176；OR03/CROX/Quarter/Report1!A176 → 數值行176; OR09/CROX/Year/Report1!A176 → 數值行176 |
| 意義候選 | 借款／發債取得之現金 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 借款流入、發股流入與資產出售收款不是同義；不使用同一行號跨公司取數 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-036。 |

## OR03-Report1-A177

原始英文：`　　Repayments of bank borrowings`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行177；OR03/CROX/Quarter/Report1!A177 → 數值行177; OR09/CROX/Year/Report1!A177 → 數值行177 |
| 意義候選 | 償還融資現金流；須逐項辨識本金、借款種類及費用 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 廣義還債tag不證明是該項特定借款；不等同debt service，亦不預設包含利息或融資租賃 |
| 既有代碼 | METRICS候選：無；raw候選：debt_repayment, debt_repayment_lt。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | us-gaap:RepaymentsOfDebt → raw.debt_repayment; us-gaap:RepaymentsOfLongTermDebt → raw.debt_repayment_lt |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-037。 |

## OR03-Report1-A178

原始英文：`　　Deferred debt issuance costs`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行178；OR03/CROX/Quarter/Report1!A178 → 數值行178; OR09/CROX/Year/Report1!A178 → 數值行178 |
| 意義候選 | 支付或遞延處理的債務發行／融資成本 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 費用認列、實付現金與借款淨收款須區分；不可直接當償還本金 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-038。 |

## OR03-Report1-A179

原始英文：`　　Repurchases of common stock`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行179；OR03/CROX/Quarter/Report1!A179 → 數值行179; OR09/CROX/Year/Report1!A179 → 數值行179 |
| 意義候選 | 股份買回相關付款，需辨識普通股、庫藏股或代扣稅 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 員工代扣稅款與普通股買回的涵蓋範圍須另核 |
| 既有代碼 | METRICS候選：無；raw候選：buybacks。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | us-gaap:PaymentsForRepurchaseOfCommonStock → raw.buybacks |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-039, ISS-062。 |

## OR03-Report1-A180

原始英文：`　　Repurchases of common stock for tax withholding`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行180；OR03/CROX/Quarter/Report1!A180 → 數值行180; OR09/CROX/Year/Report1!A180 → 數值行180 |
| 意義候選 | 股份買回相關付款，需辨識普通股、庫藏股或代扣稅 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 員工代扣稅款與普通股買回的涵蓋範圍須另核 |
| 既有代碼 | METRICS候選：無；raw候選：buybacks。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | us-gaap:PaymentsForRepurchaseOfCommonStock → raw.buybacks |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-040。 |

## OR03-Report1-A188

原始英文：`　　Others`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行188；OR03/CROX/Quarter/Report1!A188 → 數值行188; OR04/Insulet/Quarter/Report1!A188 → 數值行188; OR09/CROX/Year/Report1!A188 → 數值行188; OR10/Insulet/Year/Report1!A188 → 數值行188 |
| 意義候選 | 來源該活動分類的其他調整／流量；必須取得組成 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 不能作為現金不勾稽的補差欄或從其他公司挪用 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-045, ISS-056, ISS-064。 |

## OR03-Report1-A190

原始英文：`Effect of exchange rate changes`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行190；OR03/CROX/Quarter/Report1!A190 → 數值行190; OR04/Insulet/Quarter/Report1!A190 → 數值行190; OR09/CROX/Year/Report1!A190 → 數值行190; OR10/Insulet/Year/Report1!A190 → 數值行190 |
| 意義候選 | 匯率變動對現金之影響或未實現兌換損益調整，須依位置與附註區別 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 影響現金餘額的匯率效果與非現金損益回加不是同一概念 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-046, ISS-063。 |

## OR04-Report1-A19

原始英文：`Prepaid expenses and other current assets`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | BS 名稱行19；OR04/Insulet/Quarter/Report1!A19 → 數值行19; OR10/Insulet/Year/Report1!A19 → 數值行19 |
| 意義候選 | 預付費用及其他流動資產組合 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅該原文實際涵蓋項目 |
| 排除與不可替代項 | 同一行號的稅款與預付資產不是同義；不可固定映射 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Balance Sheets；資產負債表；該資產／負債／權益附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=instant；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-003。 |

## OR04-Report1-A48

原始英文：`Accrued Expenses - Related Party`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | BS 名稱行48；OR04/Insulet/Quarter/Report1!A48 → 數值行48; OR10/Insulet/Year/Report1!A48 → 數值行48 |
| 意義候選 | 應計關係人費用 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 依關係人／合約負債附註核對 |
| 排除與不可替代項 | 應計費用與預收款不是同義；不能依行號替代 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Balance Sheets；資產負債表；該資產／負債／權益附註；Related-party transactions／關係人交易附註；核對交易對手及合併沖銷 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=instant；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-004。 |

## OR04-Report1-A57

原始英文：`Other`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | BS 名稱行57；OR04/Insulet/Quarter/Report1!A57 → 數值行57; OR10/Insulet/Year/Report1!A57 → 數值行57 |
| 意義候選 | 其他長期債務；若僅稱Other則組成仍未定 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源特定長期負債／債務組成 |
| 排除與不可替代項 | 不預設為全部Other Liabilities；不決定租賃與Total Debt範圍 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Balance Sheets；資產負債表；該資產／負債／權益附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=instant；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | DEC-02；ISS-005, ISS-064。 |

## OR04-Report1-A83

原始英文：`Revenue from related party`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | IS 名稱行83；OR04/Insulet/Quarter/Report1!A83 → 數值行83; OR10/Insulet/Year/Report1!A83 → 數值行83 |
| 意義候選 | 來自關係人之收入 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 關係人交易附註支持的收入 |
| 排除與不可替代項 | 確認是否已含Net Sales；集團內部沖銷另核 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Operations / Income；損益表；該收入／成本／費用及稅項附註；Related-party transactions／關係人交易附註；核對交易對手及合併沖銷 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR04-Report1-A108

原始英文：`Loss On Fixed Asset Disposal`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | IS 名稱行108；OR04/Insulet/Quarter/Report1!A108 → 數值行108; OR05/TransUnion/Quarter/Report1!A108 → 數值行108; OR06/TransUnion/Quarter/Report1!A108 → 數值行108; OR08/XPO/Year/Report1!A108 → 數值行108; OR10/Insulet/Year/Report1!A108 → 數值行108; OR11/TransUnion/Year/Report1!A108 → 數值行108 |
| 意義候選 | 處分固定資產損失 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 該公司該期該名稱實際損失 |
| 排除與不可替代項 | 不能將本行跨公司或跨檔固定為一種損失；CF回加數另核 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Operations / Income；損益表；該收入／成本／費用及稅項附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-048。 |

## OR04-Report1-A113

原始英文：`Income tax benefit (expense)`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | IS 名稱行113；OR04/Insulet/Quarter/Report1!A113 → 數值行113; OR10/Insulet/Year/Report1!A113 → 數值行113 |
| 意義候選 | 來源所得稅利益／費用調整，符號與主表稅項關係待核 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源明列的稅利益或費用 |
| 排除與不可替代項 | 不與Income Tax Expense(Credit)重複；不視為停業單位損益 |
| 既有代碼 | METRICS候選：income_tax；raw候選：income_tax_expense。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Operations / Income；損益表；該收入／成本／費用及稅項附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | us-gaap:IncomeTaxExpenseBenefit → raw.income_tax_expense |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：DER-05, DER-06。 |
| 核准公式／推導條件引用 | DER-05: Net Income + signed Income Tax Expense；只限淨利與所得稅對應同一稅前損益範圍，且沒有未處理的停業單位、非控制權益或其他橋接項。所得稅費用為正、利益為負；不得使用 `abs(tax)`。若有橋接項，須有來源及經確認的完整公式。；DER-06: Pre-tax Profit − signed Income Tax Expense；與 DER-05 相同的適用條件；不得把 continuing operations、歸屬母公司淨利與合併淨利直接互換。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-049。 |

## OR04-Report1-A134

原始英文：`　　Stock-based compensation expense`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行134；OR04/Insulet/Quarter/Report1!A134 → 數值行134; OR10/Insulet/Year/Report1!A134 → 數值行134 |
| 意義候選 | 來源間接法中的非現金損益／費用調整 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 損益表金額不必然等於CF回加；須核範圍、符號及是否已在其他調整中包含 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-008。 |

## OR04-Report1-A135

原始英文：`　　Deferred income taxes`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行135；OR04/Insulet/Quarter/Report1!A135 → 數值行135; OR10/Insulet/Year/Report1!A135 → 數值行135 |
| 意義候選 | 來源CF中的稅款支付、稅項變動或遞延稅調整，依原文確認 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | Income tax payable、Income tax paid及Deferred taxes不可互換；不能套用所得稅費用tag |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-009。 |

## OR04-Report1-A136

原始英文：`　　Non-cash interest expense`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行136；OR04/Insulet/Quarter/Report1!A136 → 數值行136; OR10/Insulet/Year/Report1!A136 → 數值行136 |
| 意義候選 | 來源間接法中的非現金損益／費用調整 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 損益表金額不必然等於CF回加；須核範圍、符號及是否已在其他調整中包含 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-010。 |

## OR04-Report1-A137

原始英文：`　　Loss on extinguishment of convertible debt`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行137；OR04/Insulet/Quarter/Report1!A137 → 數值行137; OR10/Insulet/Year/Report1!A137 → 數值行137 |
| 意義候選 | 來源間接法中的非現金損益／費用調整 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 損益表金額不必然等於CF回加；須核範圍、符號及是否已在其他調整中包含 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-011。 |

## OR04-Report1-A138

原始英文：`　　Provision for credit losses`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行138；OR04/Insulet/Quarter/Report1!A138 → 數值行138; OR10/Insulet/Year/Report1!A138 → 數值行138 |
| 意義候選 | 來源間接法中的非現金損益／費用調整 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 損益表金額不必然等於CF回加；須核範圍、符號及是否已在其他調整中包含 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-012。 |

## OR04-Report1-A139

原始英文：`　　Unrealized loss (gain) on investments`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行139；OR04/Insulet/Quarter/Report1!A139 → 數值行139; OR10/Insulet/Year/Report1!A139 → 數值行139 |
| 意義候選 | 來源間接法中的非現金損益／費用調整 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 損益表金額不必然等於CF回加；須核範圍、符號及是否已在其他調整中包含 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-013。 |

## OR04-Report1-A143

原始英文：`　　Others`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行143；OR04/Insulet/Quarter/Report1!A143 → 數值行143; OR10/Insulet/Year/Report1!A143 → 數值行143 |
| 意義候選 | 來源該活動分類的其他調整／流量；必須取得組成 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 不能作為現金不勾稽的補差欄或從其他公司挪用 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-016, ISS-056, ISS-064。 |

## OR04-Report1-A145

原始英文：`　　Accounts receivable`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行145；OR04/Insulet/Quarter/Report1!A145 → 數值行145; OR08/XPO/Year/Report1!A145 → 數值行145; OR10/Insulet/Year/Report1!A145 → 數值行145 |
| 意義候選 | 營業相關資產負債變動或其他CF調整；必須核實是變動而非餘額 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | BS時點餘額tag不適用此處流量；不以兩期餘額差代替完整CF調整，除非已核非現金與合併變動 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-017, ISS-066。 |

## OR04-Report1-A146

原始英文：`　　Accounts receivable — related party`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行146；OR04/Insulet/Quarter/Report1!A146 → 數值行146; OR10/Insulet/Year/Report1!A146 → 數值行146 |
| 意義候選 | 營業相關資產負債變動或其他CF調整；必須核實是變動而非餘額 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | BS時點餘額tag不適用此處流量；不以兩期餘額差代替完整CF調整，除非已核非現金與合併變動 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註；Related-party transactions／關係人交易附註；核對交易對手及合併沖銷 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-018。 |

## OR04-Report1-A147

原始英文：`　　Inventories`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行147；OR04/Insulet/Quarter/Report1!A147 → 數值行147; OR10/Insulet/Year/Report1!A147 → 數值行147 |
| 意義候選 | 營業相關資產負債變動或其他CF調整；必須核實是變動而非餘額 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | BS時點餘額tag不適用此處流量；不以兩期餘額差代替完整CF調整，除非已核非現金與合併變動 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-019, ISS-054, ISS-065。 |

## OR04-Report1-A148

原始英文：`　　Prepaid expenses and other assets`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行148；OR04/Insulet/Quarter/Report1!A148 → 數值行148; OR10/Insulet/Year/Report1!A148 → 數值行148 |
| 意義候選 | 來源CF原文所指之現金流或調整項，須逐項核附註 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 不只依名稱、行號或金額相同判定其經濟內容 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-020, ISS-057。 |

## OR04-Report1-A149

原始英文：`　　Other current assets`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行149；OR04/Insulet/Quarter/Report1!A149 → 數值行149; OR10/Insulet/Year/Report1!A149 → 數值行149 |
| 意義候選 | 來源CF原文所指之現金流或調整項，須逐項核附註 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 不只依名稱、行號或金額相同判定其經濟內容 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-021。 |

## OR04-Report1-A150

原始英文：`　　Accounts payable`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行150；OR04/Insulet/Quarter/Report1!A150 → 數值行150; OR10/Insulet/Year/Report1!A150 → 數值行150 |
| 意義候選 | 營業相關資產負債變動或其他CF調整；必須核實是變動而非餘額 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | BS時點餘額tag不適用此處流量；不以兩期餘額差代替完整CF調整，除非已核非現金與合併變動 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-022, ISS-051。 |

## OR04-Report1-A151

原始英文：`　　Accrued expenses and other liabilities`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行151；OR04/Insulet/Quarter/Report1!A151 → 數值行151; OR10/Insulet/Year/Report1!A151 → 數值行151 |
| 意義候選 | 營業相關資產負債變動或其他CF調整；必須核實是變動而非餘額 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | BS時點餘額tag不適用此處流量；不以兩期餘額差代替完整CF調整，除非已核非現金與合併變動 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-023, ISS-052。 |

## OR04-Report1-A152

原始英文：`　　Accrued expenses and other liabilities — related party`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行152；OR04/Insulet/Quarter/Report1!A152 → 數值行152; OR10/Insulet/Year/Report1!A152 → 數值行152 |
| 意義候選 | 營業相關資產負債變動或其他CF調整；必須核實是變動而非餘額 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | BS時點餘額tag不適用此處流量；不以兩期餘額差代替完整CF調整，除非已核非現金與合併變動 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註；Related-party transactions／關係人交易附註；核對交易對手及合併沖銷 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-024。 |

## OR04-Report1-A153

原始英文：`　　Other current liabilities`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行153；OR04/Insulet/Quarter/Report1!A153 → 數值行153; OR10/Insulet/Year/Report1!A153 → 數值行153 |
| 意義候選 | 來源CF原文所指之現金流或調整項，須逐項核附註 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 不只依名稱、行號或金額相同判定其經濟內容 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-025。 |

## OR04-Report1-A161

原始英文：`　　Capital expenditures`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行161；OR04/Insulet/Quarter/Report1!A161 → 數值行161; OR05/TransUnion/Quarter/Report1!A161 → 數值行161; OR06/TransUnion/Quarter/Report1!A161 → 數值行161; OR10/Insulet/Year/Report1!A161 → 數值行161; OR11/TransUnion/Year/Report1!A161 → 數值行161 |
| 意義候選 | 購置資本資產付款 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 軟體、租賃或併購可能另列；不可把CapEx當作償還本金 |
| 既有代碼 | METRICS候選：無；raw候選：capex。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | us-gaap:PaymentsToAcquirePropertyPlantAndEquipment → raw.capex |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-028。 |

## OR04-Report1-A162

原始英文：`　　Investments in developed software`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行162；OR04/Insulet/Quarter/Report1!A162 → 數值行162; OR10/Insulet/Year/Report1!A162 → 數值行162 |
| 意義候選 | 來源CF原文所指之現金流或調整項，須逐項核附註 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 不只依名稱、行號或金額相同判定其經濟內容 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-029。 |

## OR04-Report1-A163

原始英文：`　　Cash paid for investments`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行163；OR04/Insulet/Quarter/Report1!A163 → 數值行163; OR10/Insulet/Year/Report1!A163 → 數值行163 |
| 意義候選 | 來源CF原文所指之現金流或調整項，須逐項核附註 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 不只依名稱、行號或金額相同判定其經濟內容 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-030。 |

## OR04-Report1-A164

原始英文：`　　Acquisition of other intangible assets`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行164；OR04/Insulet/Quarter/Report1!A164 → 數值行164; OR10/Insulet/Year/Report1!A164 → 數值行164 |
| 意義候選 | 來源所列收購、資產取得或播映權付款 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 扣除取得現金與否、業務併購及資產購置須分開；不得套用全部CapEx |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-031。 |

## OR04-Report1-A165

原始英文：`　　Acquisition of a business`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行165；OR04/Insulet/Quarter/Report1!A165 → 數值行165; OR10/Insulet/Year/Report1!A165 → 數值行165 |
| 意義候選 | 來源所列收購、資產取得或播映權付款 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 扣除取得現金與否、業務併購及資產購置須分開；不得套用全部CapEx |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-032。 |

## OR04-Report1-A175

原始英文：`　　Proceeds from issuance of term loan, net of issuance costs`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行175；OR04/Insulet/Quarter/Report1!A175 → 數值行175; OR10/Insulet/Year/Report1!A175 → 數值行175 |
| 意義候選 | 借款／發債取得之現金 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 借款流入、發股流入與資產出售收款不是同義；不使用同一行號跨公司取數 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-035。 |

## OR04-Report1-A176

原始英文：`　　Repayment of term loan`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行176；OR04/Insulet/Quarter/Report1!A176 → 數值行176; OR10/Insulet/Year/Report1!A176 → 數值行176 |
| 意義候選 | 償還融資現金流；須逐項辨識本金、借款種類及費用 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 廣義還債tag不證明是該項特定借款；不等同debt service，亦不預設包含利息或融資租賃 |
| 既有代碼 | METRICS候選：無；raw候選：debt_repayment, debt_repayment_lt。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | us-gaap:RepaymentsOfDebt → raw.debt_repayment; us-gaap:RepaymentsOfLongTermDebt → raw.debt_repayment_lt |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-036。 |

## OR04-Report1-A177

原始英文：`　　Repayment of equipment financings`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行177；OR04/Insulet/Quarter/Report1!A177 → 數值行177; OR10/Insulet/Year/Report1!A177 → 數值行177 |
| 意義候選 | 償還融資現金流；須逐項辨識本金、借款種類及費用 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 廣義還債tag不證明是該項特定借款；不等同debt service，亦不預設包含利息或融資租賃 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-037。 |

## OR04-Report1-A178

原始英文：`　　Financing lease payments`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行178；OR04/Insulet/Quarter/Report1!A178 → 數值行178; OR10/Insulet/Year/Report1!A178 → 數值行178 |
| 意義候選 | 來源CF原文所指之現金流或調整項，須逐項核附註 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 不只依名稱、行號或金額相同判定其經濟內容 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-038。 |

## OR04-Report1-A179

原始英文：`　　Repayment of mortgage`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行179；OR04/Insulet/Quarter/Report1!A179 → 數值行179; OR10/Insulet/Year/Report1!A179 → 數值行179 |
| 意義候選 | 償還融資現金流；須逐項辨識本金、借款種類及費用 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 廣義還債tag不證明是該項特定借款；不等同debt service，亦不預設包含利息或融資租賃 |
| 既有代碼 | METRICS候選：無；raw候選：debt_repayment, debt_repayment_lt。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | us-gaap:RepaymentsOfDebt → raw.debt_repayment; us-gaap:RepaymentsOfLongTermDebt → raw.debt_repayment_lt |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-039。 |

## OR04-Report1-A180

原始英文：`　　Proceeds from secured borrowing (Note 6)`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行180；OR04/Insulet/Quarter/Report1!A180 → 數值行180; OR10/Insulet/Year/Report1!A180 → 數值行180 |
| 意義候選 | 借款／發債取得之現金 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 借款流入、發股流入與資產出售收款不是同義；不使用同一行號跨公司取數 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-040。 |

## OR04-Report1-A181

原始英文：`　　Repayment of secured borrowing (Note 6)`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行181；OR04/Insulet/Quarter/Report1!A181 → 數值行181; OR10/Insulet/Year/Report1!A181 → 數值行181 |
| 意義候選 | 償還融資現金流；須逐項辨識本金、借款種類及費用 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 廣義還債tag不證明是該項特定借款；不等同debt service，亦不預設包含利息或融資租賃 |
| 既有代碼 | METRICS候選：無；raw候選：debt_repayment, debt_repayment_lt。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | us-gaap:RepaymentsOfDebt → raw.debt_repayment; us-gaap:RepaymentsOfLongTermDebt → raw.debt_repayment_lt |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-041。 |

## OR04-Report1-A182

原始英文：`　　Proceeds from exercise of stock options`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行182；OR04/Insulet/Quarter/Report1!A182 → 數值行182; OR10/Insulet/Year/Report1!A182 → 數值行182 |
| 意義候選 | 發行股份、員工行使選擇權或購股計畫之收款 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 借款流入、發股流入與資產出售收款不是同義；不使用同一行號跨公司取數 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-042。 |

## OR04-Report1-A183

原始英文：`　　Proceeds from issuance of common stock under employee stock purchase plan`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行183；OR04/Insulet/Quarter/Report1!A183 → 數值行183; OR10/Insulet/Year/Report1!A183 → 數值行183 |
| 意義候選 | 發行股份、員工行使選擇權或購股計畫之收款 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 借款流入、發股流入與資產出售收款不是同義；不使用同一行號跨公司取數 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-043。 |

## OR04-Report1-A184

原始英文：`　　Payment of withholding taxes in connection with vesting of restricted stock units`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行184；OR04/Insulet/Quarter/Report1!A184 → 數值行184; OR10/Insulet/Year/Report1!A184 → 數值行184 |
| 意義候選 | 股權薪酬相關員工代扣稅款之付款 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 不是企業所得稅費用；與買回股份或融資費用的涵蓋範圍須核對 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-044。 |

## OR04-Report1-A185

原始英文：`　　Repayment of convertible debt`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行185；OR04/Insulet/Quarter/Report1!A185 → 數值行185; OR10/Insulet/Year/Report1!A185 → 數值行185 |
| 意義候選 | 償還融資現金流；須逐項辨識本金、借款種類及費用 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 廣義還債tag不證明是該項特定借款；不等同debt service，亦不預設包含利息或融資租賃 |
| 既有代碼 | METRICS候選：無；raw候選：debt_repayment, debt_repayment_lt。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | us-gaap:RepaymentsOfDebt → raw.debt_repayment; us-gaap:RepaymentsOfLongTermDebt → raw.debt_repayment_lt |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR04-Report1-A186

原始英文：`　　Proceeds from issuance of senior unsecured notes, net of issuance costs`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行186；OR04/Insulet/Quarter/Report1!A186 → 數值行186; OR10/Insulet/Year/Report1!A186 → 數值行186 |
| 意義候選 | 借款／發債取得之現金 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 借款流入、發股流入與資產出售收款不是同義；不使用同一行號跨公司取數 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR04-Report1-A187

原始英文：`　　Repurchase of common stock`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行187；OR04/Insulet/Quarter/Report1!A187 → 數值行187 |
| 意義候選 | 股份買回相關付款，需辨識普通股、庫藏股或代扣稅 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 員工代扣稅款與普通股買回的涵蓋範圍須另核 |
| 既有代碼 | METRICS候選：無；raw候選：buybacks。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | us-gaap:PaymentsForRepurchaseOfCommonStock → raw.buybacks |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-058, ISS-062。 |

## OR05-Report1-A133

原始英文：`　　Depreciation and amortization`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行133；OR05/TransUnion/Quarter/Report1!A133 → 數值行133; OR06/TransUnion/Quarter/Report1!A133 → 數值行133; OR11/TransUnion/Year/Report1!A133 → 數值行133 |
| 意義候選 | 營業現金流中的非現金折舊攤銷調整 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源間接法明列之調整 |
| 排除與不可替代項 | 不預設等同IS補充D&A或全公司EBITDA輸入；不得重複回加 |
| 既有代碼 | METRICS候選：da；raw候選：da。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | us-gaap:DepreciationDepletionAndAmortization → raw.da |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：DER-07。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-007, ISS-059。 |

## OR05-Report1-A134

原始英文：`　　Loss on repayment of loans`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行134；OR05/TransUnion/Quarter/Report1!A134 → 數值行134; OR06/TransUnion/Quarter/Report1!A134 → 數值行134; OR11/TransUnion/Year/Report1!A134 → 數值行134 |
| 意義候選 | 償還融資現金流；須逐項辨識本金、借款種類及費用 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 廣義還債tag不證明是該項特定借款；不等同debt service，亦不預設包含利息或融資租賃 |
| 既有代碼 | METRICS候選：無；raw候選：debt_repayment, debt_repayment_lt。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | us-gaap:RepaymentsOfDebt → raw.debt_repayment; us-gaap:RepaymentsOfLongTermDebt → raw.debt_repayment_lt |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-008。 |

## OR05-Report1-A135

原始英文：`　　Deferred taxes`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行135；OR05/TransUnion/Quarter/Report1!A135 → 數值行135; OR06/TransUnion/Quarter/Report1!A135 → 數值行135; OR11/TransUnion/Year/Report1!A135 → 數值行135 |
| 意義候選 | 來源CF原文所指之現金流或調整項，須逐項核附註 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 不只依名稱、行號或金額相同判定其經濟內容 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-009, ISS-053。 |

## OR05-Report1-A136

原始英文：`　　Stock-based compensation`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行136；OR05/TransUnion/Quarter/Report1!A136 → 數值行136; OR06/TransUnion/Quarter/Report1!A136 → 數值行136; OR11/TransUnion/Year/Report1!A136 → 數值行136 |
| 意義候選 | 來源間接法中的非現金損益／費用調整 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 損益表金額不必然等於CF回加；須核範圍、符號及是否已在其他調整中包含 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-010。 |

## OR05-Report1-A143

原始英文：`　　Other`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行143；OR05/TransUnion/Quarter/Report1!A143 → 數值行143; OR06/TransUnion/Quarter/Report1!A143 → 數值行143; OR08/XPO/Year/Report1!A143 → 數值行143; OR11/TransUnion/Year/Report1!A143 → 數值行143 |
| 意義候選 | 來源該活動分類的其他調整／流量；必須取得組成 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 不能作為現金不勾稽的補差欄或從其他公司挪用 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-016, ISS-055, ISS-064。 |

## OR05-Report1-A145

原始英文：`　　Trade accounts receivable`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行145；OR05/TransUnion/Quarter/Report1!A145 → 數值行145; OR06/TransUnion/Quarter/Report1!A145 → 數值行145; OR11/TransUnion/Year/Report1!A145 → 數值行145 |
| 意義候選 | 營業相關資產負債變動或其他CF調整；必須核實是變動而非餘額 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | BS時點餘額tag不適用此處流量；不以兩期餘額差代替完整CF調整，除非已核非現金與合併變動 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-017, ISS-066。 |

## OR05-Report1-A146

原始英文：`　　Other current and long-term assets`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行146；OR05/TransUnion/Quarter/Report1!A146 → 數值行146; OR06/TransUnion/Quarter/Report1!A146 → 數值行146; OR11/TransUnion/Year/Report1!A146 → 數值行146 |
| 意義候選 | 營業相關資產負債變動或其他CF調整；必須核實是變動而非餘額 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | BS時點餘額tag不適用此處流量；不以兩期餘額差代替完整CF調整，除非已核非現金與合併變動 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-018。 |

## OR05-Report1-A147

原始英文：`　　Trade accounts payable`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行147；OR05/TransUnion/Quarter/Report1!A147 → 數值行147; OR06/TransUnion/Quarter/Report1!A147 → 數值行147; OR11/TransUnion/Year/Report1!A147 → 數值行147 |
| 意義候選 | 營業相關資產負債變動或其他CF調整；必須核實是變動而非餘額 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | BS時點餘額tag不適用此處流量；不以兩期餘額差代替完整CF調整，除非已核非現金與合併變動 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-019。 |

## OR05-Report1-A148

原始英文：`　　Other current and long-term liabilities`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行148；OR05/TransUnion/Quarter/Report1!A148 → 數值行148; OR06/TransUnion/Quarter/Report1!A148 → 數值行148; OR11/TransUnion/Year/Report1!A148 → 數值行148 |
| 意義候選 | 營業相關資產負債變動或其他CF調整；必須核實是變動而非餘額 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | BS時點餘額tag不適用此處流量；不以兩期餘額差代替完整CF調整，除非已核非現金與合併變動 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-020。 |

## OR05-Report1-A162

原始英文：`　　Proceeds from sale/maturities of other investments`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行162；OR05/TransUnion/Quarter/Report1!A162 → 數值行162; OR06/TransUnion/Quarter/Report1!A162 → 數值行162; OR11/TransUnion/Year/Report1!A162 → 數值行162 |
| 意義候選 | 資產／投資出售、到期或其他處分收款 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 借款流入、發股流入與資產出售收款不是同義；不使用同一行號跨公司取數 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-029。 |

## OR05-Report1-A163

原始英文：`　　Investments in nonconsolidated affiliates and notes receivable`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行163；OR05/TransUnion/Quarter/Report1!A163 → 數值行163; OR06/TransUnion/Quarter/Report1!A163 → 數值行163; OR11/TransUnion/Year/Report1!A163 → 數值行163 |
| 意義候選 | 營業相關資產負債變動或其他CF調整；必須核實是變動而非餘額 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | BS時點餘額tag不適用此處流量；不以兩期餘額差代替完整CF調整，除非已核非現金與合併變動 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-030。 |

## OR05-Report1-A175

原始英文：`　　Proceeds from term loans`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行175；OR05/TransUnion/Quarter/Report1!A175 → 數值行175; OR06/TransUnion/Quarter/Report1!A175 → 數值行175; OR11/TransUnion/Year/Report1!A175 → 數值行175 |
| 意義候選 | 借款／發債取得之現金 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 借款流入、發股流入與資產出售收款不是同義；不使用同一行號跨公司取數 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-035。 |

## OR05-Report1-A176

原始英文：`　　Repayments of term loans`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行176；OR05/TransUnion/Quarter/Report1!A176 → 數值行176; OR06/TransUnion/Quarter/Report1!A176 → 數值行176; OR11/TransUnion/Year/Report1!A176 → 數值行176 |
| 意義候選 | 償還融資現金流；須逐項辨識本金、借款種類及費用 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 廣義還債tag不證明是該項特定借款；不等同debt service，亦不預設包含利息或融資租賃 |
| 既有代碼 | METRICS候選：無；raw候選：debt_repayment, debt_repayment_lt。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | us-gaap:RepaymentsOfDebt → raw.debt_repayment; us-gaap:RepaymentsOfLongTermDebt → raw.debt_repayment_lt |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-036。 |

## OR05-Report1-A177

原始英文：`　　Repayments of debt`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行177；OR05/TransUnion/Quarter/Report1!A177 → 數值行177; OR06/TransUnion/Quarter/Report1!A177 → 數值行177; OR11/TransUnion/Year/Report1!A177 → 數值行177 |
| 意義候選 | 償還融資現金流；須逐項辨識本金、借款種類及費用 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 廣義還債tag不證明是該項特定借款；不等同debt service，亦不預設包含利息或融資租賃 |
| 既有代碼 | METRICS候選：無；raw候選：debt_repayment, debt_repayment_lt。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | us-gaap:RepaymentsOfDebt → raw.debt_repayment; us-gaap:RepaymentsOfLongTermDebt → raw.debt_repayment_lt |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-037。 |

## OR05-Report1-A178

原始英文：`　　Debt financing fees`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行178；OR05/TransUnion/Quarter/Report1!A178 → 數值行178; OR06/TransUnion/Quarter/Report1!A178 → 數值行178; OR11/TransUnion/Year/Report1!A178 → 數值行178 |
| 意義候選 | 支付或遞延處理的債務發行／融資成本 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 費用認列、實付現金與借款淨收款須區分；不可直接當償還本金 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-038。 |

## OR05-Report1-A179

原始英文：`　　Dividends to shareholders`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行179；OR05/TransUnion/Quarter/Report1!A179 → 數值行179; OR06/TransUnion/Quarter/Report1!A179 → 數值行179; OR11/TransUnion/Year/Report1!A179 → 數值行179 |
| 意義候選 | 股利支付現金 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 不等同宣告股利、應付股利或收取股利 |
| 既有代碼 | METRICS候選：無；raw候選：dividends_paid。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註；Related-party transactions／關係人交易附註；核對交易對手及合併沖銷 |
| 候選XBRL tags | us-gaap:PaymentsOfDividendsCommonStock → raw.dividends_paid |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-039。 |

## OR05-Report1-A180

原始英文：`　　Proceeds from issuance of common stock`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行180；OR05/TransUnion/Quarter/Report1!A180 → 數值行180; OR06/TransUnion/Quarter/Report1!A180 → 數值行180; OR11/TransUnion/Year/Report1!A180 → 數值行180 |
| 意義候選 | 發行股份、員工行使選擇權或購股計畫之收款 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 借款流入、發股流入與資產出售收款不是同義；不使用同一行號跨公司取數 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-040。 |

## OR05-Report1-A181

原始英文：`　　Employee taxes paid on restricted stock units recorded as treasury stock`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行181；OR05/TransUnion/Quarter/Report1!A181 → 數值行181; OR06/TransUnion/Quarter/Report1!A181 → 數值行181; OR11/TransUnion/Year/Report1!A181 → 數值行181 |
| 意義候選 | 股份買回相關付款，需辨識普通股、庫藏股或代扣稅 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 員工代扣稅款與普通股買回的涵蓋範圍須另核 |
| 既有代碼 | METRICS候選：無；raw候選：buybacks。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | us-gaap:PaymentsForRepurchaseOfCommonStock → raw.buybacks |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-041。 |

## OR05-Report1-A182

原始英文：`　　Repurchase of common stock`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行182；OR05/TransUnion/Quarter/Report1!A182 → 數值行182; OR06/TransUnion/Quarter/Report1!A182 → 數值行182; OR11/TransUnion/Year/Report1!A182 → 數值行182 |
| 意義候選 | 股份買回相關付款，需辨識普通股、庫藏股或代扣稅 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 員工代扣稅款與普通股買回的涵蓋範圍須另核 |
| 既有代碼 | METRICS候選：無；raw候選：buybacks。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | us-gaap:PaymentsForRepurchaseOfCommonStock → raw.buybacks |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-042, ISS-058, ISS-062。 |

## OR05-Report1-A183

原始英文：`　　Proceeds from revolving credit facility`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行183；OR05/TransUnion/Quarter/Report1!A183 → 數值行183; OR06/TransUnion/Quarter/Report1!A183 → 數值行183 |
| 意義候選 | 借款／發債取得之現金 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 借款流入、發股流入與資產出售收款不是同義；不使用同一行號跨公司取數 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-043。 |

## OR07-Report1-A108

原始英文：`Impairment of an equity method investment`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | IS 名稱行108；OR07/Nexstar/Year/Report1!A108 → 數值行108 |
| 意義候選 | 採權益法投資減損損失 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 該公司該期該名稱實際損失 |
| 排除與不可替代項 | 不能將本行跨公司或跨檔固定為一種損失；CF回加數另核 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Operations / Income；損益表；該收入／成本／費用及稅項附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-048。 |

## OR07-Report1-A142

原始英文：`　　Impairment of an equity method investment`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行142；OR07/Nexstar/Year/Report1!A142 → 數值行142 |
| 意義候選 | 來源間接法中的非現金損益／費用調整 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 損益表金額不必然等於CF回加；須核範圍、符號及是否已在其他調整中包含 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-015。 |

## OR07-Report1-A154

原始英文：`　　Income tax paid`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行154；OR07/Nexstar/Year/Report1!A154 → 數值行154 |
| 意義候選 | 來源CF中的稅款支付、稅項變動或遞延稅調整，依原文確認 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | Income tax payable、Income tax paid及Deferred taxes不可互換；不能套用所得稅費用tag |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-026。 |

## OR08-Report1-A22

原始英文：`Current assets of discontinued operations`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | BS 名稱行22；OR08/XPO/Year/Report1!A22 → 數值行22 |
| 意義候選 | 停業單位分類之流動資產 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源已分類的停業單位流動資產 |
| 排除與不可替代項 | 不與持續營業的流動資產重複加總 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Balance Sheets；資產負債表；該資產／負債／權益附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=instant；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR08-Report1-A52

原始英文：`Current Liabilities of discontinued operations`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | BS 名稱行52；OR08/XPO/Year/Report1!A52 → 數值行52 |
| 意義候選 | 停業單位之流動負債 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源停業單位分類負債 |
| 排除與不可替代項 | 不與已包含於主表的小計重複 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Balance Sheets；資產負債表；該資產／負債／權益附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=instant；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR08-Report1-A57

原始英文：`Other Long Term Debt`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | BS 名稱行57；OR08/XPO/Year/Report1!A57 → 數值行57 |
| 意義候選 | 其他長期債務；若僅稱Other則組成仍未定 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源特定長期負債／債務組成 |
| 排除與不可替代項 | 不預設為全部Other Liabilities；不決定租賃與Total Debt範圍 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Balance Sheets；資產負債表；該資產／負債／權益附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=instant；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | DEC-02；ISS-005。 |

## OR08-Report1-A89

原始英文：`Purchased transportation`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | IS 名稱行89；OR08/XPO/Year/Report1!A89 → 數值行89 |
| 意義候選 | 外購運輸服務成本 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源運輸服務成本 |
| 排除與不可替代項 | 不依產業別或固定行號外推其他公司科目 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Operations / Income；損益表；該收入／成本／費用及稅項附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR08-Report1-A90

原始英文：`Fuel, operating expenses and supplies`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | IS 名稱行90；OR08/XPO/Year/Report1!A90 → 數值行90 |
| 意義候選 | 燃料、營運費用及耗材成本 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源該成本組成 |
| 排除與不可替代項 | 不預設等同全部營業費用 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Operations / Income；損益表；該收入／成本／費用及稅項附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## OR08-Report1-A91

原始英文：`Depreciation and amortization expense`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | IS 名稱行91；OR08/XPO/Year/Report1!A91 → 數值行91 |
| 意義候選 | 列於營業成本中的折舊攤銷 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源該成本位置之折舊攤銷 |
| 排除與不可替代項 | 不得直接當全公司D&A或再扣一次費用 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Operations / Income；損益表；該收入／成本／費用及稅項附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-059。 |

## OR08-Report1-A102

原始英文：`Gain On Sale of Fixed Asset`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | IS 名稱行102；OR08/XPO/Year/Report1!A102 → 數值行102 |
| 意義候選 | 處分固定資產利益 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源資產處分損益 |
| 排除與不可替代項 | 出售現金收款不是處分利益 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Operations / Income；損益表；該收入／成本／費用及稅項附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：無核准推導式，只能查來源。 |
| 核准公式／推導條件引用 | 無獨立核准算式；不得自行建立缺項補值式。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-047。 |

## OR08-Report1-A133

原始英文：`　　Depreciation and Amortization`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行133；OR08/XPO/Year/Report1!A133 → 數值行133 |
| 意義候選 | 營業現金流中的非現金折舊攤銷調整 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 來源間接法明列之調整 |
| 排除與不可替代項 | 不預設等同IS補充D&A或全公司EBITDA輸入；不得重複回加 |
| 既有代碼 | METRICS候選：da；raw候選：da。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | us-gaap:DepreciationDepletionAndAmortization → raw.da |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 直接查找原始揭露；尚未核准組成關係時不加總、不推導；規則：DER-07。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-007, ISS-059。 |

## OR08-Report1-A134

原始英文：`　　Stock compensation expense`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行134；OR08/XPO/Year/Report1!A134 → 數值行134 |
| 意義候選 | 來源間接法中的非現金損益／費用調整 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 損益表金額不必然等於CF回加；須核範圍、符號及是否已在其他調整中包含 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-008。 |

## OR08-Report1-A135

原始英文：`　　Accretion of debt`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行135；OR08/XPO/Year/Report1!A135 → 數值行135 |
| 意義候選 | 來源間接法中的非現金損益／費用調整 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 損益表金額不必然等於CF回加；須核範圍、符號及是否已在其他調整中包含 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-009。 |

## OR08-Report1-A136

原始英文：`　　Deferred tax expense`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行136；OR08/XPO/Year/Report1!A136 → 數值行136 |
| 意義候選 | 來源CF原文所指之現金流或調整項，須逐項核附註 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 不只依名稱、行號或金額相同判定其經濟內容 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-010。 |

## OR08-Report1-A137

原始英文：`　　Gains on sales of property and equipment`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行137；OR08/XPO/Year/Report1!A137 → 數值行137 |
| 意義候選 | 來源間接法中的非現金損益／費用調整 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 損益表金額不必然等於CF回加；須核範圍、符號及是否已在其他調整中包含 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-011。 |

## OR08-Report1-A146

原始英文：`　　Accounts payable`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行146；OR08/XPO/Year/Report1!A146 → 數值行146 |
| 意義候選 | 營業相關資產負債變動或其他CF調整；必須核實是變動而非餘額 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | BS時點餘額tag不適用此處流量；不以兩期餘額差代替完整CF調整，除非已核非現金與合併變動 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-018, ISS-051。 |

## OR08-Report1-A147

原始英文：`　　Accrued expenses and other liabilities`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行147；OR08/XPO/Year/Report1!A147 → 數值行147 |
| 意義候選 | 營業相關資產負債變動或其他CF調整；必須核實是變動而非餘額 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | BS時點餘額tag不適用此處流量；不以兩期餘額差代替完整CF調整，除非已核非現金與合併變動 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-019, ISS-052。 |

## OR08-Report1-A161

原始英文：`　　Payment for purchases of property and equipment`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行161；OR08/XPO/Year/Report1!A161 → 數值行161 |
| 意義候選 | 購置資本資產付款 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 軟體、租賃或併購可能另列；不可把CapEx當作償還本金 |
| 既有代碼 | METRICS候選：無；raw候選：capex。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | us-gaap:PaymentsToAcquirePropertyPlantAndEquipment → raw.capex |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-028。 |

## OR08-Report1-A162

原始英文：`　　Proceeds from sale of property and equipment`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行162；OR08/XPO/Year/Report1!A162 → 數值行162 |
| 意義候選 | 資產／投資出售、到期或其他處分收款 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 借款流入、發股流入與資產出售收款不是同義；不使用同一行號跨公司取數 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-029。 |

## OR08-Report1-A175

原始英文：`　　Repayment of debt and finance leases`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行175；OR08/XPO/Year/Report1!A175 → 數值行175 |
| 意義候選 | 償還融資現金流；須逐項辨識本金、借款種類及費用 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 廣義還債tag不證明是該項特定借款；不等同debt service，亦不預設包含利息或融資租賃 |
| 既有代碼 | METRICS候選：無；raw候選：debt_repayment, debt_repayment_lt。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | us-gaap:RepaymentsOfDebt → raw.debt_repayment; us-gaap:RepaymentsOfLongTermDebt → raw.debt_repayment_lt |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-035。 |

## OR08-Report1-A176

原始英文：`　　Payment for debt issuance costs`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行176；OR08/XPO/Year/Report1!A176 → 數值行176 |
| 意義候選 | 支付或遞延處理的債務發行／融資成本 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 費用認列、實付現金與借款淨收款須區分；不可直接當償還本金 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-036。 |

## OR08-Report1-A177

原始英文：`　　Repurchase of common stock`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行177；OR08/XPO/Year/Report1!A177 → 數值行177 |
| 意義候選 | 股份買回相關付款，需辨識普通股、庫藏股或代扣稅 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 員工代扣稅款與普通股買回的涵蓋範圍須另核 |
| 既有代碼 | METRICS候選：無；raw候選：buybacks。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | us-gaap:PaymentsForRepurchaseOfCommonStock → raw.buybacks |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-037, ISS-058, ISS-062。 |

## OR08-Report1-A178

原始英文：`　　Change in bank overdrafts`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行178；OR08/XPO/Year/Report1!A178 → 數值行178 |
| 意義候選 | 來源CF原文所指之現金流或調整項，須逐項核附註 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 不只依名稱、行號或金額相同判定其經濟內容 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-038。 |

## OR08-Report1-A179

原始英文：`　　Payment for tax withholdings for restricted shares`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行179；OR08/XPO/Year/Report1!A179 → 數值行179 |
| 意義候選 | 股權薪酬相關員工代扣稅款之付款 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 不是企業所得稅費用；與買回股份或融資費用的涵蓋範圍須核對 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-039。 |

## OR08-Report1-A180

原始英文：`　　Repurchase of debt`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行180；OR08/XPO/Year/Report1!A180 → 數值行180 |
| 意義候選 | 買回債務之現金付款 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 不要套用普通股買回tag或將帳面債務減少視為付款 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註；依原文主題查所得稅／債務利息／租賃／無形資產附註，不只讀tag |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-040。 |

## OR08-Report1-A181

原始英文：`　　Distribution from RXO and GXO spins, net`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行181；OR08/XPO/Year/Report1!A181 → 數值行181 |
| 意義候選 | 來源CF原文所指之現金流或調整項，須逐項核附註 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 不只依名稱、行號或金額相同判定其經濟內容 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；ISS-041。 |

## OR08-Report1-A192

原始英文：`　　Net cash provided by (used in) discontinued operations`

| 欄位 | 逐項查找與核對規則 |
|---|---|
| 位置與來源 | CF 名稱行192；OR08/XPO/Year/Report1!A192 → 數值行192 |
| 意義候選 | 來源CF原文所指之現金流或調整項，須逐項核附註 |
| 合併範圍 | 依G04逐期核對；entity-wide不是母公司／合併／非控制權益範圍自動相同的證據。 |
| 包含候選 | 僅來源逐項證實且不重疊之交易 |
| 排除與不可替代項 | 不只依名稱、行號或金額相同判定其經濟內容 |
| 既有代碼 | METRICS候選：無；raw候選：無。兩者不可互換。 |
| SEC查找位置 | Consolidated Statements of Cash Flows；現金流量表與補充揭露；現金／受限制現金調節及相關交易附註 |
| 候選XBRL tags | 未登錄可靠候選；須查當期iXBRL／附註，不能猜造名稱。 |
| 計算輸入tag候選 | 沒有獨立計算輸入，或須先核定完整組成。 |
| 接受條件 | G01–G10全部適用；候選tag不自動代表有效對應。 |
| 取值／加總／推導 | 來源原文、活動分類及附註逐項核對；現金流正負號依來源語義與契約轉換，不直接照抄付款tag正值為流入；規則：DER-07, DER-08。 |
| 核准公式／推導條件引用 | DER-07: Σ 已確認、不重疊的組成項目（依來源符號處理減項）；資產、負債、權益、收入、費用及三類現金流的小計須有來源支持的組成關係。未揭露明細不能一律當0，已披露總額也不能因明細未齊而被不完整加總覆蓋。；DER-08: Ending Cash − Beginning Cash = CFO + CFI + CFF + FX + 其他經核實的調節項；期初、期末及變動均須採相同現金定義；核對受限制現金、匯率、停業單位及其他來源列示項目的涵蓋範圍，避免重複計入。缺少必要橋接項時，只能記錄未勾稽，不得反推未知項或宣稱計算的期末現金為已確認來源值。 |
| 必要輸入與版本 | 直接值需要當期來源證據；明細加總須先核完整組成；未登錄的輸入名稱不是新metric key。公式版本依核准規格。 |
| 單位與期間 | 參考值型=money（非新契約enum）；同幣別、原值與scale分別保留；money以Decimal正規化，不換幣。比率與天數依CF定義；period_kind=duration；使用已核實的FY／YTD／時點／LTM角色，不能沿用Excel預設日期。 |
| 找不到時 | 依F01–F07補查並保留狀態；不得填0或反推。 |
| 必須保留證據 | 依E01；含各輸入fact IDs、文件版本、來源原值與精確位置。 |
| 待確認 | 逐期來源定義仍待核；另見全部84項盤點待確認清單。 |

## 最終報表既有代碼補充

以下直接重用METRICS。Excel沒有某項，不代表可刪除最終報表要求，也不代表可新增不同名稱的替代科目。

| 既有key | 定義 | 單位／期間 | 公式／規則 | 待確認 |
|---|---|---|---|---|
| revenue | Source revenue or net sales | money / duration | FMT-A1/FMT-Q1 | 仍須來源核驗 |
| cost_of_revenue | Source cost of revenue, sales or services | money / duration | FMT-A1/FMT-Q1 | 仍須來源核驗 |
| gross_profit | Source gross profit; derive only with verified identity | money / duration | CALC-14 | 仍須來源核驗 |
| operating_expense | Operating expense excluding cost of revenue; verified scope | money / duration | CALC-14 | 仍須來源核驗 |
| operating_income | Source operating profit | money / duration | FMT-A1/FMT-Q1 | 仍須來源核驗 |
| interest_expense | Interest expense with verified gross/net definition | money / duration | FMT-A1/FMT-A4/FMT-Q1 | DEC-05 |
| pretax_profit | Source pre-tax profit; preserve signed tax benefits in identities | money / duration | CALC-14 | 仍須來源核驗 |
| income_tax | Signed income tax expense or benefit | money / duration | CALC-14 | 仍須來源核驗 |
| net_income | Source net income with consolidation scope | money / duration | FMT-A1/FMT-Q1 | 仍須來源核驗 |
| beginning_cash | Cash at start of fiscal period, consistent cash definition | money / opening | CALC-15 | 仍須來源核驗 |
| cfo | Net cash inflow/outflow from operating activities | money / duration | CF-03 | 仍須來源核驗 |
| cfi | Net cash inflow/outflow from investing activities | money / duration | FMT-A2 | 仍須來源核驗 |
| cff | Net cash inflow/outflow from financing activities | money / duration | FMT-A2 | 仍須來源核驗 |
| ending_cash | Cash at fiscal period end, consistent cash definition | money / instant | CALC-15 | 仍須來源核驗 |
| cash_change | Ending cash - beginning cash; full FX/restricted-cash bridge required | money / duration | CASH-CHANGE-v1 | 仍須來源核驗 |
| current_ratio | Current Assets / Current Liabilities | percent / instant | CF-01 | 仍須來源核驗 |
| quick_ratio | Quick Assets / Current Liabilities | percent / instant | CF-02 | DEC-01 |
| cash_flow_ratio | CFO / Current Liabilities | percent / duration | CF-03 | 仍須來源核驗 |
| debt_ratio | Total Liabilities / Net Worth | percent / instant | CF-06 | DEC-02 |
| interest_coverage | (Pre-tax Profit + Interest Expense) / (Interest Expense + Capitalized Interest) | multiple / duration | CF-04 | DEC-05 |
| total_debt | Verified debt components, lease treatment and scope; not total liabilities | money / instant | CALC-09 | DEC-02 |
| debt_service | Pending approved debt-service definition; no CapEx proxy | money / duration | CALC-10 | DEC-03 |
| ltm_ebitda | Complete fiscal-year EBITDA ending at the column date, with explicit basis | money / ltm | CALC-11/CALC-12 | DEC-06 |
| ebitda_basis | Source and actual EBITDA definition, including adjustments | text / ltm | FMT-A4/FMT-Q3 | DEC-06 |
| total_leverage | Total debt / applicable LTM EBITDA | multiple / ltm | LEVERAGE-v1 | DEC-02, DEC-06 |
| ebitda_interest | (Pre-tax Profit + Interest Expense + D&A) / (Interest Expense + Capitalized Interest) | multiple / duration | CF-05 | DEC-05 |
| dscr | Pending approved DSCR numerator and debt-service definition | multiple / duration | CALC-10 | DEC-03 |
| revenue_growth | (Current Year Revenues - Previous Year Revenues) / Previous Year Revenues | percent / duration | CF-09 | 仍須來源核驗 |
| gross_margin | Gross Profit / Revenues | percent / duration | CF-10 | 仍須來源核驗 |
| operating_margin | Operating Profit / Revenues | percent / duration | CF-11 | 仍須來源核驗 |
| pretax_margin | Pre-tax Profit / Revenues | percent / duration | CF-12 | 仍須來源核驗 |
| operating_margin_change | Current Operating Profit Margin - Previous Operating Profit Margin | percentage_points / duration | CF-16 | 仍須來源核驗 |
| current_assets | Verified source Current Assets | money / instant | DATA-01 | 仍須來源核驗 |
| current_liabilities | Verified source Current Liabilities | money / instant | DATA-01 | 仍須來源核驗 |
| quick_assets | Verified source Quick Assets | money / instant | DATA-01 | DEC-01 |
| total_liabilities | Verified source Total Liabilities | money / instant | DATA-01 | 仍須來源核驗 |
| net_worth | Verified source Net Worth | money / instant | DATA-01 | DEC-02 |
| capitalized_interest | Verified source Capitalized Interest | money / duration | DATA-01 | DEC-05 |
| da | Verified source Depreciation & Amortization | money / duration | DATA-01 | 仍須來源核驗 |
