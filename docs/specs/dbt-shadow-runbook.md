# dbt 財務影子比對操作手冊

本手冊包含 [遷移規格](dbt-financial-calculation-migration.md) 的 M0–M3 候選功能；不代表各階段均已完成。依使用者指示，精度仍待定，**不切換 cloud authority**。本機／既有 cloud 預設仍為 Python。新增 SQL-only 候選測試不會取代需要獨立執行的遷移影子比對。

## 已實作的範圍

- `scripts/dbt_shadow.py` 固定 source bundle hash、無數值的 slots／有序依賴 plan、Python baseline、Decimal context、commit 與相關來源 code hash。
- SQL 從完整 source candidates 獨立選取與採用數值，不讀 Python baseline 或 Python 已算好的 inputs.value。
- `references/dbt/models/shadow/` 形成 staging → selection → adoption → 分層計算 → Fact、input bridge、診斷對帳及公式 fixtures。
- 新增 `scripts/shadow_reconciliation.py` 與 `--reconciliations`：SQL 獨立重算 BS equation／cash bridge，檢查有序組成、來源證據、結構化覆核 binding、原始來源精度 tolerance 及申報期間。未提供覆核的期間仍為 not_calculable／未驗證。
- SQL macro 涵蓋 21 個現有 formula IDs。DER identity 可透過來源綁定的個別覆核進入影子報表；CASH-CHANGE 需完整橋接及相符 definition evidence 才採用。沒有完整覆核就不推算補值。
- BigQuery 原生 BIGNUMERIC 與 Python Decimal 原結果逐一比對，不加 ROUND、不用 epsilon。非數值狀態、identity、定義、原值／scale、有序 input_ids、evidence IDs 也比對。
- CLI 輸出 comparison JSON／CSV、原始 warehouse facts、kernel results、baseline 與 run／test／manifest hashes。
- `fct_review_shadow_acceptance` 從 SQL Facts、必要報表格子、政策及對帳覆蓋獨立產生財務 readiness；與 Python 比較後保存 `acceptance_comparison.json`。財務 readiness 不包含精度核准／交付放行，所有正式發布旗標仍關閉。
- `scripts/warehouse_candidate.py` 以外部固定的計算收據 hash 讀取已保存的 BigQuery 結果快照，生成 dbt 數值的 MD／JSON／HTML 草稿；不讀 Python baseline，也不呼叫 Python 財務計算／驗收引擎。
- 每次 live 執行建立獨立 `sec_review_shadow_<run_id>` dataset；表預設七天到期。dataset／views 不宣稱自動刪除。拒絕重用 dataset 或已有的輸出目錄，不操作既有 `sec_raw`。

## 候選結果雲端保存與讀回

此介面只接受 `sec_review_shadow_*` dataset；不寫正式表。保存的是已完成計算的快照，archive attempt 不代表重新計算財務數字。不要以最新時間或不完整 run key 選取資料。

```bash
python -m scripts.candidate_archive store \
  --shadow-dir /absolute/path/completed-shadow \
  --receipt-sha256 CALCULATION_RECEIPT_SHA256 \
  --project your-project --dataset sec_review_shadow_archive_unique \
  --attempt-id UNIQUE_32_HEX_ID --build-models \
  --output-dir /absolute/path/new-archive-output

python -m scripts.candidate_archive restore \
  --archive-receipt /absolute/path/new-archive-output/archive_receipt.json \
  --archive-receipt-sha256 PINNED_ARCHIVE_RECEIPT_SHA256 \
  --output-dir /absolute/path/new-restored-calculation

python -m scripts.candidate_archive facts \
  --archive-receipt /absolute/path/new-archive-output/archive_receipt.json \
  --archive-receipt-sha256 PINNED_ARCHIVE_RECEIPT_SHA256 \
  --output-dir /absolute/path/new-typed-facts
```

呼叫端應從可信的前一步保存收據 hash，不能把剛讀到的不可信檔案自行計算 hash 當成驗證。`restore` 逐 byte 驗證檔案並恢復計算套件；`facts` 另外查詢 typed Warehouse view，檢查完整 identity、coverage、Decimal 與原快照相同。兩者都不呼叫 Python 財務公式補值。

`--build-models` 執行 `formal_review_archive` tag 的八個 models 與完整性測試。保存失敗會保留 failed manifest；相同 attempt、相同內容的重試可讀回相同收據，已有部分或不同內容時拒絕覆寫。新程式／來源版本應建立新 run；同一 run 的 bindings 不能改寫。

目前表預設七天到期。這不是正式歷史保留或 WORM：具有管理權限的人仍可能改表；digest／receipt 用於偵測異動，正式 IAM 和發布隔離仍待完成。雲端 Excel／HTML 備份亦不在此 archive 範圍。實際驗證與失敗注入見 [候選保存驗證](dbt-candidate-archive-validation-20261110.md)。

