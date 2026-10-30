# 缺少資料、待確認定義與勾稽結果

完整項目見同目錄 missing_data.csv；逐項來源、單位與差額見 reconciliations.csv。

## 仍未完成的驗收條件

- 來源為使用者e-loan工作底稿，未取得／核驗對應SEC原始申報與CIK；不得標為SEC已核驗報告
- 原檔未提供公布日期；Evidence日期為本機覆核快照日期，不能用於證明歷史as-of可用性
- CF期間未重列，財務定義、完整現金橋接及DEC待確認事項尚未完成
- Required report cells are unavailable or definitions unresolved
- Required analytical coverage remains incomplete
- Reconciliation is incomplete or contains unexplained differences

## 無法勾稽的數值差額

| 檢查 | 期間 | 差額（計算－原檔） | 單位 |
| --- | --- | ---: | --- |
| cash_end_minus_begin_vs_reported_change | 2022-01-01~2022-12-31 | 32 | USD, scale=1000 |
| cash_end_minus_begin_vs_reported_change | 2023-01-01~2023-12-31 | 3,900 | USD, scale=1000 |
| prior_end_vs_current_opening | 2024-01-01~2024-12-31 | -12,000 | USD, scale=1000 |

差額只是已列來源數字的算術比較，原因尚未確定；未知FX、現金定義與其他調節未補0或反推。
