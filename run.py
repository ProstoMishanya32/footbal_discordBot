import logging, sys
from bot import bot
from kernel import config

if __name__ == '__main__':
    bot.run(config.bot.token)