## 不執行 Python 基準的 SQL-only 候選入口

```bash
python -m scripts.warehouse_execution \
  --source-bundle /absolute/path/source_inputs.json \
  --project your-project \
  --kernel-cases tests/fixtures/dbt_shadow/kernel_cases.json \
  --reconciliations /absolute/path/reconciliations.json \
  --candidate-preview --output-dir /absolute/path/new-sql-execution
```

此入口使用同一套 value-free 計畫與 raw candidates，但不呼叫 Python 來源採用、財務計算、對帳、readiness 或影子比較引擎。公司來源、公式與驗收由 SQL 執行，Python 只做 metadata／結構／收據核對與呈現。`--reconciliations`、`--commentary-documents` 可省略；缺少必要覆核仍按 SQL 規則保留缺值或 draft。

收據型別為 `warehouse-execution-v1`，另綁定 `request_hash`；comparison 明確是 `{"status":"not_run","mode":"dbt-only"}`，不填零差異。輸出 `execution_manifest.json`，不產生 baseline／comparison 檔案；失敗保留 failed manifest，禁止 Python fallback。現有 v1／v2 shadow 收據仍照原方式讀取，不能把 shadow mismatch 改寫成 SQL-only 成功。

目前仍使用獨立 `sec_review_shadow_<run>` dataset，precision／publication 均為 false；不是正式 cloud 模式。發布前診斷會指出這份執行沒有遷移比對證據。切換前仍須用獨立 shadow 路徑、完整案例矩陣及版本化放行證據證明政策／模型版本已驗證；正式 runtime 未來不應再以每次執行 Python 公式作第二個權威。

原生禁用函式驗證另用 `python -m scripts.validate_sql_only`，參數同上但不帶 `--candidate-preview`（固定要求 `--kernel-cases`，預設產生草稿），只接受 SYNTHETIC-ONLY。詳見 [SQL-only 驗證紀錄](dbt-only-execution-validation-20261110.md)。

## SQL 的公式契約

`dim_review_shadow_configuration` 固定當前 SQL 版本的百萬金額 scale、Standard EBITDA basis、formula／policy／precision versions 與未核准精度旗標。來源 normalization 與 basis 採用這份 SQL 設定；producer 的同名欄位另以 `declared_*` 保存，必須相符才通過契約。修改 CLI metadata、甚至同時修改計畫與 metadata，不能改變計算基礎或自行核准精度。需要新政策時必須有版本化 SQL 變更與對應放行，而非修改輸入 JSON。

`dim_review_shadow_formulas` 在 dbt 內定義 21 個公式 ID 的合法目標、輸入科目順序與單位；COMMON-SIZE 另展開九個收入表科目。`int_review_shadow_formula_contracts` 對照每個 slot 的計畫，而不是從 Python 傳來的 plan 推定何者正確。

SQL 從原始 request periods 重建合法期間／期初現金日期、前期角色與 LTM 起點，檢查目標幣別、instant／duration、輸入單位／順序／角色／日期、版本及依賴深度。`dim_review_shadow_metric_policies` 另固定合法單位、必要核准項目及受政策約束的定義；來源採用依此清單，不使用 Python 刪改後的 pending 清單放行。首個 FY 沒有前期、或缺少來源格子，可以是合法的不可計算；不能因此把輸入換成其他科目或年度。

契約不符時，計算 gate 不產生衍生數值，必要 dbt test 以 error 拒絕整個執行收據。候選表可能已存在，仍不能當成成功或可發布結果。驗證工具 `python -m scripts.validate_formula_contracts` 只接受合成 annual 來源，注入交換輸入、錯公式、arity、錯年度，以及刪除 DEC-03 後提供 DSCR 數字五種計畫，並固定更新 plan hash，以證明是 SQL 商業契約拒絕。實際證據見 [公式與政策驗證](dbt-formula-policy-validation-20261111.md)。

設定竄改另用 `python -m scripts.validate_canonical_configuration --case scale|basis|versions`，搭配 `--source-bundle`、`--kernel-cases`、`--output-dir` 及選用 `--project`；僅允許合成資料。各 case 使用新的隔離 dataset，不能重用既有目錄。見 [設定驗證](dbt-configuration-validation-20261111.md)。

## DER identity 覆核輸入

Shadow 來源包可附加 `identity_reviews`，不需另開核准旗標。它是公司／期間個別覆核資料，不是一般商業政策核准；沒有此欄位就不推算 DER。現有 Python 正式入口尚不採用這個影子擴充。

