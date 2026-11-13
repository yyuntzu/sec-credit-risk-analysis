# 期間與核准公式：本次最小修改

日期：2026-10-23。本文件說明實作，不修改核准公式、DEC決策、科目代碼或資料契約。

## 白話說明

以前有些數字雖然能算出來，卻可能用了錯誤期間或未核准的替代方式。現在先確認資料是哪家公司、哪一段期間、哪個申報版本，再決定能不能算。資料不足就留下缺值，不為了填滿報表而補0。

- 年度／季度查詢改用既有source-request的實際起訖、模式、CIK、scope、as-of與單位。不同開始日不再只因截止日相同而合併；現金流與損益必須同段期間。沒有損益資料時，已取得的現金流與餘額仍保留；缺期也保留欄位。
- 查詢改讀經來源適配驗證的快照，不再回到無法證明as-of／定義的舊staging值。晚於as-of的來源排除並保留排除紀錄，未核准的版本衝突仍會擋下。
- 負稅益不再取絕對值。只有有完整同口徑橋接審閱證據，才能由淨利與帶符號稅費推導稅前利益。毛利、成本及營業費用推導也要先有定義與完整橋接證據，不能互相循環倒推。
- CF-04與CF-05分開，兩個分母都含資本化利息。成長率使用帶符號基期，合法0值不當缺失，分母0不硬算。
- 移除速動比率、負債比率、Debt Service／DSCR、EBITDA／LTM與期初現金的代理推算。DEC-01／02／03／05／06等未決時保持無法計算。舊dbt同名輸出不再用近似值填入，相關缺資料旗標也不能顯示健康。
- writer不再用OI減利息補稅前利益，不再用1代替營收，不會把未知或0營收顯示為100%。缺值不判改善／惡化，相等不說增加；模式由request傳入，不再因缺季度資料改成年度。

## 沿用的邊界與呼叫方式

沒有新建科目表、狀態enum、請求JSON schema、BQ原始資料schema或另一套ETL。沿用既有METRICS、Period、Fact、Evidence、Report、Status、parse_request、來源ledger、supplement與snapshot機制。

`loan_review_contract.py`增加顯式的計算方法：

- `calculate_fact(report, fact_id, input_ids=..., formula_version=...)`：計算既有科目slot，保留formula ID、版本、input IDs；驗證單位、精確期間、來源與決策證據。待確認／缺輸入／分母0維持not_calculable，不覆蓋已取得的來源／計算值。
- 支援既有契約中的CF-01／02／03／04／05／06／09／10／11／12／16、COMMON-SIZE-v1及LEVERAGE-v1。百分比保留Decimal小數比例，顯示時才轉百分比。
- `calculate_identity(..., formula_id='DER-01'..'DER-06', definition_evidence_id=...)`：要求既有definition Evidence記錄已審閱的完整同口徑恆等式；缺證據、期間錯配或循環推導會拒絕。審閱證據不是只填tag名稱或「金額相同」。程式能驗證引用與資料契約，不能自動保證人填入的語義審閱內容真實。
- 現金差額仍受完整同口徑勾稽限制；此輪不自動建立FX、restricted cash或其他未知橋接項。LTM EBITDA的DEC-06未決，不新增YTD EBITDA科目或自行決定adjusted basis。

原 `--source-request` 路徑仍只準備來源，維持 `source_inputs_prepared`、`final_report_accepted=False`，不在來源層偷偷執行新計算。

舊報表查詢增加 `period_request` 參數，內容完全沿用既有source-request schema；CLI可使用：

```text
venv/bin/python scripts/agent_runner.py TICKER --period-request /absolute/path/request.json --no-html
```

其中request必須是該公司已核實的實際會計日曆／來源證據，不能拿測試fixture或別家範例當公司資料。此legacy格式仍只支援entity-wide、USD及百萬單位，其他scope／幣別／scale走原source-only路徑。HTTP `/analyze/<ticker>`的POST body可提供同一份 `period_request`。

舊的FY／Q文字標籤不再足以自動選期；缺少request時會在取數前明確停止。模式與查詢角色依request，矛盾的FY／quarter labels會拒絕。Quarterly request同時提供兩個FY-end與兩個可比較YTD角色。dbt未取得核實會計日曆時，不再把曆年year／quarter標成fiscal year／quarter；保留實際日期標籤。

## 這次沒有宣稱完成的部分

- 新的契約計算方法是顯式呼叫；尚未將來源bundle、審閱決策、計算、敘述與最終contract renderer全部串成自動交付流程。舊writer沒有可信決策／橋接資料的欄位保持缺值。
- CF-07／08、13／14／15、17–21等未登錄的完整計算／輸入，不在本次新增科目或最終報表列。CF-08仍須包含投資項；平均餘額、Months與備抵符號不自行核准。
- 尚未自動補查所有SEC主表／附註、自訂taxonomy／IFRS，或完成資產與完整現金勾稽。舊敘述層與新版最終版型的完整整合仍是後續工作。
- 不變更DEC-01–11或84項待確認事項，不將本次合成測試中的審閱證據當成正式核准。
- 沒有跑SEC／BigQuery／GCS／AI服務、部署dbt、抓新公司資料或改動既有Excel。

## 驗證

執行專案虛擬環境的既有Loan Review測試與新回歸測試。新增案例包括：CF-04／05資本化利息非0、負稅益與橋接要求、0與缺失、負基期成長、未決定義、同截止日QTD／YTD、非曆年日期、缺期保留、無損益但有現金流、as-of排除、CIK衝突、模式與入口、過舊／不足LTM拒絕、營收0與敘述方向。

查詢測試執行實際產生的SQL與實際採用快照，使用SQLGlot轉譯及SQLite離線核對數值。dbt SQL另做移除config／替換ref與source後的BigQuery語法解析；不等同於在正式BigQuery執行或部署驗收。

```text
PYTHONDONTWRITEBYTECODE=1 venv/bin/python -m unittest discover -s tests -p 'test_loan_review_*.py'
git diff --check
```


## 後續串接更新（2026-10-24）

本文件記錄的是2026-10-23的第一輪修改。來源、計算、敘述、正式版型及技術驗收已於後續接通，詳[正式報表串接與驗收](loan-review-report-integration.md)。現金差額只有在明確的同口徑完整橋接審閱證據存在時才可計算；不自動建立未知調節。Nexstar來源與定義仍不足，實質驗收保留未通過；沒有改寫本文件中尚未核准的決策。
