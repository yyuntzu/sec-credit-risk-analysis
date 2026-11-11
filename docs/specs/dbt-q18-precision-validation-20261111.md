# q18 HALF_EVEN 精度核准與候選驗證

2026-11-11。使用者明確回覆「核准上述方案，開始實作與驗證」。本頁取代先前「精度待定」對本方案的限制；**正式報告來源、發布及切換尚未放行**。

## 已核准的規則

- 財務來源以原始字串、scale／quantum 保存，無損 normalization 失敗直接阻擋，整筆金額不經 FLOAT64。
- `bignumeric-q18-half-even-v1`：每個除法公式結果取小數點後 18 位，HALF_EVEN；下一層使用此 canonical Fact。加減保留 BIGNUMERIC 可精確表示的值，超界阻擋。
- 同一新規則下 Python 獨立參考值與 SQL 要求數值完全相等；沒有 epsilon。舊 Python 預設 28 有效位數的結果與差額另外保存，歷史結果不回填。
- 缺值／零分母維持不可用，不將溢位當作缺資料。微小除法結果可能依規則成為零；下游若因此遇零分母就不可計算。

`precision_policy_implementation_approved=true` 表示此次規則實作核准。既有 candidate `precision_approved=false` 是尚未啟用正式 release 的門檻，並不否認此次使用者核准；`publication_eligible` 仍 false。preflight 現在區別「規則核准但 release 尚未啟用」與舊未核准精度，不以 26／18 筆已核實政策差異冒充未解算式錯誤。

## 為何多一個精確除法函式

直接 `ROUND(n/d,18,'ROUND_HALF_EVEN')` 無法復原原生除法先修約掉的尾數。本次原生反例：

`50000000000000000000.00000000000000000001 / 1e38` 嚴格大於 `0.0000000000000000005`，q18 應為 `0.000000000000000001`；原生先除法再 ROUND 得到零。負數對應案例也重現此問題。

`references/dbt/macros/shadow_precision.sql` 定義 BigQuery 內的 `review_divide_q18_v1`。其 JavaScript UDF 接收 BIGNUMERIC operands 的十進位字串，以字串整數長除法及餘數比較直接進行一次 HALF_EVEN，再 cast 回 BIGNUMERIC。只有單一數字、進借位與小指數使用 Number，整筆財務值不轉浮點，也不依賴外部 library／遠端函式或 Python 計算結果。由 configuration model 的 pre-hook 建立，每個 run 各用自己的隔離 dataset；runner 核對實際 routine body 與固定 macro，並保存 body SHA256。

