# Pets v2 驗收清單與紀錄模板

這是一份**供人工／自動化共同使用的模板**。請記錄可追溯證據；沒有實際檢查的項目一律是 `REVIEW_REQUIRED`，不能填 `PASS`。

## 驗收狀態

- `PASS`：有實際圖檔、腳本結果或視覺證據支持。
- `FAIL`：已確認違反規格或有明顯畫面缺陷。
- `REVIEW_REQUIRED`：證據不足，尚未完成目視或播放驗收。
- `BLOCKED`：工具／權限／來源不可用，暫時無法執行。

## Gate 0：來源與權利

- [ ] 已記錄角色名稱、canonical base、來源及需要保留的識別特徵。
- [ ] 了解版本及原始素材是否能公開分享。
- [ ] 讀取當前安裝版本的官方 create-pet 技能與共享規格。
- [ ] 原圖、候選、驗收結果集中保存；公開 repo 不放私人原檔、金鑰或電腦絕對路徑。

## Gate 1：結構與透明背景

- [ ] 遵守該版本要求的列數、欄數、每格尺寸、影格數及檔案格式。
- [ ] 正式圖集和獨立影格的可見像素與相對定位相符。
- [ ] 去背後沒有假棋盤格、色鍵殘邊、大片雜訊與角色被切斷。
- [ ] 全透明像素的殘留 RGB 已檢查；如需清理，清理後**重新對最終檔驗證**。
- [ ] 官方 `validate_atlas.py` 的實際報告有 `ok: true`；Pets `validate_pet_spritesheet` 為 `valid: true`。

全透明像素殘留顏色可能完全看不到，卻造成本機品質檢查失敗。對這類問題可以做 deterministic 清理，但它**不會修好頭部重畫、方向錯誤或動畫接縫**。

## Gate 2：九個動作

| 動作 | 應看見什麼 | 結果／證據 |
| --- | --- | --- |
| `idle` | 待機、呼吸／眨眼有自然微動 | REVIEW_REQUIRED |
| `running-right` | 朝右，步態有交替 | REVIEW_REQUIRED |
| `running-left` | 朝左，角色特徵沒有被不當鏡像 | REVIEW_REQUIRED |
| `waving` | 明確揮手／招呼 | REVIEW_REQUIRED |
| `jumping` | 確實離地後落回原基準線 | REVIEW_REQUIRED |
| `failed` | 明確失敗／受阻反應 | REVIEW_REQUIRED |
| `waiting` | 可辨識的等待狀態 | REVIEW_REQUIRED |
| `running` | 工作處理中，不是單純腳部跑步 | REVIEW_REQUIRED |
| `review` | 完成／成果檢視 | REVIEW_REQUIRED |

另需觀看完整播放及**待機→跳躍→待機**切換。不能把「有 57 張影格」等同「57 張都已通過動態驗收」。

## Gate 3：16 方向逐格紀錄

方向以觀眾畫面為基準，從上開始順時針。以下為**待填模板**；每一列要記錄可見證據（如瞳孔／鼻尖相對頭部、龍角透視與遮擋）：

| row／角度 | expected | observed（人工填寫） | verdict | evidence（檔名／截圖／理由） |
| --- | --- | --- | --- | --- |
| 9／0° | 上 | — | REVIEW_REQUIRED | — |
| 9／22.5° | 上偏右 | — | REVIEW_REQUIRED | — |
| 9／45° | 右上 | — | REVIEW_REQUIRED | — |
| 9／67.5° | 偏右上 | — | REVIEW_REQUIRED | — |
| 9／90° | 右 | — | REVIEW_REQUIRED | — |
| 9／112.5° | 右偏下 | — | REVIEW_REQUIRED | — |
| 9／135° | 右下 | — | REVIEW_REQUIRED | — |
| 9／157.5° | 下偏右 | — | REVIEW_REQUIRED | — |
| 10／180° | 下 | — | REVIEW_REQUIRED | — |
| 10／202.5° | 下偏左 | — | REVIEW_REQUIRED | — |
| 10／225° | 左下 | — | REVIEW_REQUIRED | — |
| 10／247.5° | 左偏下 | — | REVIEW_REQUIRED | — |
| 10／270° | 左 | — | REVIEW_REQUIRED | — |
| 10／292.5° | 左偏上 | — | REVIEW_REQUIRED | — |
| 10／315° | 左上 | — | REVIEW_REQUIRED | — |
| 10／337.5° | 上偏左 | — | REVIEW_REQUIRED | — |

額外記錄跨列的 157.5°→180°、337.5°→0° 與其他相鄰方向：有無頭頸跳動、龍角消失、眼睛換造型、胸晶錯位、錯誤遮擋。**輪廓差異數值只能輔助找異常，不等於視覺語意 PASS。**

## Gate 4：最終品質與交付

- [ ] 官方 `validate_pet_quality.py` 對確切最終圖集報告 `ok: true`。
- [ ] 方向語意、連續性與各動作有相對應的真實報告，非模型自述。
- [ ] 在正常寵物大小觀看 contact sheet、GIF／影片，沒有跳格或身份漂移。
- [ ] 圖檔在品質檢查後未再變動；若有變動，重新執行必要檢查。
- [ ] 已展示動態讓使用者確認；依授權才開始上傳／建立，建立後查到穩定寵物 ID。

### 建議每次記錄的最小資料

```json
{
  "artifact": "final-atlas.png",
  "source_version": "example",
  "validation": {
    "atlas_ok": null,
    "pets_preflight_valid": null,
    "pet_quality_ok": null
  },
  "visual_review": "REVIEW_REQUIRED",
  "blocking_issues": [],
  "evidence_paths": [],
  "pet_created": false
}
```

`null` 代表**未執行或尚未取得結果**，不等於失敗，也絕對不等於通過。
