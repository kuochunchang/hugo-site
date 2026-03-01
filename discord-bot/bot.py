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
