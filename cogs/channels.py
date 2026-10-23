import discord
from discord.ext import commands
from discord import app_commands
import config
import logging

logger = logging.getLogger("OpysterBot.Channels")

class ChannelsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    channel_group = app_commands.Group(name="channel", description="Manage server channels safely.")

    @channel_group.command(name="list", description="List all server channels.")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def channel_list(self, interaction: discord.Interaction):
        guild = interaction.guild
        text_count = len(guild.text_channels)
        voice_count = len(guild.voice_channels)
        category_count = len(guild.categories)

        embed = discord.Embed(
            title=f"📁 Channels in {guild.name}",
            description=f"Categories: {category_count} | Text Channels: {text_count} | Voice Channels: {voice_count}",
            color=config.EMBED_COLOR
        )
        
        text_list = ", ".join([c.mention for c in guild.text_channels[:15]])
        if len(guild.text_channels) > 15:
            text_list += f" ... and {len(guild.text_channels) - 15} more."
        if text_list:
            embed.add_field(name="💬 Text Channels (Sample)", value=text_list, inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @channel_group.command(name="create", description="Create a new text or voice channel.")
    @app_commands.choices(channel_type=[
        app_commands.Choice(name="Text", value="text"),
        app_commands.Choice(name="Voice", value="voice")
    ])
    @app_commands.checks.has_permissions(manage_channels=True)
    async def channel_create(self, interaction: discord.Interaction, name: str, channel_type: str):
        guild = interaction.guild
        try:
            if channel_type == "text":
                ch = await guild.create_text_channel(name=name)
            else:
                ch = await guild.create_voice_channel(name=name)
            await interaction.response.send_message(f"✅ Successfully created {channel_type} channel {ch.mention}.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Failed to create channel: {e}", ephemeral=True)

    @channel_group.command(name="delete", description="Delete a specified channel safely.")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def channel_delete(self, interaction: discord.Interaction, channel: discord.abc.GuildChannel):
        class ConfirmDelete(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=30)
                self.value = None

            @discord.ui.button(label="Confirm Delete", style=discord.ButtonStyle.danger)
            async def confirm(self, inter: discord.Interaction, button: discord.ui.Button):
                self.value = True
                self.stop()

            @discord.ui.button(label="Cancel", style=discord.ButtonStyle.secondary)
            async def cancel(self, inter: discord.Interaction, button: discord.ui.Button):
                self.value = False
                self.stop()

        view = ConfirmDelete()
        await interaction.response.send_message(f"⚠️ **WARNING**: Are you sure you want to delete channel `{channel.name}`?", view=view, ephemeral=True)
        
        await view.wait()
        if view.value is True:
            try:
                name = channel.name
                await channel.delete(reason=f"Deleted by admin {interaction.user}")
                await interaction.edit_original_response(content=f"✅ Channel `{name}` has been deleted.", view=None)
            except Exception as e:
                await interaction.edit_original_response(content=f"❌ Failed to delete channel: {e}", view=None)
        else:
            await interaction.edit_original_response(content="❌ Channel deletion cancelled.", view=None)

async def setup(bot):
    await bot.add_cog(ChannelsCog(bot))
