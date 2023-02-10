import nextcord
from nextcord import utils as nextcord_utils
from nextcord.ext.commands import Bot, Cog
from nextcord.ext import commands
from nextcord import application_command
from kernel import config
from modules import start_game, finish_game, db, create_pict_raiting
from bot import bot
from datetime import datetime
import pytz
import random

def check_admin(roles):
    for i in roles:
        if str(i) == config.server.admin_role or str(i) == config.server.moderator_role or str(i) == config.server.moderator_role_2:
            return True

class Raiting(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @nextcord.slash_command(name="rating", description='Посмотреть свой рейтинг || работает только  в канале "рейтинг" ', guild_ids = config.bot.guilds)
    async def get_raiting_top_players(self, interaction: nextcord.Interaction ):
        await interaction.response.defer()
        if interaction.channel.id == config.server.channel_rating:
            result = db.get_raiting_top(interaction.user.id, str(interaction.user), "raiting")
            result_2 = db.get_raiting_top(None, None, "raiting")
            create_pict_raiting.create_pict(result, result_2, interaction, "player")
            await interaction.followup.send(file = nextcord.File(fp = 'user_card.png'))


    @nextcord.slash_command(name="rating_capitans", description='Посмотреть свой рейтинг капитанов || работает только  в канале "рейтинг" ', guild_ids = config.bot.guilds)
    async def get_raiting_top_capitans(self, interaction: nextcord.Interaction ):
        await interaction.response.defer()
        if interaction.channel.id == config.server.channel_rating:
            result = db.get_raiting_top(interaction.user.id, str(interaction.user), "raiting_capitans")
            result_2 = db.get_raiting_top(None, None, "raiting_capitans")
            create_pict_raiting.create_pict(result, result_2, interaction, "capitans")
            await interaction.followup.send(file = nextcord.File(fp = 'user_card.png'))



    @nextcord.slash_command(name="rating_players", description=  "Посмотреть рейтинг всех игроков", guild_ids= config.bot.guilds)
    async def get_raiting_top_players_all(self, interaction: nextcord.Interaction ):
        await interaction.response.defer()
        if check_admin(interaction.user.roles):
            result = db.get_raiting_top(None, None, "raiting")
            message = ''
            if result:
                for character in result:
                    if character['member'] == None:
                        character['position'] = ""
                        character['member'] = ''
                        character['raiting'] = ''
                    else:
                        character['position'] = f"{character['position']}."
                        character['raiting'] = f" - {character['raiting']} очков"
                    message += f"{character['position']} {character['member']}{character['raiting']}\n"
                emb = nextcord.Embed(title=f'''**Рейтинг всех игроков**''', description=f'''{message}''', colour=0xe74c3c)
                await interaction.followup.send(embed=emb)
        else:
            await interaction.followup.send("**Ох нет:( У вас недостаточно прав**")

    @nextcord.slash_command(name="rating_capitans_all", description=  "Посмотреть рейтинг капитанов всех игроков", guild_ids= config.bot.guilds)
    async def get_raiting_top_capitans_all(self, interaction: nextcord.Interaction ):
        await interaction.response.defer()
        result = db.get_raiting_top(None, None, "raiting_capitans")
        message = ''
        if result:
            for character in result:
                if character['member'] == None:
                    character['position'] = ""
                    character['member'] = ''
                    character['raiting'] = ''
                else:
                    character['position'] = f"{character['position']}."
                    character['raiting'] = f" - {character['raiting']} очков"
                message += f"{character['position']} {character['member']}{character['raiting']}\n"
            emb = nextcord.Embed(title=f'''**Рейтинг всех капитанов**''', description=f'''{message}''', colour=0xe74c3c)
            await interaction.followup.send(embed=emb)




def setup(bot: Bot):
    bot.add_cog(Raiting(bot))