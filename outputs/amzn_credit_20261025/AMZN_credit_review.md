## B. Quarterly Review
### Financial Analysis
#### YTD (Quarterly) Income

AMZN consolidated; USD millions; as of 2026-10-25. Requested dates retained. Q1 2025 is three months and Q2 2026 is six months: their income amounts are not directly comparable and no growth rate between those columns is calculated.
Draft: master-branch legacy report queries were blocked by older rows missing company identity; the newly ingested BigQuery records were separately verified by immutable IDs. dbt failed; no final v1.0 acceptance is claimed.

| Metric | Q1 2025 YTD (3 months) | % sales | Q2 2026 YTD (6 months) | % sales |
|---|---:|---:|---:|---:|
| Net sales | 155,667.00 | 100.00% | 382,125.00 | 100.00% |
| Cost of sales | 76,976.00 | 49.45% | 183,241.00 | 47.95% |
| Implied gross profit | 78,691.00 | 50.55% | 198,884.00 | 52.05% |
| Operating expense excluding cost of sales | 60,286.00 | 38.73% | 147,571.00 | 38.62% |
| Operating income | 18,405.00 | 11.82% | 51,313.00 | 13.43% |
| Gross interest expense | 541.00 | 0.35% | 2,114.00 | 0.55% |
| Income before taxes | 21,680.00 | 13.93% | 120,661.00 | 31.58% |
| Income tax expense | 4,553.00 | 2.92% | 27,759.00 | 7.26% |
| Net income | 17,127.00 | 11.00% | 92,902.00 | 24.31% |

- Matched-period context: H1 2026 revenue was $382,125.00m, up 18.17% against H1 2025, not against the requested Q1 2025 column. The filing attributes growth to AWS customer usage and higher retail unit volumes, third-party seller activity, advertising and subscriptions.
- Implied gross margin was 52.05% versus 51.21% in H1 2025. This is revenue less cost of sales, not an Amazon-reported gross-profit subtotal; AWS infrastructure costs also appear elsewhere in operating expenses, limiting interpretation.
- H1 operating margin increased from 11.62% to 13.43%. MD&A identifies AWS growth and retail operating leverage; continued infrastructure investment remains a material expense and funding requirement.
- H1 interest expense increased from $1,057.00m to $2,114.00m. The filing attributes the increase to debt, including new Notes issuances, and finance leases.
- H1 2026 pre-tax earnings include material non-cash Anthropic investment valuation and reclassification gains. Standard EBITDA retains these gains under the selected Net Income + Interest + Taxes + D&A definition; it should not be read as recurring cash earnings.

Source: [Amazon Q2 2026 10-Q, MD&A and financial statements](https://www.sec.gov/Archives/edgar/data/1018724/000101872426000026/amzn-20260630.htm).

#### Ratios YTD

| Metric | 2024-12-31 | 2025-03-31 | 2025-12-31 | 2026-06-30 |
|---|---:|---:|---:|---:|
| Current ratio | 106.37% | 104.81% | 105.08% | 103.31% |
| Quick ratio | Pending verification | Pending verification | Pending verification | Pending verification |
| Debt ratio (liabilities / equity) | 118.52% | 110.31% | 99.01% | 98.63% |

- Current ratio changed from 1.05x at December 2025 to 1.03x at June 2026. Quick ratio remains pending verification of unrestricted cash, liquid securities and eligible net receivables; it is not substituted with current assets less inventory.
- Debt ratio below means total liabilities divided by consolidated equity. Total liabilities are derived from assets less equity and checked against the consolidated balance-sheet structure.

#### Leverage Analysis YTD

| Metric | 2024-12-31 | 2025-03-31 | 2025-12-31 | 2026-06-30 |
|---|---:|---:|---:|---:|
| Total debt | Pending reconciliation | Pending reconciliation | Pending reconciliation | Pending reconciliation |
| LTM Standard EBITDA | 123,714.00 | 134,971.00 | 164,787.00 | 253,427.00 |
| EBITDA basis | NI + Interest + Taxes + D&A | NI + Interest + Taxes + D&A | NI + Interest + Taxes + D&A | NI + Interest + Taxes + D&A |
| Total leverage | Not calculable | Not calculable | Not calculable | Not calculable |

- Total debt and leverage remain pending full reconciliation of borrowings, finance leases and financing obligations. Operating leases are excluded under the previously approved policy; the legacy mart borrowing subtotal is not presented as complete debt.
- The filing reports H1 2026 cash capital expenditure of $96.3bn versus $71.4bn operating cash flow, alongside substantial strategic investment outflows and new borrowing. Credit implication: investment spending is absorbing operating cash generation and increasing reliance on financing. These MD&A amounts are rounded source disclosures.
- Standard EBITDA is calculated for exact LTM windows using prior FY + current YTD - prior comparable YTD for interim dates. It includes non-cash investment gains and has not been substituted with adjusted EBITDA or operating income.