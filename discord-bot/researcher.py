import asyncio
import logging
import os
import signal
import time
from dataclasses import dataclass

import config
from prompt import build_research_prompt

log = logging.getLogger(__name__)


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


async def run_research(topic: str) -> ResearchResult:
    """呼叫 Claude CLI 執行深度研究。"""
    prompt = build_research_prompt(topic, config.TTS_VOICE)

    cmd = [
        "claude",
        "-p", prompt,
        "--allowedTools", "WebSearch,WebFetch,Read,Write,Edit,Bash,Glob,Grep,Agent",
        "--max-turns", str(config.CLAUDE_MAX_TURNS),
        "--dangerously-skip-permissions",
        "--model", "sonnet",
        "--strict-mcp-config",  # 不載入任何 MCP server，避免初始化阻塞
    ]

    start = time.monotonic()

    # 清除 CLAUDECODE 環境變數，避免巢狀 session 檢查
    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}

    log.info("開始研究：%s", topic)

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

    elapsed = time.monotonic() - start
    output = stdout.decode(errors="replace")

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
        log.warning("研究未成功解析結果（耗時 %.0f 秒）：%s", elapsed, reason)

    return ResearchResult(
        success=success,
        title=title,
        slug=slug,
        reason=reason,
        duration_seconds=elapsed,
    )
