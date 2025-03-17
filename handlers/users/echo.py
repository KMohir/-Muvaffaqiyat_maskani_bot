from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from db import db
from loader import dp
from keyboards.default.reply import get_lang_for_button, change_lang
from states.state import answer, language
from translation import _
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandHelp, Command
from aiogram.types import ReplyKeyboardRemove
import pandas as pd
from db import db
from loader import dp
from states.state import RegistrationStates
from translation import _
import os

@dp.message_handler(text="/change_language")
@dp.message_handler(text="Tilni o'zgartirish")
@dp.message_handler(text="Смена языка")
async def bot_echo(message: types.Message):
    lang=db.get_lang(message.from_user.id)
    await message.answer(_('Tilni tanlang',lang),reply_markup=change_lang())
    await language.lang.set()
@dp.message_handler(state=language.lang)
async def bot_echo(message: types.Message,state: FSMContext):
    if message.text == "O'zbek tili":
        db.change_lang(message.from_user.id, 'uz')
        await message.answer("Til o'zgartirildi",reply_markup=get_lang_for_button(message))
        await state.finish()
    elif message.text == "Русский язык":
        db.change_lang(message.from_user.id, 'ru')
        await message.answer("Язык был обновлен",reply_markup=get_lang_for_button(message))
        await state.finish()
    else:
        await state.finish()

# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    try:
        lang=db.get_lang(message.from_user.id)
        await message.answer(_('Iltimos operator javobini kuting!',lang))
    except Exception as e:
        await message.answer('Iltimos operator javobini kuting!')

# Эхо хендлер, куда летят ВСЕ сообщения с указанным состоянием
@dp.message_handler(state="*", content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    lang=db.get_lang(message.from_user.id)
    state = await state.get_state()
    try:
        lang=db.get_lang(message.from_user.id)
        await message.answer(_('Pastdagi tugmani bosing',lang))
    except Exception as e:

        await message.answer(_('Tugmani bosing',lang))
    # await message.answer(f"Эхо в состоянии <code>{state}</code>.\n"
    #                      f"\nСодержание сообщения:\n"
    #                      f"<code>{message}</code>")
IMAGE_PATH = 'contact1.jpg'

