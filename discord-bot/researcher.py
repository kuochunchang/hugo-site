import asyncio
import json
import logging
import os
import signal
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Coroutine

import config
from prompt import build_draft_prompt, build_final_prompt, build_research_prompt, build_review_prompt

log = logging.getLogger(__name__)

# 進度階段定義（只定義能從文件系統確實偵測到的階段）
PHASE_WORKING = "🔍 研究與撰寫中..."
PHASE_ARTICLE_DONE = "✅ 文章已完成，正在生成語音..."
PHASE_AUDIO_DONE = "✅ 語音已生成，正在推送到網站..."

# Claude 輸出日誌目錄
LOG_DIR = config.HUGO_DIR / "discord-bot" / "logs"


@dataclass
class ActivityTracker:
    """追蹤 Claude stream-json 事件，提取即時活動摘要。"""

    current_activity: str = ""
    tool_count: int = 0
    _collected_text: list[str] = field(default_factory=list)

    def get_output(self) -> str:
        return "".join(self._collected_text)

    def process_event(self, event: dict) -> None:
        etype = event.get("type", "")
        if etype == "assistant":
            self._process_assistant(event)
        elif etype == "result":
            self._process_result(event)

    def _process_assistant(self, event: dict) -> None:
        for block in event.get("message", {}).get("content", []):
            btype = block.get("type", "")
            if btype == "tool_use":
                self.tool_count += 1
                self._update_activity(block)
            elif btype == "text":
                self._collected_text.append(block.get("text", ""))

    def _process_result(self, event: dict) -> None:
        for block in event.get("message", {}).get("content", []):
            if block.get("type") == "text":
                self._collected_text.append(block.get("text", ""))

    def _update_activity(self, block: dict) -> None:
        name = block.get("name", "?")
        inp = block.get("input", {})

        if name in ("WebSearch", "WebFetch"):
            target = inp.get("query") or inp.get("url") or ""
            self.current_activity = f"🌐 {name}: {target[:80]}"
        elif name in ("Read", "Glob", "Grep"):
            target = inp.get("file_path") or inp.get("pattern") or ""
            self.current_activity = f"📄 {name}: {target[:80]}"
        elif name == "Write":
            target = inp.get("file_path", "")
            self.current_activity = f"✏️ Write: {target[:80]}"
        elif name == "Edit":
            target = inp.get("file_path", "")
            self.current_activity = f"✏️ Edit: {target[:80]}"
        elif name == "Bash":
            cmd = inp.get("command", "")
            self.current_activity = f"💻 {cmd[:80]}"
        else:
            self.current_activity = f"🔧 {name}"


@dataclass
class ResearchResult:
    success: bool
    title: str = ""
    slug: str = ""
    reason: str = ""
    duration_seconds: float = 0


@dataclass
class ProcessResult:
    """Claude CLI 子進程的執行結果。"""
    success: bool           # exit code == 0
    output: str             # 收集的文字輸出
    return_code: int | None
    duration_seconds: float
    tool_count: int
    last_activity: str
    reason: str = ""        # 失敗原因


def _parse_result(output: str) -> tuple[bool, str, str, str]:
    """從 Claude 輸出中解析 RESULT 行。"""
    for line in reversed(output.splitlines()):
        line = line.strip()
        idx = line.find("RESULT::")
        if idx == -1:
            continue
        result_str = line[idx:].removeprefix("RESULT::")
        parts = dict(
            segment.split("=", 1)
            for segment in result_str.split("::")
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
    """掃描 content/posts/ 偵測研究進度階段。"""
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
    tracker: ActivityTracker,
    interval: int = 20,
) -> None:
    """背景任務：定期偵測進度並透過 callback 回報，包含即時活動摘要。"""
    last_msg = ""
    while True:
        await asyncio.sleep(interval)
        phase, slug = _detect_phase(posts_dir, known_slugs)
        elapsed = time.monotonic() - start_time

        # 組合階段 + 即時活動資訊
        parts = [phase]
        if tracker.tool_count > 0:
            parts.append(f"🔧 已執行 {tracker.tool_count} 個步驟")
        if tracker.current_activity:
            parts.append(f"📍 {tracker.current_activity}")
        msg = "\n".join(parts)

        if msg != last_msg:
            log.info(
                "進度更新：%s (tools=%d, slug=%s, %.0f 秒)",
                phase, tracker.tool_count, slug, elapsed,
            )
            last_msg = msg
        try:
            await callback(msg, elapsed, slug)
        except Exception:
            log.exception("進度回調失敗")


