import nextcord
from nextcord import utils as nextcord_utils
from nextcord.ext.commands import Bot, Cog
from nextcord.ext import commands
from kernel import config
from modules import db
from bot import bot




class Start_game(nextcord.ui.View):
    def __init__(self, game):
        self.game = game
        super().__init__(timeout = None)
    @nextcord.ui.button(label = 'Регистрация', style = nextcord.ButtonStyle.blurple, custom_id = "game_registation")
    async def registration(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        emb = nextcord.Embed(
            title=f'**Вы зарегистрованы**',
            colour=000000,)
        db.add_member_in_raiting(str(interaction.user), interaction.user.id)
        check = db.add_capitans(self.game, str(interaction.user))
        if check:
            emb = nextcord.Embed(
                title=f'**Вы уже зарегистрованы**',
                colour=000000, )
        await interaction.response.send_message(embed=emb, ephemeral = True)

class Start_capitans(nextcord.ui.View):
    def __init__(self, game):
        self.game = game
        super().__init__(timeout = None)
    @nextcord.ui.button(label = 'Первая команда', style = nextcord.ButtonStyle.green, custom_id = "first_team")
    async def first_team(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        db.add_member_in_raiting(str(interaction.user), interaction.user.id)
        db.add_player_in_team(self.game, str(interaction.user), interaction.user.id, 0, 0)
        channel = bot.get_channel(config.server.channel_id_first_team)
        invitelink = await channel.create_invite(max_uses=1, unique=True)
        await interaction.response.send_message(content = f"**Ccылка на канал вашей команды** - {invitelink}", ephemeral=True)


    @nextcord.ui.button(label = 'Вторая команда', style = nextcord.ButtonStyle.red, custom_id = "second_team")
    async def second_team(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        db.add_member_in_raiting(str(interaction.user), interaction.user.id)
        db.add_player_in_team(self.game, str(interaction.user), interaction.user.id, 0, 1)
        channel = bot.get_channel(config.server.channel_id_second_team)
        invitelink = await channel.create_invite(max_uses=1, unique=True)
        await interaction.response.send_message(content = f"**Ccылка на канал вашей команды** - {invitelink}", ephemeral=True)


    @nextcord.ui.button(label = 'Отказаться от участия', style = nextcord.ButtonStyle.grey, custom_id = "exit_game")
    async def exit_game(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        try:
            db.delete_player(self.game, interaction.user.id)
        except Exception as i:
            print(i)
        finally:
            await interaction.response.send_message(content=f"**Успено** :thumbsup:", ephemeral=True)
