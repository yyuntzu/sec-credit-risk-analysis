## B. Quarterly Review
### Financial Analysis
#### YTD (Quarterly) Income

Block, Inc.（Square 母公司；XYZ）合併範圍；USD 百萬元；資料截止 2026-10-27。兩期損益均為 1/1–6/30 六個月。
待驗收草稿：master 舊查詢及 dbt 未完整完成；本次另以新入庫 fact IDs 讀回核對 BigQuery，並呼叫 MD&A 模型後人工對照原文整理。

| Metric／科目 | H1 2025 | % revenue | H1 2026 | % revenue |
|---|---:|---:|---:|---:|
| Total net revenue／營業收入 | 11,826.25 | 100.00% | 12,674.53 | 100.00% |
| Cost of revenue／營業成本 | 7,000.12 | 59.19% | 6,599.21 | 52.07% |
| Gross profit／毛利 | 4,826.13 | 40.81% | 6,075.32 | 47.93% |
| Operating expenses／營業費用 | 4,012.54 | 33.93% | 5,800.44 | 45.76% |
| Operating income／營業利益 | 813.60 | 6.88% | 274.88 | 2.17% |
| Gross interest expense／總額利息費用 | 待核實總額 | 無法計算 | 待核實總額 | 無法計算 |
| Income before tax／稅前損益 | 886.43 | 7.50% | (91.10) | -0.72% |
| Income tax expense／所得稅費用 | 159.38 | 1.35% | 130.42 | 1.03% |
| Consolidated net income／合併稅後損益 | 727.06 | 6.15% | (221.53) | -1.75% |

> 合併淨利由已核對的稅前損益減帶符號稅費計算；與股東歸屬損益分開。總額利息尚未完整核實，不以淨額代填。

- 上半年營收由 USD 11,826.25m 增至 12,674.53m（7.17%）。管理階層指出，Commerce enablement 與 Financial solutions 的成長抵銷 Bitcoin ecosystem 收入下降；Cash App Borrow、Square processing 等產品是主要成長來源。
- 毛利成長 25.88%，毛利率由 40.81% 升至 47.93%。低毛利 Bitcoin ecosystem 收入占比下降及較高毛利金融產品成長改善組合；總營收受 Bitcoin 總額認列影響，因此毛利也是重要觀察指標。
- 營業利益由 USD 813.60m 降至 274.88m，營業利益率由 6.88% 降至 2.17%。MD&A 說明訴訟／監管提列、信用損失與 Workforce Plan 重整費用推高營業費用；毛利成長尚未轉為 GAAP 營業利益成長。
- 報表揭露的淨利息費用由 USD 40.93m 增至 108.92m，原文歸因於 2025 年第三季發行的 2030／2033 Senior Notes。這是淨額，未直接填入要求總額費用的正式科目；warehouse 利息另列於 G&A，仍須完整核對。
- 稅前損益由 USD 886.43m 轉為 -91.10m；原文指出，營業利益下降另受 Bitcoin 投資重估由利益轉為損失及淨利息費用增加影響。合併稅後損益由 727.06m 轉為 -221.53m；未將歸屬普通股股東損益混用為合併淨利。

來源：[2026 Q2 10-Q，財務報表、Indebtedness 與 MD&A](https://www.sec.gov/Archives/edgar/data/1512673/000162828026053368/xyz-20260630.htm)。

#### Ratios YTD

| Metric | 2024-12-31 | 2025-06-30 | 2025-12-31 | 2026-06-30 |
|---|---:|---:|---:|---:|
| Current ratio／流動比率 | 232.60% | 195.68% | 220.11% | 220.88% |
| Quick ratio／速動比率 | 待核實 | 待核實 | 待核實 | 待核實 |
| Debt ratio／總負債÷合併權益 | 73.19% | 66.61% | 78.39% | 77.89% |

- 流動比率由 2025 年底 220.11% 變為 2026 年 6 月底 220.88%。該比率包含客戶資金及應付客戶款等支付業務項目，不能單憑比率判定公司可自由償債現金。速動比率保留待核實，未把受限制客戶資金或全部貸款列為 Quick Assets。
- 總負債／含非控制權益的合併權益由 78.39% 降至 77.89%；本表採 liabilities / equity，不是 liabilities / assets。數字已以 assets = liabilities + consolidated equity 勾稽。

#### Leverage Analysis YTD

| Metric | 2024-12-31 | 2025-06-30 | 2025-12-31 | 2026-06-30 |
|---|---:|---:|---:|---:|
| Total debt／借款本金 | 7,631.68 | 5,853.92 | 8,714.88 | 6,936.94 |
| LTM Standard EBITDA | 待核實總額利息 | 待核實總額利息 | 待核實總額利息 | 待核實總額利息 |
| EBITDA basis | NI + Interest + Taxes + D&A | NI + Interest + Taxes + D&A | NI + Interest + Taxes + D&A | NI + Interest + Taxes + D&A |
| Total leverage | 無法計算 | 無法計算 | 無法計算 | 無法計算 |

- 票據本金加 warehouse 借款本金由 2025 年底 USD 8,714.88m 降至 6,936.94m。票據本金下降 USD 1,575.00m，與 2026 年到期票據償還一致；warehouse 餘額下降 202.94m。未將未動用額度或客戶應付款加入借款。
- Standard EBITDA 保留待核實：需總額費用化利息並涵蓋票據及 G&A 中的 warehouse 利息；淨利息費用或公司 Adjusted EBITDA 均不替代。未以 operating income 或 YTD 年化冒充 LTM。
- 總槓桿倍數暫不計算，因 Standard LTM EBITDA 尚未完成。信用判斷上，借款本金下降是可觀察的改善，但毛利成長、GAAP 利潤壓力、貸款信用損失及支付客戶資金限制須一併評估，不能僅以 Adjusted EBITDA 判斷償債能力。