這是 dbt 定義、BigQuery 執行的財務邏輯。Python `scripts/precision_policy.py` 使用獨立 Fraction／整數 divmod oracle 作遷移驗證；SQL-only 路徑不呼叫它。Google 官方支援 [十進位 HALF_EVEN ROUND](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/mathematical_functions#round)，亦提醒 [JavaScript UDF 的 NUMERIC／BIGNUMERIC 轉換可能失去精度](https://docs.cloud.google.com/bigquery/docs/user-defined-functions)；本函式明確使用 STRING 跨界。

## 追溯與比對

`int_review_shadow_calculated`／最終 Fact 的 `precision_audit` 保存 policy、精確分子／分母、原生未量化除法值與 canonical 結果。重複小數的真正未量化值以分子／分母完整表示；native_value 只是 BIGNUMERIC 原生近似結果，不能當作精確有理數。source original value／scale 仍在原本欄位。

影子比較新增 canonical reference graph，先獨立選取的 Python baseline 來源，依有序依賴逐 Fact 計算新規則，再核對全部值、狀態、身份／公式契約與 division audit；commentary 成長率也依新規則核對。canonical mismatch 進入既有 mismatch gate／固定計算收據，失敗時候選 reader 拒絕。`comparison.json` 同時保留舊 Python 差異與新規則逐 Fact 比較；不能只把舊 28 位結果取 18 位當作參考。

## 原生證據

Project `focus-heuristic-438521-v4`、US；全為 SYNTHETIC-ONLY。共同財務 code hash：`1e3c61ae7710e2e62e7bdee1f78c4d29bdb13ae00630364baff1ae5c39408c73`。routine body SHA256：`e3e47cc5f824c8ed9afbdab9bfd8c07aba8a3ef4bb7c6afb03f651182ae60b95`。

| 執行 | run ID | Facts | canonical mismatch | 舊 Python 值不同 | 計算收據 SHA256 |
| --- | --- | ---: | ---: | ---: | --- |
| Annual shadow | a44f3f703c774be3aef9cac649be8b2b | 186 | 0 | 26 | ef9100225ff866e0a7fa4ca1c922d652db52ad530d830555c5be547362acab00 |
| Quarterly shadow | a80f6a7f22f34fd1b4a85a6b8cc84faa | 124 | 0 | 18 | 55b5fb9d4a563bab197592feb2bb90d40b50a8cf25bba697dd1ce331a1644793 |
| Annual SQL-only | 143e863f43684981bca4c50eacd04649 | 186 | 未執行比較 | 未執行比較 | 63108a2c6b6e8a79708402d12499d2347d990d40c64c1ecd25b3cbc7274aa1e2 |

前兩次 source／status／公式／對帳／readiness／commentary 的未解 mismatch 都是零；獨立核對 division audit 分別 61／37 筆。每次 dbt integrity test 通過含 21 公式的 62 kernels。SQL-only 停用 27 個 Python 財務／比較函式，含新增 Fraction formula／q18／canonical graph，仍成功；其 comparison=not_run 不冒充比較證據。

`validate_precision_boundaries.py` 另跑 **224 個原生案例，零 mismatch**，包含正負 ties、carry、tiny／large、NULL、零分母與 200 組固定種子隨機值。native 直接 ROUND 的兩個 double-rounding 錯誤由精確函式正確處理；串接 canonical `1/3`、精確加總三份 `1/3`、除以 2 的 tie、canonical 零分母也通過。正負 `1e38 / 1e-38` 都因輸出超界而失敗，沒有藏成 NULL。

主 boundary job：`49e875e5-0cac-4f02-a7cf-2b392e68991f`；chain job：`4f733b5b-ea7b-4848-8033-c2ecc4c89e4c`。原始證據在忽略的 `outputs/dbt_q18_validation_20261111/{annual,quarterly,sql_only,boundaries}`，包含完整 fixtures、原生值／naive 值／精確預期值、失敗 job 及收據 pins。

完整 `REVIEW_EXCEL_TEST=1 python -m unittest discover -s tests`：**357 tests，OK、無略過，95.354 秒**；log `/tmp/sec-q18-final-full-20261111.log`。含獨立手算 signed ties、二次修約反例、固定種子隨機 JavaScript／Fraction 交叉驗證、context independence、canonical parents、來源不改寫、audit 拒絕、範圍拒絕與 preflight 分離核准。原生 Microsoft Excel 未執行。

## 固定候選套件整合

新 q18 source／SQL／kernels 封成 49 個檔案的固定 ZIP：SHA256 `a074b24fc4e0fc2ddae287e96c912e802e041add9a2ea1836044454cd9d0f0c9`，共同 dependency lock 沿用 `467d4f91c1adba42f5ac2f987528234a9b6db67dbd6b600883f46cb4741ace5f`。存到既有隔離 bucket `sec-review-shadow-runtime-20261111-c54e291a`，object generation `1794419891904722`。

使用上表 Annual／Quarterly 證據註冊新候選 release `99999999999999999999999999999999`，generation `1794419934339750`、SHA256 `ae7c99d59c26a2456e51dadb49a22efdcd92f212c91c67b04fa789b11b9cf111`。僅更新此隔離 selector，event `44444444444444444444444444444444`、pointer generation `1794420121365065`；未覆寫舊 A／B release，也未變更正式 workflow。

selector 實際執行固定 q18 套件，run `42d15eae08654c5b8124e6003b2a0152`、186 Facts，計算收據 SHA256 `6a8ce9c38fbe6108a335f0ce2b4d43c182ae208a72895c45219567cc31276229`。在 SQL 前有對應固定 GCS binding，package receipt 中的 code／runtime hash 正確；完整 warehouse Facts 只排除 run ID 後，與已完成 Fraction 比較的 Annual run 全部相同。這次 packaged run 本身仍為 comparison=not_run，不能與前面的獨立比較混為一筆證據。

原始 artifacts 在 `outputs/dbt_q18_validation_20261111/{runtime,runtime_store,runtime_release,runtime_selection,selected_execution}`；同根目錄 `verified_summary.json` 固定各比較檔案／收據 hashes 及此次相同結果核對。預檢仍明確 blocked（CLI 預期 exit 2），正確列出 precision release 未啟用、財務必要欄位缺件與發布／交付／保存／IAM 缺口；規則實作核准及 canonical verification 均明確辨識。

## 剩餘邊界

本頁完成第 2 項「明確精度規則、獨立驗收及差異記錄」的候選實作；不是完整 M4 案例矩陣或正式部署。每公式的業務狀態、極端複合運算／財期／來源組合仍見完成矩陣。表格保留七日測試到期設定，routine 不會隨 table expiration 自動消失；正式保存與 IAM 尚未部署。精度核准不代替 financial acceptance、delivery、publication registry 或正式切換核准。
