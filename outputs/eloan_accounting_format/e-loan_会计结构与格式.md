# e-loan 会计结构与 Quarter / Year 格式

本报告依据文件夹内 6 个 Quarter 档及 5 个 Year 档的实际内容整理。每档均为 Report1，使用至第 245 行、T 栏。此处是财务报表列报结构，不是带有总账编码的完整会计科目表；下方建议编码为新建格式，并非原档编码。

## 1. 共同结构

| 区域 | 原档位置 | 内容 |
|---|---|---|
| 基本资料 | 1–8 行 | 合并口径、客户名称、识别号、币别、金额单位、汇率、报表日期 |
| 资产负债表 BS | 10–71 行 | 资产、负债、权益与合计 |
| 资产负债补充项目 | 72–73 行 | 存货跌价备抵、坏账损失 |
| 损益表 IS | 80–117 行 | 收入、成本、费用、营业外损益、所得税、税后净利 |
| 损益补充项目 | 118–125 行 | 关联方交易、资本化利息、折旧摊销、租金收入 |
| 现金流量表 CF | 129–194 行 | 期初现金、经营／投资／筹资现金流、汇率影响、期末现金 |
| 财务比率 RATIO | 196–233 行 | 流动性、财务结构、获利能力、周转效率；属于指标，不是会计科目 |
| 财报来源及审计资料 | 235–245 行 | 财报来源、会计师名称、纪律记录等 |

金额栏依次是 D、I、M、R；BS／IS 的对应百分比栏依次是 G、K、P、T。CF 及比率区主要使用 D、I、M、R。BS 百分比以资产总额为基准，IS 百分比以营收为基准。

## 2. Quarter 格式

Quarter 采用「年度—同期累计—年度—本期累计」四栏比较，不能将四栏视为连续四季。

| 科目 | 2024 FY | 2025 同期 YTD | 2025 FY | 2026 本期 YTD |
|---|---|---|---|---|
| BS 日期：Q1 档 | 2024-12-31 | 2025-03-31 | 2025-12-31 | 2026-03-31 |
| IS／CF 期间：Q1 档 | 2024 全年 | 2025-01-01 至 03-31 | 2025 全年 | 2026-01-01 至 03-31 |
| BS 日期：Q2 档 | 2024-12-31 | 2025-06-30 | 2025-12-31 | 2026-06-30 |
| IS／CF 期间：Q2 档 | 2024 全年 | 2025-01-01 至 06-30 | 2025 全年 | 2026-01-01 至 06-30 |

Q2 的 IS／CF 是上半年累计。如需单独第二季，在相同公司、单位、口径下用 Q2 YTD 减 Q1 YTD。BS 是时点余额，不能用这种相减方式产生“单季资产负债表”。本文件夹只有 Nexstar、TransUnion 同时提供 Q1 与 Q2。

## 3. Year 格式

| 科目 | FY2022 | FY2023 | FY2024 | FY2025 |
|---|---|---|---|---|
| BS 日期 | 2022-12-31 | 2023-12-31 | 2024-12-31 | 2025-12-31 |
| IS／CF 期间 | 2022 全年 | 2023 全年 | 2024 全年 | 2025 全年 |

Quarter 与 Year 共用科目主档，但各公司及个别期间的明细名称会变动，不能假定相同行号就是相同科目。

## 4. 建议资料格式

每一列代表「某公司、某报表科目、某一期间」；Quarter／Year 作为来源类型，FY／YTD／POINT_IN_TIME 作为期间口径。

