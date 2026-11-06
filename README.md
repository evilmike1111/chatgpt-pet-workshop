# chatgpt-pet-workshop

從零開始，使用 GPT 逐步製作、驗收並發布 ChatGPT 虛擬寵物的開源教學。

**主線：全程在自己的電腦上做，不花額度。** 用本機 ComfyUI＋Qwen-Image-2.1 生成 16 個視線方向，用腳本組圖集、驗證，最後放進 Codex 的本機寵物資料夾，寵物就會出現在桌面。範例角色是「玄龍 ZERO」（黑金機械幼龍）。

| 文件 | 內容 |
|---|---|
| [docs/01-準備.md](docs/01-準備.md) | 硬體、軟體、模型與檢查方式 |
| [docs/02-本機免費流程.md](docs/02-本機免費流程.md) | 主線：六個步驟，每步有腳本與檢查 |
| [docs/03-驗收清單.md](docs/03-驗收清單.md) | 提交前要確認的項目 |
| [docs/04-常見失敗.md](docs/04-常見失敗.md) | 實際踩過的坑與修正方式 |
| [docs/05-付費替代路線-Codex.md](docs/05-付費替代路線-Codex.md) | 全部交給 Codex 的付費路線（附錄） |
| [scripts/](scripts/) | 四支 Python 腳本（MIT） |

## 驗證狀態（誠實標示）

| 項目 | 狀態 |
|---|---|
| 本機 Qwen-Image-2.1 生成 16 方向 | 已實測（玄龍，RTX 4060 Ti） |
| 腳本 01 從乾淨資料夾重跑，輸出與原作逐位元相同 | 已驗證 |
| 圖集通過 OpenAI Pets 外掛的 `validate_atlas`（v2、`#FF00FF`） | 已驗證（PNG 與 WebP） |
| 方向連續性腳本 | 通過，但有 5 項「中心位移」警告，靠目視判斷 |
| 放進 Codex 寵物資料夾後顯示在桌面 | 已實測（作者截圖確認） |
| 三人盲測方向、官方 quality 總閘門、MP4 | **未做** |
| 上傳到 ChatGPT Pets 雲端並通過審核 | **未做**；官方規範要求寵物影像由 `$imagegen` 生成，本機模型的結果能否過審未知 |
| 免費方案（Free）走付費路線 | **不行**：官方說明寫 Free 方案沒有圖片生成（[learn.chatgpt.com/docs/pricing](https://learn.chatgpt.com/docs/pricing)） |

## 授權

文字與腳本以 MIT 授權釋出（見 LICENSE）。
Pets 外掛與驗證腳本屬 OpenAI 專有軟體，本 repo **不包含**也不轉載；請讀者在自己的 Codex 安裝。
Qwen-Image 模型與 ComfyUI 依各自授權使用。
