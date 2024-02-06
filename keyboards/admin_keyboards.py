from aiogram.types.reply_keyboard import (
    ReplyKeyboardMarkup,
    KeyboardButton
)

from database.tools import DBTools



def generate_admin_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.row(
        KeyboardButton(text="Рассылка")
    )
    markup.row(
        KeyboardButton(text="Выйти с админки")
    )
    return markup

def generate_admin_confirm():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.row(
        KeyboardButton(text="Да"),
        KeyboardButton(text="Нет")
    )
    return markup