async def _stream_stdout(
    stream: asyncio.StreamReader,
    log_file: Path,
    tracker: ActivityTracker,
) -> None:
    """即時讀取 stream-json stdout，解析事件並寫入日誌檔。"""
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"\n{'='*60}\n")
        f.write(f"[stdout] started at {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"{'='*60}\n")
        while True:
            line = await stream.readline()
            if not line:
                break
            text = line.decode(errors="replace")
            f.write(text)
            f.flush()
            try:
                event = json.loads(text.strip())
                tracker.process_event(event)
            except (json.JSONDecodeError, ValueError):
                pass


async def _stream_stderr(
    stream: asyncio.StreamReader,
    log_file: Path,
    collected: list[str],
) -> None:
    """即時讀取 stderr 並寫入日誌檔。"""
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"\n{'='*60}\n")
        f.write(f"[stderr] started at {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"{'='*60}\n")
        while True:
            line = await stream.readline()
            if not line:
                break
            text = line.decode(errors="replace")
            collected.append(text)
            f.write(text)
            f.flush()


# ── 通用 Claude CLI 執行器 ────────────────────────────────


async def _run_claude_process(
    prompt: str,
    *,
    label: str,
    tracker: ActivityTracker,
    max_turns: int | None = None,
    timeout: int | None = None,
    stall_timeout: int | None = None,
) -> ProcessResult:
    """啟動 Claude CLI 子進程，串流讀取輸出，處理超時，返回結果。"""
    cmd = [
        "claude",
        "-p", prompt,
        "--max-turns", str(max_turns or config.CLAUDE_MAX_TURNS),
        "--dangerously-skip-permissions",
        "--model", "sonnet",
        "--output-format", "stream-json",
        "--verbose",
    ]
    effective_timeout = timeout or config.CLAUDE_TIMEOUT

    # 清除 CLAUDECODE 環境變數，避免巢狀 session 檢查
    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}

    # 建立日誌檔
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    safe_label = label[:50].replace("/", "_").replace(" ", "_")
    log_file = LOG_DIR / f"{timestamp}_{safe_label}.log"
    log.info("[%s] Claude 輸出日誌：%s", label, log_file)

    start = time.monotonic()
    stderr_lines: list[str] = []

    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=env,
            cwd=str(config.HUGO_DIR),
            start_new_session=True,
            limit=10 * 1024 * 1024,
        )
        log.info("[%s] Claude 子進程已啟動 (PID: %d)", label, proc.pid)

        stdout_task = asyncio.create_task(
            _stream_stdout(proc.stdout, log_file, tracker)
        )
        stderr_task = asyncio.create_task(
            _stream_stderr(proc.stderr, log_file, stderr_lines)
        )

        # 停滯偵測 watchdog
        stall_detected = False
        effective_stall = stall_timeout or 0

        async def _watchdog():
            nonlocal stall_detected
            last_count = tracker.tool_count
            last_change = time.monotonic()
            while True:
                await asyncio.sleep(30)
                if tracker.tool_count != last_count:
                    last_count = tracker.tool_count
                    last_change = time.monotonic()
                elif effective_stall and time.monotonic() - last_change > effective_stall:
                    stall_detected = True
                    log.warning(
                        "[%s] 偵測到停滯（%d 秒無新步驟，停在第 %d 步），終止進程",
                        label, effective_stall, last_count,
                    )
                    _kill_process_group(proc)
                    return

        watchdog_task = asyncio.create_task(_watchdog()) if effective_stall else None

        try:
            await asyncio.wait_for(
                asyncio.gather(stdout_task, stderr_task, proc.wait()),
                timeout=effective_timeout,
            )
        finally:
            if watchdog_task:
                watchdog_task.cancel()

    except asyncio.TimeoutError:
        elapsed = time.monotonic() - start
        log.warning(
            "[%s] 超時（%d 秒），正在終止進程組 %d",
            label, effective_timeout, proc.pid,
        )
        _kill_process_group(proc)
        await asyncio.sleep(3)
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except (ProcessLookupError, OSError):
            pass
        return ProcessResult(
            success=False,
            output=tracker.get_output(),
            return_code=None,
            duration_seconds=elapsed,
            tool_count=tracker.tool_count,
            last_activity=tracker.current_activity,
            reason=f"超時（{effective_timeout}秒），已執行 {tracker.tool_count} 個步驟",
        )
    except FileNotFoundError:
        log.error("[%s] claude CLI 未找到", label)
        return ProcessResult(
            success=False,
            output="",
            return_code=None,
            duration_seconds=0,
            tool_count=0,
            last_activity="",
            reason="claude CLI 未找到，請確認已安裝",
        )

    elapsed = time.monotonic() - start
    err_output = "".join(stderr_lines)
    if err_output.strip():
        log.info("[%s] Claude stderr：%s", label, err_output.strip()[:500])

    if stall_detected:
        log.warning(
            "[%s] 因停滯被終止（耗時 %.0f 秒，%d 個工具）",
            label, elapsed, tracker.tool_count,
        )
        return ProcessResult(
            success=False,
            output=tracker.get_output(),
            return_code=proc.returncode,
            duration_seconds=elapsed,
            tool_count=tracker.tool_count,
            last_activity=tracker.current_activity,
            reason=f"停滯（{effective_stall}秒無新步驟，停在第 {tracker.tool_count} 步）",
        )

    if proc.returncode != 0:
        err = err_output[:500]
        tail = tracker.get_output().strip()[-500:] or "(空輸出)"
        log.error(
            "[%s] 失敗（exit code %d，耗時 %.0f 秒，%d 個工具）：%s",
            label, proc.returncode, elapsed, tracker.tool_count, err[:200],
        )
        log.error("[%s] stdout 尾部：%s", label, tail)
        return ProcessResult(
            success=False,
            output=tracker.get_output(),
            return_code=proc.returncode,
            duration_seconds=elapsed,
            tool_count=tracker.tool_count,
            last_activity=tracker.current_activity,
            reason=f"Claude CLI 回傳錯誤（exit code {proc.returncode}）: {err}",
        )

    return ProcessResult(
        success=True,
        output=tracker.get_output(),
        return_code=0,
        duration_seconds=elapsed,
        tool_count=tracker.tool_count,
        last_activity=tracker.current_activity,
    )


