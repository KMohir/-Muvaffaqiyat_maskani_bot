from sqlite3 import DatabaseError

from aiogram import executor

from db import create_database
from loader import dp
import middlewares, filters, handlers
from utils.misc.set_bot_commands import set_default_commands
from utils.notify_admins import on_startup_notify


async def on_startup(dispatcher):
    await set_default_commands(dispatcher)
    await on_startup_notify(dispatcher)
    try:
        create_database("databaseprotestim.db")
    except DatabaseError as e:
        print(" table support already exists")

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