Envelope 固定欄位為 `schema_version: 1`、`source_hash`、`reviews`。`source_hash` 是移除整個 `identity_reviews` 欄位後，對原來源包計算 canonical SHA256。每個 review 固定欄位：`fact_id`、`formula_id`（DER-01..06）、非空 `formula_version`、有序兩個 `input_ids`、完整 `Evidence` 物件 `evidence`。

Evidence 必須是同 entity／scope、涵蓋目標期間、截至 as_of 已存在的 definition；`content` 是以下物件的 JSON 字串，所有欄位必須符合實際請求：

```json
{
  "source_hash": "HASH_OF_SOURCE_WITHOUT_IDENTITY_REVIEWS",
  "entity": "ENTITY", "scope": "SCOPE", "fact_id": "gross_profit:fy_t",
  "formula_id": "DER-01", "formula_version": "REVIEWED_VERSION",
  "input_ids": ["revenue:fy_t", "cost_of_revenue:fy_t"],
  "period_role": "fy_t", "start": "2025-01-01", "end": "2025-12-31",
  "currency": "USD", "unit": "money", "complete": true
}
```

覆核應由人確認包含／排除項目及同一會計範圍；欄位寫成 true 或 hash 相符本身不能證明文件真實性。不得憑數字湊得出來而自行建立業務覆核。合成測試中的證據只用於測試。

計算 plan 保存覆核與有序依賴，來源包與 plan hash 一併綁定收據。SQL 自行檢查 formula／metric 對應、期間／幣別／單位、證據 claim 與來源 binding，並保留 sourced／conflict／not_applicable；consumer 只採用收據中的結果及證據，不重算 DER。

## CASH-CHANGE 的完整橋接門檻

沿用 `--reconciliations`，不另設自動放行旗標。SQL 先形成 `int_review_shadow_calculated`，由 reconciliation model 獨立驗證橋接，再讓最終 `fct_review_shadow_facts` 採用現金變動；readiness 與敘述均讀最終 Facts。這個順序避免對帳與最終數值互相循環依賴。

必要條件：同期間／範圍／幣別的 ending cash 與 beginning cash、CFO、CFI、CFF、cash_fx、cash_other 全部可用；有序 terms、來源 lineage、金額 claim、原始精度 tolerance 與結構化覆核相符；覆核日期不能晚於 as_of。橋接須 verified，而且至少一個 **definition** evidence 綁定同一份橋接。只有 kind=review 雖可能通過對帳，仍不能授權 CASH-CHANGE。

放行後由 BigQuery 算 ending−beginning，保留兩個有序 input_ids、來源證據與 definition evidence；不覆寫來源衝突／不適用。沒有 FX／other 或只是金額剛好相等，不會以零補缺值。Quarterly 既有版型沒有 Annual Cash Flows，不因此新增報表列；未提供的現金橋接仍保留為驗收阻擋。

## 發布前診斷（仍不發布）

```bash
python -m scripts.publication_preflight \
  --candidate-dir /absolute/path/new-restored-calculation \
  --receipt-sha256 PINNED_CALCULATION_RECEIPT_SHA256 \
  --output-dir /absolute/path/new-publication-preflight
```

先驗證完整計算套件，再保存 `publication_preflight.json`。目前 shadow 收據缺乏正式 release 核准、交付收據、永久保存與 consumer IAM 證據，因此 CLI 預期回傳 exit code 2，結果為 blocked。這是診斷，不是 publication receipt；沒有可跳過核准的 CLI 旗標。精度差異與財務 readiness 阻擋另列，不能用其他技術檢查成功抵銷。

## 交付檔案的 Cloud Storage 保存

BigQuery archive 保存計算與分析資料；Cloud Storage 保存固定的 HTML／MD／JSON／Excel。先建立目前 consumer 版本的候選預覽，再固定 preview manifest hash。下列命令預設要求 Excel 成功；`--without-excel` 只適用於明確不要求 Excel 的候選交付，並會寫入不同的交付契約，不能繞過正式發布要求。

```bash
python -m scripts.delivery_archive store \
  --calculation-dir /absolute/path/completed-shadow \
  --preview-dir /absolute/path/verified-preview \
  --calculation-receipt-sha256 PINNED_CALCULATION_RECEIPT_SHA256 \
  --preview-manifest-sha256 PINNED_PREVIEW_MANIFEST_SHA256 \
  --archive-receipt /absolute/path/archive_receipt.json \
  --archive-receipt-sha256 PINNED_ARCHIVE_RECEIPT_SHA256 \
  --delivery-id UNIQUE_32_HEX_ID \
  --project your-project --bucket sec-review-shadow-delivery-unique \
  --create-bucket --output-dir /absolute/path/new-delivery-attempt

python -m scripts.delivery_archive restore \
  --storage-receipt /absolute/path/new-delivery-attempt/storage_receipt.json \
  --storage-receipt-sha256 PINNED_STORAGE_RECEIPT_SHA256 \
  --output-dir /absolute/path/new-restored-delivery
```

