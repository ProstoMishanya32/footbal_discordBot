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
        db.add_member_in_raiting(str(interaction.user), interaction.user.id, "")  # добавление в обычный рейтинг
        check = db.add_capitans(self.game, str(interaction.user))
        if check:
            emb = nextcord.Embed(
                title=f'**Вы уже зарегистрованы**',
                colour=000000, )
        await interaction.response.send_message(embed=emb, ephemeral = True)


async def selected_team(interaction, game, team):
    db.add_member_in_raiting(str(interaction.user), interaction.user.id, "")
    db.add_player_in_team(game, str(interaction.user), interaction.user.id, 0, team)
    #TODO дичайший колхоз, исправить!
    if team == 1:
        channel_url = config.server.channel_id_first_team
    elif team == 2:
        channel_url = config.server.channel_id_second_team
    elif team == 3:
        channel_url = config.server.channel_id_three_team
    elif team == 4 :
        channel_url = config.server.channel_id_four_team

    channel = bot.get_channel(channel_url)
    invitelink = await channel.create_invite(max_uses=1, unique=True)
    await interaction.response.send_message(content=f"**Ccылка на канал вашей команды** - {invitelink}", ephemeral=True)

async def exit_team(interaction, game):
    try:
        list_id = db.get_id_players(game)
        guild = interaction.guild
        for i in list_id:
            member = nextcord.utils.get(guild.members, id=i[0])
            for row in config.server.roles_team:
                await member.remove_roles(nextcord.utils.get(guild.roles, name=row))
        db.delete_player(game, interaction.user.id)
    except Exception as i:
        pass
    finally:
        await interaction.response.send_message(content=f"**Успешно** :thumbsup:", ephemeral=True)

async def add_roles(interaction, role_name):
    guild = interaction.guild
    role = nextcord.utils.get(guild.roles, name = role_name)
    member = interaction.user
    for i in interaction.user.roles:
        if str(i) in config.server.roles_team:
            await member.remove_roles(nextcord.utils.get(guild.roles, name = str(i)))
    await member.add_roles(nextcord.utils.get(guild.roles, name = role_name))
class Start_capitans_two(nextcord.ui.View):
    def __init__(self, game, ):
        self.game = game
        super().__init__(timeout = None)
    @nextcord.ui.button(label = 'Первая команда', style = nextcord.ButtonStyle.green, custom_id = "first_team")
    async def first_team(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await add_roles(interaction, config.server.roles_team[0])
        await selected_team(interaction, self.game, 1)
    @nextcord.ui.button(label = 'Вторая команда', style = nextcord.ButtonStyle.red, custom_id = "second_team")
    async def second_team(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await add_roles(interaction, config.server.roles_team[1])
        await selected_team(interaction, self.game, 2)
    @nextcord.ui.button(label = 'Отказаться от участия', style = nextcord.ButtonStyle.grey, custom_id = "exit_game")
    async def exit_game(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await exit_team(interaction, self.game)

class Start_capitans_four(nextcord.ui.View):
    def __init__(self, game, ):
        self.game = game
        super().__init__(timeout = None)
    @nextcord.ui.button(label = 'Первая команда', style = nextcord.ButtonStyle.green, custom_id = "first_team_2")
    async def first_team(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await add_roles(interaction, config.server.roles_team[0])
        await selected_team(interaction, self.game, 1)
    @nextcord.ui.button(label = 'Вторая команда', style = nextcord.ButtonStyle.red, custom_id = "second_team_2")
    async def second_team(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await add_roles(interaction, config.server.roles_team[1])
        await selected_team(interaction, self.game, 2)
    @nextcord.ui.button(label = 'Третья команда', style = nextcord.ButtonStyle.green, custom_id = "three_team")
    async def three_team(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await add_roles(interaction, config.server.roles_team[2])
        await selected_team(interaction, self.game, 3)

    @nextcord.ui.button(label = 'Четвертая команда', style = nextcord.ButtonStyle.red, custom_id = "four_team")
    async def four_team(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await add_roles(interaction, config.server.roles_team[3])
        await selected_team(interaction, self.game, 4)
    @nextcord.ui.button(label = 'Отказаться от участия', style = nextcord.ButtonStyle.grey, custom_id = "exit_game_2")
    async def exit_game(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await exit_team(interaction, self.game)