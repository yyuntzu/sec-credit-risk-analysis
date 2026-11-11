# 2026-11-10：dbt 候選 Excel 綁定與試算隔離

本交付推進 M3 的 Excel consumer，**不是 M3–M5 全部完成或 authority 切換**。精度政策仍待定，`final_report_accepted`／`precision_approved`／`publication_eligible` 始終 false。參見 [遷移規格](dbt-financial-calculation-migration.md)。

## 路徑與契約

1. `warehouse_candidate.read_preview_data()` 驗證固定計算收據，讀取保存的 BigQuery Facts／SQL 敘述結果；不讀 Python baseline。
2. `write_preview(..., excel=True)` 保存 MD／JSON／HTML、`commentary.json` 與預覽 hashes。
3. `warehouse_excel.export_candidate_excel()` 重新核對來源、版本、所有輸出 hashes、完整 Report／敘述及 Markdown 的表格值／期間／單位。
4. `review_workflow._run_excel_exporter()` 使用既有 bundled Node／artifact-tool 執行同一個 `export_loan_review_excel.mjs`，以明確 `--warehouse-candidate` 模式產生檔案。原本 Python `export_excel()` 仍先執行原有 `validate_saved_artifacts()`；沒有共用一個略過驗收的旗標。
5. `audit_workbook()` 讀取真正存檔的 XLSX XML，確認完整字串、typed 數值 caches、Fact IDs 及每個主表公式。通過後才保存 workbook hash 與技術驗證收據。

| 工作表 | 用途與數字來源 |
| --- | --- |
| Review | 原報表版型；每個數值只引用 Warehouse 的固定 dbt 值，不依賴 Sources 試算或差額檢查 |
| Sources | 來源原值／scale、既有本機試算公式、相對倉儲差額、完整 Evidence registry；編輯不回流到 Review 或倉儲 |
| Warehouse | 固定十進位值的 Excel numeric 近似及完整字串、Fact 原始值／scale、狀態、公式／版本、有序 inputs、evidence IDs、單位／日期／basis、run／source／計算收據 |

Sources 中的試算仍是 Excel 本機用途，沒有成為 cloud 第二個財務權威。Warehouse 沒有計算公式；原始報表 JSON／計算收據不隨 Excel 編輯改變。未提供從 XLSX 回寫 BigQuery 的功能。

## 實際結果

沿用已經真正在隔離 BigQuery 執行過的三份 SQL 快照，沒有修改或重跑其計算收據。對應 run IDs 與來源見 [敘述驗證](dbt-shadow-commentary-validation-20261110.md)。三份都是合成案例，不能作為真實借款人的授信報告。

| 案例 | Facts／完整字串 | Review 綁定 | 倉儲 numeric binary64 近似筆數 | Excel 結果 |
| --- | ---: | ---: | ---: | --- |
| Annual | 186 | 130 | 29 | passed，仍為草稿 |
| Quarterly | 124 | 64 | 18 | passed，仍為草稿 |
| 來源衝突／重疊／幣別案例 | 186 | 130 | 29 | passed，原始不可用狀態保留，仍為草稿 |

合計 496 個 Facts、324 個主表綁定。每個 Fact 的完整值字串或空值狀態均與讀入的 SQL 結果相同；原始 Fact value／scale 字串也驗證。原始來源 payload 的原始 lexical 形式仍由來源包／計算收據保留，不能將 Fact scale 的規範化字串冒充整份原始 payload。

Excel 數字不能儲存 BIGNUMERIC 的完整十進位精度，因此完整字串另存 Warehouse C 欄，實際 numeric 值的 exact binary64 Decimal 與差額逐項保存在 `excel_validation.json`。`1e-12 * max(1,abs(value))` 只檢查這次 Excel 交付的近似誤差，沒有批准 precision policy，也沒有放寬財務對帳或 Python／dbt 差異。

最終輸出目錄：`outputs/dbt_shadow_excel_validation_20261110/{annual_reviewed,quarterly_reviewed,adversarial_reviewed}/`。較早的 initial／final 目錄是版面 QA 中間 artifacts，未改寫其檔案或原始計算收據。

consumer code hash：`7cd84d21c14914186187138c73463fa5efb982d5314e3d4e1de7908e75e13b13`。

workbook SHA-256：

- Annual：`a8ff25c4685f888681fc07b7b997dccc96e93ef20603560ba7abce77cbc2802f`
- Quarterly：`34678168e070aed37aff4a6a38c4e102d0bccc5e33cf1b2b09066577d62352cc`
- Adversarial：`b57f219242065a13ea93cc40600c9b58c622b291c8601dea297ef899f45826d6`

## 驗證與失敗注入

- 每個 available Fact 的本機試算值與固定倉儲 numeric 值均檢查；不可用值不能變成數字。
- 在來源試算中加值、清空與設為真實零，確認重算／缺值傳遞；固定 Warehouse 值不隨來源試算改變。Review 的所有公式存檔後仍只指向 Warehouse，且 cached 值一致。
- 改寫 report、換 receipt、偽造發布旗標、改寫 Markdown 即使同步更新預覽 hash，也會在必要的語意／來源邊界被拒絕。
- 對真正匯出的 XLSX 改寫固定 numeric cell，保持原驗證 claims 不變；存檔稽核正確拒絕。
- 要求的 Excel 執行失敗會留下 `excel_status=failed` 與錯誤，不回退 Python 財務公式；MD／JSON／HTML 草稿保留。既有 Excel 輸出不能被覆寫。
- 既有 Python 年度／季度的兩頁籤匯出，以及既有 ratio commentary 的實際 Excel 測試保持通過。

最終命令 `REVIEW_EXCEL_TEST=1 python -m unittest discover -s tests`：**291 項成功、沒有略過**。Log：`/tmp/sec-warehouse-excel-reviewed-suite-20261110.log`。所有工作表及年度／季度主表已用 artifact-tool render 做視覺檢查。

renderer 對純數字字串存在呈現限制：例如 Quarterly Warehouse C10 在 PNG 顯示縮短的小數，但實際 XLSX 的該 cell 為 `t="str"`，完整保存 `0.33333333333333333333333333333333333333`。完整精度是逐一以存檔 XML 與 canonical Fact 核對，不能拿 PNG 顯示作精度驗證。沒有為改善預覽而改寫或 round 原始字串。

使用 workspace loader 提供的 bundled runtime `26.1105.12137`，未安裝 repo dependencies。執行的是 artifact-tool 重算與 XLSX 存檔檢查，**沒有執行原生 Microsoft Excel**；不能將此結果描述為原生 Excel 測試通過。

## 尚待完成

正式 warehouse reader／不可變候選與發布收據、BI views、失敗回退、identity／cash-change 採用、完整矩陣及 M4 放行仍待完成。這三份活頁簿的技術成功不授予任何發布資格。
