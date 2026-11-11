# 遷移完成條件與證據索引

2026-11-11。依據 `dbt-financial-calculation-migration.md` 的完整範圍；這是現況稽核，不把候選功能重新定義成整體完成。18 位 HALF_EVEN 規則已於 2026-11-11 獲核准並完成候選驗證；僅隔離執行、正式切換另行放行仍有效。

「已有證據」只指本列範圍；未涵蓋、只在 mock 驗證或只有設計者一律不算完成。M4／M5 尚未放行。

| 規格範圍 | 現有實作／證據 | 未完成或需更強證據 |
| --- | --- | --- |
| §2 責任分離 | SQL-only runtime 禁用 24 個 Python 財務函式成功；舊 shadow 獨立比較 | 正式 workflow 尚未改讀此引擎；M4 後移除 cloud 雙重計算 |
| §3 原始、request、policy 分層 | raw observations／metadata／review records 在隔離 raw table；typed staging／SQL policy dims | 正式 physical schema、完整欄位契約、retention／IAM 尚未部署；不以建議表名已存在冒充完成 |
| §3 run／attempt 固定 | candidate archive 內容 hash、run binding、固定 attempt、同內容重試與異內容拒絕實測 | 發布 registry 的完整身份 JOIN 與正式 writer／reader 權限 |
| §3 request hash | 新 SQL-only receipt 獨立 request_hash | 舊 shadow 收據不回填；正式 schema／release 需綁定新契約 |
| §3 最後 publication receipt | GCS candidate delivery 最後寫 commit、完整 object generations | 候選 commit 不是 publication receipt；BigQuery 正式發布登錄未完成 |
| §4 21 公式 | dbt macros、48 手算 kernels、SQL formula registry；多個原生案例 | 每公式零／負／缺值與各狀態的完整映射及 native 採用矩陣未齊 |
| §4 目標／順序／角色／單位 | SQL independent formula contract；五種錯誤計畫 native 拒絕 | source tag／概念映射尚未全面 SQL 固定；其餘失敗組合未齊 |
| §4 identity | source-bound review、六個 DER、本機反向循環、原生連續推算 | 所有 DER 的原生採用與循環／既存來源／conflict／scope 失敗矩陣未齊 |
| §4 cash change | SQL 完整橋接後採用；成功與偽造覆核拒絕 native 證據 | 非零 FX／restricted cash 等更廣的原生缺件／期間矩陣 |
| §4 LTM | exact interval 限制；不加入 FY＋YTD−prior YTD 捷徑 | Quarterly 直接 LTM 與完整 exact components 的正／負原生案例；不以 YTD 當 LTM |
| §4 status／reason codes | 六種 status 保留；缺值 NULL；財務 readiness draft | 有序多重 reason codes、明確 zero_divisor 等診斷仍未完整提供 |
| §4 overflow／casts／SUM | 無損 BIGNUMERIC preflight；除法溢位不隱藏；arity／可用性計數 | 全型別範圍、超界、極端複合運算的 native 完整矩陣 |
| §5 原始精度 | 字串、scale、quantum、round-trip；不用 float 入倉 | 分數 scale、長字尾零、極小／大值的逐項 native 證據仍需補齊 |
| §5 precision policy | 已核准 q18 HALF_EVEN；dbt 精確除法、Fraction oracle、canonical parents／audit；年度／季度新政策零 mismatch，舊差異逐筆保存；224 原生邊界含 double rounding 反例及正負溢位拒絕，見 q18 驗證 | 更廣的每公式極端複合／臨界業務驗收值矩陣仍需補齊；正式 precision release／M4 尚未啟用 |
| §5 三種誤差分離 | q18 canonical exact equality 與舊 Python 政策差異分開；reconciliation source bounds、Excel binary64 另行驗證 | 正式 release 對應及完整交付驗收，不能互相代用 |
| §6 來源採用追蹤 | candidates／版本／amendment 與 source IDs、原始檔案保存 | 明確 selected／superseded／excluded IDs＋各原因碼、完整來源欄位矩陣仍未齊 |
| §6 lineage bridges | 有序 input bridge、direct／inherited evidence、archive typed readers | 正式 published lineage views 與 reader IAM |
| §6 serialization／歷史 | pins、字串數字、UTF-8 canonical hashes；舊 v1／v2 快照讀取 | 正式已發布歷史的保留／release pin 與回退實測 |
| §7 結構／公式／對帳 gate | dbt error tests；來源綁定覆核；八項／四項缺口如實保存 | 全部規格案例的 coverage、規則漏洞稽核未齊 |
| §7 financial acceptance | SQL required cells／decisions／reconciliation readiness 與 Python 比較 | positive readiness 路徑仍需更強 E2E 證據；Annual DEC-03 有缺口時維持 draft 才正確，不為遷移另造業務定義 |
| §7 交付 | receipt-bound MD／JSON／HTML／Excel，current-consumer 重現與 ZIP audit | SQL-only 新收據的 Excel／GCS 完整 E2E、正式 delivery requirement registry |
| §7 發布 | preflight 明確列 blockers，所有 candidate flags=false | 最終 publication receipt、完整 JOIN view、失敗注入、獨立 reader 身份驗證 |
| §8 同源比對 | 固定 bundle／code／Decimal context；不重抓 API；未知 mismatch 阻擋 | 所有矩陣均需一致的可重現 fixtures 與版本 coverage 清單 |
| §8.3 財期 | annual／quarterly 原生案例，YTD／LTM 不混算 | 非曆年、52／53 週、閏日、缺去年同期等完整 native 矩陣 |
| §8.3 來源邊界 | amendment／衝突／currency 等已有部分 native 案例 | 同值異版本、tag／定義／CIK／scope／as_of 全組合、ignored rows 的原因追蹤 |
| §8.3 數值邊界 | kernels、source precision bounds、binary64 delivery 差異 | signed ties／double rounding／極端 scale／溢位完整矩陣 |
| §8.3 管線故障 | archive／delivery retry、部分寫入、tamper、job confirmation、錯誤 pin 拒絕 | 同 run 多 attempt／並行、發布中失敗、manifest 寫失敗、發布後改公式與 rollback 的完整 E2E |
| §9 release／rollback | 候選 selector 已串接固定 generation 的 GCS ZIP、隔離 runtime 與 SQL 前 run binding；原生 A → B → rollback A 各 186 Facts，歷史收據不變且 A／回退 A 全 Fact 相同，見 selected-runtime 驗證 | 跨主機環境重建、正式 release gate／IAM／部署與正式發布結果的完整回退 E2E 仍未完成；目前只核實候選執行 |
| §9 M4 | 尚未啟用正式 dbt authority；q18 計算規則已獲使用者核准實作驗證 | 完整 M4 驗收與具體切換仍須明確放行；此次精度規則核准不代表正式上線 |
| §9 M5 | 舊 local Python 保留；新候選入口已建立 | cloud 預設、BI 指向、移除雙重計算、更新可瀏覽 HTML 架構圖與最終文件尚未完成 |
| §10 IAM／保留／成本 | 隔離 dataset／bucket、PAP、七日測試 lifecycle | authoritative project ownership、實際 service accounts／read-only consumer、永久保存及查詢成本／耗時 dossier |

主要證據索引位於同目錄各 `dbt-*-validation-*.md`，原始執行物在忽略的 `outputs/`。七日到期的測試資料不等同永久正式保存。M0–M3 仍有上述工程可繼續；目前並非只剩使用者核准，也不應先要求切換核准。