| 字段 | 内容 |
|---|---|
| company | 公司名称 |
| source_type | Quarter / Year |
| statement | BS / IS / CF / RATIO |
| account_code | 自订稳定科目编码，例如 BS.CASH；原档未提供编码 |
| parent_account_code | 上层科目编码，避免明细与小计重复加总 |
| account_name_original | 原始英文科目名称 |
| account_name_cn | 统一中文科目名称 |
| row_type | detail / subtotal / total / metric |
| period_basis | POINT_IN_TIME / FY / YTD；比率另保留原始区间 |
| period_start | IS／CF 起日；BS 留空 |
| period_end | 期间迄日或 BS 日期 |
| currency | USD |
| amount_unit | thousand / million；须逐档保留 |
| amount | 数值；不要混入逗号或单位文字 |
| percentage_or_ratio | 原始百分比或比率值 |
| metric_unit | % / times / day 等 |
| value_status | reported / missing / not_applicable；保留空白与 N.A. 的差别 |
| source_file / source_sheet / source_cell | 来源档、Report1、原始储存格 |

建议显示格式：`报表类别｜科目编码｜上层科目｜中文科目｜原文科目｜期间1金额｜期间1%｜期间2金额｜期间2%｜期间3金额｜期间3%｜期间4金额｜期间4%`。CF 与比率按实际需要呈现金额或指标，不强塞共同比百分比。

## 5. 科目完整对照（按实际出现内容）

下表依原档行号列出两组实际出现的英文科目。同一格以「／」列出不同公司或不同档的名称；这些名称不一定同义，不应直接合并。空白表示该组所有档案在该行均未出现科目名称。

### 资产负债表及补充项目

| 原始行 | Quarter 科目 | Year 科目 |
|---|---|---|
| 10 | Current Assets | Current Assets |
| 11 | Cash & Cash Equivalents | Cash & Cash Equivalents |
| 12 | Financial Assets - Current | Financial Assets - Current |
| 13 | Receivables | Receivables |
| 14 | Notes & Accounts Receivable | Notes & Accounts Receivable |
| 15 | Notes & Accounts Receivable - Related Party | Notes & Accounts Receivable - Related Party |
| 16 | Other receivable | Other receivable |
| 17 | Inventory | Inventory |
| 18 | Prepayments | Prepayments |
| 19 | Income Taxes Receivable ／ Prepaid expenses and other current assets | Income Taxes Receivable ／ Prepaid expenses and other current assets |
| 22 |  | Current assets of discontinued operations |
| 23 | Other Current Assets | Other Current Assets |
| 24 | Funds & Investments | Funds & Investments |
| 26 | Fixed Assets | Fixed Assets |
| 27 | Land | Land |
| 28 | Buildings | Buildings |
| 29 | Machinery Equipment | Machinery Equipment |
| 30 | Transport Equipment | Transport Equipment |
| 31 | Other Fixed Assets | Other Fixed Assets |
| 32 | Less: Accumulated Depreciation & Fixed Asset Impairment | Less: Accumulated Depreciation & Fixed Asset Impairment |
| 33 | Uncompleted Constructions & Prepayments For Equipment Purchases | Uncompleted Constructions & Prepayments For Equipment Purchases |
| 34 | Studio and transmission equipment | Studio and transmission equipment |
| 35 | Intangible Assets | Intangible Assets |
| 36 | Intangible Assets | Intangible Assets |
| 37 | Goodwill | Goodwill |
| 38 | Other Assets | Other Assets |
| 39 | Total Assets | Total Assets |
| 40 | Current Liabilities | Current Liabilities |
| 41 | Short Term Loans (including short term notes payable) | Short Term Loans (including short term notes payable) |
| 43 | Long Term Liabilities Maturing Within One Year | Long Term Liabilities Maturing Within One Year |
| 44 | Payables | Payables |
| 45 | Notes & Accounts Payable | Notes & Accounts Payable |
| 46 | Notes & Accounts Payable - Related Party | Notes & Accounts Payable - Related Party |
| 47 | Accrued Expenses | Accrued Expenses |
| 48 | Advance Receipts ／ Accrued Expenses - Related Party | Advance Receipts ／ Accrued Expenses - Related Party |
| 49 | Amount Owed To/From Shareholders | Amount Owed To/From Shareholders |
| 50 | Income Taxes Payable | Income Taxes Payable |
| 52 |  | Current Liabilities of discontinued operations |
| 53 | Other Current Liabilities | Other Current Liabilities |
| 54 | Long Term Liabilities | Long Term Liabilities |
| 55 | Long Term Bank Loans | Long Term Bank Loans |
| 56 | Corporate Bond Payable | Corporate Bond Payable |
| 57 | Other | Other Long Term Debt ／ Other |
| 58 | Provisions | Provisions |
| 59 | Deferred tax liabilities ／ Long-Term Income Taxes Payable | Deferred tax liabilities ／ Long-Term Income Taxes Payable |
| 60 | Long-Term Operating Lease Liabilities | Long-Term Operating Lease Liabilities |
| 61 | Other Liabilities | Other Liabilities |
| 62 | Total Liabilities | Total Liabilities |
| 63 | Share Capital / Paid-up Capital | Share Capital / Paid-up Capital |
| 65 | Additional paid-in capital | Additional paid-in capital |
| 66 | Retained Earnings | Retained Earnings |
| 67 | Adjustments To Shareholders' Equity | Adjustments To Shareholders' Equity |
| 68 | Less: Treasury Stock | Less: Treasury Stock |
| 69 | Minority Interest | Minority Interest |
| 70 | Total Net Worth | Total Net Worth |
| 71 | Total Liabilities & Net Worth | Total Liabilities & Net Worth |
| 72 | Allowance For Inventory Devaluation | Allowance For Inventory Devaluation |
| 73 | Bad Debt Loss | Bad Debt Loss |

