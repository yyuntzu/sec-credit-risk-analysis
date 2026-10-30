# 缺少資料、待確認定義與勾稽結果

完整項目見同目錄 missing_data.csv；逐項來源、單位與差額見 reconciliations.csv。

## 仍未完成的驗收條件

- User e-loan workpaper; SEC source and CIK not independently verified
- Source publication date unknown; review date does not prove historical as-of availability
- Cash flow periods/bridge and company-specific definitions remain subject to review
- Required report cells are unavailable or definitions unresolved
- Required analytical coverage remains incomplete
- Reconciliation is incomplete or contains unexplained differences

## 無法勾稽的數值差額

| 檢查 | 期間 | 差額（計算－原檔） | 單位 |
| --- | --- | ---: | --- |
| cash_end_minus_begin_vs_reported_change | 2026-01-01~2026-06-30 | 130,000 | USD, scale=1000 |

差額只是已列來源數字的算術比較，原因尚未確定；未知FX、現金定義與其他調節未補0或反推。
