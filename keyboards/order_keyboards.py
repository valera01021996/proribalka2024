from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def generate_request_contact_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(
        KeyboardButton(text="📞   Отправить контакт", request_contact=True)
    )
    markup.row(KeyboardButton(text="Отменить"))
    return markup


def generate_request_location_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(
        KeyboardButton(text="🗺   Отправить локацию", request_location=True)
    )
    markup.row(KeyboardButton(text="Отменить"))
    return markup


def generate_confirm_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.row(
        KeyboardButton(text="Да")
    )
    markup.row(
        KeyboardButton(text="Отменить заказ")
    )
    return markup
