# 固定候選程式套件與歷史版本執行驗證

2026-11-11。SYNTHETIC-ONLY、隔離 BigQuery；不是正式部署／切換核准。

## 解決的缺口

候選 selector 先前只能記錄 A／B 的 code hash，不能證明實際執行了那個版本。新增 `scripts/runtime_package.py`：

- deterministic ZIP 封存完整財務 Python source、dbt shadow models／macros／tests、固定 kernels；同一份來源／環境可產生相同 bytes。
- SHA256 綁定套件與每份檔案；另保留原 financial code hash。安全解壓拒絕 duplicate、越界路徑、symlink、過大檔案與缺失／額外檔案；完整檢查成功才建立可用的輸出樹。
- 鎖定 Python binary hash／版本／平台，以及 dbt、BigQuery／Storage 及其遞迴相依與 extras 共 103 個 distributions 的版本和實際內容 hash。相同版本但內容不同也拒絕。
- 隔離 Python module path，使用套件內 dbt project／profile／入口及固定 Python；清除外部 PYTHONPATH，避免工作目錄或外部 dbt entry script 取代程式。dbt core／adapter 模組仍由內容鎖定的既有環境提供。
- 不打包 ADC、source bundle、報告或私密憑證；profile 只用 OAuth。失敗保存 manifest，沒有 current-code fallback。

Historical SQL 由固定 dbt manifest 的 raw_code 還原後，需重現整體原 code hash。這次 A 成功是因為其 Python／macro 等未變部分仍存在，SQL 還原也可逐 byte 重現；不保證任意歷史版本都能這樣重建。缺來源或 hash 不符會拒絕，不能猜回歷史程式。

## 套件

| 套件 | financial code hash | package SHA256 | source files |
| --- | --- | --- | ---: |
| A | 84519f624f0682396b1c0439e8a08fbe51b92cc8a04dc3ed288d297462c1a83c | 30b71d99781acaee78724f26354a332220d3f879d0af965da1083dfa776a4eca | 46 |
| B | 3b4abe108edaa84fd854e52038d61bad1227e14a6354c14050400ac0bb90aa77 | 474a65f5886da6cfc1964598ac441b2c72aab8d3ae2df654fee43742218d3154 | 47 |

共同 runtime lock SHA256：`467d4f91c1adba42f5ac2f987528234a9b6db67dbd6b600883f46cb4741ace5f`；實際 dbt-core／dbt-bigquery 均為 1.12.0。

A 的歷史 dbt manifest pin：`159a51cfdd64515ed855f531fdee919d9cbc7178ae58a3c4153e28b2c618d1c1`。兩份套件包含獨立、最小的候選 dbt project，沒有打包無關 Legacy models；其設定亦由整個 ZIP pin 固定，不宣稱原 financial code hash 本身涵蓋所有執行環境。

## 原生執行

先執行 B，再執行舊 A，均使用相同固定合成 Annual 來源與完整 reconciliation envelope；Project `focus-heuristic-438521-v4`，US，各自建立獨立 `sec_review_shadow_<run>` dataset。

| 執行 | run_id | dbt models | Facts | 計算收據 SHA256 |
| --- | --- | ---: | ---: | --- |
| B | 32cc75453f114773a25759efa5093b83 | 17 | 186 | 69e4e1be0e0662de8b99da3e67b6dbc14cadec978daf9a44f03487eaa079a83f |
| A | 9c0b49564a1c4e66b49cffd8f6cb0b05 | 16 | 186 | e32e48c202a47045560ef923fa1443cba638c46ce479c33f3cc493d320b60d31 |

兩次都通過必要 test／48 kernels 並產生 MD／JSON／HTML 草稿。收據 code hash 分別符合 A／B，A 沒有偷用工作目錄的新版 B。再次檢查 B 原計算收據，SHA 未改寫。

另對 A／B 的 186 個 SQL Fact 值、狀態、期間、定義、input／evidence 等契約欄位逐一比較，186 全數相同。這是 **SQL A 對 SQL B** 的比較，不是 Python baseline 比對，不代表核准 precision policy 或完整 M4 案例矩陣。

證據在忽略的 `outputs/dbt_runtime_package_validation_20261111/`：`package_a_final`、`package_b_final`、`b_execution/calculation`、`a_execution/calculation`、外層 package execution receipts 與 `verified_summary.json`。先前未加隔離 dbt 入口的中間 build 目錄保留原樣，不當成最終套件。

## 測試與剩餘工作

七項 unit tests：determinism、source／credential 排除、錯誤 pin／路徑／symlink、改 source 並更新個別 hash 仍無法偽裝原指紋、同 dependency version 內容異動、程序失敗保存且不 fallback、extras closure／內容 hash、無法重建或錯 manifest pin 拒絕。完整回歸 343 tests、OK、無略過，85.081 秒；最後補強的 manifest-pin assertion 亦重跑七項套件測試成功。既有 Excel 匯出／重算仍包含於回歸，原生 Microsoft Excel 未執行。

目前套件是 code＋已安裝 dependency content lock，不含可離線安裝的 wheels 或 OCI image，其他環境不符就拒絕；沒有宣稱跨平台部署重現已完成。沒有打包／驗證 Node／Excel runtime，本次 native 也沒有新的 GCS runtime 保存證據。

仍需將 runtime artifact 存放到固定 generation 的受控儲存，讓 selector 綁定並載入套件，在 SQL 執行前固定該 run 的 release，完成真正 selector→執行→回退 E2E。正式 publication registry、IAM、永久保留、完整邊界矩陣及 M4 精度／切換核准仍未完成。

同日接續已補齊上述候選接線及 GCS runtime 保存，並由 selector 驅動原生 A → B → rollback A；見 [候選選版執行驗證](dbt-selected-runtime-validation-20261111.md)。本頁保留套件建立當時的歷史驗證範圍；正式發布等剩餘項目以完成矩陣為準。
