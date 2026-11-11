# 候選 release 選擇與回退控制驗證

2026-11-11。限候選控制，不是 M4 核准、正式部署或 production rollback。

## 控制契約

`candidate_release_control.py` 以至少 Annual／Quarterly 兩份固定計算收據建立 release。同一組收據需同一 code／formula／policy／precision version，保存完整比較狀態；comparison=not_run 不改寫成成功比對。candidate 不要求未核准精度差異已放行，也不因此取得正式資格。

GCS `candidate-control/` 下的 releases、events、run bindings 不可覆寫；只有 current pointer 可用預期 generation 做 CAS 更新。事件保留 release 的固定 generation／hash 與上一個 event 的固定 descriptor。新 run 綁定當時 event／release；後續 selector 更新或回退不改寫既有 binding。

rollback 的目標必須曾在目前歷史鏈成功選用，不能回退到只是註冊或孤立失敗 event 的 release。reason／actor 必填，actor 只是稽核標籤。控制層強制 precision_approved=false、publication_eligible=false；沒有 approve／production CLI。

## 實際 GCS 證據

Project `focus-heuristic-438521-v4`；新隔離 bucket `sec-review-shadow-control-20261111-d3814e92`，US、uniform bucket access、public access prevention、七日 object lifecycle。不是正式永久保留／project ownership／IAM 授權證據。

兩個 release 使用實際已有計算收據，沒有重新計算那些歷史結果：

| release | 計算 code hash | 證據 |
| --- | --- | --- |
| A：11111111111111111111111111111111 | 84519f624f0682396b1c0439e8a08fbe51b92cc8a04dc3ed288d297462c1a83c | metric-policy 版本 Annual／Quarterly SQL-only 收據 |
| B：22222222222222222222222222222222 | 3b4abe108edaa84fd854e52038d61bad1227e14a6354c14050400ac0bb90aa77 | configuration 版本 Annual／Quarterly shadow 收據，精度仍未核准 |

Release A object generation `1794406656865491`，SHA256 `ff21a7ba87882c44c8e1f3bd8ad6144f9c5fa512fc0efa7ec336e5eedb874ae2`；B generation `1794406657169958`，SHA256 `9b0296fcf00998a64bf331f39b5c8d637533d3536ebf523aea5c12f95dabe802`。相同 A 註冊重試取得相同 descriptor。

實際選擇流程：

| 動作 | pointer generation | 新建 logical run binding |
| --- | --- | --- |
| select A | 1794406658242364 | 44444444444444444444444444444444 → A |
| select B | 1794406659990427 | 55555555555555555555555555555555 → B |
| rollback A | 1794406663926566 | 66666666666666666666666666666666 → A |

重新讀取前兩個 run，得到完全相同的原 binding 與 generation。這三個是 **selector 的合成 logical bindings**，沒有對它們執行新的財務計算，不是三份已發布報告。A／B 原有計算收據也未改寫。

實際拒絕檢查：

- GCS stale generation CAS 失敗，current pointer 未改變。
- registered 但從未 selected 的 release C 不可 rollback。
- 同 release ID 不同 code hash／內容不可覆寫。
- 嘗試 precision_approved=true 的候選 release 在上傳前拒絕。
- 已完成的相同 selection event 重試回傳相同結果。

工具 `validate_candidate_release_control.py` 保存以上完整 object descriptors、history、bindings 與拒絕結果於忽略的 `outputs/dbt_candidate_release_validation_20261111/probe_manifest.json`。該檔 SHA256：`efaad84f4cd1ced9581973adb48c1b2c6d83ee415ecb38efc7f046d6065d7fdb`。

## 測試與尚未完成

七項單元測試覆蓋 rollback 只影響新 run、stale update、CAS race 的孤立 event、不可回退到孤立版本、操作冪等／衝突、run 的來源 pin 不可改、release／precision 不可覆寫，以及 current CLI 不改變選擇。完整 `REVIEW_EXCEL_TEST=1 python -m unittest discover -s tests`：336 tests、OK、無略過，52.097 秒；包含既有 Excel 匯出／重算，原生 Microsoft Excel 尚未執行。另實際以 current CLI 讀取 GCS，回傳與 rollback 後完全相同的 pointer／generation，證據在 `current_status/control_receipt.json`。

控制層不是正式 release verifier：case coverage／precision／delivery／IAM／永久保留尚未全部放行。仍需保存並執行固定的程式／dbt／adapter 套件、在執行前使用 run binding、接入正式 publication registry，並測試真正財務 runtime 的版本回退與失敗恢復。不能用這份 selector 測試宣稱整體遷移完成。
