# SQL-only 候選執行驗證

日期：2026-11-10。限 SYNTHETIC-ONLY 隔離工程驗證；不是 M4 切換，precision／publication 仍為 false。

## 解決的缺口

Shadow 為了遷移比對，本來就會執行 Python baseline；這不能作為未來正式 cloud runtime 的唯一入口。新增 `scripts/warehouse_execution.py`，使用同一份 raw observations 與 value-free plan 執行 SQL，但不執行 Python 來源採用、normalize、財務公式、對帳、readiness 或結果比對引擎。

`dbt_shadow.prepare_run(..., with_baseline=False)` 只建立 request／policy／Evidence metadata、有序依賴、原始候選值與覆核輸入；Evidence 的期間由原始區間／科目 metadata 建立，不採用 Python 已選數值。SQL 執行來源選取、公式、identity、cash bridge、readiness 與敘述數值。Python 仍可做來源數字保真／範圍 preflight、結構與收據驗證、顯示單位轉換及呈現；不宣稱 Python 完全沒有任何算術操作。

收據 `warehouse-execution-v1` 額外綁定獨立 `request_hash`，明確保存 `comparison={"status":"not_run","mode":"dbt-only"}`。不產生 baseline 或 comparison 檔案，不把未執行比對寫成零差異。reader 保留舊 shadow v1／v2 相容，並檢查新型別、request hash 與 SQL-only metadata；影子 mismatch 不能靠改成此型別繞過固定收據／metadata。

這是未來正式引擎的候選基礎，仍強制 `sec_review_shadow_<run>` 命名與七日表期限。未接入正式預設或發布入口。發布前診斷會列出此次未執行 migration comparison；M4 仍須以獨立 shadow 比對、完整案例矩陣及版本化放行證據驗證 release，而不是要求每次正式 runtime 都重算 Python。

## 原生 BigQuery 證據

`scripts/validate_sql_only.py` 將 24 個 Python 財務／比較函式及既有 aliases 全部替換成一呼叫即失敗的函式，範圍包括來源採用、normalize、calculate_fact／identity／report、complete_report、acceptance、reconciliation 與 shadow comparisons。保留此限制完整執行輸入準備、BigQuery、收據 reader 及草稿呈現。

固定合成來源另刻意將舊 `inputs.value/status` 寫成 `FORBIDDEN-PYTHON-*`。原始 observation 值、來源 metadata 與覆核內容仍固定有效。SQL inputs 沒有這些污染值，且最終來源 revenue 仍是原始的 120，證明沒有採用舊 Python selection 結果。這是測試用的污染欄位，不是實際借款人輸入。

Project：`focus-heuristic-438521-v4`；US；datasets 依 run 獨立建立。

| 案例 | run_id | Facts | 結果 |
| --- | --- | ---: | --- |
| Annual identity＋cash | abc9333e16c3498c9557959be9361d3c | 186 | revenue=120、gross profit=80、operating income=60、margin=0.5、cash change=10 |
| Quarterly | 03b32cd834b54cf8851709dd4c61f5b7 | 124 | 季度期間／原始值／不可用狀態與草稿成功形成，不新增現金列 |

兩份均完成 13 個 dbt models、一項完整性 test、48 個手算 kernels；310 個 Facts 全部經固定收據讀取，MD／JSON／HTML 草稿成功產生，沒有 Python baseline 檔案。**沒有執行 Python 結果比對，因此不宣稱本次零 mismatch 或精度差異通過。** 財務缺口仍由 SQL readiness 保留，均未取得正式發布資格。

共同 code hash：`3580b9d9e59e2735a4b25f63c04812c4111114110100bf38c223473b19967231`。

| 案例 | request_hash | 計算收據 SHA256 |
| --- | --- | --- |
| Annual | a1570c9712346bbe07033a745b7cd3f1dbd464191e4b9095528cb8ae170eddf8 | b3f61269c12bcb45b3e09fd8945cbd90bbe59e41f3778082b80a8ef7992319f2 |
| Quarterly | 808f40b80ea9947a38755445aa3facf665f28e25d5c318037c745922ada6e408 | d4b5dde7e41328443b80be5d31828ff5e497c43a0e9bd2c2e35af0ced4732be0 |

本機另用這兩份實際收據建立 candidate archive package，完成 `verify_snapshot`；這驗證新收據與 archive package 相容，沒有在本次重新上傳 archive／GCS，不冒充新的雲端保存證據。

證據在被忽略的 `outputs/dbt_only_execution_validation_20261110/`，包括兩份 `*_live`、`disabled_functions_proof.json`、`execution_manifest.json`、SQL artifacts 與根目錄 `verified_summary.json`。

## 測試與剩餘工作

三項新增單元測試涵蓋禁用財務函式、污染既有 selected values、identity／覆核 metadata、新收據與 reader／呈現、雲端失敗保存及禁止 fallback。完整回歸：`REVIEW_EXCEL_TEST=1 python -m unittest discover -s tests`，327 tests、OK、無略過，99.411 秒。此回歸包括既有 Excel 匯出／重算；不宣稱新 SQL-only receipt 已完成原生 Excel 或新的雲端交付 E2E。

完整來源／財期／精度邊界矩陣、SQL 對每個公式目標與依賴的獨立契約檢查、正式 publication registry、IAM、永久保存、release／rollback 與 M4 明確核准仍待完成。
