import nextcord
from nextcord.ext import commands
from kernel import config
import os
from cogs import positions
from modules import list_positions, db

class PersistentViewBot(commands.Bot):
    def __init__(self):
        intents = nextcord.Intents.all()
        intents.message_content = True
        super().__init__(command_prefix=commands.when_mentioned_or(config.bot.prefix), intents=intents)
        self.persistent_views_added = False

    async def on_ready(self):
        db.create_table_raitins()
        print(f'Бот успешно запустился и вошел в сеть {self.user}\n{"*"* 50}')
        if not self.persistent_views_added:
            self.add_view(view = list_positions.Select())
            self.persistent_views_added = True



bot = PersistentViewBot()

for filename in os.listdir("cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")