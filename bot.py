import asyncio
import logging
import os
import sys
import discord
from discord.ext import commands
import config

os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/bot.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    encoding="utf-8"
)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
logging.getLogger().addHandler(console_handler)

logger = logging.getLogger("OpysterBot")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

INITIAL_EXTENSIONS = [
    "cogs.setup_panel",
    "cogs.channels",
    "cogs.roles",
    "cogs.moderation",
    "cogs.security",
    "cogs.audit_logs",
    "cogs.backups"
]

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    try:
        # مزامنة الأوامر عالمياً ومع السيرفر الحالي فوراً
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} commands globally!')
        
        for guild in bot.guilds:
            bot.tree.copy_global_to(guild=guild)
            synced_guild = await bot.tree.sync(guild=guild)
            print(f'Synced {len(synced_guild)} commands directly to guild: {guild.name}')
    except Exception as e:
        print(f'Failed to sync commands: {e}')

async def main():
    async with bot:
        # تحميل الملفات الفرعية (Cogs) أولاً
        for ext in INITIAL_EXTENSIONS:
            try:
                await bot.load_extension(ext)
                logger.info(f"Loaded extension: {ext}")
            except Exception as e:
                logger.error(f"Failed to load extension {ext}: {e}")
        
        # تشغيل البوت بالتوكن الموجود في ملف config.py
        await bot.start(config.BOT_TOKEN)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot shutdown requested by user.")