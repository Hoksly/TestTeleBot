from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from sqlite3 import connect
from data import config
import os

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
if 'data/database' not in os.getcwd():
    db = connect(config.WEATHER_DB_ADDRES)
else:
    db = connect('db/weather.db')