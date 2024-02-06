from aiogram.types.inline_keyboard import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from aiogram.types.reply_keyboard import (
    ReplyKeyboardMarkup,
    KeyboardButton
)

from database.tools import DBTools


def generate_cart_menu(cart_id: int, chat_id: int):
    markup = InlineKeyboardMarkup(row_width=2)
    user_id = DBTools().user_tools.get_user_id(chat_id)
    product_name = DBTools().cart_tools.get_cart_product(user_id)

    for name in product_name:
        product_id = DBTools().cart_tools.get_cart_product_id(name)
        name = str(*name)
        markup.add(
            InlineKeyboardButton(text='❌    ' + name, callback_data=f"delete_{product_id}")
        )

    markup.row(
        InlineKeyboardButton(text="Оформить заказ", callback_data=f"create-order_{cart_id}")
    )
    return markup


def generate_cart_menu_reply_markup(chat_id):
    markup = ReplyKeyboardMarkup(row_width=2)
    user_id = DBTools().user_tools.get_user_id(chat_id)
    product_names = DBTools().cart_tools.get_cart_product(user_id)

    for name in product_names:
        name = str(*name)
        markup.add(
            KeyboardButton(text='❌    ' + name)
        )

    markup.row(
        KeyboardButton(text="🔄   Очистить корзину"),
        KeyboardButton(text="◀   Назад")
    )

    markup.row(
        KeyboardButton(text="🚖   Оформить заказ")
    )
    return markup
