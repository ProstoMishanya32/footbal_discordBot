import nextcord
from nextcord import utils as nextcord_utils
from nextcord.ext.commands import Bot, Cog
from nextcord.ext import commands
from kernel import config
import asyncio

class Select(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout = None)

    list = []
    for i in config.positions.list_postitions:
        list.append(nextcord.SelectOption(label=i, value=i ))
    @nextcord.ui.select(placeholder="Выберите позицию ⚽", options = list, custom_id = 'list_positions')
    async def select_callback(self, select:nextcord.ui.Select, interaction: nextcord.Interaction):
        select.disabled = False
        member = interaction.user
        guild = interaction.guild
        role = nextcord.utils.get(guild.roles, name = select.values[0])
        for i in member.roles:
            if str(i) == select.values[0]:
                await member.remove_roles(nextcord.utils.get(guild.roles, name = str(i)))
                return
            else:
                await member.add_roles(role)