# ── 單進程研究（向後兼容）────────────────────────────────


async def run_research(
    topic: str,
    progress_callback: ProgressCallback | None = None,
) -> ResearchResult:
    """呼叫 Claude CLI 執行深度研究（單進程模式）。"""
    prompt = build_research_prompt(topic, config.TTS_VOICE)

    # 記錄研究前已存在的 slug，用於偵測新文章
    posts_dir = config.HUGO_DIR / "content" / "posts"
    known_slugs: set[str] = set()
    if posts_dir.exists():
        known_slugs = {d.name for d in posts_dir.iterdir() if d.is_dir()}

    log.info("開始研究：%s", topic)

    start = time.monotonic()
    tracker = ActivityTracker()
    monitor_task: asyncio.Task | None = None

    if progress_callback:
        monitor_task = asyncio.create_task(
            _progress_monitor(
                posts_dir, known_slugs, start, progress_callback, tracker,
            )
        )

    try:
        proc_result = await _run_claude_process(
            prompt,
            label=topic,
            tracker=tracker,
        )
    finally:
        if monitor_task:
            monitor_task.cancel()
            try:
                await monitor_task
            except asyncio.CancelledError:
                pass

    if not proc_result.success:
        return ResearchResult(
            success=False,
            reason=proc_result.reason,
            duration_seconds=proc_result.duration_seconds,
        )

    success, title, slug, reason = _parse_result(proc_result.output)

    if success:
        log.info(
            "研究完成：%s (slug: %s，耗時 %.0f 秒，%d 個工具)",
            title, slug, proc_result.duration_seconds, proc_result.tool_count,
        )
    else:
        tail = proc_result.output.strip()[-500:] or "(空輸出)"
        log.warning("研究未成功解析結果（耗時 %.0f 秒）：%s", proc_result.duration_seconds, reason)
        log.warning("Claude 輸出尾部：%s", tail)

    return ResearchResult(
        success=success,
        title=title,
        slug=slug,
        reason=reason,
        duration_seconds=proc_result.duration_seconds,
    )


# ── 雙路並行研究 ──────────────────────────────────────────


async def _dual_progress_monitor(
    start_time: float,
    callback: ProgressCallback,
    trackers: list[ActivityTracker],
    interval: int = 20,
) -> None:
    """草稿階段的進度監控，同時追蹤兩個 tracker（支援中途替換）。"""
    last_msg = ""
    while True:
        await asyncio.sleep(interval)
        elapsed = time.monotonic() - start_time

        lines = ["📝 雙路並行研究中..."]
        for label, t in [("路線 A", trackers[0]), ("路線 B", trackers[1])]:
            activity = t.current_activity or "準備中"
            lines.append(f"{label}：{t.tool_count} 步驟 | {activity}")
        msg = "\n".join(lines)

        if msg != last_msg:
            log.info(
                "雙路進度：A=%d步 B=%d步 (%.0f 秒)",
                trackers[0].tool_count, trackers[1].tool_count, elapsed,
            )
            last_msg = msg
        try:
            await callback(msg, elapsed, None)
        except Exception:
            log.exception("進度回調失敗")


