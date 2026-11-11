# dbt 公式與必要核准契約驗證

日期：2026-11-11。SYNTHETIC-ONLY、隔離候選測試；precision／publication=false，正式預設未切換。

## 改變與責任邊界

舊 SQL 可依傳入的 plan 做除法，但一般 CF 尚未獨立確認目標科目、分子／分母順序及期間是否正確。新增：

- `dim_review_shadow_formulas`：dbt 內固定 21 個公式 ID 的目標、輸入科目順序與單位；COMMON-SIZE 展開九個收入表科目。
- `int_review_shadow_formula_contracts`：依原始 request periods 重建期間／前期角色／LTM 起點／期初現金日期，檢查目標單位、幣別、instant／duration、輸入角色／日期／順序／單位、版本與依賴深度。
- `dim_review_shadow_metric_policies`：dbt 內固定合法單位、必要 decisions 及受政策約束的定義。來源採用改用這份 canonical pending 清單，計畫刪除 DEC-03 不會放行 DSCR。
- 計算 gate 需通過 formula contract；必要 dbt test 以 error 拒絕不合格計畫，不核發成功的執行收據。候選資料保留作診斷。

首個 FY 沒有前期，或合法缺少輸入格子，仍可保留 not_calculable；不把正常缺值誤判成錯誤公式。SQL-only 候選收據仍明確 comparison=not_run，不能視為通過 Python／dbt 比對。

## 最終原生 BigQuery 結果

Project `focus-heuristic-438521-v4`，US，各 run 為獨立 `sec_review_shadow_<run>` dataset，表七天到期。

| 案例 | run_id | Facts | 結果 |
| --- | --- | ---: | --- |
| Annual identity＋cash | bd6f393ed4ab4024ac5c2ae1a395108a | 186 | 完成 SQL-only 計算、契約檢查與草稿 |
| Quarterly | 8c0b1cc2b0ed40d5a1f6b16f307a80ac | 124 | 完成契約檢查，合法缺值／未完成對帳仍保留 |
| 錯誤計畫注入 | 23c718724830479f899c07e83f65553d | — | 五個目標 contract=false，均 not_calculable／NULL，dbt test 拒絕 |

兩個正常案例禁用既有 24 個 Python 財務／採用／驗收／比較函式，仍完成 16 個 dbt models、一項完整性 test、48 個手算 kernels 與 MD／JSON／HTML 草稿，共 310 個 Facts。沒有執行 Python baseline，因此不宣稱本次零比較差異或精度放行。

錯誤注入另使用獨立 dataset；四種錯誤公式計畫均更新 plan hash，排除僅靠舊 checksum 不一致而失敗的解釋：

| 目標 | 故障 | 結果 |
| --- | --- | --- |
| current_ratio:fy_t | 交換 current liabilities／current assets | SQL 契約拒絕；不做倒數計算 |
| quick_ratio:fy_t | 改用 CF-01 | 目標／公式不符，拒絕 |
| interest_coverage:fy_t | 刪除 capitalized interest 輸入 | arity 不符，拒絕 |
| operating_margin:fy_t | 分母引用前一年度 revenue | 角色不符，拒絕 |
| dscr:fy_t | 刪除 pending DEC-03，額外提供 raw DSCR=2 | canonical pending 仍阻擋採用；契約不符並拒絕收據 |

五個目標均已實際查詢 SQL contract 與最終 Facts，狀態為 not_calculable、值為 NULL。拒絕來自資料契約 test，不是 SQL 語法錯誤。此 fixture 是直接在 raw plan 注入故障；不適用實際借款人，也沒有建立正式發布紀錄。

共同 code hash：`84519f624f0682396b1c0439e8a08fbe51b92cc8a04dc3ed288d297462c1a83c`。

計算收據 SHA256（Annual／Quarterly）：

```text
2d17919dd37b44c899b63379b024e3ffbb4fb0be26d1fe2902ab35eb5ac321fd
25f34cb4ebdd1060733b6fd37f5aefd8953201d89dd12a54d536323429296134
```

證據位於忽略的 `outputs/dbt_metric_policy_validation_20261111/`：`annual_live`、`quarterly_live`、`rejection_probes/probe_manifest.json`、`verified_summary.json`。先前只有公式契約的中間版本保存在 `outputs/dbt_formula_contract_validation_20261110/`，其收據與版本保持原樣，不改寫成此版本。

## 回歸與剩餘工作

完整回歸：`REVIEW_EXCEL_TEST=1 python -m unittest discover -s tests`，328 tests、OK、無略過，56.550 秒；包含既有 Excel 實際匯出與重算，原生 Microsoft Excel 尚未執行。

這不證明所有 source／tag 映射、canonical 配置（例如 scale／standard basis）與政策版本都已完全由 dbt 獨立固定；其餘來源、財期與精度邊界及失敗矩陣仍需補齊。正式 publication registry、IAM、永久保存、release／rollback 與精度核准也尚未完成。不得以這些測試綠燈視為整體遷移完成。