`--create-bucket` 只建立隔離命名的測試 bucket，設定 uniform bucket-level access、禁止公開存取及七日 object lifecycle delete rule；不建立正式永久保留或服務帳號權限配置。既有 bucket 必須符合相同用途 labels 與公開存取限制；labels 不是 IAM 授權或 project ownership 證明。正式使用前仍需驗證實際專案、consumer 權限與保存政策。

上傳前驗證計算 pin、archive attempt、preview pin、全部檔案 hashes、重新呈現內容及 Excel 實際存檔。每個 object 使用 `if_generation_match=0`，不覆寫；重試必須與既有 bytes 完全相同。最後才寫 `delivery_commit.json`，收據列出指定 generation、SHA256 與大小。restore 依固定 generation 讀取，全部檔案核對成功才建立輸出目錄，不取 latest。

更動程式、交付需求或內容應建立新的 delivery ID。失敗保留 manifest；已上傳的部分檔案不刪除，沒有完整 commit 就不是完成的候選交付。保存成功也不是 publication receipt；正式發布仍需獨立 gate。實際證據見 [交付保存驗證](dbt-delivery-storage-validation-20261110.md)。

## 候選 release 選擇與回退

這是候選控制層，不能切換正式 authority。`candidate_release_control` 以固定 Annual／Quarterly 計算收據建立 release，保留 code／formula／policy／precision versions 與每個 case 的比較狀態；同一 release ID 不可覆寫。只有 candidate flags=false 的紀錄可註冊。

```bash
python -m scripts.candidate_release_control \
  --project your-project --bucket sec-review-shadow-control-unique \
  --output-dir /absolute/path/register-output --create-bucket \
  register --release-id RELEASE_32_HEX \
  --case /absolute/path/annual-calculation ANNUAL_RECEIPT_SHA256 \
  --case /absolute/path/quarterly-calculation QUARTERLY_RECEIPT_SHA256

python -m scripts.candidate_release_control \
  --project your-project --bucket sec-review-shadow-control-unique \
  --output-dir /absolute/path/select-output \
  select --release-id RELEASE_32_HEX --event-id EVENT_32_HEX \
  --reason 'Candidate evaluation' --actor 'operator' --expected-generation 0

python -m scripts.candidate_release_control \
  --project your-project --bucket sec-review-shadow-control-unique \
  --output-dir /absolute/path/current-output current
```

首次選擇的 expected-generation 是 0；後續從 `current` 的 **pointer record.generation** 取得，不是 release object 的 generation。選擇事件先不可變保存，再以 generation CAS 更新唯一 `current.json`；同時更新時只有符合舊 generation 的請求成功，不能用重試直接覆蓋別人的選擇。相同 event ID／同內容在已完成後重試會得到相同結果；同 ID 不同內容拒絕。

`rollback` 參數同 `select`，但指定的 release 必須曾在目前事件歷史中成功選用，且需明確 reason／actor。未註冊／未選用、stale generation 與提升 precision flags 均拒絕。actor 是提交的稽核標籤，不是身份驗證或使用者切換核准。

`bind --run-id ... --entity ... --scope ... --source-hash ... --request-hash ...` 固定 run 的版本。已綁定 run 永遠讀回原 binding；更改來源／request 直接拒絕。A→B→rollback A 只讓之後的新 binding 回到 A，不改寫舊 B binding。

release／events／run bindings 都使用 create-only objects，generation／SHA256 固定；CAS 只修改 current pointer。失敗的 CAS event 可能留下不可變孤立紀錄，不代表它已選用；回退只沿 current 的 parent chain 查歷史。這不是 WORM，正式 IAM／永久保存與固定程式套件 runtime 仍待接線。候選 selector 尚未接入正式報告執行，不宣稱已完成財務 runtime 回退。見 [候選版控驗證](dbt-candidate-release-validation-20261111.md)。

## 固定候選程式套件

`runtime_package` 將財務 Python 原始碼、shadow dbt models／macros／tests、手算 kernels 與無金鑰 OAuth profile 封成 deterministic ZIP。來源包、報告、ADC 與憑證不放進套件；套件需要外部固定 SHA256。Python binary、平台與 dbt／BigQuery 等 103 個相依 distribution 的版本及內容 hash 一併鎖定，環境不符就拒絕，不自動改裝或換版。

