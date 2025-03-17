from aiogram import types


async def set_default_commands(dp):

    await dp.bot.set_my_commands([
        types.BotCommand("start", "Botni ishga tushurish"),
        types.BotCommand("takliflar", "Takliflarni yuborish"),
        types.BotCommand("change_language", "Tilni ozgartirish"),
        types.BotCommand("contact",'Centris Towers haqida bilish'),
        types.BotCommand("about",'Centris Towers haqida bilish'),
    ])
