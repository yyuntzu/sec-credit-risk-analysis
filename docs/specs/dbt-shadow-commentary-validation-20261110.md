# 2026-11-10：敘述數字與資產負債組成遷移驗證

此交付推進 M3，**未切換正式 authority、未核准精度，尚未完成整體遷移**。參見 [遷移規格](dbt-financial-calculation-migration.md) 與 [操作手冊](dbt-shadow-runbook.md)。

## 數字由哪裡計算

| 處理 | 程式／模型 | 保存結果 |
| --- | --- | --- |
| 來源／文件結構驗證及 raw observations 入倉 | `scripts/dbt_shadow.py`、既有 `formal_commentary.validate_documents()`／`document_observations()` | `commentary_documents.json`、`shadow_inputs.json`、隔離 raw table |
| Annual／Quarterly 跨期選擇、增減／成長率／方向 | `int_review_shadow_comparisons.sql` | BigQuery typed 比較表 |
| SEC／文件科目篩選、明確 amendment、幣別／scale、衝突保留 | `int_review_shadow_commentary_components.sql` | 選定來源、原始來源鏈與 normalization loss 診斷 |
| 分子／分母相對成長、組成排序、來源總額比較、選定流動科目加總／殘差／重疊／覆蓋 | `fct_review_shadow_commentary.sql`／`shadow_commentary.sql` macro | `warehouse_commentary.json` 及 BigQuery 候選表 |
| 轉接 SQL 字串、狀態及排序，引用 canonical Facts 組文 | `scripts/warehouse_commentary.py` | 候選 `ratio_commentary_analysis.json`、MD／JSON／HTML |
| Python 獨立基準與 SQL 比較 | `scripts/shadow_commentary.py` | `commentary_comparison.json`；不回流成候選數值 |

Python 不將算好的 component sum／growth 傳給 SQL；SQL 不讀 baseline。原因分析仍需原文與覆核，數值比較不能被當作公司交易或經營原因。

## 實際 BigQuery 驗證

三組合成案例皆使用 `focus-heuristic-438521-v4` 的獨立新 dataset，未操作正式 `sec_raw`。模型建置、error-severity tests 與候選輸出成功；每組均執行 48 個手算 formula kernels。

| 案例 | run_id | 主表 Facts／完全一致／未核准除法差異 | 敘述 records／跨期 comparisons | 主表／對帳／readiness／敘述 mismatch | 敘述未核准除法差異 |
| --- | --- | --- | --- | --- | ---: |
| Annual＋明確 amendment | `635cbe41327b4092ab33e36e58565324` | 186／161／25 | 108／82 | 0／0／0／0 | 3 |
| Quarterly＋明確 amendment | `444a70613dcb4f64aa85501be965797e` | 124／106／18 | 86／60 | 0／0／0／0 | 3 |
| 非 amendment 衝突＋重疊組成＋不同幣別 | `6e5db6818f934c398fd12d765868c0a8` | 186／161／25 | 112／82 | 0／0／0／0 | 3 |

正常案例的手算結果：

- current assets 90 → 120，差額 30；current liabilities 30 → 40，差額 10。
- quick assets 60 → 90，成長率 0.5，大於 current liabilities 的 1/3；SQL 判 `numerator_faster`。
- cash 10 → 15，差額 5；current 的舊來源 999 由明確 `10-K/A` 的 15 取代，保留 v2 來源定位。
- 選定的 current assets 科目合計 90／120，current liabilities 科目合計 30／40；兩組各期間的殘差均為 0，狀態為 `matched_selected_lines`。這不代表完整會計科目覆核。

衝突案例中同期間的 999 與 15 都是普通 `10-K`，cash 不選最新值，而保留缺值／來源矛盾。流動資產包含 `PrepaidExpenseAndOtherAssetsCurrent` 及 `OtherAssetsCurrent` 時，標 `overlapping_components`，不輸出組成合計與殘差。EUR 的 AssetsCurrent 不混入 USD 計算，留下幣別警告。以上狀態與 Python 基準一致，零 mismatch 不表示這些資料可正式驗收。

三組共有 9 個敘述除法差異，均位於 numerator／denominator 的 growth；例如 1/3 的原生 BIGNUMERIC 與 Python 50 位基準不同。全部仍是 `numeric_difference_unapproved`，未使用 epsilon 放行。

## 收據與追溯

三組計算 code hash：
`057c9a8e9d2f88fdb3b563b08c956e50f581c38f1215faa20b54eb2787d91a3a`。

計算收據 hashes：

- Annual：`c70049473c20a95850c11c85c21b833d7ffcd915cff1fd2d8351d15bed6caf4a`
- Quarterly：`3f5fc44a65a4edc4e22b71e1a58c859bdf2c4a8d86fe8749c7c16a8f31b8acf6`
- Adversarial：`083f6d2398f3d585ab4b500fefb8d47e4a3363e3174fda51e29fe06fd037a1f5`

完整本機 artifacts 在 `outputs/dbt_shadow_commentary_validation_20261110/{annual_final,quarterly_final,adversarial_final}/`。`warehouse-candidate-v2` 收據綁定敘述 rows 與原始文件 hash；舊 v1 的 186-Fact 實際快照也經目前 reader 讀取成功，沒有改寫舊檔案。

較早的 `annual_live` 因 SQL CTE 名稱 `groups` 與 BigQuery 保留字衝突而失敗，已更名並用新 dataset 重跑；失敗 run 沒有計算收據／候選預覽，紀錄保留，不冒充成功測試。

## consumer 與瀏覽器

已逐組確認候選 `ratio_commentary_analysis.json` 完整等於 SQL rows 經純 adapter 組裝的結果；測試強制 Python 舊 ratio／narrative／arithmetic 函式報錯，候選預覽仍成功，證明沒有偷偷 fallback。

瀏覽器 QA 發現窄視窗的多期表格會超出頁面，因此新增表格內水平捲動與提示，明確標示影子草稿。這是呈現變更，沒有重跑或改寫原 SQL 計算收據；另外以同一份 Annual 計算收據產生 `annual_browser_preview/`，`preview_manifest.json` 保存本次 `consumer_code_hash` 與交付 hashes，區分計算與呈現版本。未改寫三個既有 candidate_preview。

## 本機測試與剩餘工作

全套 287 項測試成功（3 項略過）；包含 raw normalization／quantum underflow、v1 收據相容、缺／重複／其他 run 的敘述 rows、錯誤 delta 不得歸類精度，以及 annual／quarterly 期間差異。最後完整測試 log：`/tmp/sec-dbt-shadow-commentary-tests-20261110-complete.log`。

原始值／scale 及乘法中間值、換算結果與金額 precision bound 若不能無損表示，會在建 dataset 前被拒絕。這是原始資料精度驗證，不是將 Python 財務結果當作 SQL 權威。

後續仍需 Excel 轉接、identity／cash-change 的完整採用、正式不可變 warehouse reader／publication receipt／BI views／回退與完整矩陣。精度政策與正式切換保持未放行，沒有修改正式 cloud 預設。
