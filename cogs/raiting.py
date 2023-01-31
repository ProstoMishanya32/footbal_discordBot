import nextcord
from nextcord import utils as nextcord_utils
from nextcord.ext.commands import Bot, Cog
from nextcord.ext import commands
from kernel import config
from modules import start_game, finish_game, db, create_pict_raiting
from bot import bot
from datetime import datetime
import pytz
import random

class Raiting(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot


    @commands.command(aliases=['рейтинг', 'Рейтинг', 'Raiting', 'raiting']) #Варианты вызова функции
    async def get_raiting_top_players(self, ctx):
        result = db.get_raiting_top_players()
        create_pict_raiting.create_pict(result, ctx, "player")
        message = ''
        if result:
            await ctx.send(file = nextcord.File(fp = 'user_card.png') )

    @commands.command(aliases=["рейтинг_кап", "рейтинг_капитанов", 'Рейтинг_Кап', "Рейтинг_Капитанов"]) #Варианты вызова функции
    async def get_raiting_top_capitans(self, ctx):
        result = db.get_raiting_top_capitans(ctx.author.id, str(ctx.author))
        create_pict_raiting.create_pict(result, ctx, "capitans")
        message = ''
        if result:
            await ctx.send(file = nextcord.File(fp = 'user_card.png') )

def setup(bot: Bot):
    bot.add_cog(Raiting(bot))