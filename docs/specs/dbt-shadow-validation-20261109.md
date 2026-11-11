# 2026-11-09：結構化對帳與影子比對驗證

本次延續影子階段；精度仍待定，不切換正式財務計算來源、不發布 shadow 結果。驗證使用合成來源與隔離 BigQuery dataset；沒有更改既有 sec_raw。

## 新增與修正

- 來源金額及純加減錯算判為 mismatch；只有除法，或已獨立確認的除法差異傳遞，標為未核准數值差異。不用 epsilon、不按顯示兩位小數放行。
- Fact 比對檢查 run／entity／scope、source／plan／precision 綁定及 evidence ID 唯一性。
- SQL 獨立重算 balance_sheet_equation／cash_bridge；比對有序組成、申報期間、幣別／範圍、來源鏈、結構化 review binding、原始 precision tolerance、輸入聲稱的金額。
- 原始來源 quantum 是描述性來源 metadata；容許差上限及方程由 SQL 計算，不是將 Python 的 PASS 或計算金額當輸入。
- 部分 checks 不會省略剩餘期間；未覆核仍明確保留 not_calculable／verified=false。

## 實際 BigQuery 結果

| 合成案例 | 對帳數 | verified | 未驗證 | 與 Python 對帳差異 | Fact 完全一致 | Fact 未核准數值差異 | 其他 Fact 差異 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 有效覆核 | 8 | 8 | 0 | 0 | 160 | 26 | 0 |
| 偽造／不完整覆核 | 8 | 0 | 8 | 0 | 160 | 26 | 0 |

有效案例：4 個 BS equation 精確 matched、4 個 cash bridge 為 within_precision。現金期末 20.5、橋接計算為 20，差額 −0.5；tolerance 0.5 在來源 precision 上限內，並有相同方程的結構化覆核。這不等於整份 Loan Review 已通過財務驗收。

拒絕案例：binding 多出未批准欄位、缺少 FX 來源證據、tolerance 超過來源上限、重複 bridge term、偽造 calculated_value、負 coefficient、term 多出欄位、以期初現金冒充期末現金。八個皆為 not_calculable／verified=false；有金額或任意 PASS 字串不會改變資格。

全部 21 個 formula ID 的 43 個 kernel cases 同時跑過；dbt run／test 成功。兩組每組 186 個 Facts 的非數值欄位均一致；26 個數值差異仍未核准，不宣稱可切換。

## 收據與本機產物

- Python 全套測試：共執行 269 項，結果成功（其中 3 項略過）；log 位於 `/tmp/sec-dbt-shadow-tests-20261109.log`。
- dbt parse 成功；live 使用 dbt-core／dbt-bigquery 1.12.0。
- 本次兩個完成 run 的 code hash：`b6dffc55d516510a7755c3200a734c7a02df66a6248136bb09bc77067cb9a3b6`。
- source hash：`3b7c14d1cfd2ffab2af3863b0b9e163bb70c46c186270f7dd5fca97d53b82976`。
- commit：`b68e4d214b0d8e8b94280b02e2f9b5b18e3a5559`，加上 code hash 綁定未提交計算／SQL 實作。

### 有效覆核

- dataset：`sec_review_shadow_b7ed944bd0e5495a86bbc5faa1212267`（表預設七天到期；dataset／views 不保證自動清除）。
- dbt test invocation：`3c89409b-b867-4117-bf38-f7bcba14295a`。
- [對帳逐項比較](../../outputs/dbt_shadow_validation_20261109/valid_final/reconciliation_comparison.json)
- [Fact 逐項比較](../../outputs/dbt_shadow_validation_20261109/valid_final/comparison.json)
- [Run manifest 與收據 hashes](../../outputs/dbt_shadow_validation_20261109/valid_final/shadow_manifest.json)

### 偽造／不完整覆核

- dataset：`sec_review_shadow_4421ea1c46c440afa0f2597db556905d`（表預設七天到期；dataset／views 不保證自動清除）。
- dbt test invocation：`291946c1-5c92-4ea9-a32b-dd9aac41d8ba`。
- [對帳逐項比較](../../outputs/dbt_shadow_validation_20261109/forged_final/reconciliation_comparison.json)
- [Fact 逐項比較](../../outputs/dbt_shadow_validation_20261109/forged_final/comparison.json)
- [Run manifest 與收據 hashes](../../outputs/dbt_shadow_validation_20261109/forged_final/shadow_manifest.json)

來源／reviews 位於 ignored `outputs/dbt_shadow_validation_20261109/`；可由 `tests/test_dbt_shadow.py` 的 `rich_bundle(values_override={"ending_cash":"20.5"})` 與 `tests/test_shadow_reconciliation.py` 的 `review_envelope(..., forged=...)` 重建。未提交雲端 artifacts、憑證或真實借款人資料。

## 限制及後續

影子 SQL 已支援個別對帳檢查，但仍不是正式計算 authority。尚未完成精度政策核准、完整財務驗收／DSCR 定義、正式 identity 採用、ratio commentary 全面移轉，以及正式 reader／publication／rollback 切換。內含 review evidence 是供應者的覆核聲明，不代表程式已獨立證明文件真實性。所有 run 與對帳仍 publication_eligible=false。

參見 [操作手冊](dbt-shadow-runbook.md) 與 [遷移規格](dbt-financial-calculation-migration.md)。
