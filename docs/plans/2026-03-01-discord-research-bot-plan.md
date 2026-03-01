# Discord Research Bot Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 建立 Discord Bot，接收 `!research` 指令後自動用 Claude Code 做深度研究、產出文章 + 語音、發布到 Hugo 網站。

**Architecture:** Python Discord Bot 常駐本機，收到 `!research` 訊息後以 `subprocess` 呼叫 `claude -p`（headless 模式）。Claude 負責研究、寫文章、生成語音、git push。Bot 解析 Claude 輸出並回覆 Discord。

**Tech Stack:** Python 3.12, discord.py, Claude Code CLI (`claude -p`), edge-tts, ffmpeg, uv (package manager)

---

### Task 1: 初始化 Python 專案

**Files:**
- Create: `discord-bot/pyproject.toml`
- Create: `discord-bot/.python-version`
- Modify: `.gitignore`

**Step 1: 建立專案目錄**

```bash
cd ~/workspace/hugo-site
mkdir -p discord-bot
```

**Step 2: 建立 pyproject.toml**

```toml
[project]
name = "discord-research-bot"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "discord.py>=2.4",
    "python-dotenv>=1.0",
]

[project.scripts]
bot = "bot:main"
```

**Step 3: 建立 .python-version**

```
3.12
```

**Step 4: 更新 .gitignore**

在現有 `.gitignore` 末尾加上：

```gitignore
# Discord bot
discord-bot/.env
discord-bot/.venv/
__pycache__/
```

**Step 5: 初始化虛擬環境**

```bash
cd ~/workspace/hugo-site/discord-bot
uv sync
```

**Step 6: Commit**

```bash
cd ~/workspace/hugo-site
git add discord-bot/pyproject.toml discord-bot/.python-version .gitignore
git commit -m "feat(discord-bot): initialize Python project with uv"
```

---

### Task 2: 建立設定模組

**Files:**
- Create: `discord-bot/config.py`
- Create: `discord-bot/.env.example`

**Step 1: 建立 config.py**

```python
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]

# Hugo 專案路徑
HUGO_DIR = Path(os.environ.get("HUGO_DIR", Path.home() / "workspace" / "hugo-site"))

# 網站 URL（用於 Discord 回覆中的連結）
SITE_URL = os.environ.get("SITE_URL", "https://kuochunchang.github.io/hugo-site")

# Claude CLI 設定
CLAUDE_MAX_TURNS = int(os.environ.get("CLAUDE_MAX_TURNS", "50"))
CLAUDE_TIMEOUT = int(os.environ.get("CLAUDE_TIMEOUT", "1800"))  # 30 分鐘

# TTS 設定
TTS_VOICE = os.environ.get("TTS_VOICE", "zh-TW-HsiaoChenNeural")
```

**Step 2: 建立 .env.example**

```bash
DISCORD_TOKEN=your-discord-bot-token-here
# HUGO_DIR=~/workspace/hugo-site
# SITE_URL=https://kuochunchang.github.io/hugo-site
# CLAUDE_MAX_TURNS=50
# CLAUDE_TIMEOUT=1800
# TTS_VOICE=zh-TW-HsiaoChenNeural
```

**Step 3: Commit**

```bash
cd ~/workspace/hugo-site
git add discord-bot/config.py discord-bot/.env.example
git commit -m "feat(discord-bot): add configuration module"
```

---

### Task 3: 建立研究 Prompt 模板

**Files:**
- Create: `discord-bot/prompt.py`

**Step 1: 建立 prompt.py**

這是給 `claude -p` 的 prompt 模板。重要：因為 `claude -p` 是 headless 模式，不能使用 `AskUserQuestion`，所以不能直接呼叫 `/publish` 和 `/narrate` skill。需要把完整步驟寫在 prompt 裡。

```python
from datetime import date


def build_research_prompt(topic: str, voice: str) -> str:
    today = date.today().isoformat()
    return f"""你是一位專業的技術研究員和繁體中文技術寫作者。

## 任務

對以下主題進行深度研究，產出一篇完整的繁體中文技術文章，並生成語音版本。

### 研究主題
{topic}

## 執行步驟

### 第一步：深度研究

1. 使用 WebSearch 從至少 3-5 個不同角度搜尋最新資料
2. 使用 WebFetch 閱讀 3-5 個最重要的參考來源全文
3. 交叉驗證不同來源的資訊

### 第二步：撰寫文章

寫一篇結構完整的繁體中文 Markdown 技術文章：

1. 用 `# ` 開頭寫標題
2. 第二行寫 `> 研究日期：{today}`
3. 包含以下結構：
   - 背景與概述
   - 核心內容（技術細節、架構分析等）
   - 比較分析（如適用）
   - 實際應用場景
   - 結論與展望
4. 引用參考來源（附上連結）
5. 技術名詞保留英文原文

### 第三步：發布到 Hugo

