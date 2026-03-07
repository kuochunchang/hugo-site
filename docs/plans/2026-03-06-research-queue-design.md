# Research Queue 設計

## 問題

Discord bot 目前一次只能做一個研究報告，新請求直接被拒絕。

## 目標

- 用 queue 接多個請求，排隊一個接一個進行
- 失敗時自動重試一次，重試無論成功失敗都接下一個
- 顯示排隊位置，輪到時通知開始

## 方案：asyncio.Queue + 背景 worker

### 資料結構

```python
@dataclass
class ResearchTask:
    topic: str
    ctx: commands.Context
    status_msg: discord.Message
    force: bool = False
```

### 流程

```text
!research topic
  ├─ 去重檢查（同現有邏輯）
  ├─ queue 已滿（5 個）→ 拒絕
  ├─ 發送確認訊息「已加入排隊，前面還有 N 個」
  └─ put 到 asyncio.Queue(maxsize=5)

背景 worker（on_ready 啟動）
  └─ 無限迴圈：
      ├─ task = await queue.get()
      ├─ 更新 status_msg：「開始研究...」
      ├─ 執行 run_dual_research()
      ├─ 失敗 → 更新「重試中...」→ 再跑一次
      ├─ 最終結果更新 status_msg（成功/失敗）
      └─ queue.task_done()
```

### 變更範圍

- **bot.py**：移除 `_research_lock`，改用 `asyncio.Queue` + worker task
- **researcher.py**：不需要改動
- **config.py**：新增 `QUEUE_MAX_SIZE = 5`

### 重試邏輯

- 第一次失敗後自動重試一次
- 重試時更新 Discord 訊息「重試中...」
- 重試結果無論成功失敗都接下一個

### 排隊上限

- `asyncio.Queue(maxsize=5)`
- 滿了拒絕：「排隊已滿（5/5），請稍後再試」
