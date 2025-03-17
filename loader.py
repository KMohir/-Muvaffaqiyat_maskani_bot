from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
# PROXY_URL = "http://proxy.server:3128"
#
#
# from data import config
#
# bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML,proxy=PROXY_URL)
# storage = MemoryStorage()
# dp = Dispatcher(bot, storage=storage)
# from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage



from data import config

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