### 损益表及补充项目

| 原始行 | Quarter 科目 | Year 科目 |
|---|---|---|
| 80 | Revenues | Revenues |
| 81 | Net Sales | Net Sales |
| 82 | Other Revenues | Other Revenues |
| 83 | Revenue from related party | Revenue from related party |
| 86 | Operating Cost | Operating Cost |
| 87 | Cost Of Goods Sold | Cost Of Goods Sold |
| 88 | Other Operating Costs | Other Operating Costs |
| 89 |  | Purchased transportation |
| 90 |  | Fuel, operating expenses and supplies |
| 91 |  | Depreciation and amortization expense |
| 92 | Realized Gains On Associated Companies | Realized Gains On Associated Companies |
| 93 | Unrealized Gains On Associated Companies | Unrealized Gains On Associated Companies |
| 94 | Gross Profit | Gross Profit |
| 95 | Bad Debt Expense | Bad Debt Expense |
| 96 | Operating Expense | Operating Expense |
| 97 | Operating Profit | Operating Profit |
| 98 | Non-operating Revenues & Expenses - Net | Non-operating Revenues & Expenses - Net |
| 99 | Non-operating Revenues | Non-operating Revenues |
| 100 | Interest Income | Interest Income |
| 101 | Investment Gains | Investment Gains |
| 102 | Gain On Fixed Asset Disposal | Gain On Fixed Asset Disposal ／ Gain On Sale of Fixed Asset |
| 103 | Gain On Investment Disposal | Gain On Investment Disposal |
| 104 | Other Income | Other Income |
| 105 | Non-operating Expenses | Non-operating Expenses |
| 106 | Interest Expense | Interest Expense |
| 107 | Investment Loss | Investment Loss |
| 108 | Loss on extinguishment of debt ／ Asset impairments ／ Loss On Fixed Asset Disposal | Impairment of an equity method investment ／ Loss On Fixed Asset Disposal ／ Asset impairments |
| 109 | Loss On Investment Disposal | Loss On Investment Disposal |
| 110 | Other Expenses | Other Expenses |
| 111 | Pre-tax Profit (Loss) | Pre-tax Profit (Loss) |
| 112 | Income Tax Expense(Credit) | Income Tax Expense(Credit) |
| 113 | Profit (Loss) From Discontinued Operations ／ Income tax benefit (expense) | Profit (Loss) From Discontinued Operations ／ Income tax benefit (expense) |
| 114 | Extraordinary Profit (Loss) | Extraordinary Profit (Loss) |
| 115 | Cumulative Effects Of Changes In Accounting Policies | Cumulative Effects Of Changes In Accounting Policies |
| 116 | Other Adjustments | Other Adjustments |
| 117 | After-tax Net Profit (Loss) | After-tax Net Profit (Loss) |
| 118 | Sales To Related Parties | Sales To Related Parties |
| 119 | % Of Related Party Sales To Total Sales | % Of Related Party Sales To Total Sales |
| 120 | Capitalized Interest | Capitalized Interest |
| 121 | Depreciation & Amortization | Depreciation & Amortization |
| 122 | Prepayments To Related Parties | Prepayments To Related Parties |
| 123 | (operating income) Rental income from properties | (operating income) Rental income from properties |
| 125 | (non-operating income) Rental income from properties | (non-operating income) Rental income from properties |

