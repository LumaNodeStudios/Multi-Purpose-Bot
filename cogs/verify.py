import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import View, Modal, TextInput
import config
import asyncio

cooldowns = {}

class VerifyModal(Modal, title="Verification"):
    char_name = TextInput(
        label="Character Name",
        placeholder="Enter your character name",
        required=True
    )
    steam_name = TextInput(
        label="Steam Name",
        placeholder="Enter your Steam name",
        required=True
    )
    backstory = TextInput(
        label="Character Backstory",
        placeholder="Write a short backstory for your character...",
        style=discord.TextStyle.paragraph,
        required=True,
        max_length=3000
    )

    def __init__(self, user: discord.Member):
        super().__init__()
        self.user = user

    async def on_submit(self, interaction: discord.Interaction):
        if self.user.id in config.BLACKLIST:
            await interaction.response.send_message("You are blacklisted and cannot verify.", ephemeral=True)
            return

        embed = discord.Embed(title="Verification Request", color=config.EMBED_COLOR)
        embed.add_field(name="User", value=f"{self.user.mention} ({self.user.id})", inline=False)
        embed.add_field(name="Character Name", value=self.char_name.value, inline=False)
        embed.add_field(name="Steam Name", value=self.steam_name.value, inline=False)
        embed.add_field(name="Backstory", value=self.backstory.value, inline=False)

        staff_channel = interaction.client.get_channel(config.VERIFY_LOG_CHANNEL_ID)
        view = StaffDecisionView(self.user, self.char_name.value, self.steam_name.value, self.backstory.value)
        await staff_channel.send(content="@here", embed=embed, view=view)

        await interaction.response.send_message("Your verification request has been sent to staff.", ephemeral=True)

class StaffDecisionView(View):
    def __init__(self, user: discord.Member, char_name: str, steam_name: str, backstory: str):
        super().__init__(timeout=None)
        self.user = user
        self.char_name = char_name
        self.steam_name = steam_name
        self.backstory = backstory

    @discord.ui.button(label="Approve", style=discord.ButtonStyle.success)
    async def approve(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = interaction.guild.get_role(config.VERIFIED_ROLE_ID)
        await self.user.add_roles(role)

        new_nickname = f"{self.char_name} [{self.steam_name}]"
        try:
            await self.user.edit(nick=new_nickname)
        except discord.Forbidden:
            await interaction.response.send_message(
                "I don't have permission to change that user's nickname.", ephemeral=True
            )
            return

        embed = discord.Embed(title="Verification Request - Approved", color=discord.Color.green())
        embed.add_field(name="User", value=f"{self.user.mention} ({self.user.id})", inline=False)
        embed.add_field(name="Character Name", value=self.char_name, inline=False)
        embed.add_field(name="Steam Name", value=self.steam_name, inline=False)
        embed.add_field(name="Backstory", value=self.backstory, inline=False)

        await interaction.response.edit_message(embed=embed, view=None)

        public_embed = discord.Embed(
            title="✅ Verification Approved",
            description=f"{self.user.mention} has been **approved and verified!**",
            color=discord.Color.green()
        )
        public_embed.add_field(name="Character Name", value=self.char_name, inline=False)
        public_embed.add_field(name="Steam Name", value=self.steam_name, inline=False)

        public_embed.set_image(url=config.APPROVED_IMAGE_URL)

        public_log = interaction.client.get_channel(config.VERIFY_PUBLIC_LOG_CHANNEL)
        if public_log:
            await public_log.send(embed=public_embed)

        self.stop()

    @discord.ui.button(label="Deny", style=discord.ButtonStyle.danger)
    async def deny(self, interaction: discord.Interaction, button: discord.ui.Button):
        cooldowns[self.user.id] = asyncio.get_event_loop().time() + 600

        embed = discord.Embed(title="Verification Request - Denied", color=discord.Color.red())
        embed.add_field(name="User", value=f"{self.user.mention} ({self.user.id})", inline=False)
        embed.add_field(name="Character Name", value=self.char_name, inline=False)
        embed.add_field(name="Steam Name", value=self.steam_name, inline=False)
        embed.add_field(name="Backstory", value=self.backstory, inline=False)
        embed.set_footer(text="User may retry in 10 minutes.")

        await interaction.response.edit_message(embed=embed, view=None)

        public_embed = discord.Embed(
            title="❌ Verification Denied",
            description=f"{self.user.mention}, your verification request was denied.",
            color=discord.Color.red()
        )
        public_embed.add_field(name="Character Name", value=self.char_name, inline=False)
        public_embed.add_field(name="Steam Name", value=self.steam_name, inline=False)
        public_embed.add_field(name="Backstory", value=self.backstory, inline=False)
        public_embed.set_footer(text="You may retry after 10 minutes.")

        public_embed.set_image(url=config.DENIED_IMAGE_URL)

        public_log = interaction.client.get_channel(config.VERIFY_PUBLIC_LOG_CHANNEL)
        if public_log:
            await public_log.send(embed=public_embed)

        self.stop()

class VerifyView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Verify", style=discord.ButtonStyle.primary)
    async def verify(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = interaction.user

        if user.id in cooldowns and asyncio.get_event_loop().time() < cooldowns[user.id]:
            remaining = int(cooldowns[user.id] - asyncio.get_event_loop().time())
            await interaction.response.send_message(
                f"You must wait {remaining // 60}m {remaining % 60}s before trying again.",
                ephemeral=True
            )
            return

        await interaction.response.send_modal(VerifyModal(user))

class Verify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="setupverify", description="Setup verification embed")
    @app_commands.guilds(discord.Object(id=config.GUILD_ID))
    async def setupverify(self, interaction: discord.Interaction):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "You don't have permission to use this command.",
                ephemeral=True
            )
            return

        await interaction.response.send_message(
            "Verification system has been set up!",
            ephemeral=True
        )

        embed = discord.Embed(
            title="Verification",
            description="Click the button below to start the verification process.",
            color=config.EMBED_COLOR
        )
        view = VerifyView()
        await interaction.channel.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(Verify(bot))