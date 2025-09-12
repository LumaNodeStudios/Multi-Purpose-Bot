import discord
from discord.ext import commands
import config

class Welcome(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """Event triggered when a new member joins the server."""

        channel = self.bot.get_channel(config.WELCOME_CHANNEL_ID)

        if channel is None:
            channel = member.guild.system_channel

        if channel is None:
            return

        embed = discord.Embed(
            title="Welcome to the Server!",
            description=f"Hey {member.mention}, welcome to **{member.guild.name}**!",
            color=discord.Color.green()
        )

        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="Username", value=member.name, inline=True)
        embed.add_field(name="ID", value=member.id, inline=True)
        embed.add_field(
            name="Joined Discord",
            value=member.created_at.strftime("%b %d, %Y"),
            inline=False
        )
        embed.set_footer(text=f"Member #{len(member.guild.members)}")

        await channel.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Welcome(bot))