### 现金流量表

| 原始行 | Quarter 科目 | Year 科目 |
|---|---|---|
| 129 | Cash and cash equivalents - beginning of period | Cash and cash equivalents - beginning of period |
| 130 | Cash Flow From Operating Activities | Cash Flow From Operating Activities |
| 131 | Net profit (loss) after tax | Net profit (loss) after tax |
| 132 | Income and loss items that do not affect cash flow from operating activities | Income and loss items that do not affect cash flow from operating activities |
| 133 | Depreciation & Amortization ／ Depreciation and amortization expenses ／ Depreciation and amortization | Depreciation & Amortization ／ Depreciation and Amortization ／ Depreciation and amortization expenses ／ Depreciation and amortization |
| 134 | Other Adjustment items ／ Operating lease cost ／ Stock-based compensation expense ／ Loss on repayment of loans | Other Adjustment items ／ Stock compensation expense ／ Operating lease cost ／ Stock-based compensation expense ／ Loss on repayment of loans |
| 135 | Dividend and interest income ／ Inventory donations ／ Deferred income taxes ／ Deferred taxes | Dividend and interest income ／ Accretion of debt ／ Inventory donations ／ Deferred income taxes ／ Deferred taxes |
| 136 | Loss (gain) on valuation of financial assets ／ Provision (recovery) for doubtful accounts, net ／ Non-cash interest expense ／ Stock-based compensation | Loss (gain) on valuation of financial assets ／ Deferred tax expense ／ Provision (recovery) for doubtful accounts, net ／ Non-cash interest expense ／ Stock-based compensation |
| 137 | Investment loss (gain) recognized under equity method ／ Share-based compensation ／ Loss on extinguishment of convertible debt | Investment loss (gain) recognized under equity method ／ Gains on sales of property and equipment ／ Share-based compensation ／ Loss on extinguishment of convertible debt |
| 138 | Loss (gain on reversal) of bad debts ／ Asset impairments ／ Provision for credit losses | Loss (gain on reversal) of bad debts ／ Asset impairments ／ Provision for credit losses |
| 139 | Allowance (reversal) for inventory valuation and obsolescence loss ／ Deferred taxes ／ Unrealized loss (gain) on investments | Allowance (reversal) for inventory valuation and obsolescence loss ／ Deferred taxes ／ Unrealized loss (gain) on investments |
| 140 | Loss (gain) on disposal of investments ／ Loss on disposal of assets | Loss (gain) on disposal of investments ／ Loss on disposal of assets |
| 141 | Loss (gain) on disposal of property, equipment and plant | Loss (gain) on disposal of property, equipment and plant |
| 142 | Unrealized foreign exchange loss (gain) ,net | Impairment of an equity method investment |
| 143 | Payment for broadcast rights ／ Payments for broadcast rights ／ Other non-cash items ／ Others ／ Other | Payments for broadcast rights ／ Other ／ Other non-cash items ／ Others |
| 144 | Changes in assets/liabilities associated with operating activities | Changes in assets/liabilities associated with operating activities |
| 145 | Decrease (Increase) In Accounts Receivable ／ Accounts receivable, net of allowances ／ Accounts receivable ／ Trade accounts receivable | Decrease (Increase) In Accounts Receivable ／ Accounts receivable ／ Accounts receivable, net of allowances ／ Trade accounts receivable |
| 146 | Other receivables ／ Inventories ／ Accounts receivable — related party ／ Other current and long-term assets | Other receivables ／ Accounts payable ／ Inventories ／ Accounts receivable — related party ／ Other current and long-term assets |
| 147 | Decrease (Increase) In Other noncurrent assets ／ Prepaid expenses and other assets ／ Inventories ／ Trade accounts payable | Decrease (Increase) In Other noncurrent assets ／ Accrued expenses and other liabilities ／ Prepaid expenses and other assets ／ Inventories ／ Trade accounts payable |
| 148 | Prepayments ／ Accounts payable ／ Prepaid expenses and other assets ／ Other current and long-term liabilities | Prepayments ／ Accounts payable ／ Prepaid expenses and other assets ／ Other current and long-term liabilities |
| 149 | Increase (Decrease) In Accrued expenses and other current liabilities ／ Accrued expenses and other liabilities ／ Other current assets | Increase (Decrease) In Accrued expenses and other current liabilities ／ Accrued expenses and other liabilities ／ Other current assets |
| 150 | Increase (Decrease) In Accounts Payable ／ Right-of-use assets and operating lease liabilities ／ Accounts payable | Increase (Decrease) In Accounts Payable ／ Right-of-use assets and operating lease liabilities ／ Accounts payable |
| 151 | Expense payable ／ Income taxes ／ Accrued expenses and other liabilities | Expense payable ／ Income taxes ／ Accrued expenses and other liabilities |
| 152 | Unearned receipts ／ Accrued expenses and other liabilities — related party | Unearned receipts ／ Accrued expenses and other liabilities — related party |
| 153 | Increase (Decrease) In Other noncurrent Liabilities ／ Other current liabilities | Increase (Decrease) In Other noncurrent Liabilities ／ Other current liabilities |
| 154 | Income tax payable | Income tax paid |
| 155 | Interest paid | Interest paid |
| 156 | Interest received | Interest received |
| 157 | Dividends received | Dividends received |
| 158 | Other ／ Others | Other ／ Others |
| 159 | Net cash generated by (used in) operating activities | Net cash generated by (used in) operating activities |
| 160 | Cash Flow From Investing Activities | Cash Flow From Investing Activities |
| 161 | Financial assets - current ／ Purchases of property, equipment, and software ／ Capital expenditures | Financial assets - current ／ Payment for purchases of property and equipment ／ Purchases of property, equipment, and software ／ Capital expenditures |
| 162 | Financial assets - non-current ／ Proceeds from disposal of property and equipment ／ Investments in developed software ／ Proceeds from sale/maturities of other investments | Financial assets - non-current ／ Proceeds from sale of property and equipment ／ Proceeds from disposal of property and equipment ／ Investments in developed software ／ Proceeds from sale/maturities of other investments |
| 163 | Investments accounted for using equity method ／ Acquisition of HEYDUDE, net of cash acquired ／ Cash paid for investments ／ Investments in nonconsolidated affiliates and notes receivable | Investments accounted for using equity method ／ Acquisition of HEYDUDE, net of cash acquired ／ Cash paid for investments ／ Investments in nonconsolidated affiliates and notes receivable |
| 164 | Proceeds from disposals of property and equipment ／ Acquisition of other intangible assets | Proceeds from disposals of property and equipment ／ Acquisition of other intangible assets |
| 165 | Intangible assets ／ Acquisition of a business | Intangible assets ／ Acquisition of a business |
| 166 | Dviidends and interest received | Dviidends and interest received |
| 167 | Purchases of property and equipment | Purchases of property and equipment |
| 168 | Proceeds from sale of stations | Proceeds from sale of stations |
| 169 | Payment for acquisition ／ Payments for acquisitions | Payment for acquisition |
| 170 | Proceeds from disposal of an investment |  |
| 171 | Proceeds received from life insurance policies |  |
| 172 | Other ／ Others | Other ／ Others |
| 173 | Net cash generated by (used in) investing activities | Net cash generated by (used in) investing activities |
| 174 | Cash flow from financing activities | Cash flow from financing activities |
| 175 | Repayments of long-term debt ／ Proceeds from notes issuance ／ Proceeds from issuance of term loan, net of issuance costs ／ Proceeds from term loans | Repayments of long-term debt ／ Repayment of debt and finance leases ／ Proceeds from notes issuance ／ Proceeds from issuance of term loan, net of issuance costs ／ Proceeds from term loans |
| 176 | Proceeds from long-term debt, including debt premium and discounts ／ Proceeds from bank borrowings ／ Repayment of term loan ／ Repayments of term loans | Proceeds from long-term debt, including debt premium and discounts ／ Payment for debt issuance costs ／ Proceeds from bank borrowings ／ Repayment of term loan ／ Repayments of term loans |
| 177 | Payables-related parties ／ Repayments of bank borrowings ／ Repayment of equipment financings ／ Repayments of debt | Payables-related parties ／ Repurchase of common stock ／ Repayments of bank borrowings ／ Repayment of equipment financings ／ Repayments of debt |
| 178 | Issuances of bonds payable ／ Deferred debt issuance costs ／ Financing lease payments ／ Debt financing fees | Issuances of bonds payable ／ Change in bank overdrafts ／ Deferred debt issuance costs ／ Financing lease payments ／ Debt financing fees |
| 179 | Repayments of bonds payable ／ Repurchases of common stock ／ Repayment of mortgage ／ Dividends to shareholders | Repayments of bonds payable ／ Payment for tax withholdings for restricted shares ／ Repurchases of common stock ／ Repayment of mortgage ／ Dividends to shareholders |
| 180 | Payments for debt financing costs ／ Repurchases of common stock for tax withholding ／ Proceeds from secured borrowing (Note 6) ／ Proceeds from issuance of common stock | Payments for debt financing costs ／ Repurchase of debt ／ Repurchases of common stock for tax withholding ／ Proceeds from secured borrowing (Note 6) ／ Proceeds from issuance of common stock |
| 181 | Premium paid on debt extinguishment ／ Repayment of secured borrowing (Note 6) ／ Employee taxes paid on restricted stock units recorded as treasury stock | Premium paid on debt extinguishment ／ Distribution from RXO and GXO spins, net ／ Repayment of secured borrowing (Note 6) ／ Employee taxes paid on restricted stock units recorded as treasury stock |
| 182 | Common stock dividends paid ／ Proceeds from exercise of stock options ／ Repurchase of common stock | Common stock dividends paid ／ Proceeds from exercise of stock options ／ Repurchase of common stock |
| 183 | Purchase of treasury stock ／ Proceeds from issuance of common stock under employee stock purchase plan ／ Proceeds from revolving credit facility | Purchase of treasury stock ／ Proceeds from issuance of common stock under employee stock purchase plan |
| 184 | Cash paid for shares withheld for taxes ／ Payment of withholding taxes in connection with vesting of restricted stock units | Payment of withholding taxes in connection with vesting of restricted stock units |
| 185 | Repayment of convertible debt | Repayment of convertible debt |
| 186 | Proceeds from issuance of senior unsecured notes, net of issuance costs | Proceeds from issuance of senior unsecured notes, net of issuance costs |
| 187 | Repurchase of common stock |  |
| 188 | Other ／ Others | Other ／ Others |
| 189 | Net cash generated by (used in) financing activities | Net cash generated by (used in) financing activities |
| 190 | Effects Of Exchange Rate Variation ／ Effect of exchange rate changes | Effects Of Exchange Rate Variation ／ Effect of exchange rate changes |
| 191 | Net Cash Inflow (outflow) for current period | Net Cash Inflow (outflow) for current period |
| 192 |  | Net cash provided by (used in) discontinued operations |
| 194 | Cash and cash equivalents - end of period | Cash and cash equivalents - end of period |

