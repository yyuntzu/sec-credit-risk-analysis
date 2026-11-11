# dbt 財務影子比對驗證紀錄：2026-11-07

本紀錄是隔離 BigQuery 的實際 SQL／dbt 執行證據，不是僅 parse 或 mock。來源均為合成案例，未使用真實借款人資料、未修改既有 sec_raw、未發布正式結果。精度政策依使用者指示仍待定。

## 結果

| 案例 | Facts | 完全一致 | 僅數值差異（未核准） | 其他 mismatch | 手算 kernel 案例 |
| --- | ---: | ---: | ---: | ---: | ---: |
| 年度 | 186 | 160 | 26 | 0 | 43 |
| 季度 | 124 | 106 | 18 | 0 | 43 |
| 來源例外案例 | 186 | 184 | 2 | 0 | 43 |

全部執行的 dbt run／test 成功；kernel fixtures 涵蓋 21 個公式 ID、零分母、signed tax、capitalized interest 與 repeating decimal。比較不使用 epsilon；例如 CFO／current liabilities 的 2/3，Python 為 `0.6666666666666666666666666667`，BigQuery 為 `0.66666666666666666666666666666666666667`，差額保留為 `-3.333333333E-29`。數值差異未當作已批准／可發布。

來源例外案例包括明確 amendment、非 amendment 數字衝突、晚於 as_of 的申報、同科目幣別衝突、確認不適用及真實零值。季度案例保留完整年度與 comparable YTD 角色，不把缺少完整 LTM 的值年化。

## 固定版本與收據

- Python baseline Decimal context：precision 28、ROUND_HALF_EVEN；記錄 traps。
- dbt-core／dbt-bigquery：1.12.0。
- 來源 commit：`b68e4d214b0d8e8b94280b02e2f9b5b18e3a5559`；另以 code hash 綁定此次未提交實作。
- 相關計算與 dbt 來源 code hash：`f93b4de9b606e707f3506799ca4585c022a708d6ae64ae5813427baa78f36a66`。
- 所有 run：`precision_approved=false`、`publication_eligible=false`。

| 案例 | 隔離 dataset | dbt test invocation |
| --- | --- | --- |
| 年度 | `sec_review_shadow_7f7b8b6cf2de4fa8ba02e8086501b935` | `1eaf3e09-201a-4ab6-86cf-37f788029152` |
| 季度 | `sec_review_shadow_a813a68b2f5b471886d437ec58e772fb` | `1374dd40-0407-483c-822a-e49bb24ed93d` |
| 來源例外案例 | `sec_review_shadow_2f7c9fe5e9dd4f358085c8fdc72891ac` | `370f3e07-4a35-4967-b571-1317dba94c7d` |

## 本機產物

以下位於 ignored outputs，未把執行日誌或原始 bundle 提交進版本控制；在本工作目錄可直接開啟。完整 JSON／CSV 逐項列出 metadata、值與差異。

- 年度：[比較摘要](../../outputs/dbt_shadow_validation_20261107/annual_live5/comparison.json)、[CSV](../../outputs/dbt_shadow_validation_20261107/annual_live5/comparison.csv)、[run manifest](../../outputs/dbt_shadow_validation_20261107/annual_live5/shadow_manifest.json)。

- 季度：[比較摘要](../../outputs/dbt_shadow_validation_20261107/quarterly_live/comparison.json)、[CSV](../../outputs/dbt_shadow_validation_20261107/quarterly_live/comparison.csv)、[run manifest](../../outputs/dbt_shadow_validation_20261107/quarterly_live/shadow_manifest.json)。

- 來源例外案例：[比較摘要](../../outputs/dbt_shadow_validation_20261107/adversarial_live/comparison.json)、[CSV](../../outputs/dbt_shadow_validation_20261107/adversarial_live/comparison.csv)、[run manifest](../../outputs/dbt_shadow_validation_20261107/adversarial_live/shadow_manifest.json)。

每個 dbt 產物目錄另含 `run_results_run.json`、`run_results_test.json`、`target/manifest.json`，hash 均記錄在 shadow manifest。失敗嘗試也保留稽核資料，未覆寫成成功。隔離表預設七天到期，dataset／views 並無自動清除保證。

## 驗證限制與後續

這些證據支持當前 shadow 實作；不等於全案例矩陣已完成，亦不授權正式切換。尚需完整 structured reconciliation／source precision tolerance、identity review、ratio commentary、warehouse reader、發布收據及失敗回退等工作。DER 算式在 kernel 測試，但報告不自動用 identity 補值；診斷對帳始終 verified=false。workbook source 明確不支援此第一版 shadow。

參見 [操作手冊](dbt-shadow-runbook.md) 與 [完整規格](dbt-financial-calculation-migration.md)。
