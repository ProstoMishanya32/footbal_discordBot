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


    @commands.command(aliases=['капитан', 'Капитан', 'capitan', 'Capitans']) #Варианты вызова функции
    @commands.has_any_role(config.server.admin_role, config.server.moderator_role) #Проверка, есть ль нужные роли у пользователя
    async def choice_capittan(self, ctx, arg):
        await ctx.channel.purge(limit=1) # Удаление сообщение с вызовом команды
        amount = db.get_amount_match(arg) # Бот узнает количество команд
        list = db.get_capitans(arg) #Бот узнает количество желающих капитанов
        capitans_list  = [] #Список капитанов
        if amount == 2:
            view = start_game.Start_capitans_two(arg)  # Подключение кнопокк
        else:
            view = start_game.Start_capitans_four(arg)
        for i, name_capitan in enumerate(random.sample(list, amount), start = 1):
            capitan = bot.get_user(db.get_id_capitan(name_capitan[0]))
            db.add_member_in_raiting(str(capitan), capitan.id, "_capitans") # добавление в рейтинг капитанов
            db.add_player_in_team(arg, str(capitan), capitan.id , 1, int(i)) #Сделать заполнение в ретинг TODO
            capitans_list.append(f"**{db.get_amount_team_capitan(int(capitan.id), arg)} - {capitan.mention}**")
            capitans_list.sort()
        temp = '\n' #TODO убрать из комментариев про удаление
        db.delete_table(arg)  # Удаление таблицы с тренерами
        emb = nextcord.Embed( # Создание Embed
            title = config.startGame_with_capitans.title,
            description = f"*Команды --- Капитаны:*\n{temp.join(capitans_list)}\n{config.startGame_with_capitans.description}",
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
        amount = db.get_amount_match(arg)
        if match:
            if amount == 2:
                view = finish_game.FinishGame_two(arg)  # Подключение кнопок
            else:
                view = finish_game.FinishGame_four(arg)
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