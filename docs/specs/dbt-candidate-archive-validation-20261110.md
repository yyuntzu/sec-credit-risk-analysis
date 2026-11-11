# 候選雲端保存與讀回驗證

日期：2026-11-10。對應 M3 部分工程。精度待定、只做影子比對；未切換正式 authority，未發布財務結果。所有資料均為 `SYNTHETIC-ONLY`，不是實際借款人。

## 保存的內容及邊界

`scripts/candidate_archive.py` 保存固定計算收據、13 份 artifact（含收據）、Facts、Evidence、有序 input bridge、直接／繼承 evidence bridge、SQL 對帳、readiness 及敘述結果。`references/dbt/models/warehouse_candidate/` 建立八個 read-only views；`review_candidate_integrity.sql` 檢查 identity、hash、coverage 與關聯。

每個 attempt 使用獨立實體表；run 綁定來源、plan、計算程式與政策版本。單次 load 使用 `WRITE_EMPTY`、固定 job ID，讀回後重驗內容與 commit digest；相同 attempt 重試必須取得相同結果，不追加或覆寫。BigQuery 的 load 原子性及 job 重試語意依據 [可靠性文件](https://docs.cloud.google.com/bigquery/docs/reliability-intro?hl=en) 與 [Job API](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=en)。這些機制不代替發布門檻或管理權限隔離。

隔離 project：`focus-heuristic-438521-v4`；dataset：`sec_review_shadow_archive_20261110_a74c219e`；location：US。表七天到期，並非正式保留政策或 WORM。dataset 包含一份早期 annual attempt 加以下三份最終 attempt；496 是以下三份的 Facts 合計，不是整個 dataset 的列數。

| 案例 | 原計算 run | archive attempt | Facts |
| --- | --- | --- | ---: |
| Annual | 635cbe41327b4092ab33e36e58565324 | 11111111111111111111111111111111 | 186 |
| Quarterly | 444a70613dcb4f64aa85501be965797e | 22222222222222222222222222222222 | 124 |
| Adversarial | 6e5db6818f934c398fd12d765868c0a8 | 33333333333333333333333333333333 | 186 |

Archive receipt SHA256（依序 Annual、Quarterly、Adversarial）：

```text
2b7978023a429e58122e173b342845aae28339598d860a3a114cac471daf4b56
f04c0fd52d5f9556db623a2393397c15db4f87f5ad710bfe8a38842c7ebbefa9
a3ff0c3ba4893e6f171ba3be19e88845e3302d79d76a2d6db30898a7db09b863
```

三份原計算收據和輸入案例詳見 [敘述驗證](dbt-shadow-commentary-validation-20261110.md)。保存時 archive producer code hash 為 `9ad58dfeeab5c4daf0a0af6613d9e50b7396c1caa53bd20f7f79fcc293b41300`。之後加入 typed reader，reader 檔案 hash 為 `7460195f0b12a9198f9b9b4c9af65ad50d06652e42e7ca38d09769de3497b22f`；舊收據保持原版本，不用新 hash 改寫歷史。

## 實際驗證

- Annual 相同 attempt 重試得到與首次相同的 archive receipt SHA256。隔離 dataset 的八個 dbt models 與一項完整性 test 成功。
- 三份快照均可還原計算套件；artifact hash 必須符合原計算收據。沒有 Python 財務公式 fallback。
- 三份 typed reader 實際從 BigQuery views 讀回 186／124／186 個 Facts。逐一核對身份、完整 coverage、內容 binding、狀態與數值；BIGNUMERIC 以 Decimal 接收，不能轉 float。
- 保留來源值與 SQL 計算值，不因保存成功將精度差異判成通過。`precision_approved=false`、`publication_eligible=false`。

失敗注入使用另一個 fresh dataset `sec_review_shadow_archive_probe_20261110_b8194a2e`，不修改正確資料：

| 損壞 | reader 拒絕理由 | SQL |
| --- | --- | --- |
| 修改 payload、保留舊 hash | Archive payload hash mismatch | 完整性未通過 |
| 同時修改 payload 與 row hash、保留舊 commit | Archive content checksum mismatch | 完整性未通過 |
| 移除 commit | Missing or duplicate archive commit | 完整性未通過 |
| 混入不同 entity | Archive attempt identity mismatch | 完整性未通過 |

四種 reader 均拒絕還原，dbt test 亦因資料完整性失敗而拒絕；不是 SQL 語法錯誤。`validate_candidate_archive.py` 保存 probe manifest。單元測試另涵蓋部分寫入、同 run 改 bindings、重試 job 確認、程式中途變動、typed reader 混入別的 attempt／Decimal 異動／漏列。

完整回歸以 `REVIEW_EXCEL_TEST=1` 執行 `python -m unittest discover -s tests`：**300 tests，OK，無略過**；包含實際活頁簿匯出與重算。原生 Microsoft Excel 尚未執行。

本機證據位於被忽略的 `outputs/dbt_candidate_archive_validation_20261110/`：三個 `*_final_store`、`annual_retry_verified`、三個 `*_restored`、三個 `*_typed_read` 與 `rejection_probes`。雲端測試表會到期，這些記錄不能當成永久雲端保存承諾。

## 發布前診斷後續

新增 `scripts/publication_preflight.py`，對三份實際還原的套件執行 pin 驗證後產生阻擋清單，保存在 `publication_preflights/{annual,quarterly,adversarial}.json`。三份均為 blocked：精度未核准、財務驗收未完成、Fact／commentary 精度差異，以及 release 核准、交付收據、永久保存、published consumer IAM 證據缺少。原有未知比較 mismatch 仍為零。

這個入口永遠不核發發布收據，CLI 回傳 2；即使手動修改 precision 旗標，也不會繞過正式 release 等缺失。四項新增單元測試通過，涵蓋不同 readiness／precision 組合、每種比較差異、pin 驗證失敗傳遞與 CLI 不覆寫。這四項是上述 300 項回歸之後的獨立驗證，不宣稱已重跑 304 項全套。

## 尚未完成

正式發布收據、published views、consumer IAM、交付檔案的雲端保存、release 配置與回退仍待實作；完整來源／公式案例矩陣與 identity 採用也未完成。M4 必須取得精度政策及切換的明確核准。候選可讀、dbt 測試成功與財務 readiness 都不能各自取得正式發布資格。
