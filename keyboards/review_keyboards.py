from aiogram.types.reply_keyboard import (
    ReplyKeyboardMarkup,
    KeyboardButton
)


def generate_cancel():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(
        KeyboardButton(text="Отменить")
    )
    return markup
