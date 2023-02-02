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

class Raiting(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot


    @nextcord.slash_command(name="raiting", description="Посмотреть свой рейтинг", guild_ids= [1057047620524179556])
    async def get_raiting_top_players(self, interaction: nextcord.Interaction ):
        await interaction.response.defer()
        result = db.get_raiting_top(interaction.user.id, str(interaction.user), "raiting")
        create_pict_raiting.create_pict(result, interaction, "player")
        await interaction.followup.send(file = nextcord.File(fp = 'user_card.png'))

    @nextcord.slash_command(name="raiting_capitans", description="Посмотреть свой рейтинг Капитанов", guild_ids= [1057047620524179556])
    async def get_raiting_top_capitans(self, interaction: nextcord.Interaction ):
        await interaction.response.defer()
        result = db.get_raiting_top(interaction.user.id, str(interaction.user), "raiting_capitans")
        create_pict_raiting.create_pict(result, interaction, "capitans")
        await interaction.followup.send(file = nextcord.File(fp = 'user_card.png'))


    @commands.command(aliases=['рейтинг_и', 'Рейтинг_и', 'Raiting_all', 'raiting_all']) #Варианты вызова функции
    @commands.has_any_role(config.server.admin_role, config.server.moderator_role)
    async def get_raiting_top_players_all(self, ctx):
        await ctx.channel.purge(limit = 1)
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
            await ctx.send(embed=emb)

    @commands.command(aliases=['рейтинг_к', 'Рейтинг_к'])  # Варианты вызова функции
    @commands.has_any_role(config.server.admin_role, config.server.moderator_role)
    async def get_raiting_top_capitans_all(self, ctx):
        await ctx.channel.purge(limit = 1)
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
            await ctx.send(embed=emb)




def setup(bot: Bot):
    bot.add_cog(Raiting(bot))