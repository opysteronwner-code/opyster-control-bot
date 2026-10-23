import discord
from discord.ext import commands
from discord import app_commands
import config
import logging
from collections import defaultdict, deque
import datetime

logger = logging.getLogger("OpysterBot.Security")

class SecurityCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message_tracker = defaultdict(deque)
        self.protection_enabled = True

    security_group = app_commands.Group(name="security", description="Server security and anti-spam protection.")

    @security_group.command(name="status", description="Check current security protection status.")
    async def security_status(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🔒 Security Protection Status",
            description=f"Anti-Spam Protection: **{'ENABLED ✅' if self.protection_enabled else 'DISABLED ❌'}**",
            color=config.EMBED_COLOR
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @security_group.command(name="toggle", description="Toggle anti-spam protection on or off.")
    @app_commands.checks.has_permissions(administrator=True)
    async def security_toggle(self, interaction: discord.Interaction):
        self.protection_enabled = not self.protection_enabled
        status = "ENABLED ✅" if self.protection_enabled else "DISABLED ❌"
        await interaction.response.send_message(f"🔒 Anti-spam protection is now {status}.", ephemeral=True)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if not self.protection_enabled or message.author.bot or not message.guild:
            return

        user_id = message.author.id
        now = datetime.datetime.utcnow()
        timestamps = self.message_tracker[user_id]
        
        timestamps.append(now)
        while timestamps and (now - timestamps[0]).total_seconds() > 4:
            timestamps.popleft()

        if len(timestamps) >= 6:
            try:
                if message.author.guild_permissions.administrator:
                    return
                await message.author.timeout(datetime.timedelta(minutes=2), reason="Anti-Spam: Message burst detected.")
                await message.channel.send(f"⚠️ {message.author.mention} was temporarily timed out for message bursting.", delete_after=10)
                timestamps.clear()
            except Exception as e:
                logger.error(f"Failed to timeout spammer: {e}")

async def setup(bot):
    await bot.add_cog(SecurityCog(bot))
