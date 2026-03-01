# Discord Research Bot

Discord 訊息觸發自動深度研究 → 產出文章 + 語音 → 發布到 Hugo 網站。

## 設定

1. 複製 `.env.example` 為 `.env`，填入 Discord Bot Token
2. 安裝依賴：`uv sync`
3. 確認 `claude` CLI 和 `edge-tts` 可用

## 啟動

```bash
uv run python bot.py
```

## 使用

在 Discord 頻道中發送：

```
!research 研究一下 MCP Protocol 的最新發展
```

## 背景執行

```bash
nohup uv run python bot.py > bot.log 2>&1 &
```

或使用 systemd service。
