import asyncio
import logging
import os
import signal
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Coroutine

import config
from prompt import build_research_prompt

log = logging.getLogger(__name__)

# 進度階段定義（只定義能從文件系統確實偵測到的階段）
PHASE_WORKING = "🔍 研究與撰寫中..."
PHASE_ARTICLE_DONE = "✅ 文章已完成，正在生成語音..."
PHASE_AUDIO_DONE = "✅ 語音已生成，正在推送到網站..."


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


def _kill_process_group(proc: asyncio.subprocess.Process) -> None:
    """殺掉整個進程組（含子進程如 MCP server）。"""
    try:
        os.killpg(proc.pid, signal.SIGTERM)
        log.info("已發送 SIGTERM 到進程組 %d", proc.pid)
    except ProcessLookupError:
        pass
    except OSError:
        # fallback: 只殺主進程
        try:
            proc.kill()
        except ProcessLookupError:
            pass


def _detect_phase(posts_dir: Path, known_slugs: set[str]) -> tuple[str, str | None]:
    """掃描 content/posts/ 偵測研究進度階段。

    只回報能從文件系統確實觀察到的變化：
    - index.md 出現 → 文章已完成
    - audio.mp3 出現 → 語音已生成
    其餘時間統一顯示「研究與撰寫中」。
    """
    if not posts_dir.exists():
        return PHASE_WORKING, None

    for d in posts_dir.iterdir():
        if not d.is_dir() or d.name.startswith("_") or d.name in known_slugs:
            continue
        slug = d.name
        if (d / "audio.mp3").exists():
            return PHASE_AUDIO_DONE, slug
        if (d / "index.md").exists():
            return PHASE_ARTICLE_DONE, slug

    return PHASE_WORKING, None


# 進度回調類型：async def callback(phase: str, elapsed: float, slug: str | None)
ProgressCallback = Callable[[str, float, str | None], Coroutine]


async def _progress_monitor(
    posts_dir: Path,
    known_slugs: set[str],
    start_time: float,
    callback: ProgressCallback,
    interval: int = 20,
) -> None:
    """背景任務：定期偵測進度並透過 callback 回報。"""
    last_phase = ""
    while True:
        await asyncio.sleep(interval)
        phase, slug = _detect_phase(posts_dir, known_slugs)
        elapsed = time.monotonic() - start_time
        if phase != last_phase:
            log.info("進度更新：%s (slug=%s, %.0f 秒)", phase, slug, elapsed)
            last_phase = phase
        try:
            await callback(phase, elapsed, slug)
        except Exception:
            log.exception("進度回調失敗")


async def run_research(
    topic: str,
    progress_callback: ProgressCallback | None = None,
) -> ResearchResult:
    """呼叫 Claude CLI 執行深度研究。"""
    prompt = build_research_prompt(topic, config.TTS_VOICE)

    cmd = [
        "claude",
        "-p", prompt,
        "--max-turns", str(config.CLAUDE_MAX_TURNS),
        "--dangerously-skip-permissions",
        "--model", "sonnet",
    ]

    start = time.monotonic()

    # 清除 CLAUDECODE 環境變數，避免巢狀 session 檢查
    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}

    # 記錄研究前已存在的 slug，用於偵測新文章
    posts_dir = config.HUGO_DIR / "content" / "posts"
    known_slugs: set[str] = set()
    if posts_dir.exists():
        known_slugs = {d.name for d in posts_dir.iterdir() if d.is_dir()}

    log.info("開始研究：%s", topic)

    monitor_task: asyncio.Task | None = None

    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=env,
            cwd=str(config.HUGO_DIR),
            start_new_session=True,  # 建立新進程組，方便整組清理
        )
        log.info("Claude 子進程已啟動 (PID: %d)", proc.pid)

        # 啟動進度監控背景任務
        if progress_callback:
            monitor_task = asyncio.create_task(
                _progress_monitor(posts_dir, known_slugs, start, progress_callback)
            )

        stdout, stderr = await asyncio.wait_for(
            proc.communicate(),
            timeout=config.CLAUDE_TIMEOUT,
        )
    except asyncio.TimeoutError:
        log.warning(
            "研究超時（%d 秒），正在終止進程組 %d",
            config.CLAUDE_TIMEOUT,
            proc.pid,
        )
        _kill_process_group(proc)
        await asyncio.sleep(3)
        # SIGTERM 可能被忽略，補發 SIGKILL 確保清理
        try:
            os.killpg(proc.pid, signal.SIGKILL)
            log.info("已發送 SIGKILL 到進程組 %d", proc.pid)
        except (ProcessLookupError, OSError):
            pass
        return ResearchResult(
            success=False,
            reason=f"Claude CLI 執行超時（{config.CLAUDE_TIMEOUT}秒）",
            duration_seconds=time.monotonic() - start,
        )
    except FileNotFoundError:
        log.error("claude CLI 未找到")
        return ResearchResult(
            success=False,
            reason="claude CLI 未找到，請確認已安裝",
            duration_seconds=0,
        )
    finally:
        if monitor_task:
            monitor_task.cancel()
            try:
                await monitor_task
            except asyncio.CancelledError:
                pass

    elapsed = time.monotonic() - start
    output = stdout.decode(errors="replace")
    err_output = stderr.decode(errors="replace")
    if err_output.strip():
        log.info("Claude stderr：%s", err_output.strip()[:500])

    if proc.returncode != 0:
        err = stderr.decode(errors="replace")[:500]
        log.error(
            "研究失敗（exit code %d，耗時 %.0f 秒）：%s",
            proc.returncode,
            elapsed,
            err[:200],
        )
        return ResearchResult(
            success=False,
            reason=f"Claude CLI 回傳錯誤（exit code {proc.returncode}）: {err}",
            duration_seconds=elapsed,
        )

    success, title, slug, reason = _parse_result(output)

    if success:
        log.info("研究完成：%s (slug: %s，耗時 %.0f 秒)", title, slug, elapsed)
    else:
        # 記錄 Claude 輸出的最後 500 字，方便排查
        tail = output.strip()[-500:] if output.strip() else "(空輸出)"
        log.warning("研究未成功解析結果（耗時 %.0f 秒）：%s", elapsed, reason)
        log.warning("Claude 輸出尾部：%s", tail)

    return ResearchResult(
        success=success,
        title=title,
        slug=slug,
        reason=reason,
        duration_seconds=elapsed,
    )
