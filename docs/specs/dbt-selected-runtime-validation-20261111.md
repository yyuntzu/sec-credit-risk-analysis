# 候選選版、固定套件執行與回退驗證

2026-11-11。SYNTHETIC-ONLY、隔離 GCS／BigQuery。第 1 項「選版本與實際執行未串接」已在候選流程補齊；正式 workflow、發布、精度及切換仍依完成矩陣處理。

## 執行流程

`scripts/selected_runtime.py` 新增候選入口：讀取啟動時的 selector → 取得該 release 固定的 GCS runtime ZIP generation → 完整檢查套件 bytes／financial code hash／dependency content lock → 在隔離 Python 中執行 → 寫入候選報告及可追查收據。

`scripts/selected_runtime_worker.py` 包住套件內的 SQL-only warehouse。它在建立真正 BigQuery client／寫入 dataset 前，確認 release 的 code／formula／policy／precision versions，將實際 run ID、entity／scope、source／request hashes 綁定到該 release 與成功 selection event。綁定完成才交給原套件執行；SQL 引擎本身沒有新增 Python 財務計算。`runtime_package.py` 記錄與財務套件分開的三份調度程式 hashes；不以財務 code hash 代表整個控制平面。

`candidate_release_control.py` 接受固定 selection snapshot，並從目前成功歷史鏈核實該 event。途中改選不改變已捕捉的版本；失敗 CAS 留下的孤立 event 不可授權執行。同一 run 若已綁定另一個 event／release，重試會拒絕。失敗可留下 binding／manifest，這些不代表計算完成；成功才寫最終 selected execution receipt。

既有 metadata-only release 保持原樣；沒有 runtime reference 時不可執行。本次使用新 release ID，沒有覆寫舊 A／B。操作方式見 [runbook](dbt-shadow-runbook.md#固定候選版本執行與回退)。

## 原生雲端證據

Project `focus-heuristic-438521-v4`，US。新 bucket `sec-review-shadow-runtime-20261111-c54e291a` 使用 uniform bucket access、public access prevention 與七日 lifecycle；不是永久保存或正式 reader／writer IAM 證據。

固定 ZIP 沿用 [套件驗證](dbt-runtime-package-validation-20261111.md) 的 final A／B 及共同 dependency lock。GCS runtime object generations 分別為 `1794417700963169`、`1794417702224424`；相同內容重試回傳相同 descriptor。註冊時保留原有同版本 Annual／Quarterly 證據，新 release A 為 `77777777777777777777777777777777`、B 為 `88888888888888888888888888888888`。

此次由 selector 實際驅動三次 Annual SQL-only 執行：

| 選擇 | 實際 run ID | 財務 code hash 開頭 | Facts | 計算收據 SHA256 |
| --- | --- | --- | ---: | --- |
| A | 3219ec680ee241c6a1145455e957229b | 84519f624f06 | 186 | b24cc1eec71228d5bd58c7e255403abdede153b167b3047f70f5313e9e025c13 |
| B | 963dbee4bcfe4c06a05db20bc81f6fda | 3b4abe108eda | 186 | 62abc043d9dc0070241a172c20fcbeda0b7ffa1ece38ab85cc37cb01d2844164 |
| rollback A | d5faf50ae6bd4a8ea4d86aef05b6e922 | 84519f624f06 | 186 | d3bb5043bae1fa013dab60587d30824b6577b4b211a59e6341e2692f426a34da |

三次均通過套件內 dbt tests／kernels，產生候選 MD／JSON／HTML。每個實際 run 都有對應固定 generation 的 GCS binding，並與最後計算收據核對身份及版本。改選、回退之後重驗前面已完成收據，bytes 未改變；最初 A 與回退 A 的 186 個完整 warehouse Fact rows，在只排除 `run_id` 後全數相同。

實際 GCS 拒絕兩項：下載後 SHA256 校驗錯誤、指定 object generation 不存在。失敗沒有退回當前 source 或 Python 計算。這不是 production 發布中斷或真實服務帳號 IAM 故障注入的證據。

可重跑驗證工具為 `scripts/validate_selected_runtime.py`；需新 bucket／selector 與新輸出目錄。此次完整證據在忽略的 `outputs/dbt_selected_runtime_validation_20261111/native/`，包含 `probe_manifest.json`、`verified_summary.json` 及三個 `run_*/`。probe manifest SHA256：`1aca515ecb1f5bcef0635105e54f19ec445a6bd8fbadc93aae911649409f0700`。先前沙箱 DNS 失敗只留下外層空目錄，已確認程序結束才改用允許連線的 native 執行，未重跑已完成批次。

## 本機驗證與範圍

完整 `REVIEW_EXCEL_TEST=1 python -m unittest discover -s tests`：**349 tests，OK，無略過，97.392 秒**；log `/tmp/sec-selected-runtime-full-20261111.log`。新增覆蓋 selection snapshot 跨 pointer 變更、同 run 改綁拒絕、孤立 event 拒絕、runtime generation／checksum／版本、缺件時不啟動計算、SQL 前固定 binding 以及版本不符時不建立 warehouse client。途中改選與孤立 CAS 的執行授權由本機測試驗證；雲端原生則為依序 A → B → A，不宣稱已做原生並行競爭測試。

精度與 publication flags 全程 false。這次三份結果是候選 SQL-only 執行，沒有 Python baseline 比對；不以 A／A 相同推定 Python 精度差異已通過。環境需符合已安裝 dependency 內容鎖，跨主機 wheels／OCI、Node／Excel runtime 打包、永久保存、正式 publication registry／IAM 與正式預設切換仍未完成。
