import discord
from discord.ext import commands
import config
import logging

logger = logging.getLogger("OpysterBot.AuditLogs")

class AuditLogsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        await self.log_event(channel.guild, "Channel Created", f"Channel `{channel.name}` ({channel.type}) was created.")

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        await self.log_event(channel.guild, "Channel Deleted", f"Channel `{channel.name}` was deleted.")

    async def log_event(self, guild, action: str, description: str):
        if not config.AUDIT_LOG_CHANNEL_ID:
            return
        channel = guild.get_channel(config.AUDIT_LOG_CHANNEL_ID)
        if not channel:
            return

        embed = discord.Embed(
            title=f"📜 Audit Log: {action}",
            description=description,
            color=config.EMBED_COLOR,
            timestamp=discord.utils.utcnow()
        )
        try:
            await channel.send(embed=embed)
        except Exception as e:
            logger.error(f"Failed to send audit log: {e}")

async def setup(bot):
    await bot.add_cog(AuditLogsCog(bot))
