import nextcord
from nextcord import utils as nextcord_utils
from nextcord.ext.commands import Bot, Cog
from nextcord.ext import commands
from kernel import config
from bot import bot


class Main_commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['Clear', 'очистка', 'Очистка'])
    @commands.has_any_role(config.server.admin_role)
    async def clear(self, ctx, amount=+ 1):
        try:
            await ctx.channel.purge(limit=amount)
            embed = nextcord.Embed(title = config.text.successfully, description = config.text.clear.format(amount=amount), colour=0xe74c3c)
            embed.set_footer(text=ctx.guild, icon_url=config.server.url_pict)
            await ctx.send(embed=embed)
        except Exception as i:
            print(i)

    @commands.command(aliases=['Повтори', 'повтори', 'Repeat'])
    @commands.has_any_role(config.server.admin_role)
    async def repeat(self, ctx, arg):
        try:
            await ctx.channel.purge(limit=1)
            embed = nextcord.Embed(description=arg, colour=000000)
            embed.set_footer(text=ctx.guild, icon_url=config.server.url_pict)
            await ctx.send(embed = embed)
        except Exception as i:
            print(i)

def setup(bot):
	 bot.add_cog(Main_commands(bot))
