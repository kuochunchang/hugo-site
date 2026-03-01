# Discord Research Bot Design

**Date:** 2026-03-01
**Goal:** Discord 訊息觸發自動深度研究，產出繁體中文文章 + 語音，發布到 Hugo 網站。

## Architecture

```
Discord 訊息 (!research <主題>)
  → Discord Bot (Python, discord.py, 常駐本機)
    → claude -p (headless 研究 + 寫文章)
      → WebSearch/WebFetch 深度研究
      → 寫 Markdown 文章
      → /publish skill (發布到 Hugo)
      → /narrate skill (TTS 語音, zh-TW-HsiaoChenNeural)
      → git push (觸發 GitHub Pages 部署)
    → Discord 回覆結果 + 網站連結
```

## Key Decisions

- **Bot 框架:** discord.py (Python)
- **研究引擎:** Claude Code CLI (`claude -p`)，復用現有 `/publish` 和 `/narrate` skill
- **運行位置:** 與 Hugo 專案同一台機器
- **語言:** 繁體中文
- **TTS 語音:** zh-TW-HsiaoChenNeural（固定）
- **發布流程:** 全自動（commit → push → GitHub Actions 部署）
- **程式碼位置:** `hugo-site/discord-bot/`

## Directory Structure

```
discord-bot/
├── bot.py              # Discord Bot 主程式
├── config.py           # 設定（頻道 ID、網站 URL、Claude 參數）
├── requirements.txt    # discord.py 依賴
└── .env                # DISCORD_TOKEN（不進 git）
```

## Trigger Format

```
!research 研究一下 MCP Protocol 的最新發展
!research 比較 LangGraph 和 CrewAI，重點放在效能和易用性，至少比較三個面向
```

支援簡單一句話或帶有細節的指令。

## Claude CLI Invocation

```bash
claude -p "<研究 prompt>" \
  --cwd ~/workspace/hugo-site \
  --allowedTools "WebSearch,WebFetch,Read,Write,Edit,Bash,Glob,Grep,Agent" \
  --max-turns 50
```

Prompt 指示 Claude：
1. WebSearch 搜尋最新資料（3-5 次不同角度）
2. WebFetch 閱讀重要參考來源
3. 整理成完整繁體中文技術文章（Markdown）
4. /publish 發布到 Hugo
5. /narrate 生成語音（zh-TW-HsiaoChenNeural，不詢問使用者）
6. git push
7. 輸出 TITLE 和 SLUG 供 Bot 解析

## Discord Response Format

成功：
```
✅ 研究完成！
📝 <文章標題>
🔗 <網站連結>
🎧 含語音版本
⏱ 研究耗時：X 分 Y 秒
```

失敗：
```
❌ 研究失敗
原因：<錯誤描述>
```

## Error Handling

- Claude CLI 非零 exit code → Discord 回覆失敗
- 30 分鐘 timeout 防止無限運行
- Bot 啟動時檢查 `claude` CLI 可用性
- 同時只允許一個研究任務（避免資源衝突）

## Future Extensions

- 支援 `!status` 查看當前研究進度
- 支援 `!list` 列出最近的研究文章
- 支援指定研究深度（quick / deep）
