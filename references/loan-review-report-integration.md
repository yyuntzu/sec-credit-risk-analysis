# 正式報表串接與驗收

日期：2026-10-24。沿用既有科目代碼、資料契約、來源request／snapshot／supplement及核准公式，不變更DEC-01–11。

## 已接通的資料流

```text
agent_runner 的明確 report request／既有來源快照
  → prepare_loan_review_source_stage／prepare_source_inputs
  → loan_review_pipeline.adopt_inputs：保留原值、精確期間、來源及未決狀態
  → calculate_report：既有calculate_fact／calculate_identity及公式版本
  → build_narratives：只有已核實的比較；沒有來源原因就不寫原因
  → credit_memo_writer.render_loan_review：固定Annual／Quarterly版型
  → validate_report＋validate_arithmetic＋validate_rendered_report
  → 報表、逐項缺資料、勾稽差異、來源與驗收結果
```

Nexstar既有.xls另外使用唯讀的 `nexstar_workbook_review.py` 適配器，檢查公司、合併範圍、單位、原始英文、報表區域與儲存格後，進入**同一個**Fact／Report、計算、敘述、渲染及驗收流程。沒有另建一套財務計算或將原始底稿冒充SEC ledger。

## 入口與相容性

原source-only CLI保持不變：`--source-request`只產生來源，不能聲稱是最終報表。

嚴格報表CLI沿用同一JSON schema：

```text
venv/bin/python scripts/agent_runner.py TICKER \
  --report-request /absolute/path/request.json \
  --source-snapshot /absolute/path/snapshot.json \
  --output-dir /absolute/path/review
```

如需既有已覆核supplement，可重複傳入 `--supplement /absolute/path/evidence.json`。省略snapshot才使用既有SEC來源入口；本次Nexstar測試沒有執行這個連線路徑。

Python可呼叫原 `analyze_ticker(..., source_request=..., source_snapshot=..., formal_report=True, report_output_dir=...)`。不帶formal_report的source_request仍停在來源層，避免破壞舊source-only契約。正式路徑不經過舊_enrich_rows、寬表mart代理公式或LLM原因生成。

Nexstar原始.xls測試例：

```text
python scripts/nexstar_workbook_review.py "/absolute/path/E-Loan YQYQ-Nexstar Q2.xls" \
  --mode quarterly --quarter 2 --review-date 2026-10-24 \
  --output-dir outputs/nexstar_report_acceptance_20261024/Quarter_Q2
```

Year使用 `--mode annual`；Q1使用 `--mode quarterly --quarter 1`。讀取舊.xls需要可匯入的 `xlrd==2.0.2`，本次僅下載至核准的暫存目錄供讀檔，沒有變更核心runtime或部署環境；選用依賴列於 `scripts/requirements-workbook-review.txt`，可用 `venv/bin/python -m pip install -r scripts/requirements-workbook-review.txt` 安裝於本機。核心SEC／報表流程不依賴xlrd。回歸測試內附標明來源及雜湊的Nexstar儲存格快照，不需連線或依賴使用者Downloads目錄。

## 驗收結果與檔案

- `report.md`：嚴格版型報表。缺期不改模式、刪欄或換成另一段期間；缺值與限制放在相關表旁，不新增Data Quality Appendix。
- `report.json`：原有Report／Fact／Evidence／Narrative紀錄，包括Decimal值、原值及scale、日期、公式版本與input IDs。
- `source_inputs.json`：全部候選及採用／未採用原因。未核准的利息、Net Worth等候選值不會因為在這裡有數字，就進入正式可用Fact。
- `acceptance.json`：contract／計算／render驗證、未完成的實質驗收條件、缺資料及勾稽結果。
- `missing_data.csv`、`reconciliations.csv`、`review_findings.md`：獨立工作底稿，不塞進正式版型內。每項保留必要輸入、定義、來源、單位與差額；金額與比率單位分開。
- Nexstar測試另有 `original_cells.json`，保留原始名稱與值、不依同列或同額合併。總覽另列不同檔案同一行的名稱差異。

`technical_validation_passed` 與 `rendered_validation_passed` 表示程式及渲染檢查結果；`final_report_accepted` 表示資料與政策是否足以完成實質驗收，兩者不得混用。即使全部程式測試通過，必要來源、定義或勾稽未完成仍為false。呼叫者傳入的PASS旗標會依實際Report重新檢查，不可直接強制通過。

實質驗收要求：必要表格事實可用或有證據確認不適用；必要分析有資料；缺值及顯示政策有明確決策；每個日期的資產／完整現金勾稽有可追溯來源與審閱證據。只有一個任意PASS字串或三類流量小計相符不算通過。

## Nexstar目前的資料限制

- 底稿列有實際IS起訖與BS日期，但尚未獨立核對SEC會計日曆／CIK／原始申報；原Identity No.不是CIK。
- 原檔沒有公布日期。Evidence日期明示為本機覆核快照日期，不冒充SEC filing date，也不證明歷史as-of當時可用。
- CF區沒有重列期間，原科目盤點已要求確認上方IS日期是否適用，因此原值保留、正式CF／CF-03不自行採用。
- FX及Capitalized Interest空白不等於0；速動資產、Net Worth／債務／租賃、償債及EBITDA定義不自行核准。未核實的營業費用範圍不只因版面／數字相符就採用。
- 現金差額只列算術比較及來源，不推測是匯率、受限制現金或SEC財報錯誤，也不塞入Other補平。

本次三份Nexstar報表皆為「正式版型、待資料／定義驗收」，不是已核准交付的完整信用評估。沒有部署、抓新公司的資料或改動原始Excel。
