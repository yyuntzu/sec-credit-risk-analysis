# Loan Review skill 與 dbt／BigQuery 串接驗證

2026-11-11。使用者要求讓「give me loan review」自動啟動遷移後的報告流程。已更新並安裝 `sec-credit-analysis` skill，使用 `skill-creator`／`writing-for-agents` 整理入口，保持自動選用啟用。

## 自然語句入口

根目錄 `SKILL.md` description 明列 `give me loan review`、含公司名稱的 Loan Review 與中文授信報告請求。`agents/openai.yaml` 的 `allow_implicit_invocation=true`。本機技能目錄 `/Users/yuntzuyu/.codex/skills/sec-credit-analysis` 連結至此 worktree；安裝後已出現在本對話的可用 skills 清單。

如果缺少公司、Annual／Quarterly、分析期間／as-of，先一次詢問缺少的意圖；已有資訊沿用。CIK、實際財年日期、幣別與範圍由當前借款人 SEC 來源核實，不用範例或合成資料代替。自然語句觸發屬於技能選擇，並非註冊一個字串相等的 HTTP endpoint；本次驗證了可發現性、技能結構與完整執行入口，沒有宣稱所有改寫問句都必定選中同一 skill。

## 執行路徑

`scripts/run_loan_review_skill.sh` 選擇既有 Python 環境，啟動 `scripts/loan_review_skill.py`：

1. 既有 SEC／snapshot 來源 adapter 或固定 source bundle；核對 ticker／request／scope，保留 source inputs。必要時接收 supplements、來源綁定的 reconciliation 與 filing documents。
2. 從 `references/loan-review-runtime.json`／明確 overrides 讀隔離資源。`execute_selected` 在自己的 selection snapshot 內確認 q18 precision policy，下載固定 GCS runtime，SQL 前綁定實際 run。
3. 套件內 dbt／BigQuery 選來源、計算、驗證與產出固定收據；不呼叫 Python report calculator，也不啟動 Legacy 或舊 publisher。
4. `write_preview` 從同一計算收據生成 Markdown／JSON／HTML 與預設 Excel；Sources 的本機試算不改 warehouse 值。commentary documents 可穿過 selected runtime／package launcher 進入既有 SQL-only 引擎。
5. `archive_calculation` 將 Fact／evidence／lineage／原始 artifacts 封存至隔離 BigQuery；固定 run binding 與 attempt。
6. `prepare_delivery` 重驗同一批計算／預覽／archive receipt，`ShadowDeliveryStorage` 保存報告 bytes 與固定 object generations，最後才寫 delivery commit。
7. 保留 publication preflight 與 `run_manifest.json` 的逐階段狀態／實際檔案路徑。成功仍是 draft、exit 2；缺套件、政策不符、dbt、Excel 或保存失敗為 failed、exit 1，保留可用產物，不 fallback。

舊大型 skill 指引移至 `references/legacy-credit-skill.md`，只在明確 Legacy 請求時讀取；現有 standalone CLI／HTTP／本機 workbook 的預設與介面沒有改成正式 dbt 發布。

## 原生完整執行證據

以固定 SYNTHETIC-ONLY Annual source bundle／reviews 執行 shell skill 入口，使用預設 Excel，完整產生並保存：

- 計算 run：`7e0d5b63f290499c9fea923254594ad0`；候選 release `99999999999999999999999999999999`，q18 policy。
- 計算 receipt SHA256：`bfbd44d82e17c6e9d9c7f66c0cef3a1451419cff966602631733227161976f44`。
- 套件 pin：`a074b24fc4e0fc2ddae287e96c912e802e041add9a2ea1836044454cd9d0f0c9`；財務 source hash 沿用已驗證的 `1e3c61ae7710e2e62e7bdee1f78c4d29bdb13ae00630364baff1ae5c39408c73`，此次 skill 接線不改公式。
- BigQuery archive：`focus-heuristic-438521-v4.sec_review_shadow_skill_archive.review_candidate_1025fb0721024166a8955d872540580a`；寫後下載並完整核對 snapshot。
- GCS report bucket：`sec-review-shadow-runtime-20261111-c54e291a`；delivery commit generation `1794423303264624`，SHA256 `68cb622288bc2cb04f4d2ec972f72c4efede81253578e0ddab33a42c065cf58e`。
- Storage receipt SHA256：`8517afcc342c8b94d3c0514b9dbb10de5fcb179cb25432b1cc8863d22d9e1706`。

原始證據在忽略的 `outputs/loan_review_skill_validation_20261111/annual/`：`run_manifest.json`、`selected/`、`report/`、`archive/`、`storage_receipt.json`、`publication_preflight.json`。report 包含 `report.md`／`report.json`／`dashboard.html`／`commentary.json`／`ratio_commentary_analysis.json`／`loan_review.xlsx`／`excel_validation.json`／`preview_manifest.json`。本次是固定合成來源流程，並未替未指定的真實公司執行 SEC 抓取。

manifest 的 sources／calculation／report／preflight 均 passed，warehouse_archive／delivery_storage 均 stored，最終 draft、exit 2。SQL-only comparison=not_run 不冒充 Python 比較；Financial readiness 仍 false，原有必要欄位／DEC-03 缺口如實保留。

## 本機驗證與限制

`REVIEW_EXCEL_TEST=1 python -m unittest discover -s tests`：**367 tests，OK、無略過，93.500 秒**。Log `/tmp/sec-loan-review-skill-full-20261111.log`。新增測試涵蓋來源排他／公司不符／缺 request、SEC contact、候選 namespace、選版政策不符、套件失敗不 fallback、同計算收據交付／封存、Excel 失敗保留及 exit 2；並驗證 commentary 文件參數可傳進隔離套件。shell syntax、launcher `--help` 與 skill `quick_validate.py` 通過。

自動發現的連結指向此 worktree，不會根據另一個聊天的 git branch 自動改指向。部署到其他機器／移動 repo 時需在該環境安裝並配置對應入口。當前候選 runtime、archive 與 GCS 使用隔離測試資源／七日保存，沒有變成正式 IAM 或永久存放。原生 Microsoft Excel 未執行；不以生成草稿或技能啟用宣稱整體 M4／M5 遷移與正式切換完成。
