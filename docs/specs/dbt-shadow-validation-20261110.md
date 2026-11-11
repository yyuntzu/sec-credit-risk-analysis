# 2026-11-10：SQL readiness、計算收據與候選 Report consumer

本次完成 M3 的部分工程，**未完成整個遷移，未核准精度、未切換 authority**。依據 [遷移規格](dbt-financial-calculation-migration.md) 與使用者「先保留精度待定，只做影子比對」。既有 cloud Report／正式發布仍使用 Python 路徑。

## 改動

- `fct_review_shadow_acceptance.sql` 根據必要報表格子、DEC-08／09、來源限制及逐期 BS／cash 覆核 coverage 產生 `substantive_data_ready`。不因 dbt 建置成功就宣稱整份報告 accepted；三個精度／最終驗收／發布旗標皆 false。
- `compare_acceptance()` 對照完整 unavailable IDs、blockers 與 readiness；錯誤 run、缺少／重複驗收列或偽造正式旗標皆拒絕。
- `calculation_receipt.json` 保存來源、計算計畫、版本、結果快照與完整 dbt 成功紀錄的 hashes；consumer 必須接收計算流程提供的固定 receipt hash。
- `warehouse_candidate.read_candidate()` 不讀 baseline，也不呼叫 Python 採用、財務公式或財務驗收。由 BigQuery 回傳的字串精確恢復 Decimal，驗證固定表格、期間、來源、定義及有序依賴。
- `write_preview()` 產生 dbt 數字的 `report.md`、`report.json`、`dashboard.html` 及交付 hashes；保留未驗收與缺少敘述狀態。原 Python renderer 仍先獨立重算算術；候選入口以收據驗證後共用純呈現程式碼。
- 除法改成明確判斷零分母。BIGNUMERIC 溢位會失敗，不能被 SAFE_DIVIDE 轉成一般 NULL。

## 實際 BigQuery 結果

專案 `focus-heuristic-438521-v4`，每次使用新 `sec_review_shadow_<run_id>` dataset；沒有修改既有 `sec_raw`。以下都是合成資料，不代表真實公司的財務驗收。

| 案例 | run_id | Facts | 完全一致 | 未核准數值差異 | Fact／對帳／readiness mismatch | 實際結果 |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Annual＋8 個有效覆核 | `7a92b0feb6a14d9abda9188af3c83378` | 186 | 160 | 26 | 0／0／0 | dbt、收據與 MD／JSON／HTML 預覽成功 |
| Quarterly，未提供覆核 | `c748848b41c04ffaba5f3bc004b488ef` | 124 | 106 | 18 | 0／0／0 | 未覆核狀態保留；dbt、收據與預覽成功 |
| `1e38 / 1e-38` 溢位 | `9005277b1a314bfeb8d9c6cc45667be2` | 不適用 | 不適用 | 不適用 | 執行失敗 | BigQuery 明確回報 BIGNUMERIC overflow；無計算收據／預覽 |

兩個成功案例各通過 48 個手算 kernel cases，涵蓋全部 21 個現有 formula IDs；新增大／小精確值、負分子、負基期與跨零差額。此小型邊界集合不等於已完成第 8.3 節的所有 rounding／double rounding／財期矩陣。

Annual 有 8 個 verified 對帳，但仍有 12 個必要格子不可用；Quarterly 未提供覆核，有 0 個 verified、12 個必要格子不可用。兩者 SQL／Python 均判 financial readiness=false。這驗證的是正確保留 draft，並非取得正式授信報告驗收。

兩個成功 run 及失敗案例的 code hash：
`bea2117b22fffa6e315b7166ec072a1a3a3d729161772a501df9f6957b092aaf`。

固定計算收據 hashes：

- Annual：`1a5f7a1107d6f42e9560433459a07fa0f75171b59b004e82a83f28b8c8497ba2`
- Quarterly：`8814740f8ce539f91e790046aa2f267a19e679392f77ee9026af31436084c1de`

本機完整 artifacts 位於 `outputs/dbt_shadow_validation_20261110/{annual_final,quarterly_final,overflow}/`（不提交 Git）。成功 run 的 `candidate_preview/` 保存預覽與其 hashes；表預設七天到期，dataset／views 不保證自動清除。這些隔離結果不是正式歷史倉儲的長期保存設計。

## 本機驗證

`python -m unittest discover -s tests` 共 279 項，成功（3 項略過）。新增測試包含：每份受綁定 artifact 被改寫、錯誤／重複／缺少 Facts、浮點輸入、缺來源證據、錯公式、其他 run、dbt skip／空測試、驗收列偽造、preview 不覆寫，以及明確禁止 Python 財務 fallback。

測試輸出：`/tmp/sec-dbt-shadow-tests-20261110-m3.log`。SQL 執行與溢位錯誤收據位於各 run 的 `dbt/`，不能用單元測試或 parse 取代。

## 尚未完成與下一步

1. 將 ratio commentary 的衍生數字與組成檢查移至 dbt；目前候選 preview 沒有使用 Python 另算敘述數字。
2. 完整 identity 採用／cash-change 覆核與更廣泛來源、財期、精度案例。
3. Excel 與正式 warehouse reader／不可變候選表、publication receipt、BI views、發布／回退失敗注入。
4. M4 必要的 precision policy 與明確放行。目前 44 個除法差異仍未核准，不可放寬 epsilon 當通過。

收據 hash 是內容完整性檢查，不是簽章。正式部署仍須有可信收據來源、IAM 與固定版本；不能由可任意編輯的本機檔案自行授權發布。
