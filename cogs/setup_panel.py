import discord
from discord.ext import commands
from discord import app_commands
import config
import logging

logger = logging.getLogger("OpysterBot.SetupPanel")

class MainControlView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != config.OWNER_ID and not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "❌ **Access Denied**: You are not authorized to use this control panel.",
                ephemeral=True
            )
            return False
        return True

    @discord.ui.button(label="Server Overview", style=discord.ButtonStyle.secondary, emoji="📊", row=0)
    async def server_overview(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        embed = discord.Embed(
            title=f"📊 Server Overview: {guild.name}",
            description="Detailed statistics and configuration summary.",
            color=config.EMBED_COLOR
        )
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        embed.add_field(name="🆔 Server ID", value=str(guild.id), inline=True)
        embed.add_field(name="👑 Owner", value=f"<@{guild.owner_id}>", inline=True)
        embed.add_field(name="👥 Members", value=str(guild.member_count), inline=True)
        embed.add_field(name="💬 Channels", value=str(len(guild.channels)), inline=True)
        embed.add_field(name="🛡️ Roles", value=str(len(guild.roles)), inline=True)
        embed.add_field(name="🚀 Boost Level", value=f"Level {guild.premium_tier} ({guild.premium_subscription_count} boosts)", inline=True)
        embed.set_footer(text="Opyster Control Bot • Graphite Security Suite")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Channel Management", style=discord.ButtonStyle.primary, emoji="📁", row=0)
    async def channel_mgmt(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="📁 Channel Management",
            description="Use slash commands `/channel list`, `/channel create`, or `/channel delete` to manage server channels securely.",
            color=config.EMBED_COLOR
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Role Management", style=discord.ButtonStyle.primary, emoji="🛡️", row=0)
    async def role_mgmt(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="🛡️ Role Management",
            description="Use slash commands `/role list`, `/role create`, or `/role assign` respecting role hierarchy.",
            color=config.EMBED_COLOR
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Member Moderation", style=discord.ButtonStyle.danger, emoji="🔨", row=1)
    async def moderation_panel(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="🔨 Member Moderation Suite",
            description="Use slash commands `/mod timeout`, `/mod kick`, `/mod ban`, or `/mod warn` to moderate members safely.",
            color=config.EMBED_COLOR
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Security & Anti-Spam", style=discord.ButtonStyle.danger, emoji="🔒", row=1)
    async def security_panel(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="🔒 Security & Anti-Spam Protection",
            description="Use `/security status` or `/security toggle` to manage automated spam and raid protection.",
            color=config.EMBED_COLOR
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Audit Logs", style=discord.ButtonStyle.secondary, emoji="📜", row=1)
    async def audit_logs_panel(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="📜 Audit Logs",
            description="Administrative actions and security alerts are logged to the configured audit channel.",
            color=config.EMBED_COLOR
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Backup & Recovery", style=discord.ButtonStyle.secondary, emoji="💾", row=2)
    async def backup_panel(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="💾 Backup & Recovery System",
            description="Use `/backup create`, `/backup list`, or `/backup restore` to manage server state backups.",
            color=config.EMBED_COLOR
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Refresh Panel", style=discord.ButtonStyle.success, emoji="🔄", row=2)
    async def refresh_panel(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="🛡️ OPYSTER CONTROL ROOM",
            description="Welcome to your private administrative control center. Select an option below to manage server infrastructure securely.",
            color=config.EMBED_COLOR
        )
        embed.set_footer(text="Opyster Control Bot • Secure Admin Terminal")
        await interaction.message.edit(embed=embed, view=self)
        await interaction.response.send_message("✅ Control panel refreshed successfully.", ephemeral=True)

class SetupCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="setup", description="Create or refresh the private administrative control room.")
    @app_commands.checks.has_permissions(administrator=True)
    async def setup(self, interaction: discord.Interaction):
        guild = interaction.guild
        if interaction.user.id != config.OWNER_ID and not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ You are not authorized to run setup.", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)

        me = guild.me
        if not me.guild_permissions.manage_channels or not me.guild_permissions.manage_roles:
            await interaction.followup.send("❌ Bot lacks required permissions (`Manage Channels`, `Manage Roles`) to set up the control room.", ephemeral=True)
            return

        control_channel_name = "opyster-control-room"
        existing_channel = discord.utils.get(guild.text_channels, name=control_channel_name)

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_channels=True),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        if config.OWNER_ID:
            owner_member = guild.get_member(config.OWNER_ID)
            if owner_member:
                overwrites[owner_member] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

        if existing_channel:
            try:
                await existing_channel.edit(overwrites=overwrites, topic="Opyster Control Bot - Private Administrative Terminal")
                control_channel = existing_channel
                created_new = False
            except Exception as e:
                logger.error(f"Failed to update existing control channel: {e}")
                await interaction.followup.send(f"❌ Failed to configure existing control channel: {e}", ephemeral=True)
                return
        else:
            try:
                control_channel = await guild.create_text_channel(
                    name=control_channel_name,
                    overwrites=overwrites,
                    topic="Opyster Control Bot - Private Administrative Terminal"
                )
                created_new = True
            except Exception as e:
                logger.error(f"Failed to create control channel: {e}")
                await interaction.followup.send(f"❌ Failed to create control room channel: {e}", ephemeral=True)
                return

        embed = discord.Embed(
            title="🛡️ OPYSTER CONTROL ROOM",
            description="Welcome to your private administrative control center. Select an option below to manage server infrastructure securely.",
            color=config.EMBED_COLOR
        )
        embed.set_footer(text="Opyster Control Bot • Secure Admin Terminal")

        await control_channel.send(embed=embed, view=MainControlView())
        
        status_msg = f"✅ Control room successfully created: {control_channel.mention}" if created_new else f"✅ Control room already exists and has been refreshed: {control_channel.mention}"
        await interaction.followup.send(status_msg, ephemeral=True)

async def setup(bot):
    await bot.add_cog(SetupCog(bot))
