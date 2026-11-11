# 候選交付 Cloud Storage 保存驗證

日期：2026-11-10。限 SYNTHETIC-ONLY；維持影子模式、精度待定、publication=false。

## 契約與實作

`scripts/delivery_archive.py` 將固定 SQL 計算收據、BigQuery archive attempt 與交付檔案綁定。上傳前檢查三個外部 pins（計算、preview manifest、archive receipt），確認同 run／entity／scope／計算快照；重新呈現並逐 byte 比較 HTML／MD／JSON／commentary／ratio analysis；Excel 重新稽核儲存的 ZIP XML、Fact 完整性、有序綁定及精度字串。它不執行 Python 財務公式，也不讀 baseline 補數。

GCS 對每份檔案使用 create-only generation precondition；已存在時必須讀回相同 bytes 才接受重試。最後才寫 commit，列出全部物件的 generation、SHA256 與大小。讀取端使用收據指定 generation，另驗 SHA256，完整驗證成功才寫出檔案。依據 [Cloud Storage request preconditions](https://docs.cloud.google.com/storage/docs/request-preconditions?hl=en) 與 [checksum metadata](https://docs.cloud.google.com/storage/docs/metadata)。SDK 上／下載亦要求 CRC32C；CRC32C 不取代外部固定的 SHA256 收據。

這不是 WORM 或正式 IAM 邊界。管理者仍可能更改／刪除物件，屆時固定 generation 不存在就失敗；不改讀新版。bucket labels 用於測試用途檢查，不是 project ownership 證明或正式 consumer 授權。

## 實際雲端結果

- Project：`focus-heuristic-438521-v4`；bucket：`sec-review-shadow-delivery-20261110-b41e90c2`；US。
- 建立時啟用 uniform bucket-level access、public access prevention=enforced、age=7 的 lifecycle delete rule。不是永久保存；lifecycle／soft delete 的實際刪除時間由 GCS 執行，bucket 不宣稱自動刪除。
- 原 SQL run：`635cbe41327b4092ab33e36e58565324`；archive attempt：`11111111111111111111111111111111`；delivery ID：`44444444444444444444444444444444`。
- 直接使用已固定的舊 SQL 快照，不重新計算其財務數字。此次只以目前 consumer 重新產生候選交付；186 個 Facts 的活頁簿仍是同一份 SQL 數值，精度差異不予豁免。
- 上傳並逐 byte 還原 10 份檔案，共 597,125 bytes：報告 JSON／MD／HTML、commentary、ratio analysis、Excel、Excel audit、preview manifest、計算收據及 candidate archive 收據。
- 相同 delivery ID 重試得到完全相同的 storage receipt，所有 object generations 保持固定。

Storage receipt SHA256：`6ebda53e05b45caab16ff7a0ba42bd9e666e833b035ebd2f7f064bae7d43d43c`。

Commit generation：`1794370055035774`；commit SHA256：`7af6d6c14a741ae3051790797f668cfc7b4ecb4721d63d24dc5ffa3ac84edb3f`。

計算收據 pin：`c70049473c20a95850c11c85c21b833d7ffcd915cff1fd2d8351d15bed6caf4a`；archive pin：`2b7978023a429e58122e173b342845aae28339598d860a3a114cac471daf4b56`；preview manifest pin：`7541a66a38b4627abcac15615cf7e7eef61402fb1bae6addc3d924f2cbe073b6`。

Delivery verifier code hash：`c2e9878f2710cce8c87fd74c1b70611f7a36dd99aee84aa916ac97120b313d02`；consumer hash：`6b9837cf8f5dda8bd062286cff4629c38301b43d45cadfa69ee77feb13855e26`。

## 拒絕案例與回歸

`scripts/validate_delivery_storage.py` 在同一個合成測試 bucket 實際驗證：

| 案例 | 結果 |
| --- | --- |
| 收據提供錯誤的預期 checksum | 下載後 SHA256 檢查拒絕，沒有還原輸出 |
| 收據指定不存在的 generation | GCS NotFound；不改讀 latest |
| 收據 run 與 commit 不同 | 拒絕 Mixed delivery run |
| 同 delivery ID、相同 bytes，但改動 required_excel 契約 | create-only commit 拒絕不同內容，不覆寫原 commit |

四項均通過拒絕檢查；最後重新讀取原 commit，bytes 與 live generation 仍相同。這些是指定 checksum／generation／身份／契約的失敗注入，不宣稱已實際破壞正確的 GCS 物件。

五項新增單元測試另涵蓋：重新填入 artifact hash 與 preview pin 仍無法掩蓋錯誤內容、要求 Excel 卻未產生、混入其他 archive run、部分上傳重試、損壞下載內容、歷史 generation 與 current 分離、錯誤 namespace／pin／路徑。

完整回歸 `REVIEW_EXCEL_TEST=1 python -m unittest discover -s tests`：324 tests、OK、無略過，106.440 秒。包含實際 Excel 匯出與重算；原生 Microsoft Excel 尚未執行。此次候選活頁簿沿用已檢查的版型及相同 SQL 快照，未改動視覺內容或樣式。

證據位於被忽略的 `outputs/dbt_delivery_storage_validation_20261110/`：`annual_preview`、`annual_store`、`annual_retry`、`annual_restored`、`rejection_probes/probe_manifest.json`。

## 尚未完成

GCS commit 是候選交付完成紀錄，不是正式發布收據。它尚未自動寫回 BigQuery 的正式 publication registry；正式 consumer IAM、永久保存、release／rollback 與精度核准仍待完成。正式發布前亦須重新驗證完整 BigQuery candidate snapshot；本次交付準備只驗證固定 archive receipt 的交叉 binding，不宣稱它已重新查核所有遠端 BQ 列。
