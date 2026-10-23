import discord
from discord.ext import commands
from discord import app_commands
import json
import os
import datetime
import config
import logging

logger = logging.getLogger("OpysterBot.Backups")

class BackupsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        os.makedirs("data/backups", exist_ok=True)

    backup_group = app_commands.Group(name="backup", description="Server backup and recovery system.")

    @backup_group.command(name="create", description="Create a local metadata backup of the server.")
    @app_commands.checks.has_permissions(administrator=True)
    async def backup_create(self, interaction: discord.Interaction):
        guild = interaction.guild
        await interaction.response.defer(ephemeral=True)

        backup_data = {
            "server_name": guild.name,
            "server_id": guild.id,
            "created_at": datetime.datetime.utcnow().isoformat(),
            "channels": [{"name": c.name, "type": str(c.type), "position": c.position} for c in guild.channels],
            "roles": [{"name": r.name, "color": r.color.value, "position": r.position} for r in guild.roles]
        }

        filename = f"data/backups/backup_{guild.id}_{int(datetime.datetime.utcnow().timestamp())}.json"
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(backup_data, f, indent=4)
            await interaction.followup.send(f"✅ Successfully created server backup: `{filename}`", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"❌ Failed to create backup: {e}", ephemeral=True)

    @backup_group.command(name="list", description="List available local server backups.")
    @app_commands.checks.has_permissions(administrator=True)
    async def backup_list(self, interaction: discord.Interaction):
        files = [f for f in os.listdir("data/backups") if f.endswith(".json")]
        if not files:
            await interaction.response.send_message("📁 No local backups found.", ephemeral=True)
            return

        embed = discord.Embed(
            title="💾 Available Server Backups",
            description="\n".join([f"`{f}`" for f in files[:10]]),
            color=config.EMBED_COLOR
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(BackupsCog(bot))
