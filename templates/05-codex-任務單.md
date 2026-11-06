# Codex 任務單範本

把 `<…>` 換成你的內容後，整段貼給 Codex。

```text
使用 Pets 外掛的 create-pet 技能與它的 sprite-sheet 合約，製作一隻新的 v2 ChatGPT 寵物。上架前停下來。

寵物名稱：<名稱>
一句描述：<描述>
參考圖：<圖片路徑；說明哪一張是身份基準>
風格：<例如 pixel／chibi／flat>

工作方式：
1. 在 <專案資料夾>\run 建立工作目錄，所有專案檔都寫在那裡。內建 image_gen 存到預設的 $CODEX_HOME/generated_images 是允許的，請把選定的圖複製進工作目錄。不要修改參考圖原檔。
2. 先生成基準圖，給我看，等我確認造型再繼續。
3. 依合約逐列生成第 0–8 列，每列用內附腳本立即檢查。
4. 生成四方位錨點（000 上、090 畫面右、180 下、270 畫面左），通過後生成第 9 列，再生成第 10 列。不可鏡像、拼接或單格重做。
5. 用內附腳本組出 1536x2288 圖集，跑 validate_atlas、validate_pet_quality、連續性與方向 QA，產出接觸表、方向表、各狀態 GIF、全狀態預覽、16 方向 GIF 與 MP4。
6. 可以對最終檔呼叫 validate_pet_spritesheet。不要呼叫 prepare_pet_upload、create_pet、update_pet、select_pet，也不要寫入 Library。

最後寫 run\RESULT.md：最終圖集路徑與 SHA-256、每個關卡的 PASS/FAIL 與報告路徑、16 個方向的判定、預覽路徑、用了幾次生圖、未解決的問題。失敗也要照實寫。
```

我看完預覽同意後，再另外跟 Codex 說：

```text
對 run 裡的最終圖集執行 validate_pet_spritesheet；valid 為 true 才依序呼叫 prepare_pet_upload 與 create_pet，回報 pet ID。不要設成使用中。
```
