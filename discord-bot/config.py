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
CLAUDE_TIMEOUT = int(os.environ.get("CLAUDE_TIMEOUT", "900"))  # 15 分鐘

# 草稿階段（只做研究+寫文）
CLAUDE_DRAFT_MAX_TURNS = int(os.environ.get("CLAUDE_DRAFT_MAX_TURNS", "30"))
CLAUDE_DRAFT_TIMEOUT = int(os.environ.get("CLAUDE_DRAFT_TIMEOUT", "900"))  # 15 分鐘

# 合併發布階段
CLAUDE_MERGE_TIMEOUT = int(os.environ.get("CLAUDE_MERGE_TIMEOUT", "900"))  # 15 分鐘

# 事實查核階段
CLAUDE_REVIEW_MAX_TURNS = int(os.environ.get("CLAUDE_REVIEW_MAX_TURNS", "20"))
CLAUDE_REVIEW_TIMEOUT = int(os.environ.get("CLAUDE_REVIEW_TIMEOUT", "600"))  # 10 分鐘

# 停滯偵測（tool_count 無變化超過此秒數則判定停滯）
CLAUDE_STALL_TIMEOUT = int(os.environ.get("CLAUDE_STALL_TIMEOUT", "300"))  # 5 分鐘

# 研究佇列設定
QUEUE_MAX_SIZE = int(os.environ.get("QUEUE_MAX_SIZE", "5"))

# TTS 設定
TTS_VOICE = os.environ.get("TTS_VOICE", "zh-TW-HsiaoChenNeural")