### 财务比率及分组

| 原始行 | Quarter 科目 | Year 科目 |
|---|---|---|
| 196 | Liquidity | Liquidity |
| 197 | Current Ratio | Current Ratio |
| 198 | Quick Ratio | Quick Ratio |
| 199 | Cash Flow Ratio | Cash Flow Ratio |
| 200 | Interest Coverage Ratio | Interest Coverage Ratio |
| 201 | EBITDA / Interest Expenses | EBITDA / Interest Expenses |
| 202 | Financial Structure | Financial Structure |
| 203 | Debt Ratio | Debt Ratio |
| 204 | Fixed Asset To Net Worth Ratio | Fixed Asset To Net Worth Ratio |
| 205 | Fixed Assets To Long Term Capital Ratio | Fixed Assets To Long Term Capital Ratio |
| 206 | Profitability | Profitability |
| 207 | Revenue Growth Rate | Revenue Growth Rate |
| 208 | Gross Profit Margin | Gross Profit Margin |
| 209 | Operating Profit Margin | Operating Profit Margin |
| 210 | Pre-tax Profit Margin | Pre-tax Profit Margin |
| 211 | Return On Net Worth | Return On Net Worth |
| 212 | Return On Asset | Return On Asset |
| 213 | Financial Expense Ratio | Financial Expense Ratio |
| 214 | Change In Operating Profit Margin | Change In Operating Profit Margin |
| 215 | Business Management | Business Management |
| 217 | Accounts Receivable Turnover | Accounts Receivable Turnover |
| 221 | Accounts Payable Turnover | Accounts Payable Turnover |
| 225 | Inventory Turnover | Inventory Turnover |
| 229 | Fixed Asset Turnover | Fixed Asset Turnover |
| 232 | Total Asset Turnover | Total Asset Turnover |

