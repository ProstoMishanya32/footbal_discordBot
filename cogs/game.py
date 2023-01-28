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

class Game(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.command(aliases=['старт', 'Старт', 'Start', 'start']) #Варианты вызова функции
    @commands.has_any_role(config.server.admin_role, config.server.moderator_role) #Проверка, есть ль нужные роли у пользователя
    async def create_game(self, ctx):
        await ctx.channel.purge(limit=1) # Удаление сообщение с вызовом команды
        result = db.create_game((datetime.now(pytz.timezone('Europe/Moscow')).strftime("%d.%m.%Y || %H:%M:%S")))
        view = start_game.Start_game(f"game_{result}")  # Подключение списка
        emb = nextcord.Embed( # Создание Embed
            title = config.startgame.title.format(game_id = result),
            description = config.startgame.description,
            colour = 000000)
        emb.set_footer(
            text=ctx.guild,
            icon_url=config.server.url_pict,)
        await ctx.send(embed = emb, view = view)


    @commands.command(aliases=['капитан', 'Капитан', 'capitan', 'Capitans']) #Варианты вызова функции
    @commands.has_any_role(config.server.admin_role, config.server.moderator_role) #Проверка, есть ль нужные роли у пользователя
    async def choice_capittan(self, ctx, arg):
        await ctx.channel.purge(limit=1) # Удаление сообщение с вызовом команды
        list = db.get_capitans(arg)
        capitans = random.sample(list, 2)
        view = start_game.Start_capitans(arg)  # Подключение кнопок
        first_capitan  = bot.get_user(db.get_id_capitan(capitans[0][0]))
        db.add_player_in_team(arg, str(first_capitan), first_capitan.id , 1, 0)
        second_capitan = bot.get_user(db.get_id_capitan(capitans[1][0]))
        db.add_player_in_team(arg, str(second_capitan), second_capitan.id,  1, 1)
        db.delete_table(arg)  # Удаление таблицы с тренерами
        emb = nextcord.Embed( # Создание Embed
            title = config.startGame_with_capitans.title,
            description = f"**Капитан первой команды - {first_capitan.mention}\n\n Капитан второй команды - {second_capitan.mention}**\n{config.startGame_with_capitans.description}",
            colour = 000000)
        emb.set_footer(
            text=ctx.guild,
            icon_url=config.server.url_pict,)
        await ctx.send(embed = emb, view = view)

    @commands.command(aliases=['финиш', 'Финиш', 'Finish', 'finish']) #Варианты вызова функции
    @commands.has_any_role(config.server.admin_role, config.server.moderator_role) #Проверка, есть ль нужные роли у пользователя
    async def finish_game(self, ctx, arg):
        await ctx.channel.purge(limit=1) # Удаление сообщение с вызовом команды
        match = db.get_match(arg)
        if match:
            view = finish_game.FinishGame(arg)  # Подключение кнопок
            emb = nextcord.Embed( # Создание Embed
                title = "Каков результат матча?",
                colour = 000000)
            emb.set_footer(
                text=ctx.guild,
                icon_url=config.server.url_pict,)
            await ctx.send(embed = emb, view = view)
        else:
            await ctx.send("Игра не найдена :disappointed_relieved: ")



def setup(bot: Bot):
    bot.add_cog(Game(bot))