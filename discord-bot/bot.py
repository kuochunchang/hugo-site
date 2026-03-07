import asyncio
import logging
from dataclasses import dataclass
from pathlib import Path

import discord
from discord.ext import commands

import config
from researcher import run_dual_research, run_research

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger(__name__)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=["!", ".", "?"], intents=intents)

# 已完成研究的 slug 集合（內存去重）
_completed_slugs: set[str] = set()


# ── 研究任務佇列 ──────────────────────────────────────────


@dataclass
class ResearchTask:
    topic: str
    ctx: commands.Context
    status_msg: discord.Message
    force: bool = False


_queue: asyncio.Queue[ResearchTask] = asyncio.Queue(maxsize=config.QUEUE_MAX_SIZE)
# 追蹤佇列中 + 執行中的主題（防止重複排隊）
_pending_topics: set[str] = set()


def _find_existing_post(topic: str) -> str | None:
    """掃描 content/posts/ 目錄，檢查是否已有相似主題的文章。

    用簡單的關鍵字比對：把 topic 中的英文單詞轉為小寫，
    檢查是否出現在已有的 slug 目錄名中。
    """
    posts_dir = config.HUGO_DIR / "content" / "posts"
    if not posts_dir.exists():
        return None

    # 從主題提取英文關鍵字（去除常見停用詞）
    stop_words = {"the", "a", "an", "of", "in", "on", "for", "to", "and", "or", "is", "are", "was", "with"}
    keywords = [
        w.lower()
        for w in topic.split()
        if w.isascii() and len(w) > 2 and w.lower() not in stop_words
    ]

    if not keywords:
        return None

    for d in posts_dir.iterdir():
        if not d.is_dir() or not (d / "index.md").exists():
            continue
        slug = d.name.lower()
        # 至少有一半的關鍵字出現在 slug 中
        matches = sum(1 for kw in keywords if kw in slug)
        if matches >= max(1, len(keywords) // 2):
            return d.name

    return None


async def _execute_research(task: ResearchTask) -> None:
    """執行單個研究任務，失敗時重試一次。"""
    topic = task.topic

    async def _update_progress(phase: str, elapsed: float, slug: str | None):
        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)
        text = (
            f"📝 研究中：**{topic}**\n"
            f"{phase}\n"
            f"⏱ 已經過：{minutes} 分 {seconds} 秒"
        )
        try:
            await task.status_msg.edit(content=text)
        except Exception:
            pass

    # 第一次嘗試
    result = await run_dual_research(topic, progress_callback=_update_progress)

    # 失敗時重試一次
    if not result.success:
        log.info("研究失敗，準備重試：topic=%r, reason=%s", topic, result.reason)
        try:
            await task.status_msg.edit(
                content=(
                    f"⚠️ 研究失敗，自動重試中...\n\n"
                    f"📋 主題：**{topic}**\n"
                    f"原因：{result.reason}"
                ),
            )
        except Exception:
            pass

        result = await run_dual_research(topic, progress_callback=_update_progress)

    # 回報最終結果
    if result.success:
        _completed_slugs.add(result.slug)
        minutes = int(result.duration_seconds // 60)
        seconds = int(result.duration_seconds % 60)
        url = f"{config.SITE_URL}/posts/{result.slug}/"
        log.info(
            "研究完成並回報 Discord：title=%r, slug=%s, duration=%dm%ds",
            result.title,
            result.slug,
            minutes,
            seconds,
        )
        await task.status_msg.edit(
            content=(
                f"✅ 研究完成！\n\n"
                f"📝 **{result.title}**\n"
                f"🔗 {url}\n"
                f"🎧 含語音版本\n"
                f"⏱ 研究耗時：{minutes} 分 {seconds} 秒"
            ),
        )
    else:
        log.warning("研究最終失敗：topic=%r, reason=%s", topic, result.reason)
        await task.status_msg.edit(
            content=(
                f"❌ 研究失敗（已重試）\n\n"
                f"📋 主題：{topic}\n"
                f"原因：{result.reason}"
            ),
        )


async def _queue_worker() -> None:
    """背景 worker：從佇列中取任務，逐個執行。"""
    log.info("研究佇列 worker 已啟動")
    while True:
        task = await _queue.get()
        log.info(
            "佇列取出任務：topic=%r, user=%s, 剩餘排隊=%d",
            task.topic,
            task.ctx.author,
            _queue.qsize(),
        )
        try:
            await task.status_msg.edit(
                content=f"📝 雙路並行研究中：**{task.topic}**\n⏳ 這可能需要幾分鐘..."
            )
        except Exception:
            pass

        try:
            await _execute_research(task)
        except Exception:
            log.exception("研究任務異常：topic=%r", task.topic)
            try:
                await task.status_msg.edit(
                    content=(
                        f"❌ 研究發生未預期的錯誤\n\n"
                        f"📋 主題：{task.topic}"
                    ),
                )
            except Exception:
                pass
        finally:
            _pending_topics.discard(task.topic)
            _queue.task_done()


@bot.event
async def on_ready():
    # 啟動時掃描已有文章，填充去重集合
    posts_dir = config.HUGO_DIR / "content" / "posts"
    if posts_dir.exists():
        for d in posts_dir.iterdir():
            if d.is_dir() and (d / "index.md").exists():
                _completed_slugs.add(d.name)
        log.info("已載入 %d 篇已有文章到去重集合", len(_completed_slugs))

    # 啟動佇列 worker
    bot.loop.create_task(_queue_worker())

    log.info("Bot 已上線：%s (ID: %s)", bot.user.name, bot.user.id)


@bot.command(name="research")
async def research(ctx: commands.Context, *, topic: str):
    """觸發深度研究。用法：!research <主題>  （加 --force 可強制重新研究）"""
    force = False
    if topic.endswith("--force"):
        force = True
        topic = topic.removesuffix("--force").strip()

    log.info(
        "收到研究指令：topic=%r, user=%s (ID: %s), force=%s",
        topic,
        ctx.author,
        ctx.author.id,
        force,
    )

    # 去重檢查
    if not force:
        # 檢查是否已在佇列中或執行中
        if topic in _pending_topics:
            log.info("去重命中（佇列中）：topic=%r", topic)
            await ctx.reply(f"⏳ 此主題已在排隊或研究中：**{topic}**")
            return

        existing_slug = _find_existing_post(topic)
        if existing_slug:
            url = f"{config.SITE_URL}/posts/{existing_slug}/"
            log.info("去重命中：topic=%r → slug=%s", topic, existing_slug)
            await ctx.reply(
                f"📝 此主題已有相似文章：\n"
                f"🔗 {url}\n\n"
                f"如需重新研究，請加上 `--force`：\n"
                f"`!research {topic} --force`"
            )
            return

    # 檢查佇列是否已滿
    if _queue.full():
        log.info("研究被拒絕（佇列已滿 %d/%d）", _queue.qsize(), config.QUEUE_MAX_SIZE)
        await ctx.reply(
            f"⏳ 排隊已滿（{config.QUEUE_MAX_SIZE}/{config.QUEUE_MAX_SIZE}），請稍後再試。"
        )
        return

    # 計算排隊位置
    pending = _queue.qsize()
    if pending == 0:
        status_text = f"📝 雙路並行研究中：**{topic}**\n⏳ 這可能需要幾分鐘..."
    else:
        status_text = f"📋 已加入排隊：**{topic}**\n⏳ 前面還有 {pending} 個任務"

    status_msg = await ctx.reply(status_text)

    task = ResearchTask(
        topic=topic,
        ctx=ctx,
        status_msg=status_msg,
        force=force,
    )
    _pending_topics.add(topic)
    await _queue.put(task)
    log.info("任務已加入佇列：topic=%r, queue_size=%d", topic, _queue.qsize())


def main():
    bot.run(config.DISCORD_TOKEN)


if __name__ == "__main__":
    main()