1. 從標題產生一個英文 slug（用小寫和連字號，例如 `mcp-protocol-analysis-2026`）
2. 建立 Page Bundle 目錄：`content/posts/<slug>/`
3. 將文章存為 `content/posts/<slug>/index.md`，加上 Hugo front matter：

```yaml
---
title: "<標題>"
date: {today}
draft: false
tags: [<從內容自動判斷 3-5 個標籤>]
summary: "<一句話摘要>"
---
```

注意：front matter 中不要包含原始的 `# 標題` 行和 `> 研究日期` 行。

### 第四步：生成語音

1. 將文章分段（按 `## ` 二級標題切分）
2. 對每個段落，改寫為適合語音朗讀的自然口語文字：
   - 使用繁體中文
   - 語氣自然流暢，像在跟聽眾說話
   - 技術名詞保留原文但用口語解釋
   - 表格改為口語描述
   - 程式碼改為描述功能
   - 連結只保留描述文字
   - 不加入原文沒有的資訊
   - 不使用 Markdown 語法
3. 合併：
   - 開頭：「以下是『<標題>』的語音版本。」
   - 段落間加空行
   - 結尾：「以上就是本篇文章的語音版本，感謝收聽。」
4. 存為 `content/posts/<slug>/audio.txt`
5. 用 edge-tts 生成音檔：
   ```bash
   edge-tts --voice "{voice}" --file "content/posts/<slug>/audio.txt" --write-media "/tmp/<slug>-raw.mp3"
   ```
6. 用 ffmpeg 壓縮：
   ```bash
   ffmpeg -y -i "/tmp/<slug>-raw.mp3" -ac 1 -ab 64k "content/posts/<slug>/audio.mp3"
   ```
7. 清理暫存檔：`rm -f /tmp/<slug>-raw.mp3`
8. 在 front matter `---` 結束後插入播放器：
   ```html
   <audio controls preload="none" style="width:100%; margin: 1rem 0;">
     <source src="audio.mp3" type="audio/mpeg">
     你的瀏覽器不支援音頻播放。
   </audio>
   ```

### 第五步：Git Push

```bash
cd ~/workspace/hugo-site
git add content/posts/<slug>/
git commit -m "feat: add research article - <標題>"
git push
```

### 第六步：輸出結果

在所有步驟完成後，最後一行輸出（Bot 會解析這一行）：

```
RESULT::TITLE=<文章標題>::SLUG=<slug>::STATUS=SUCCESS
```

如果任何步驟失敗，輸出：