def _cleanup_temp_files(*paths: str) -> None:
    """安全清理暫存檔案。"""
    for p in paths:
        try:
            Path(p).unlink(missing_ok=True)
            log.info("已清理暫存檔：%s", p)
        except OSError as e:
            log.warning("清理暫存檔失敗 %s：%s", p, e)


async def run_dual_research(
    topic: str,
    progress_callback: ProgressCallback | None = None,
) -> ResearchResult:
    """雙路並行研究：兩個 Claude CLI 各自研究+寫草稿，合併後發布。"""
    total_start = time.monotonic()

    # 準備草稿路徑
    ts = int(time.time())
    draft_a = f"/tmp/research-draft-A-{ts}.md"
    draft_b = f"/tmp/research-draft-B-{ts}.md"

    log.info("開始雙路研究：%s", topic)
    log.info("草稿路徑：A=%s B=%s", draft_a, draft_b)

    # ── 階段一：並行草稿（含停滯重試）──

    trackers = [ActivityTracker(), ActivityTracker()]
    monitor_task: asyncio.Task | None = None

    if progress_callback:
        monitor_task = asyncio.create_task(
            _dual_progress_monitor(
                total_start, progress_callback, trackers,
            )
        )

    prompt_a = build_draft_prompt(topic, draft_a)
    prompt_b = build_draft_prompt(topic, draft_b)
    stall_timeout = config.CLAUDE_STALL_TIMEOUT

    async def _run_draft_with_retry(
        prompt: str, label: str, tracker_idx: int,
    ) -> ProcessResult:
        """執行草稿，停滯時自動重試一次。"""
        result = await _run_claude_process(
            prompt,
            label=label,
            tracker=trackers[tracker_idx],
            max_turns=config.CLAUDE_DRAFT_MAX_TURNS,
            timeout=config.CLAUDE_DRAFT_TIMEOUT,
            stall_timeout=stall_timeout,
        )
        if "停滯" in (result.reason or ""):
            log.info("[%s] 停滯，重啟一次", label)
            trackers[tracker_idx] = ActivityTracker()
            result = await _run_claude_process(
                prompt,
                label=f"{label}-retry",
                tracker=trackers[tracker_idx],
                max_turns=config.CLAUDE_DRAFT_MAX_TURNS,
                timeout=config.CLAUDE_DRAFT_TIMEOUT,
                stall_timeout=stall_timeout,
            )
        return result

    try:
        result_a, result_b = await asyncio.gather(
            _run_draft_with_retry(prompt_a, f"draft-A_{topic[:30]}", 0),
            _run_draft_with_retry(prompt_b, f"draft-B_{topic[:30]}", 1),
        )
    finally:
        if monitor_task:
            monitor_task.cancel()
            try:
                await monitor_task
            except asyncio.CancelledError:
                pass

    # ── 判斷草稿結果 ──

    def _draft_ok(result: ProcessResult, path: str) -> bool:
        if not result.success:
            return False
        # 確認 RESULT 行
        for line in reversed(result.output.splitlines()):
            if "RESULT::STATUS=SUCCESS" in line:
                break
        else:
            return False
        # 確認檔案存在且有內容（>100 bytes）
        p = Path(path)
        return p.exists() and p.stat().st_size > 100

    a_ok = _draft_ok(result_a, draft_a)
    b_ok = _draft_ok(result_b, draft_b)

    log.info(
        "草稿結果：A=%s (%.0f秒, %d步) B=%s (%.0f秒, %d步)",
        "OK" if a_ok else "FAIL", result_a.duration_seconds, result_a.tool_count,
        "OK" if b_ok else "FAIL", result_b.duration_seconds, result_b.tool_count,
    )

    if not a_ok and not b_ok:
        _cleanup_temp_files(draft_a, draft_b)
        reasons = []
        if result_a.reason:
            reasons.append(f"A: {result_a.reason}")
        if result_b.reason:
            reasons.append(f"B: {result_b.reason}")
        return ResearchResult(
            success=False,
            reason=f"兩份草稿均失敗。{'; '.join(reasons)}",
            duration_seconds=time.monotonic() - total_start,
        )

    if a_ok and b_ok:
        draft_paths = [draft_a, draft_b]
        log.info("兩份草稿均成功，進入合併階段")
    elif a_ok:
        draft_paths = [draft_a]
        log.info("僅草稿 A 成功，使用單份潤飾")
    else:
        draft_paths = [draft_b]
        log.info("僅草稿 B 成功，使用單份潤飾")

    # ── 階段二：合併發布 ──

    if progress_callback:
        merge_label = "合併兩份草稿" if len(draft_paths) == 2 else "潤飾草稿"
        try:
            elapsed = time.monotonic() - total_start
            await progress_callback(
                f"📖 {merge_label}並發布中...",
                elapsed,
                None,
            )
        except Exception:
            pass

    # 記錄已有 slug，偵測新文章
    posts_dir = config.HUGO_DIR / "content" / "posts"
    known_slugs: set[str] = set()
    if posts_dir.exists():
        known_slugs = {d.name for d in posts_dir.iterdir() if d.is_dir()}

    merge_tracker = ActivityTracker()
    merge_monitor: asyncio.Task | None = None

    if progress_callback:
        merge_monitor = asyncio.create_task(
            _progress_monitor(
                posts_dir, known_slugs, total_start, progress_callback, merge_tracker,
            )
        )

    merge_prompt = build_final_prompt(topic, draft_paths)

    try:
        merge_result = await _run_claude_process(
            merge_prompt,
            label=f"merge_{topic[:30]}",
            tracker=merge_tracker,
            timeout=config.CLAUDE_MERGE_TIMEOUT,
        )
    finally:
        if merge_monitor:
            merge_monitor.cancel()
            try:
                await merge_monitor
            except asyncio.CancelledError:
                pass

    # ── 解析合併結果（需要 slug 進入查核階段）──

    if not merge_result.success:
        _cleanup_temp_files(draft_a, draft_b)
        return ResearchResult(
            success=False,
            reason=f"合併發布失敗：{merge_result.reason}",
            duration_seconds=time.monotonic() - total_start,
        )

    success, title, slug, reason = _parse_result(merge_result.output)

    if not success:
        _cleanup_temp_files(draft_a, draft_b)
        tail = merge_result.output.strip()[-500:] or "(空輸出)"
        log.warning("合併結果解析失敗（耗時 %.0f 秒）：%s", time.monotonic() - total_start, reason)
        log.warning("Claude 輸出尾部：%s", tail)
        return ResearchResult(
            success=False,
            title=title,
            slug=slug,
            reason=reason,
            duration_seconds=time.monotonic() - total_start,
        )

    log.info("合併完成：%s (slug: %s)，進入事實查核階段", title, slug)

    # ── 階段三：事實查核 ──

    if progress_callback:
        try:
            elapsed = time.monotonic() - total_start
            await progress_callback(
                "🔎 事實查核中...",
                elapsed,
                slug,
            )
        except Exception:
            pass

    review_tracker = ActivityTracker()
    review_monitor: asyncio.Task | None = None

    if progress_callback:
        review_monitor = asyncio.create_task(
            _progress_monitor(
                posts_dir, known_slugs, total_start, progress_callback, review_tracker,
            )
        )

    review_prompt = build_review_prompt(topic, slug, draft_paths, config.TTS_VOICE)

    try:
        review_result = await _run_claude_process(
            review_prompt,
            label=f"review_{topic[:30]}",
            tracker=review_tracker,
            max_turns=config.CLAUDE_REVIEW_MAX_TURNS,
            timeout=config.CLAUDE_REVIEW_TIMEOUT,
        )
    finally:
        if review_monitor:
            review_monitor.cancel()
            try:
                await review_monitor
            except asyncio.CancelledError:
                pass

    # 清理暫存檔（查核完成後才清理，因為查核需要讀取草稿）
    _cleanup_temp_files(draft_a, draft_b)

    total_elapsed = time.monotonic() - total_start

    if not review_result.success:
        return ResearchResult(
            success=False,
            reason=f"事實查核失敗：{review_result.reason}",
            duration_seconds=total_elapsed,
        )

    # 重新解析查核結果（查核步驟可能修正了標題）
    r_success, r_title, r_slug, r_reason = _parse_result(review_result.output)
    final_title = r_title or title
    final_slug = r_slug or slug

    total_tools = (
        result_a.tool_count + result_b.tool_count
        + merge_result.tool_count + review_result.tool_count
    )

    if r_success:
        log.info(
            "雙路研究完成（含查核）：%s (slug: %s，總耗時 %.0f 秒，共 %d 個工具)",
            final_title, final_slug, total_elapsed, total_tools,
        )
    else:
        tail = review_result.output.strip()[-500:] or "(空輸出)"
        log.warning("查核結果解析失敗（耗時 %.0f 秒）：%s", total_elapsed, r_reason)
        log.warning("Claude 輸出尾部：%s", tail)

    return ResearchResult(
        success=r_success,
        title=final_title,
        slug=final_slug,
        reason=r_reason,
        duration_seconds=total_elapsed,
    )