```bash
python -m scripts.runtime_package build \
  --expected-code-hash VERIFIED_FINANCIAL_CODE_HASH \
  --output-dir /absolute/path/new-runtime-package

python -m scripts.runtime_package run \
  --package /absolute/path/new-runtime-package/runtime.zip \
  --package-sha256 PINNED_PACKAGE_SHA256 \
  --source-bundle /absolute/path/source_inputs.json \
  --reconciliations /absolute/path/reconciliations.json \
  --project your-project --output-dir /absolute/path/new-package-execution
```

舊版可另外提供 `--dbt-manifest PATH --manifest-pin SHA256`，只還原該 manifest 的 SQL 原始碼；必須重現整份原有 financial code hash 才接受。Python／macro／其他來源若已無法精確重建就拒絕，不能假裝歷史版本相同。之後應保存已封好的套件，不能依賴永久可從 manifest 猜回所有來源。

執行前檢查所有檔案 hash、ZIP 路徑、重複項與 symlink、相依內容及實際程式指紋。執行使用隔離的 Python module path、套件內的 dbt project／profile／入口，不使用工作目錄的新程式或任意外部 dbt command。失敗保留 `package_execution_manifest.json`，不 fallback；成功的計算結果在 `calculation/`，外層收據連結套件 SHA、runtime lock 與計算收據。

目前驗證範圍是相符的既有 Python 環境與 MD／JSON／HTML 候選執行；沒有宣稱已打包 wheel／OCI image、跨平台部署、Node／Excel runtime、GCS runtime 存放或 selector 自動載入。見 [固定套件驗證](dbt-runtime-package-validation-20261111.md)。

## 執行前提

使用已安裝專案依賴的 Python，包含 google-cloud-bigquery、dbt-core、dbt-bigquery。ADC 必須能建立隔離 dataset、載入資料、建立 view／table 及執行查詢；缺少權限即報錯，不改走本機引擎。驗證所用版本應記錄於 dbt artifacts；本次環境為 dbt-core／dbt-bigquery 1.12.0。

來源包是新版 `source_inputs.json`（包括原 request／inputs metadata／完整 evidence candidates），不是 `report.json`。目前不支援 workbook `base_report` 路徑，會明確拒絕；不能當作已驗證的 SEC 來源。SQL 現已支援結構化對帳覆核；只通過個別對帳檢查不等於完整財務驗收，更不授予發布資格。

## 獨立執行（建議先用合成來源）

從 repo root 執行，以下以 `python` 表示具備依賴的 interpreter：

```bash
# 只保存比對基準與輸入，不使用雲端
python -m scripts.dbt_shadow \
  --source-bundle /absolute/path/source_inputs.json \
  --output-dir /absolute/path/new-shadow-prepared \
  --prepare-only

# 真正在隔離 BigQuery dataset 執行 SQL、dbt tests 與比較
python -m scripts.dbt_shadow \
  --source-bundle /absolute/path/source_inputs.json \
  --project your-project \
  --kernel-cases tests/fixtures/dbt_shadow/kernel_cases.json \
  --output-dir /absolute/path/new-shadow-live
```

`BQ_LOCATION` 預設 US；`DBT_EXECUTABLE`／`DBT_PYTHON` 等配置沿用 ReviewCloud。獨立 CLI 不呼叫 SEC／模型 API，也不具備正式發布介面。

## 跟既有報告一同執行

```bash
python scripts/agent_runner.py TICKER \
  --request /absolute/path/request.json \
  --source-snapshot /absolute/path/snapshot.json \
  --execution cloud --calculation-mode dbt-shadow \
  --shadow-reconciliations /absolute/path/reviews.json \
  --output-dir /absolute/path/new-review
```

這條命令仍依既有 cloud 流程將來源／run audit 存入所設定的 dataset。額外的 shadow 計算只寫獨立隔離 dataset；其結果不取代 Report，也不作為發布的權威值。若只想驗證 SQL 而完全不走既有來源／發布流程，使用上面的獨立 CLI。

`--calculation-mode` 只有 `python`（預設）和 `dbt-shadow`；後者要求 cloud，workbook 不支援。尚無 `dbt-authoritative` 模式。要求的 shadow 執行失敗會在 manifest 記錄 errors 並阻擋此次 cloud 發布，但已產出的本機 MD／HTML／Excel 保留。正常完成但有比較差異則記錄 warnings；原有 Python 的驗收規則不被改寫。

## 讀取結果

