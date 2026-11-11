# DER identity 影子採用驗證

後續 CASH-CHANGE 的獨立進度見 [現金變動驗證](dbt-shadow-cash-validation-20261110.md)；本文保留本階段執行時的範圍與原始收據。

日期：2026-11-10。所有案例為 SYNTHETIC-ONLY，並非公司實際覆核或正式報告。精度待定、未切換 authority。

## 實作

`scripts/shadow_identity.py` 定義來源綁定的個別 identity 覆核契約。覆核放在 source bundle 的 `identity_reviews`；hash 綁定沒有此欄位的原來源包，完整 envelope 再被 source_hash 與 plan_hash 固定。函式只檢查結構、期間、引用及定義證據，不計算財務數值。

`dbt_shadow.prepare_plan()` 將核對後的 DER／有序依賴放入計畫，重新檢查循環與深度；Python baseline 按拓樸順序套用覆核，作獨立比較。`shadow_identity.sql` 在 BigQuery 再檢查公式／科目對應、證據 claim、source binding、scope、期間、幣別、單位及祖先科目。`fct_review_shadow_facts` 分層計算並傳遞來源證據；不覆寫 sourced、conflict 或 not_applicable。consumer 只載入結果與定義證據，不重算 DER。

這個路徑限影子流程；現有 Python 正式入口不採用 bundle 裡的影子擴充。完整 Evidence 仍需指向人確認的原始覆核，hash／complete=true 只證明提交內容一致，不能證明文件真實或自行授予業務核准。CASH-CHANGE 採用仍未啟用。

## 實際 BigQuery 案例

Project `focus-heuristic-438521-v4`，US；每個 run 使用 `sec_review_shadow_<run_id>` 獨立 dataset，表七天到期。

| 案例 | run_id | 目標與預期值 | Facts | 未核准數值差異 |
| --- | --- | --- | ---: | ---: |
| Annual 毛利 | 97a6f6f4c4574e4c83d993ad994f97cb | DER-01：120−40＝80 | 186 | 26 |
| Annual signed tax | 0e1d04b2cd6f49f4ad8704b6e57ea22f | DER-05：55＋(−5)＝50 | 186 | 26 |
| Quarterly YTD 營業利益 | 578fb9e29e7b47a9885f1d4bc629b5a1 | DER-04：80−20＝60 | 124 | 18 |
| Annual 連續推算 | acdf521baaf14b5090101a05b6d46c34 | 毛利 80 → 營業利益 60 → 營業利益率 0.5 | 186 | 26 |

四份皆完成十二個 dbt models、完整性 test、48 個手算 kernel cases，並通過 Fact／對帳／財務 readiness／commentary 比較的未知 mismatch 檢查；每份均為零。候選 reader 成功產生 MD／JSON／HTML 草稿。除法差異依既有分類保留，不視為精度核准。將 Python calculate_identity／approved_formula_value／calculate_report／complete_report 全部替換成一呼叫即失敗的測試函式後，四份仍能完整讀回，共 682 個 Facts；沒有 Python 財務 fallback。

共同計算 code hash：`90508a95133ce575b13314999a39ca0c969d901f8f2825751494a2ddc054096f`。

計算收據 SHA256（依序）：

```text
362fccd80b617dcd48a13ac3c07a58cbd2174f484c27fd7779ad82aae67c4fa5
80744d0836889cd15c9ae37cc83f2ad8e8d088bc8b1e31568024227228a59d95
919d6dde1742ae40d905ce821d4f33bd424aedc1f7f55c68813e9897c64cdb61
3b1f462538e8312b1a7683f9cd6d9a8ced9aabd40bec180749b5a122e1235801
```

證據位置為忽略的 `outputs/dbt_shadow_identity_validation_20261110/`，上述案例各在 `annual_gross_final`、`annual_tax_final`、`quarterly_operating_final`、`annual_chain_final`。先前的 `*_native` 計算因空集合 commentary mismatch 被 reader 拒絕，保留失敗歷史，不改寫成成功。最早未加網路權限的 `annual_gross` 因 sandbox DNS 限制中止，不列為雲端成功證據。

## 額外發現與測試範圍

初次 native 執行發現，沒有資產組成資料時 `ARRAY_AGG(... IGNORE NULLS)` 的空集合輸出為 null，但敘述契約要求 `selected_concepts=[]`。已在 SQL 將這個 metadata 集合明確轉為空陣列；沒有把任何缺少的財務金額轉成零，也沒有放寬 reader 的 mismatch 門檻。

本機測試覆蓋六個 DER 各自的獨立預期值、來源變更、claim／scope／日期／順序錯誤、重複 review、空版本、保留 Evidence ID、complete 的 boolean 型別、沒有覆核時維持缺值、Quarterly YTD、連續依賴及互相反推的循環。並保留原有來源衝突／不適用不可覆寫測試。這不表示所有失敗注入已在 BigQuery 實跑；其他公式的 native 採用及更廣的案例矩陣仍待補齊。

最終完整回歸：`REVIEW_EXCEL_TEST=1 python -m unittest discover -s tests`，314 項測試成功、無略過（164.474 秒），包含活頁簿實際匯出與重算。原生 Microsoft Excel 尚未執行。
