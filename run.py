import logging, sys
from bot import bot
from kernel import config
logging.basicConfig(level = logging.WARNING, format = '[%(asctime)s] [%(filename)s %(levelname)s] %(message)s', datefmt='%y-%m-%d %H:%M:%S', handlers = [logging.FileHandler(
    "./logs./logs.log"), logging.StreamHandler(sys.stdout)])


if __name__ == '__main__':
    bot.run(config.bot.token)