```
RESULT::STATUS=FAILED::REASON=<失敗原因>
```
"""
```

**Step 2: Commit**

```bash
cd ~/workspace/hugo-site
git add discord-bot/prompt.py
git commit -m "feat(discord-bot): add research prompt template"
```

---

### Task 4: 建立 Claude CLI 呼叫模組

**Files:**
- Create: `discord-bot/researcher.py`

**Step 1: 建立 researcher.py**

```python
import asyncio
import re
import time
from dataclasses import dataclass

import config
from prompt import build_research_prompt


@dataclass
class ResearchResult:
    success: bool
    title: str = ""
    slug: str = ""
    reason: str = ""
    duration_seconds: float = 0


def _parse_result(output: str) -> tuple[bool, str, str, str]:
    """從 Claude 輸出中解析 RESULT 行。"""
    for line in reversed(output.splitlines()):
        line = line.strip()
        if line.startswith("RESULT::"):
            parts = dict(
                segment.split("=", 1)
                for segment in line.removeprefix("RESULT::").split("::")
                if "=" in segment
            )
            if parts.get("STATUS") == "SUCCESS":
                return True, parts.get("TITLE", ""), parts.get("SLUG", ""), ""
            else:
                return False, "", "", parts.get("REASON", "Unknown error")
    return False, "", "", "No RESULT line found in Claude output"


async def run_research(topic: str) -> ResearchResult:
    """呼叫 Claude CLI 執行深度研究。"""
    prompt = build_research_prompt(topic, config.TTS_VOICE)

    cmd = [
        "claude",
        "-p", prompt,
        "--cwd", str(config.HUGO_DIR),
        "--allowedTools", "WebSearch,WebFetch,Read,Write,Edit,Bash,Glob,Grep,Agent",
        "--max-turns", str(config.CLAUDE_MAX_TURNS),
        "--dangerously-skip-permissions",
        "--model", "sonnet",
    ]

    start = time.monotonic()

    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await asyncio.wait_for(
            proc.communicate(),
            timeout=config.CLAUDE_TIMEOUT,
        )
    except asyncio.TimeoutError:
        proc.kill()
        return ResearchResult(
            success=False,
            reason=f"Claude CLI 執行超時（{config.CLAUDE_TIMEOUT}秒）",
            duration_seconds=time.monotonic() - start,
        )
    except FileNotFoundError:
        return ResearchResult(
            success=False,
            reason="claude CLI 未找到，請確認已安裝",
            duration_seconds=0,
        )

    elapsed = time.monotonic() - start
    output = stdout.decode(errors="replace")

    if proc.returncode != 0:
        err = stderr.decode(errors="replace")[:500]
        return ResearchResult(
            success=False,
            reason=f"Claude CLI 回傳錯誤（exit code {proc.returncode}）: {err}",
            duration_seconds=elapsed,
        )

    success, title, slug, reason = _parse_result(output)
    return ResearchResult(
        success=success,
        title=title,
        slug=slug,
        reason=reason,
        duration_seconds=elapsed,
    )
```

**Step 2: Commit**

```bash
cd ~/workspace/hugo-site
git add discord-bot/researcher.py
git commit -m "feat(discord-bot): add Claude CLI research runner"
```

---

### Task 5: 建立 Discord Bot 主程式

**Files:**
- Create: `discord-bot/bot.py`

**Step 1: 建立 bot.py**

```python
import asyncio
import logging

import discord
from discord.ext import commands

import config
from researcher import run_research

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger(__name__)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# 用來限制同時只有一個研究任務
_research_lock = asyncio.Lock()


@bot.event
async def on_ready():
    log.info("Bot 已上線：%s (ID: %s)", bot.user.name, bot.user.id)


@bot.command(name="research")
async def research(ctx: commands.Context, *, topic: str):
    """觸發深度研究。用法：!research <主題>"""

    if _research_lock.locked():
        await ctx.reply("⏳ 目前有研究正在進行中，請稍後再試。")
        return

    async with _research_lock:
        status_msg = await ctx.reply(f"🔍 正在研究：**{topic}**\n⏳ 這可能需要幾分鐘...")

        result = await run_research(topic)

        if result.success:
            minutes = int(result.duration_seconds // 60)
            seconds = int(result.duration_seconds % 60)
            url = f"{config.SITE_URL}/posts/{result.slug}/"
            await status_msg.edit(
                content=(
                    f"✅ 研究完成！\n\n"
                    f"📝 **{result.title}**\n"
                    f"🔗 {url}\n"
                    f"🎧 含語音版本\n"
                    f"⏱ 研究耗時：{minutes} 分 {seconds} 秒"
                ),
            )
        else:
            await status_msg.edit(
                content=(
                    f"❌ 研究失敗\n\n"
                    f"📋 主題：{topic}\n"
                    f"原因：{result.reason}"
                ),
            )


def main():
    bot.run(config.DISCORD_TOKEN)


if __name__ == "__main__":
    main()
```

**Step 2: Commit**

```bash
cd ~/workspace/hugo-site
git add discord-bot/bot.py
git commit -m "feat(discord-bot): add main Discord bot with !research command"
```

---

### Task 6: 建立 Discord Bot 和取得 Token

**此步驟需要使用者手動操作。**

**Step 1: 說明 Discord Bot 設定步驟**

提供以下指引讓使用者操作：

1. 前往 https://discord.com/developers/applications
2. 點選「New Application」，命名為 "Research Bot"
3. 左側選 Bot → 點選「Reset Token」→ 複製 Token
4. 開啟 Privileged Gateway Intents 中的 **Message Content Intent**
5. 左側選 OAuth2 → URL Generator：
   - Scopes: `bot`
   - Bot Permissions: `Send Messages`, `Read Message History`
6. 複製產生的 URL，在瀏覽器開啟，邀請到你的 Discord server

**Step 2: 建立 .env 檔案**

```bash
cd ~/workspace/hugo-site/discord-bot
cp .env.example .env
# 手動編輯 .env，填入 DISCORD_TOKEN
```

---

### Task 7: 測試與驗證

**Step 1: 安裝依賴**

```bash
cd ~/workspace/hugo-site/discord-bot
uv sync
```

**Step 2: 驗證 Claude CLI 可用**

```bash
claude --version
```

**Step 3: 驗證 edge-tts 可用**

```bash
edge-tts --version || uv tool install edge-tts
```

**Step 4: 啟動 Bot**

```bash
cd ~/workspace/hugo-site/discord-bot
uv run python bot.py
```

**Step 5: 在 Discord 測試**

發送：
```
!research 簡單介紹一下 WebSocket 協議
```

確認：
- Bot 回覆「正在研究中...」
- 幾分鐘後更新為結果訊息（含標題、連結）
- Hugo 網站上有新文章
- 文章含音頻播放器

**Step 6: 最終 Commit**

確認所有功能正常後：

```bash
cd ~/workspace/hugo-site
git add -A discord-bot/
git commit -m "feat(discord-bot): complete Discord research bot"
```

---

### Task 8: 撰寫 Bot 啟動說明

**Files:**
- Create: `discord-bot/README.md`

**Step 1: 建立 README**

```markdown
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
```

**Step 2: Commit**

```bash
cd ~/workspace/hugo-site
git add discord-bot/README.md
git commit -m "docs(discord-bot): add README with setup instructions"
```
