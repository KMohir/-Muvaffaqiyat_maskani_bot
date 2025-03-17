from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from db import db
from translation import _


def get_lang_for_button(message):
    lang = db.get_lang(message.from_user.id)
    button=ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_("Takliflarni yuborish",lang)
    )
            ],
            [
                KeyboardButton(text=_("Tilni o'zgartirish",lang))
            ],
            [
                KeyboardButton(text=_("Centris Towers bilan bog'lanish", lang))
            ],
            [
                KeyboardButton(text=_("Centris Towers haqida bilish", lang))
            ],

        ],
        resize_keyboard=True
    )
    return button
# def get_project_for_user(message):
#     lang = db.get_lang(message.from_user.id)
#     button=ReplyKeyboardMarkup(
#         keyboard=[
#             [
#                 KeyboardButton(text=_("Centris Towers",lang)
#     )
#             ],
#             [
#                 KeyboardButton(text=_("2 chi proyekt",lang))
#             ],
#             [
#                 KeyboardButton(text=_("3 chi proyekt",lang)
#     )
#             ],
#             [
#                 KeyboardButton(text=_("4 chi proyekt",lang))
#             ],
#
#         ],
#         resize_keyboard=True
#     )
#     return button


def change_lang():

    button=ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Русский язык")

            ],
            [
                KeyboardButton(text="O'zbek tili")
            ],

        ],
        resize_keyboard=True
    )
    return button
def changelang():

    button=ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Tilni o'zgartirish")

            ],

        ],
        resize_keyboard=True
    )
    return button
def key(lang):
    if lang=='uz':
        keyboardcontakt=ReplyKeyboardMarkup(

            keyboard=[[

                KeyboardButton(text="Kontakni yuborish",
                               request_contact=True

                               )
                ],

            ],resize_keyboard=True

        )
    elif lang=='ru':
        keyboardcontakt=ReplyKeyboardMarkup(

            keyboard=[[

                KeyboardButton(text="Отправить контакт",
                               request_contact=True

                               )
                ],

            ],resize_keyboard=True

        )
    return keyboardcontakt