import nextcord
from nextcord import utils as nextcord_utils
from nextcord.ext.commands import Bot, Cog
from nextcord.ext import commands
from kernel import config
from modules import db
from bot import bot


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
        await interaction.response.send_message(embed=emb)


class FinishGame_two(nextcord.ui.View):
    def __init__(self, game):
        self.game = game
        super().__init__(timeout = None)


    @nextcord.ui.button(label = 'Первая команда', style = nextcord.ButtonStyle.green, custom_id = "first_team_finish")
    async def first_team(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        check = False
        for i in interaction.user.roles:
            if str(i) == config.server.moderator_role or str(i) == config.server.admin_role:
                check = True
        await finish_game(interaction, self.game, check, 1, "Победа")
        await finish_game(interaction, self.game, check, 2, "Поражение")

    @nextcord.ui.button(label = 'Вторая команда', style = nextcord.ButtonStyle.red, custom_id = "second_team_finish")
    async def second_team(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        check = False
        for i in interaction.user.roles:
            if str(i) == config.server.moderator_role or str(i) == config.server.admin_role:
                check = True
        await finish_game(interaction, self.game, check, 2, "Победа")
        await finish_game(interaction, self.game, check, 1, "Поражение")


    @nextcord.ui.button(label = 'Ничья', style = nextcord.ButtonStyle.grey, custom_id = "draw_finish")
    async def draw_finish(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        check = False
        for i in interaction.user.roles:
            if str(i) == config.server.moderator_role or str(i) == config.server.admin_role:
                check = True
        await finish_game(interaction, self.game, check, 1, "Ничья")
        await finish_game(interaction, self.game, check, 2, "Ничья")

class FinishGame_four(nextcord.ui.View):
    def __init__(self, game):
        self.game = game
        super().__init__(timeout = None)


    @nextcord.ui.button(label = 'Победа Первой команды', style = nextcord.ButtonStyle.green, custom_id = "first_team_finish_win")
    async def first_team_win(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        check = False
        for i in interaction.user.roles:
            if str(i) == config.server.moderator_role or str(i) == config.server.admin_role:
                check = True
        await finish_game(interaction, self.game, check, 1, "Победа")

    @nextcord.ui.button(label = 'Поражение Первой команды', style = nextcord.ButtonStyle.green, custom_id = "first_team_finish_lose")
    async def first_team_lose(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        check = False
        for i in interaction.user.roles:
            if str(i) == config.server.moderator_role or str(i) == config.server.admin_role:
                check = True
        await finish_game(interaction, self.game, check, 1, "Поражение")

    @nextcord.ui.button(label = 'Ничья у Первой команды', style = nextcord.ButtonStyle.green, custom_id = "first_team_finish_draw")
    async def first_team_draw(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        check = False
        for i in interaction.user.roles:
            if str(i) == config.server.moderator_role or str(i) == config.server.admin_role:
                check = True
        await finish_game(interaction, self.game, check, 1, "Ничья")


    @nextcord.ui.button(label='Победа Второй команды', style=nextcord.ButtonStyle.red, custom_id="second_team_finish_win")
    async def second_team_win(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        check = False
        for i in interaction.user.roles:
            if str(i) == config.server.moderator_role or str(i) == config.server.admin_role:
                check = True
        await finish_game(interaction, self.game, check, 2, "Победа")


    @nextcord.ui.button(label='Поражение Второй команды', style=nextcord.ButtonStyle.red,custom_id="second_team_finish_lose")
    async def second_team_lose(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        check = False
        for i in interaction.user.roles:
            if str(i) == config.server.moderator_role or str(i) == config.server.admin_role:
                check = True
        await finish_game(interaction, self.game, check, 2, "Поражение")


    @nextcord.ui.button(label='Ничья у Второй команды', style=nextcord.ButtonStyle.red, custom_id="second_team_finish_draw")
    async def second_team_draw(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        check = False
        for i in interaction.user.roles:
            if str(i) == config.server.moderator_role or str(i) == config.server.admin_role:
                check = True
        await finish_game(interaction, self.game, check, 2, "Ничья")

    @nextcord.ui.button(label='Победа Третьей команды', style=nextcord.ButtonStyle.grey, custom_id="three_team_finish_win")
    async def three_team_win(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        check = False
        for i in interaction.user.roles:
            if str(i) == config.server.moderator_role or str(i) == config.server.admin_role:
                check = True
        await finish_game(interaction, self.game, check, 3, "Победа")


    @nextcord.ui.button(label='Поражение Третьей команды', style=nextcord.ButtonStyle.grey,custom_id="three_team_finish_lose")
    async def three_team_lose(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        check = False
        for i in interaction.user.roles:
            if str(i) == config.server.moderator_role or str(i) == config.server.admin_role:
                check = True
        await finish_game(interaction, self.game, check, 3, "Поражение")


    @nextcord.ui.button(label='Ничья у Третьей команды', style=nextcord.ButtonStyle.grey, custom_id="three_team_finish_draw")
    async def three_team_draw(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        check = False
        for i in interaction.user.roles:
            if str(i) == config.server.moderator_role or str(i) == config.server.admin_role:
                check = True
        await finish_game(interaction, self.game, check, 3, "Ничья")

    @nextcord.ui.button(label='Победа Четвертой команды', style=nextcord.ButtonStyle.blurple, custom_id="four_team_finish_win")
    async def four_team_win(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        check = False
        for i in interaction.user.roles:
            if str(i) == config.server.moderator_role or str(i) == config.server.admin_role:
                check = True
        await finish_game(interaction, self.game, check, 4, "Победа")


    @nextcord.ui.button(label='Поражение Четвертой команды', style=nextcord.ButtonStyle.blurple,custom_id="four_team_finish_lose")
    async def four_team_lose(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        check = False
        for i in interaction.user.roles:
            if str(i) == config.server.moderator_role or str(i) == config.server.admin_role:
                check = True
        await finish_game(interaction, self.game, check, 4, "Поражение")


    @nextcord.ui.button(label='Ничья у Четвертой команды', style=nextcord.ButtonStyle.blurple, custom_id="four_team_finish_draw")
    async def four_team_draw(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        check = False
        for i in interaction.user.roles:
            if str(i) == config.server.moderator_role or str(i) == config.server.admin_role:
                check = True
        await finish_game(interaction, self.game, check, 4, "Ничья")