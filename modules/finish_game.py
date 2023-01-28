import nextcord
from nextcord import utils as nextcord_utils
from nextcord.ext.commands import Bot, Cog
from nextcord.ext import commands
from kernel import config
from modules import db
from bot import bot




class FinishGame(nextcord.ui.View):
    def __init__(self, game):
        self.game = game
        super().__init__(timeout = None)


    @nextcord.ui.button(label = 'Первая команда', style = nextcord.ButtonStyle.green, custom_id = "first_team_finish")
    async def first_team(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        result = False
        for i in interaction.user.roles:
            if str(i) == config.server.moderator_role or str(i) == config.server.admin_role:
                result = True
        if result:
            emb = nextcord.Embed( # Создание Embed
                title = "Победа первой команды",
                description = f"**Всем победителям присвоено - {config.server.score_win_player} очков**\n*Проигравшим - {config.server.score_lose_player} очков*\n**Тренеру победившей команде - {config.server.score_win_trener} очков**\n*Проигравшей - {config.server.score_lose_trener} очков*",
                colour = 000000)
            emb.set_footer(
                text = interaction.guild,
                icon_url=config.server.url_pict,)
            db.finish_match(self.game, "ПОБЕДА ПЕРВОЙ КОМАНДЫ", config)
            await interaction.response.edit_message(embed = emb, view = None)

    @nextcord.ui.button(label = 'Вторая команда', style = nextcord.ButtonStyle.red, custom_id = "second_team_finish")
    async def second_team(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        result = False
        for i in interaction.user.roles:
            if str(i) == config.server.moderator_role or str(i) == config.server.admin_role:
                result = True
        if result:
            emb = nextcord.Embed( # Создание Embed
                title = "Победа второй команды",
                description=f"**Всем победителям присвоено - {config.server.score_win_player} очков**\n*Проигравшим - {config.server.score_lose_player} очков*\n**Тренеру победившей команде - {config.server.score_win_trener} очков**\n*Проигравшей - {config.server.score_lose_trener} очков*",
                colour = 000000)
            emb.set_footer(
                text = interaction.guild,
                icon_url=config.server.url_pict,)
            db.finish_match(self.game, "ПОБЕДА ВТОРОЙ КОМАНДЫ", config)
            await interaction.response.edit_message(embed = emb, view = None)


    @nextcord.ui.button(label = 'Ничья', style = nextcord.ButtonStyle.grey, custom_id = "draw_finish")
    async def draw_finish(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        result = False
        for i in interaction.user.roles:
            if str(i) == config.server.moderator_role or str(i) == config.server.admin_role:
                result = True
        if result:
            emb = nextcord.Embed( # Создание Embed
                title = "НИЧЬЯ!",
                description = f"**Всем участникам присвоено - {config.server.score_draw_player} очков**\n*Тренерам присвоено - {config.server.score_draw_trener} очков*",
                colour = 000000)
            emb.set_footer(
                text = interaction.guild,
                icon_url=config.server.url_pict,)
            db.finish_match(self.game, "НИЧЬЯ", config)
            await interaction.response.edit_message(embed = emb, view = None)
