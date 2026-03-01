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