- `shadow_manifest.json`：`status=prepared/compared/failed`；始終 `precision_approved=false`、`publication_eligible=false`。
- `comparison.json`：完整每個 Fact 的兩邊欄位、值字串、差額及分類。
- `comparison.csv`：便於逐項檢視的摘要。
- `reconciliation_comparison.json`／`warehouse_reconciliations.json`：Python／SQL 對帳狀態、verified 及可驗證數值的比較；非法覆核的原始 claims 仍保存在 audit，但不當計算真相。
- `equivalent`：比較範圍內完全等價。
- `numeric_difference_unapproved`：除法結果，或已獨立確認加減式只傳遞其輸入的除法差異；**尚未批准，不能自動算過關**。來源值、獨立加減式自身出錯，以及受上游錯誤影響的值，均判 mismatch。此標籤不證明差異是可接受的 rounding。
- `mismatch`：身份、狀態、來源、公式等不一致或缺少／多出 Fact；需調查。
- `dbt/`：保留 manifest、run／test 收據與 log。logs／原始 sources 是本機 run artifacts，不提交 Git。

CLI exit 0 代表準備成功或比較完成且沒有 Fact／對帳 mismatch；**不是已驗收或可發布**，仍需看 numeric_differences。exit 1 表示執行失敗或有 mismatch。既有 agent_runner 的 0／2／1 語意不變。

2026-11-10 起，SQL 財務 readiness 的 `acceptance_mismatches` 也會使獨立 CLI 回傳 1，並在整合流程記錄 warnings。溢位會使建置失敗；只有零分母轉為不可計算 NULL，不使用 SAFE_DIVIDE 吞掉溢位。

## 以 dbt 結果產生候選預覽（M3 部分實作）

在獨立 live 命令加上 `--candidate-preview`，會在新 run 的 `candidate_preview/` 產生 Markdown、JSON、HTML 及 `preview_manifest.json`。此選項不適用於既有報告的正式驗收／發布。`--prepare-only` 只準備，不產生預覽。

也可分開執行，將計算流程回傳的 `calculation_receipt_sha256` 固定在消費端：

```bash
python -m scripts.warehouse_candidate \
  --shadow-dir /absolute/path/completed-shadow-run \
  --receipt-sha256 THE_HASH_FROM_THE_CALCULATION_RUN \
  --output-dir /absolute/path/new-candidate-preview
```

`calculation_receipt.json` 綁定 run／entity／scope、source／plan／code hashes、formula／policy／precision versions、覆核 hash、SQL Facts／對帳／驗收快照及完整 dbt run／test／manifest artifacts。reader 要求所有選中的 model／test 完整成功，拒絕缺列、重複、其他 run、浮點數字、缺證據、未解決的結構／對帳／驗收 mismatch，以及被修改的檔案。除法差異只保留為未核准，預覽仍不得發布。

收據是內容完整性綁定，**不是數位簽章或 IAM 授權**；消費端須從可信的計算流程取得固定 hash，不能把攻擊者重新產生的 hash 當認證。這是讀取已保存 BigQuery 結果的候選 adapter，尚非正式 published warehouse reader。既有 Python Report renderer 的獨立算術驗證仍保留；候選入口在收據／結構驗證後使用共用的純呈現程式碼。

候選預覽已接上 SQL 跨期數值比較與 ratio analysis（見下節）；公司原因分析仍需可核實原文，沒有自動產生原因。Excel 候選匯出已另接上（見下節），正式 publication receipt 或 BI views 尚未完成，不能把此預覽當成 M3–M5 已完成。SQL readiness 測試只涵蓋現行影子支援範圍，identity 的正式採用等仍待完成。

## 敘述數字與資產負債組成

新增 `int_review_shadow_comparisons`、`int_review_shadow_commentary_components`、`fct_review_shadow_commentary`。dbt 計算：跨期增減額、成長率、比率分子／分母比較、科目排序、來源總額差異、選定流動科目加總與殘差、重疊及覆蓋狀態。Annual 比較最後兩個 FY；Quarterly 損益比較前後 YTD，資產負債比較 latest FY／current interim。

`--commentary-documents /absolute/path/documents.json` 接收既有 MD&A／Balance Sheet document list 格式。Python 驗證公司、CIK、scope、as_of、期間與 raw observations schema，將原始 observations 入倉；dbt 獨立選取版本、確認單位並換算，不接收 Python 已算好的 ratio analysis。來源包中的 SEC instant observations 也由 SQL 篩選；排除紀錄、未來文件、未知概念及不同範圍不能進入計算。

沿用現行規則：最新資料必須明確為 amendment 才能取代舊版本，其他矛盾保留 conflict；組成科目不當作無重疊會計科目表。只對目前列舉的流動資產／負債科目加總。`matched_selected_lines` 只證明選定科目的加總，不證明已涵蓋完整資產負債表。commentary 成長率只對正基期計算，不改 CF-09 的 signed 分母規則。

`scripts/warehouse_commentary.py` 只複製 SQL 數字、排序、狀態及組文；預覽另保存 `ratio_commentary_analysis.json`。`scripts/shadow_commentary.py` 是遷移專用的獨立 Python 比對，檢查 exact delta，不作候選報告計算來源。`commentary_comparison.json` 保存每個差異；`commentary_mismatches` 非零會阻擋獨立 CLI 成功及候選 reader，growth 的原生除法差異仍是未核准。

