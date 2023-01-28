import nextcord
from nextcord import utils as nextcord_utils
from nextcord.ext.commands import Bot, Cog
from nextcord.ext import commands
from kernel import config
from modules import start_game, finish_game, db
from bot import bot
from datetime import datetime
import pytz
import random

class Raiting(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.command(aliases=['мойрейтинг', 'Мойрейтинг', 'myraiting', 'Myraiting']) #Варианты вызова функции
    async def get_raiting(self, ctx):
        result = db.get_raiting(ctx.message.author.id, str(ctx.message.author))
        emb = nextcord.Embed( # Создание Embed
            title = ctx.message.author.name,
            description = f"Ваш рейтинг - **{result}** очков",
            colour = 000000)
        emb.set_footer(
            text=ctx.guild,
            icon_url=config.server.url_pict,)
        emb.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.send(embed = emb)

    @commands.command(aliases=['рейтинг', 'Рейтинг', 'Raiting', 'raiting']) #Варианты вызова функции
    async def get_raiting_top(self, ctx):
        result = db.get_raiting_top()
        message = ''
        if result:
            for character in result:
                message += f"#{character['position']} {character['member']} // **{character['raiting']} Очков**\n"
            emb = nextcord.Embed(
                title=f'''**Рейтинг**''',
                description=f'{message}',
                colour=000000)
            emb.set_footer(
                text=ctx.guild,
                icon_url=config.server.url_pict,)
            await ctx.send(embed=emb)




def setup(bot: Bot):
    bot.add_cog(Raiting(bot))