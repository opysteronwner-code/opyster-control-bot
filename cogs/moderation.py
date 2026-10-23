import discord
from discord.ext import commands
from discord import app_commands
import datetime
import config
import logging

logger = logging.getLogger("OpysterBot.Moderation")

class ModerationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    mod_group = app_commands.Group(name="mod", description="Member moderation tools.")

    @mod_group.command(name="timeout", description="Timeout a member for a specified duration in minutes.")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def mod_timeout(self, interaction: discord.Interaction, member: discord.Member, minutes: int, reason: str = "No reason provided"):
        if member.top_role >= interaction.user.top_role and interaction.user.id != config.OWNER_ID:
            await interaction.response.send_message("❌ You cannot timeout a member with an equal or higher role.", ephemeral=True)
            return

        try:
            duration = datetime.timedelta(minutes=minutes)
            await member.timeout(duration, reason=reason)
            await interaction.response.send_message(f"✅ Successfully timed out {member.mention} for {minutes} minute(s). Reason: {reason}", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Failed to timeout member: {e}", ephemeral=True)

    @mod_group.command(name="kick", description="Kick a member from the server.")
    @app_commands.checks.has_permissions(kick_members=True)
    async def mod_kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        if member.top_role >= interaction.user.top_role and interaction.user.id != config.OWNER_ID:
            await interaction.response.send_message("❌ You cannot kick a member with an equal or higher role.", ephemeral=True)
            return

        try:
            await member.kick(reason=reason)
            await interaction.response.send_message(f"✅ Successfully kicked {member.mention}. Reason: {reason}", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Failed to kick member: {e}", ephemeral=True)

    @mod_group.command(name="ban", description="Ban a member from the server.")
    @app_commands.checks.has_permissions(ban_members=True)
    async def mod_ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        if member.top_role >= interaction.user.top_role and interaction.user.id != config.OWNER_ID:
            await interaction.response.send_message("❌ You cannot ban a member with an equal or higher role.", ephemeral=True)
            return

        try:
            await member.ban(reason=reason)
            await interaction.response.send_message(f"✅ Successfully banned {member.mention}. Reason: {reason}", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Failed to ban member: {e}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModerationCog(bot))
