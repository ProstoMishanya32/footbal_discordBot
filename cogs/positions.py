import nextcord
from nextcord import utils as nextcord_utils
from nextcord.ext.commands import Bot, Cog
from nextcord.ext import commands
from kernel import config
from modules import list_positions



class Main_Message(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.command(aliases=['Позиции', 'позиции', 'Positions']) #Варианты вызова функции
    @commands.has_any_role(config.server.admin_role, config.server.moderator_role) #Проверка, есть ль нужные роли у пользователя
    async def positions(self, ctx):
        await ctx.channel.purge(limit=1) # Удаление сообщение с вызовом команды
        view = list_positions.Select() # Подключение списка
        emb = nextcord.Embed( # Создание Embed
            title = config.positionstext.title,
            description = config.positionstext.description,
            colour = 000000)
        if "http" in config.positionstext.photo: #Если нету ссылки, Embed будет без фотки
            emb.set_image(config.positionstext.photo)
        emb.set_footer(
            text=ctx.guild,
            icon_url=config.server.url_pict,)
        await ctx.send(embed = emb, view = view)

def setup(bot: Bot):
    bot.add_cog(Main_Message(bot))