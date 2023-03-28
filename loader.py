import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

import pytz
from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from dotenv import load_dotenv

load_dotenv()

timezone = pytz.timezone('Etc/GMT-3')


def timetz(*args):
    return datetime.now(timezone).timetuple()


logger = logging.getLogger('main_logger')

aiogram_logger = logging.getLogger('aio_logger')

logger.setLevel(logging.INFO)
aiogram_logger.setLevel(logging.INFO)

main_handler = RotatingFileHandler('logs/my_logger.log', maxBytes=30000000,
                                   backupCount=2)
aiogram_handler = RotatingFileHandler('logs/aiogram_logger.log',
                                      maxBytes=30000000,
                                      backupCount=2)


logger.addHandler(main_handler)
aiogram_logger.addHandler(aiogram_handler)

formatter = logging.Formatter(
    fmt=('%(asctime)s.%(msecs)d %(levelname)s '
         '%(filename)s %(funcName)s %(message)s'),
    datefmt='%d-%m-%Y %H:%M:%S',
)

formatter.converter = timetz

main_handler.setFormatter(formatter)
aiogram_handler.setFormatter(formatter)

TELEGRAM_TOKEN = os.getenv("T_TOKEN")
ADMIN = list(map(int, os.getenv("ADMIN_ID").split()))
TECH = os.getenv("TECH")

storage = MemoryStorage()
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot, storage=storage)

dp.middleware.setup(LoggingMiddleware(logger=aiogram_logger))
