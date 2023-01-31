import nextcord
from nextcord import utils as nextcord_utils
from nextcord.ext.commands import Bot, Cog
from nextcord.ext import commands
from kernel import config
from modules import create_game


class Create_Game(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot


    @commands.command(aliases=['старт', 'Старт', 'Start', 'start']) #Варианты вызова функции
    @commands.has_any_role(config.server.admin_role, config.server.moderator_role) #Проверка, есть ль нужные роли у пользователя
    async def create_game(self, ctx):
        await ctx.channel.purge(limit=1) # Удаление сообщение с вызовом команды
        view = create_game.Create_Game()
        emb = nextcord.Embed( # Создание Embed
            title = config.create_game.title,
            description = config.create_game.description,
            colour = 000000)
        emb.set_footer(
            text=ctx.guild,
            icon_url=config.server.url_pict,)
        await ctx.send(embed = emb, view = view)


def setup(bot: Bot):
    bot.add_cog(Create_Game(bot))