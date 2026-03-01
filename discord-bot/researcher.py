import asyncio
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