計算收據升為 `warehouse-candidate-v2`，綁定 `warehouse_commentary.json` 與文件 hash；reader 保留讀取既有 v1 快照，且不回填或改寫舊收據。`preview_manifest.json` 額外保存 `consumer_code_hash`，區分計算 run 的程式碼與本次呈現的程式碼；重新呈現必須使用新目錄。

原始值／scale／quantum 及其換算中間值、規範化結果與金額 precision bound 都必須能無損表示；無法表示就入倉前拒絕。此 preflight 不輸出 Python 財務結果給 SQL。

實際年度、季度與衝突／重疊／幣別測試見 [敘述驗證紀錄](dbt-shadow-commentary-validation-20261110.md)。

## 候選 Excel 匯出

在 `scripts.warehouse_candidate` 命令加上 `--excel`，由已保存的 dbt 快照及固定收據生成新候選目錄：

```bash
python -m scripts.warehouse_candidate \
  --shadow-dir /absolute/path/completed-shadow-run \
  --receipt-sha256 THE_HASH_FROM_THE_CALCULATION_RUN \
  --output-dir /absolute/path/new-candidate-with-excel \
  --excel
```

沿用既有 bundled Node／`@oai/artifact-tool`，不安裝 repo dependencies。`Review` 只引用 `Warehouse` 的固定 dbt 結果；`Warehouse` 同時保存 Excel numeric 值、完整數字字串、Fact 原始值／scale、期間、公式、有序依賴及收據。`Sources` 保留可編輯的本機試算與差額，比較結果不餵回主表或倉儲。原本 Python 匯出仍使用既有驗收入口，不能以候選旗標略過。

`scripts/warehouse_excel.py` 在作者工具前驗證來源收據、所有預覽 hashes、完整 Report／敘述內容與 Markdown 表格綁定。存檔後逐一檢查精度字串、數值 caches 及每個主表公式，拒絕改寫數字、混入試算連結或缺少 Facts。Excel 的 binary64 近似值及 Decimal 差額逐筆寫入 `excel_validation.json`；`1e-12 * max(1,abs(value))` 是此活頁簿交付的誤差界限，**不核准 BigQuery 精度或財務驗收，也不放寬 Python／dbt 比對**。

`preview_manifest.json` 保存 `loan_review.xlsx`／`excel_validation.json` hashes 與 `excel_status=passed/failed`。要求的 Excel 失敗會明確拋錯，保留已產生的 MD／JSON／HTML 草稿；不回退 Python 計算。拒絕覆寫已有 Excel 輸出，須建立新目錄。所有正式驗收／發布與 precision 旗標仍為 false。

SDK 重算、加值／清空／零值試算、儲存 XML 及所有工作表呈現已驗證；沒有執行原生 Microsoft Excel。測試與本機 artifact 定位見 [Excel 驗證紀錄](dbt-shadow-excel-validation-20261110.md)。

## 尚未放行的後續項目

- q18 HALF_EVEN 規則已核准並完成候選精確比對與原生邊界驗證；更廣的每公式／業務矩陣與正式 precision release／切換仍待放行，見 [q18 驗證](dbt-q18-precision-validation-20261111.md)。
- 對帳 structured review 與來源精度上限已有影子 SQL 驗證；尚需 identity 的正式採用、完整財務驗收 SQL 與更廣泛案例。已通過的個別對帳仍不能代替報告驗收。
- 候選 ratio commentary 衍生數字已移至 dbt；正式 cloud consumer／模型原因分析的接線與完整案例矩陣尚待完成。
- Excel 候選匯出已完成；正式 cloud consumer 的接線、warehouse-authoritative reader、正式 publication receipt／BI views 與失敗回退驗證尚待完成。目前收據與快照 reader 只供候選預覽。
- M4 代表性案例全覆蓋與切換放行。以上未完成前，不變更既有 authority。

## 2026-11-09：結構化對帳覆核

獨立 CLI 可額外指定 `--reconciliations /absolute/path/reviews.json`。輸入格式為
`{"schema_version":1,"checks":[...],"evidence":{"review-id":{...}}}`。
`checks` 使用既有 `verify_reconciliation` 契約：kind、period_role、status、terms（有序 fact_id／coefficient）、reported_fact_id、evidence_ids、tolerance、calculated_value、reported_value、difference。
`evidence` 使用既有 Evidence 格式，覆核 content 必須是綁定該方程、幣別、scale、tolerance 的完整 JSON。source／review IDs 需真實存在於來源／證據集合；本功能不證明人工聲明的真實性，來源核實仍由供應覆核者負責。

