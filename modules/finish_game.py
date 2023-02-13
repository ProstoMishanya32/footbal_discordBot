import nextcord
from nextcord import utils as nextcord_utils
from nextcord import errors
from nextcord.ext.commands import Bot, Cog
from nextcord.ext import commands
from kernel import config
from modules import db
from bot import bot
from datetime import datetime
import pytz

def check_command(team):
    if team == 1:
        team = "Первой"
    elif team == 2:
        team = "Второй"
    elif team == 3:
        team = "Третьей"
    elif team == 4:
        team = "Четвертой "
    return team

def check_admin(roles):
    check = False
    for i in roles: # Развертывание списка ролей
        if str(i) == config.server.moderator_role or str(i) == config.server.admin_role: #Проверка, есть ль данные роли
            check = True
    return check


async def next_match(interaction, game, amount_team):
    game_id = db.create_next_match(game, datetime.now(pytz.timezone('Europe/Moscow')).strftime("%d.%m.%Y || %H:%M:%S"), amount_team)
    emb = nextcord.Embed(  # Создание Embed
        title = config.next_game.title.format(game_id = game_id),
        colour=000000)
    emb.set_footer(
        text=interaction.guild,
        icon_url=config.server.url_pict, )
    await interaction.response.edit_message(embed=emb, view = None)

async def finish_matches(interaction, game):
    list_id = db.get_id_players(game)
    guild = interaction.guild
    for i in list_id:
        member = nextcord.utils.get(guild.members, id = i[0])
        for row in config.server.roles_team:
            await member.remove_roles(nextcord.utils.get(guild.roles, name = row))

    emb = nextcord.Embed(  # Создание Embed
        title = config.finish_matches.title,
        colour=000000)
    emb.set_footer(
        text=interaction.guild,
        icon_url=config.server.url_pict, )
    db.delete_match(game)
    await interaction.response.edit_message(embed=emb, view = None)


async def finish_game(interaction, game, check, team, result):
    if check:
        team_name = check_command(team)
        title = f"{result} {team_name} команды"
        description = f"**Всем победителям присвоено - {config.server.score_win_player} очков**\n*Проигравшим - {config.server.score_lose_player} очков*\n**Тренеру победившей команде - {config.server.score_win_trener} очков**\n*Проигравшей - {config.server.score_lose_trener} очков*"
        result_finish = f"{result.upper()} {team_name.upper()} КОМАНДЫ"
        if result == "Ничья":
            description = f"**Всем участникам присвоено - {config.server.score_draw_player} очков**\nКапитанам команда {config.server.score_draw_trener}"
            title = result.upper()
            result_finish = "НИЧЬЯ"
        emb = nextcord.Embed(  # Создание Embed
            title = title,
            description = description,
            colour=000000)
        emb.set_footer(
            text=interaction.guild,
            icon_url=config.server.url_pict, )
        db.finish_match(game, result_finish, team, result, config)
        channel = bot.get_channel(config.server.channel_manage_game)
        await channel.send(embed = emb)


async def select_result(interaction, team, game):
    team_name = check_command(team)
    view = FinishGame_teams_4(team, game)
    emb = nextcord.Embed(  # Создание Embed
        title = config.select_result.title,
        description = config.select_result.description.format(team_name = team_name),
        colour=000000)
    emb.set_footer(
        text=interaction.guild,
        icon_url=config.server.url_pict, )
    await interaction.response.edit_message(embed=emb, view = view)



async def next_result(interaction, game):
    match = db.get_match(game)
    amount = db.get_amount_match(game)
    if match:
        if amount == 2:
            view = FinishGame_two(game)  # Подключение кнопок
        else:
            view = FinishGame_four(game)
        emb = nextcord.Embed(  # Создание Embed
            title="Каков результат матча?",
            colour=000000)
        emb.set_footer(
            text = interaction.guild,
            icon_url=config.server.url_pict, )
        await interaction.response.edit_message(embed=emb, view=view)

