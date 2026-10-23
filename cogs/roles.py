import discord
from discord.ext import commands
from discord import app_commands
import config
import logging

logger = logging.getLogger("OpysterBot.Roles")

class RolesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    role_group = app_commands.Group(name="role", description="Manage server roles respecting hierarchy.")

    @role_group.command(name="list", description="List server roles.")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def role_list(self, interaction: discord.Interaction):
        guild = interaction.guild
        roles = sorted(guild.roles, key=lambda r: r.position, reverse=True)
        role_names = [r.mention for r in roles[:20]]
        
        embed = discord.Embed(
            title=f"🛡️ Roles in {guild.name} (Total: {len(roles)})",
            description=", ".join(role_names),
            color=config.EMBED_COLOR
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @role_group.command(name="create", description="Create a new role.")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def role_create(self, interaction: discord.Interaction, name: str):
        guild = interaction.guild
        try:
            role = await guild.create_role(name=name, reason=f"Created by {interaction.user}")
            await interaction.response.send_message(f"✅ Successfully created role {role.mention}.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Failed to create role: {e}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(RolesCog(bot))