SQL 不信任輸入 status、金額或 tolerance。它讀來源 Fact 重新計算，依原始值 quantum 與 scale 建立容許差上限；再檢查來源鏈、期間／scope、組成順序、重複項及 binding。加減與來源精度錯誤不能用「除法精度待定」略過。只給部分 checks 時，其餘方程／期間會明確保留未覆核狀態。

2026-11-10 起，一般報告入口也可使用 `--shadow-reconciliations /absolute/path/reviews.json`；Python API 對應 `shadow_reconciliations`。此參數可省略；有提供時必須同時指定 `--calculation-mode dbt-shadow`，否則在執行前拒絕，避免證據被忽略。獨立 shadow CLI 仍使用 `--reconciliations`。

覆核資料只交給 shadow；原始內容保存在 `dbt_shadow/reconciliation_reviews.json`，其 hash 保存在 `shadow_manifest.json`。整合 manifest 記錄對帳 mismatch 數；執行失敗仍阻擋此次發布並保留已產出的報告。這不改寫既有 Report 或讓整合 CLI 採用新的財務驗收結果。所有 shadow run／對帳輸出仍 `publication_eligible=false`。

實際合成資料驗證見 [2026-11-09 驗證紀錄](dbt-shadow-validation-20261109.md)。

## 固定候選版本執行與回退

`scripts.selected_runtime` 串接候選 selector 與固定 ZIP。所有命令仍只使用隔離 shadow bucket／dataset，沒有正式發布或精度核准選項。使用與套件 runtime lock 一致的既有 Python 環境；環境不符會拒絕，沒有 Python 財務計算 fallback。

先將已建立且 SHA256 固定的 runtime ZIP 存進已配置的隔離 bucket：

```bash
python -m scripts.selected_runtime --project PROJECT --bucket SHADOW_BUCKET \
  --output-dir NEW_STORE_OUTPUT store --package /absolute/path/runtime.zip \
  --package-sha256 PACKAGE_SHA256
```

輸出 `receipt.json` 記錄 package hash、GCS object generation 與 runtime／code hash。以此檔案的外部 SHA256，以及既有同版本 Annual／Quarterly 計算證據註冊新的 immutable release：

```bash
python -m scripts.selected_runtime --project PROJECT --bucket SHADOW_BUCKET \
  --output-dir NEW_REGISTER_OUTPUT register --release-id NEW_32_HEX_ID \
  --runtime-reference /absolute/path/store/receipt.json --reference-sha256 REFERENCE_RECEIPT_SHA256 \
  --case /absolute/path/annual ANNUAL_CALCULATION_RECEIPT_SHA256 \
  --case /absolute/path/quarterly QUARTERLY_CALCULATION_RECEIPT_SHA256
```

沿用 `scripts.candidate_release_control select／rollback` 更新 current pointer；需 actor、reason、唯一 event ID 與預期 pointer generation。回退僅接受歷史鏈中曾成功選用的版本；新 runtime release 不覆寫舊 release。之後執行：

```bash
python -m scripts.selected_runtime --project PROJECT --bucket SHADOW_BUCKET \
  --output-dir NEW_EXECUTION_OUTPUT run --source-bundle /absolute/path/source.json \
  --reconciliations /absolute/path/reviews.json
```

流程啟動時捕捉 selection，從該 release 指定 generation 下載套件；檢查全部 bytes、source fingerprint 與已安裝 dependency 內容後，使用隔離 Python 執行。受控 wrapper 在建立 BigQuery client／寫入 dataset 前，核對 code／formula／policy／precision version，建立 immutable run binding，再交給套件內的原始 SQL-only 引擎。途中 pointer 改變不會替換此次版本；從未成功選用的孤立 event 不能授權執行，既有 run 也不能改綁另一 selection。

成功輸出 `selected_execution_receipt.json`、`run_binding.json` 及 `execution/` 下的固定套件收據、計算／預覽；失敗保留對應 manifests，缺件、checksum／版本／環境錯誤會中止。若失敗已建立 run binding，該紀錄保留但不代表成功結果；重試使用新輸出目錄及新 calculation run，不覆寫舊結果。

財務程式由 ZIP pin 固定。當前控制程式 `candidate_release_control`／`delivery_archive`／`selected_runtime_worker` 與套件分開載入，逐檔 hash 保存在 package execution receipt；這是候選調度的版本紀錄，不宣稱整個控制平面已成為可跨主機部署的 release。舊 metadata-only release 仍可讀取／選擇，但沒有 runtime reference 時執行會在 SQL 前拒絕。七日測試保存、正式 IAM、production publication 與精度核准仍依完成矩陣處理。