class FinishGame_two(nextcord.ui.View):
    def __init__(self, game):
        self.game = game
        super().__init__(timeout = None)

    @nextcord.ui.button(label = 'Первая команда', style = nextcord.ButtonStyle.green, custom_id = "first_team_finish")
    async def first_team(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):

        check = check_admin(interaction.user.roles)
        if check:
            await finish_game(interaction, self.game, check, 1, "Победа")
            await finish_game(interaction, self.game, check, 2, "Поражение")


    @nextcord.ui.button(label = 'Вторая команда', style = nextcord.ButtonStyle.red, custom_id = "second_team_finish")
    async def second_team(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        check = check_admin(interaction.user.roles)
        if check:
            await finish_game(interaction, self.game, check, 2, "Победа")
            await finish_game(interaction, self.game, check, 1, "Поражение")

    @nextcord.ui.button(label = 'Ничья', style = nextcord.ButtonStyle.grey, custom_id = "draw_finish")
    async def draw_finish(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        check = check_admin(interaction.user.roles)
        if check:
            await finish_game(interaction, self.game, check, 2, "Ничья")

    @nextcord.ui.button(label = 'Следующий матч', style = nextcord.ButtonStyle.blurple, custom_id = "next_match_2")
    async def next_match_2(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        check = check_admin(interaction.user.roles)
        if check:
            await next_match(interaction, self.game, 2)
    @nextcord.ui.button(label = 'Закончить матчи', style = nextcord.ButtonStyle.blurple, custom_id = "finish_match_2")
    async def finish_match_2(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        check = check_admin(interaction.user.roles)
        if check:
            await finish_matches(interaction, self.game)

class FinishGame_four(nextcord.ui.View):
    def __init__(self, game):
        self.game = game
        super().__init__(timeout = None)

    @nextcord.ui.button(label = 'Первая команда', style = nextcord.ButtonStyle.green, custom_id = "first_team")
    async def first_team(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        check = check_admin(interaction.user.roles)
        if check:
            await select_result(interaction, 1, self.game)


    @nextcord.ui.button(label = 'Вторая команда', style = nextcord.ButtonStyle.red, custom_id = "second_team")
    async def second_team(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        check = check_admin(interaction.user.roles)
        if check:
            await select_result(interaction, 2, self.game)

    @nextcord.ui.button(label = 'Третья команда', style = nextcord.ButtonStyle.green, custom_id = "third_team")
    async def third_team(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        check = check_admin(interaction.user.roles)
        if check:
            await select_result(interaction, 3, self.game)

    @nextcord.ui.button(label = 'Четвертая команда', style = nextcord.ButtonStyle.red, custom_id = "fourth_team")
    async def fourth_team(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        check = check_admin(interaction.user.roles)
        if check:
            await select_result(interaction, 4, self.game)

    @nextcord.ui.button(label = 'Следующий матч', style = nextcord.ButtonStyle.blurple, custom_id = "next_match")
    async def next_match(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        check = check_admin(interaction.user.roles)
        if check:
            await next_match(interaction, self.game, 4)
    @nextcord.ui.button(label = 'Завершить серию матчей', style = nextcord.ButtonStyle.grey, custom_id = "finish_matches")
    async def finish_matches(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        check = check_admin(interaction.user.roles)
        if check:
            await finish_matches(interaction, self.game)

class FinishGame_teams_4(nextcord.ui.View): # Кнопки для каждой команды
    def __init__(self, team, game):
        self.team = team
        self.game = game
        super().__init__(timeout = None)

    @nextcord.ui.button(label = 'Выигрыш', style = nextcord.ButtonStyle.green, custom_id = "win_team")
    async def first_team(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        check = check_admin(interaction.user.roles)
        if check:
            await finish_game(interaction, self.game, check, self.team, "Победа")
            await next_result(interaction, self.game)

    @nextcord.ui.button(label = 'Поражение', style = nextcord.ButtonStyle.red, custom_id = "lose_team")
    async def second_team(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        check = check_admin(interaction.user.roles)
        if check:
            await finish_game(interaction, self.game, check, self.team, "Поражение")
            await next_result(interaction, self.game)
    @nextcord.ui.button(label = 'Ничья', style = nextcord.ButtonStyle.grey, custom_id = "draw_team")
    async def third_team(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        check = check_admin(interaction.user.roles)
        if check:
            await finish_game(interaction, self.game, check, self.team, "Ничья")
            await next_result(interaction, self.game)


