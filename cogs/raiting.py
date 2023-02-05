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

def check_role(roles):
    check = False
    for i in roles:
        if str(i) == config.server.admin_role or str(i) == config.server.moderator_role:
            check = True
    return check
class Raiting(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @nextcord.slash_command(name="raiting", description="Посмотреть свой рейтинг", guild_ids = config.bot.guilds)
    async def get_raiting_top_players(self, interaction: nextcord.Interaction ):
        await interaction.response.defer()
        result = db.get_raiting_top(interaction.user.id, str(interaction.user), "raiting")
        create_pict_raiting.create_pict(result, interaction, "player")
        await interaction.followup.send(file = nextcord.File(fp = 'user_card.png'))

    @nextcord.slash_command(name="raiting_capitans", description="Посмотреть свой рейтинг Капитанов", guild_ids = config.bot.guilds)
    async def get_raiting_top_capitans(self, interaction: nextcord.Interaction ):
        await interaction.response.defer()
        result = db.get_raiting_top(interaction.user.id, str(interaction.user), "raiting_capitans")
        create_pict_raiting.create_pict(result, interaction, "capitans")
        await interaction.followup.send(file = nextcord.File(fp = 'user_card.png'))


    @nextcord.slash_command(name="raiting_players_all", description="Посмотреть рейтинг игроков всех пользователей", guild_ids =  config.bot.guilds)
    async def get_raiting_top_players_all(self, interaction: nextcord.Interaction ):
        await interaction.response.defer()
        if check_role(interaction.user.roles):
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
            await interaction.followup.send(config.text.error_access)

    @nextcord.slash_command(name="raiting_capitans_all", description="Посмотреть рейтинг капитанов всех пользователей", guild_ids =  config.bot.guilds)
    async def get_raiting_top_capitans_all(self, interaction: nextcord.Interaction ):
        await interaction.response.defer()
            if check_role(interaction.user.roles):
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
            else:
                await interaction.followup.send(config.text.error_access)



def setup(bot: Bot):
    bot.add_cog(Raiting(bot))