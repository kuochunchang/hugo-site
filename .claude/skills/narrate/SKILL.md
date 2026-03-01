---
name: narrate
description: 為 Hugo 文章生成語音版本。使用方式：/narrate <文章路徑>
arguments:
  - name: post_path
    description: content/posts/ 下的文章路徑，或文章 slug 名稱
    required: true
---

# 為文章生成語音朗讀

## Step 1: 定位文章

1. 如果傳入的是完整路徑，直接使用。
2. 如果只是 slug（如 `agent-skills-context-engineering`），到 `content/posts/` 下尋找對應的 `.md` 或 `index.md`。
3. 使用 Read 工具讀取文章全文。

Hugo 專案路徑：`~/workspace/hugo-site`

## Step 2: 轉換為 Page Bundle（如需要）

如果文章是獨立的 `.md` 檔案（如 `content/posts/my-post.md`），需要轉換為 Page Bundle：

1. 建立目錄：`content/posts/my-post/`
2. 將 `my-post.md` 移動為 `content/posts/my-post/index.md`
3. 用 Bash 執行：`mkdir -p content/posts/<slug> && mv content/posts/<slug>.md content/posts/<slug>/index.md`

如果已經是 Page Bundle（`content/posts/<slug>/index.md`），跳過此步驟。

## Step 3: 分段並用 LLM 重寫為口語文字

這是最關鍵的步驟。**不要只用程式移除 Markdown 語法**，那樣唸出來效果很差。

### 3.1 程式化分段

用程式將文章按 `## ` 二級標題分割成多個段落（section）。每個段落包含該標題下的所有內容。

### 3.2 LLM 逐段重寫

對每個段落，使用 Agent 子代理（subagent_type: haiku）進行重寫。每個子代理的 prompt：

```
你是一位專業的中文播客主持人。請將以下技術文章段落改寫為適合語音朗讀的自然口語文字。

規則：
- 使用繁體中文
- 語氣自然流暢，像在跟聽眾說話
- 技術名詞保留原文（如 Context Engineering、Token、Agent）但用口語方式解釋
- 表格內容改為口語描述（如「第一種方法是...，它的壓縮率是...」）
- 程式碼區塊改為口語描述其功能，不要逐字唸程式碼
- 連結只保留描述文字，不唸 URL
- 數據和比較用口語呈現（如「從百分之八十提升到百分之百」）
- 不要加入原文沒有的資訊
- 不要使用 Markdown 語法，輸出純文字
- 每段結尾自然過渡到下一段

以下是要改寫的段落：
---
{段落內容}
---
```

**重要**：多個段落可以並行處理（用多個 Agent 同時重寫不同段落），加快速度。

### 3.3 合併

1. 開頭加上：「以下是『<文章標題>』的語音版本。」
2. 按原始順序合併所有重寫後的段落
3. 段落之間加一個空行（TTS 會自然停頓）
4. 結尾加上：「以上就是本篇文章的語音版本，感謝收聽。」

將合併後的文字存為 `content/posts/<slug>/audio.txt`。

## Step 4: 選擇語音

使用 AskUserQuestion 讓使用者選擇 Edge-TTS 語音：

1. **zh-TW-HsiaoChenNeural** — 台灣女聲，友善正面
2. **zh-TW-HsiaoYuNeural** — 台灣女聲，友善正面
3. **zh-TW-YunJheNeural** — 台灣男聲，友善正面
4. **zh-CN-XiaoxiaoNeural** — 大陸女聲，溫暖（音質最佳）

## Step 5: 生成語音

1. 確認 `edge-tts` 已安裝，若未安裝則執行：`uv tool install edge-tts`
2. 確認 `ffmpeg` 可用。
3. 用 edge-tts 生成原始音檔：

```bash
edge-tts --voice "<選擇的語音>" --file "content/posts/<slug>/audio.txt" --write-media "/tmp/<slug>-raw.mp3"
```

4. 用 ffmpeg 壓縮為 64kbps mono mp3：

```bash
ffmpeg -y -i "/tmp/<slug>-raw.mp3" -ac 1 -ab 64k "content/posts/<slug>/audio.mp3"
```

5. 清理暫存檔：`rm -f /tmp/<slug>-raw.mp3`
6. 顯示生成的檔案大小。

## Step 6: 嵌入播放器

在文章的 front matter `---` 結束後的第一行，插入 HTML audio 播放器：

```html
<audio controls preload="none" style="width:100%; margin: 1rem 0;">
  <source src="audio.mp3" type="audio/mpeg">
  你的瀏覽器不支援音頻播放。
</audio>
```

注意：
- 如果文章已有 `<audio` 標籤，先移除舊的再插入新的。
- `src` 使用相對路徑 `audio.mp3`（Page Bundle 內的資源）。

## Step 7: Commit

```bash
cd ~/workspace/hugo-site
git add content/posts/<slug>/
git commit -m "feat: add audio narration for <標題>"
```

告知使用者語音版本已生成，可用 `hugo server` 預覽。
