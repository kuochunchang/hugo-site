# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build & Deploy

```bash
# Hugo 本地預覽
hugo server -D

# Hugo 建構（部署由 GitHub Actions 處理，push main 即觸發）
hugo --minify

# Discord bot（使用 uv 管理依賴）
cd discord-bot
uv run python bot.py

# Discord bot systemd user service
systemctl --user restart discord-bot
systemctl --user status discord-bot

# TTS 語音生成
edge-tts --voice "zh-TW-HsiaoChenNeural" --file audio.txt --write-media raw.mp3
ffmpeg -y -i raw.mp3 -ac 1 -ab 64k audio.mp3
```

## Architecture

Hugo 靜態站（PaperMod 主題，zh-TW）+ Discord bot 自動研究發布管線。

### 研究管線流程

```
Discord !research → 2 個 Claude CLI 並行草稿（/tmp）
                  → 判斷結果（雙成功合併 / 單成功潤飾 / 全失敗回報）
                  → 1 個 Claude CLI 合併 + Hugo 發布
                  → 1 個 Claude CLI 事實查核（比對草稿 + 上網驗證）+ 修正 + 語音 + git push
                  → Discord 回報結果
```

### Discord Bot (`discord-bot/`)

- **bot.py** — Discord 命令入口，前綴 `!` `.` `?`，去重檢查，任務鎖
- **researcher.py** — Claude CLI 子進程管理，stream-json 事件追蹤，雙路並行邏輯
  - `_run_claude_process()` — 通用 CLI 執行器（建立子進程、串流 stdout/stderr、超時處理）
  - `run_research()` — 單進程模式（向後兼容）
  - `run_dual_research()` — 雙路並行模式（2 草稿 + 1 合併）
- **prompt.py** — 提示詞組裝，共用片段（寫作風格、Hugo 發布、語音、git push），三個 builder
- **config.py** — 環境變數配置（超時、max turns、TTS voice）

### Hugo 內容

- 文章使用 Page Bundle：`content/posts/<slug>/index.md`（+ `audio.mp3` + `audio.txt`）
- 報告：`content/reports/ai-report-YYYY-MM-DD[-zh].md`
- 自訂 CSS：`assets/css/extended/`（Hugo 自動載入）
- Dashboard：`static/dashboard/`

## Writing Conventions

- 繁體中文 (zh-TW)
- ASCII 圖表的代碼柵欄**必須**用 ` ```text `，不能用無標記 ` ``` `（避免 Hugo GoAT SVG 渲染）
- Front matter 格式：YAML `---`，含 title/date/draft/tags/summary
- 音頻播放器 HTML 插在 front matter 後
- Git commit 格式：`feat: add research article - <標題>`

## Key Config Values

| 配置 | 預設值 | 用途 |
|------|--------|------|
| `CLAUDE_MAX_TURNS` | 50 | 單進程研究 max turns |
| `CLAUDE_DRAFT_MAX_TURNS` | 30 | 草稿階段 max turns |
| `CLAUDE_TIMEOUT` | 900s | 單進程超時 |
| `CLAUDE_DRAFT_TIMEOUT` | 600s | 草稿超時 |
| `CLAUDE_MERGE_TIMEOUT` | 600s | 合併發布超時 |
| `CLAUDE_REVIEW_MAX_TURNS` | 20 | 事實查核 max turns |
| `CLAUDE_REVIEW_TIMEOUT` | 600s | 事實查核超時 |
| `TTS_VOICE` | zh-TW-HsiaoChenNeural | Edge-TTS 語音 |
