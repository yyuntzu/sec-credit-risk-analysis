# dbt canonical 設定與竄改拒絕驗證

日期：2026-11-11。SYNTHETIC-ONLY，隔離驗證；未核准精度，未改正式預設或發布權威。

## 實作

新增 `dim_review_shadow_configuration`，在 SQL 內固定目前已採用的百萬顯示單位、Standard EBITDA basis、公式／政策版本，以及 `shadow-bignumeric-native-v1-unapproved`。這沒有採用 18 位 HALF_EVEN 提案。

`stg_review_shadow_slots` 將 producer 的同名欄位保存成 `declared_*`，實際 scale／basis／precision version 改用 SQL 設定。`int_review_shadow_formula_contracts` 要求 declared 與 SQL 值相符；即使 producer 同時修改 metadata 與 plan，仍無法通過。必要 test 亦檢查設定只有一列。

錯誤設定下可能保留原始 sourced 值供診斷，但不會用錯誤 scale 正規化成新的數字，也不會核發成功收據。修改設定必須透過版本化 SQL 與放行證據；輸入 JSON 不能代替核准。

## 原生 BigQuery 結果

Project `focus-heuristic-438521-v4`、US、獨立 `sec_review_shadow_<run>` datasets，表七天到期。共同 code hash：`3b4abe108edaa84fd854e52038d61bad1227e14a6354c14050400ac0bb90aa77`。

| 正常路徑 | run_id | 範圍 |
| --- | --- | --- |
| Annual SQL-only | 20f63324f3dd4626af9f0053b8ea4f29 | 禁用 24 個 Python 財務／比較函式，186 Facts，identity＋cash 與草稿成功；comparison=not_run |
| Annual shadow | 5c7656a655d1413d9d8c0cf4c5d40453 | 186 Facts；未知 Fact／reconciliation／readiness／commentary mismatch 均為零，26 筆未核准數值差異 |
| Quarterly shadow | 9daa64f591654532993ae2c8ff74743e | 124 Facts；未知各層 mismatch 均為零，18 筆未核准數值差異 |

每個正常 run 均完成 17 個 dbt models、一項完整性 test、48 個手算 kernels 及收據綁定草稿。影子比對沒有套用 epsilon 或核准 precision policy；SQL-only 執行沒有冒充 Python 比對成功。

計算收據 SHA256（依序）：

```text
55729a8187053142108c53e229135d448f7699489357f3c653bec8519761b008
e311c9962ad4a3f7323f6c5f14f3b1c7429194eb196c772724a0f13f6a509d24
f86e47cb15c53e6eb5c774e30591b33eed53b03389f768cb73b844f2c8eaaaf3
```

## 三種獨立故障注入

`validate_canonical_configuration.py` 各用獨立 dataset，保持原始 observations 不變，重新計算 plan hash，以排除單純 stale checksum 失敗：

| case | run_id | 改動 |
| --- | --- | --- |
| scale | f9b18b405d714f8db1da01ebf1d3aac3 | report scale 與所有 money slot scale 一起改成 1000 |
| basis | 8b151b4abc574f6ea53f816e0f82b8c7 | 宣告未核准的 Adjusted EBITDA basis |
| versions | e557f5d9dbd94017965db47c2392ec50 | 同時修改 metadata／plan 公式與政策版本、precision version，並宣告 precision_approved=true |

三個 run 都成功建置 SQL models，然後因資料契約 test 失敗而拒絕；不是 SQL 語法或連線錯誤。每個 run 的 186 個 contract 均為 false，不產生成功計算收據。實際查詢仍是 revenue=120、scale=1000000、Standard EBITDA basis、未核准的 native precision version；不因 producer 宣告而改算。保留 sourced 數字不代表該執行通過。

原始證據位於忽略的 `outputs/dbt_configuration_validation_20261111/`：`annual_live`、`annual_compared`、`quarterly_compared`、三個 `*_probe/probe_manifest.json` 與 `verified_summary.json`。

## 回歸與範圍

完整 `REVIEW_EXCEL_TEST=1 python -m unittest discover -s tests`：329 tests、OK、無略過，53.030 秒。包含既有 Excel 實際匯出與重算；原生 Microsoft Excel 尚未執行。本次沒有新的 GCS 保存或正式 published view 證據。

完整遷移仍需依 [完成條件矩陣](dbt-migration-completion-matrix.md) 補齊：來源／tag 映射、狀態 reason codes、完整財期／精度矩陣、publication registry、IAM／永久保存、release／rollback、M4 明確核准及 M5 收斂。setup 的 GitHub／triage／single-context 配置沿用既有設定，未另建 issue、PR 或變更 tracker。
