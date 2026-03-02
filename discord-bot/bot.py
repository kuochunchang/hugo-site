import asyncio
import logging
from pathlib import Path

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

# 已完成研究的 slug 集合（內存去重）
_completed_slugs: set[str] = set()


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


@bot.event
async def on_ready():
    # 啟動時掃描已有文章，填充去重集合
    posts_dir = config.HUGO_DIR / "content" / "posts"
    if posts_dir.exists():
        for d in posts_dir.iterdir():
            if d.is_dir() and (d / "index.md").exists():
                _completed_slugs.add(d.name)
        log.info("已載入 %d 篇已有文章到去重集合", len(_completed_slugs))

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

    if _research_lock.locked():
        log.info("研究被拒絕（有任務進行中）")
        await ctx.reply("⏳ 目前有研究正在進行中，請稍後再試。")
        return

    # 去重檢查
    if not force:
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

    async with _research_lock:
        status_msg = await ctx.reply(f"🔍 正在研究：**{topic}**\n⏳ 這可能需要幾分鐘...")

        result = await run_research(topic)

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
            log.warning("研究失敗並回報 Discord：topic=%r, reason=%s", topic, result.reason)
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
