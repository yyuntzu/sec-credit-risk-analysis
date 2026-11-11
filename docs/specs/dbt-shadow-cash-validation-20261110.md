# CASH-CHANGE 影子採用驗證

日期：2026-11-10。限 SYNTHETIC-ONLY 測試；精度待定、未發布、未切換 cloud authority。

## 執行邊界

新增 `int_review_shadow_calculated`，保存原本的來源採用與分層公式結果。Reconciliation model 改讀這個中間層，再由最終 `fct_review_shadow_facts` 採用已覆核的現金變動，避免 facts → reconciliation → facts 的循環。下游 readiness、敘述、input bridge、consumer 均讀最終 Facts。

Cash bridge 必須包含 beginning、CFO、CFI、CFF、FX、other 六個有序 terms 與 ending，來源 lineage、期間、幣別、範圍、精度 tolerance、覆核 claim 均經 SQL 驗證。至少一份相符 definition evidence 才能採用 CASH-CHANGE；kind=review 可支援對帳，但不授權條件式現金推算。覆核日期晚於 as_of 會被拒絕。

放行後 BigQuery 執行 ending−beginning，保留 `[ending_cash, beginning_cash]` 的有序 Fact IDs、來源 lineage 與 definition evidence。沒有 FX／other 等資料時不補零；來源衝突／不適用狀態不能被改成 calculated。Python `baseline_reviewed_cash()` 只作遷移比對，consumer 不呼叫它，也不呼叫 Python 財務引擎。

## 原生 BigQuery 結果

Project `focus-heuristic-438521-v4`、location US、獨立 `sec_review_shadow_<run_id>` datasets；表七天到期。

| 案例 | run_id | Facts | verified 對帳 | CASH-CHANGE |
| --- | --- | ---: | ---: | --- |
| Annual 完整覆核 | ec2732e6eb8f4f0682c83e241f4cf993 | 186 | 8 | 四個 FY 均 calculated，20−10＝10 |
| Quarterly 保留缺口 | c963214b7868405aa3e513656ae743cd | 124 | 4 | 版型沒有現金流量表，不新增現金變動列 |
| 偽造／不完整覆核 | a1ab9495ede34047b9ea08df3ed82440 | 186 | 0 | 四個 FY 均 not_calculable，值為 NULL |

三份均完成 13 個 dbt models、一項完整性 test、48 個手算 kernels，並成功產生收據綁定的候選 MD／JSON／HTML。Fact、reconciliation、readiness、commentary 的未知 mismatch 均為零。數值精度差異依序 26／18／26，維持未核准分類，不算切換通過。

Quarterly 合成來源未提供必要的完整現金橋接，仍未通過整份財務驗收；沒有把 expected coverage 從八項降低到四項，也沒有新增報表列。Annual 仍有 DEC-03／DSCR 等既有缺口，不能因現金橋接成功宣稱報告 accepted。

共同 code hash：`c14fc952b3762ab80447440d86fb2d5f479bc762505c7b40243a1ef0564defa4`。

計算收據 SHA256（依序）：

```text
d9c315b5996e32ad6e6b592336b76157e78335c6660285bd8b6387601cd9618b
e905cab73eff9c53733f9a73189c2f47618e18d1a61a4127034da085de983529
4eb8b51d8955f1eafc1f8c4add200ee35e1bce8e281a2ce5e63b609a9ee05034
```

證據位於被忽略的 `outputs/dbt_shadow_cash_validation_20261110/{annual_live,quarterly_live,adversarial_live}`，彙整在 `verified_summary.json`。將 Python baseline_reviewed_cash／approved_formula_value／calculate_report／complete_report／verify_reconciliation 全部替換成一呼叫就失敗的測試函式後，三份仍能完整讀回，共 496 個 Facts。這驗證了 reader 不使用 Python 財務 fallback，不表示雲端發布流程已完成。

## 測試與剩餘範圍

新增單元測試涵蓋完整覆核、無覆核、偽造覆核、只有 review 沒有 definition、刪除必要 term、未來日期及不新增 Quarterly 現金列。最終完整回歸：`REVIEW_EXCEL_TEST=1 python -m unittest discover -s tests`，319 tests、OK、無略過，82.742 秒；包含活頁簿實際匯出與重算，原生 Microsoft Excel 尚未執行。

更廣的來源／財期／精度邊界矩陣、正式交付保存、發布收據、consumer IAM 與回退仍待完成。精度政策未核准，所有正式發布旗標保持 false。
