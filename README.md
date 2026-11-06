# chatgpt-pet-workshop

從零開始，使用 GPT 逐步製作、驗收並發布 ChatGPT 虛擬寵物的開源教學。

**核心原則：只用一個工具，也就是 Codex（加裝 Pets 外掛）。** 從生圖、切圖、組圖集、驗證到上架，全部都在 Codex 裡完成。

| 文件 | 內容 |
|---|---|
| [docs/01-準備.md](docs/01-準備.md) | 需要的帳號、工具與檢查方式 |
| [docs/02-一個工具做出寵物.md](docs/02-一個工具做出寵物.md) | 從角色構想到上架的完整步驟 |
| [docs/03-驗收清單.md](docs/03-驗收清單.md) | 上架前必須全部通過的關卡 |
| [docs/04-常見失敗.md](docs/04-常見失敗.md) | 實際踩過的坑與修正方式 |
| [templates/codex-任務單.md](templates/codex-任務單.md) | 直接貼給 Codex 的任務單範本 |

## 驗證狀態（誠實標示）

| 項目 | 狀態 |
|---|---|
| Codex 內建 `$imagegen` 能生圖 | 已實測 |
| Pets 外掛的官方驗證腳本能檢查標準動作列 | 已實測 |
| 16 方向列由 Codex 一路生成並通過驗證 | 驗證中 |
| 上架（`create_pet`）成功 | 尚未實測 |
| 免費方案可完成全流程 | **不行**：OpenAI 官方定價說明寫明 Free 方案沒有圖片生成（[learn.chatgpt.com/docs/pricing](https://learn.chatgpt.com/docs/pricing)），本教學的生圖步驟需要付費方案 |

## 授權

本 repo 的教學文字以 MIT 授權釋出（見 LICENSE）。
教學會用到的 Pets 外掛屬 OpenAI 專有軟體，本 repo **不包含**也不轉載它的檔案；請讀者在自己的 Codex 安裝。