## 6. 使用时需保留的差异

- 单位：Nexstar、CROX 是 USD thousand；Insulet、TransUnion、XPO 是 USD million。跨公司比较前须统一单位。
- 层级：Receivables 与 Notes & Accounts Receivable、Revenues 与 Net Sales 可能分别是小计和明细，不可全数相加。
- 重复名称：第 35、36 行都叫 Intangible Assets；以 Nexstar 为例，第 35 行包含第 36 行及第 37 行 Goodwill，应区分“含商誉无形资产合计”与“其他无形资产”。
- 名称冲突：Nexstar Q2 第 108 行写 Loss on extinguishment of debt，Year 同行写 Impairment of an equity method investment；2025 年对应金额均为 381,000（USD thousand）。这是需要核对原始财报的名称差异，不能仅靠行号映射。
- 比率定义：Nexstar Q2 的 2026 Debt Ratio 为 682.46%，与负债 15,451,000 ÷ 净值 2,264,000 相符；不可仅凭英文名称把它解释成负债／资产。其他比率也应保留原始定义或核对计算口径。
- 原档部分现金流与比率以文字储存；后续自动化应解析数值与单位，并保留原值用于追溯。
- 第 217、221、225、229、232 行是跨行显示的周转指标名称；次数与天数在相邻不同列行，应分别保存。

## 7. 逐档来源

| 类型 | 来源档 | 金额单位 |
|---|---|---|
| Quarter | E-Loan YQYQ-Nexstar Q1.xls | Unit: USD  thousand |
| Quarter | E-Loan YQYQ-Nexstar Q2.xls | Unit: USD  thousand |
| Quarter | e-Loan YQYQ-CROX Q2.xls | Unit: USD  thousand |
| Quarter | e-Loan YQYQ-Insulet Q2.xls | Unit: USD  million |
| Quarter | e-Loan YQYQ-TransUnion Q1.xls | Unit: USD  million |
| Quarter | e-Loan YQYQ-TransUnion Q2.xls | Unit: USD  million |
| Year | E-loan YYYY_Nexstar 2025.xls | Unit: USD  thousand |
| Year | E-loan YYYY_XPO 2025.xls | Unit: USD  million |
| Year | e-Loan YYYY-CROX 2025.xls | Unit: USD  thousand |
| Year | e-Loan YYYY-Insulet 2025.xls | Unit: USD  million |
| Year | e-Loan YYYY-TransUnion 2025.xls | Unit: USD  million |
