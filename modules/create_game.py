import nextcord
from nextcord import utils as nextcord_utils
from nextcord.ext.commands import Bot, Cog
from nextcord.ext import commands
from kernel import config
from modules import db, start_game
from bot import bot
from datetime import datetime
import pytz


async def create_game(interaction, amount_team):
    result = db.create_game((datetime.now(pytz.timezone('Europe/Moscow')).strftime("%d.%m.%Y || %H:%M:%S")), amount_team)
    view = start_game.Start_game(f"game_{result}")  # Подключение списка
    emb = nextcord.Embed(  # Создание Embed
        title=config.startgame.title.format(game_id=result),
        description=config.startgame.description,
        colour=000000)
    emb.set_footer(
        text=interaction.guild,
        icon_url=config.server.url_pict, )
    await interaction.response.edit_message(embed=emb, view=view)


class Create_Game(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout = None)

    @nextcord.ui.button(label = 'Две команды', style = nextcord.ButtonStyle.green, custom_id = "one_team")
    async def one_comand(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await create_game(interaction, 2)
    @nextcord.ui.button(label = 'Четыре команды', style = nextcord.ButtonStyle.red, custom_id = "two_team")
    async def second_team(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await create_game(interaction, 4)

