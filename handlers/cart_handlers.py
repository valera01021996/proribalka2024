from config import bot, dp
from aiogram.types import CallbackQuery, Message
from database.tools import DBTools
from keyboards.main_menu_keyboards import *
from keyboards.cart_keyboards import *
from aiogram.dispatcher.filters import Text
from .main_menu_handlers import format_price

@dp.callback_query_handler(
    lambda call: call.data.startswith("add-cart"), state=MenuLevels.products_menu
)
async def add_cart_product(call: CallbackQuery):
    chat_id = call.message.chat.id
    _, product_id, current_qty = call.data.split("_")
    current_qty = int(current_qty)
    product_name = DBTools().product_tools.get_product_name_by_id(product_id)
    pk, title, description, _, price, quantity = DBTools().product_tools.get_product_detail_info(product_name)
    price = int(price)
    user_id = DBTools().user_tools.get_user_id(chat_id)
    cart_id = DBTools().cart_tools.get_active_cart(user_id)[0]
    if current_qty != 0:
        status_add = DBTools().cart_tools.add_cart_product(cart_id, pk, product_name, current_qty, current_qty * price)
        print(status_add)
        if status_add == True:
            await bot.answer_callback_query(call.id, "Продукт успешно добавлен !")
        else:
            await bot.answer_callback_query(call.id, "Кол-во продукта изменено !")

    else:
        await bot.answer_callback_query(call.id, "Добавьте количество товара !")


@dp.message_handler(Text(equals="🛒   Корзина"))
async def show_cart(message: Message):
    chat_id = message.chat.id
    user_id = DBTools().user_tools.get_user_id(chat_id)
    cart_products = DBTools().cart_tools.get_cart_products(user_id)
    if not cart_products:
        await bot.send_message(chat_id, "Ваша корзина пуста", reply_markup=generate_main_menu())

    else:
        cart_text = "<b>Ваша корзина:</b> \n\n"
        total = int()

        i = 0
        for product_id, product_name, quantity, total_coast in cart_products:
            i += 1
            total += total_coast
            cart_text += f"{i}. <b>{product_name}</b>\n" \
                         f"    <i>Общее кол-во: {quantity} шт</i>\n" \
                         f"    <i>Общая стоимость: {total_coast} сум</i>\n\n"
        last_message = cart_text + "Итого: " + str(total) + " сум"
        await bot.send_message(chat_id, "*«❌ Наименование »* - удалить одну позицию\n"
                                        "*«🔄 Очистить »* - полная очистка корзины")
        await bot.send_message(chat_id, last_message, parse_mode="HTML", reply_markup=generate_cart_menu_reply_markup(chat_id))




@dp.message_handler(lambda message: message.text.startswith("❌"))
async def delete_product_from_cart(message: Message):
    chat_id = message.chat.id
    user_id = DBTools().user_tools.get_user_id(chat_id)
    cart_id = DBTools().cart_tools.get_active_cart(user_id)[0]
    product_name = message.text[5:]
    DBTools().cart_tools.delete_product_from_cart(product_name, cart_id)
    cart_products = DBTools().cart_tools.get_cart_products(user_id)
    cart_text = "<b>Ваша корзина:</b> \n\n"
    total = int()
    i = 0
    for product_id, product_name, quantity, total_coast in cart_products:
        i += 1
        total += total_coast
        cart_text += f"{i}. <b>{product_name}</b>\n" \
                     f"    <i>Общее кол-во: {quantity} шт</i>\n" \
                     f"    <i>Общая стоимость: {total_coast} сум</i>\n\n"
    last_message = cart_text + "Итого: " + str(total) + " сум"
    if cart_products:
        await bot.send_message(chat_id, last_message, parse_mode="HTML", reply_markup=generate_cart_menu_reply_markup(chat_id))
    else:
        await bot.send_message(chat_id, "Главное меню", reply_markup=generate_main_menu())



@dp.message_handler(Text(equals="🔄   Очистить корзину"))
async def clear_cart(message: Message):
    chat_id = message.chat.id
    user_id = DBTools().user_tools.get_user_id(chat_id)
    cart_id = DBTools().cart_tools.get_active_cart(user_id)[0]
    DBTools().cart_tools.delete_all_products_from_cart(cart_id)
    await bot.send_message(chat_id, "Ваша корзина очищена", reply_markup=generate_main_menu())

@dp.message_handler(Text(equals="◀   Назад"))
async def back_to_main_menu(message: Message):
    chat_id = message.chat.id
    await bot.send_message(chat_id, "Главное меню", reply_markup=generate_main_menu())



@dp.callback_query_handler(
    lambda call: call.data.startswith("add-cart"), state=MenuLevels.bu_products_menu
)
async def add_cart_product(call: CallbackQuery):
    chat_id = call.message.chat.id
    _, product_id, current_qty = call.data.split("_")
    current_qty = int(current_qty)
    product_name = DBTools().product_tools_bu.get_bu_product_name_by_id(product_id)
    pk, title, description, _, price, quantity = DBTools().product_tools_bu.get_bu_product_detail_info(product_name)
    price = int(price)
    user_id = DBTools().user_tools.get_user_id(chat_id)
    cart_id = DBTools().cart_tools.get_active_cart(user_id)[0]
    if current_qty != 0:
        status_add = DBTools().cart_tools.add_cart_product(cart_id, pk, product_name, current_qty, current_qty * price)
        print(status_add)
        if status_add == True:
            await bot.answer_callback_query(call.id, "Продукт успешно добавлен !")
        else:
            await bot.answer_callback_query(call.id, "Кол-во продукта изменено !")

    else:
        await bot.answer_callback_query(call.id, "Добавьте количество товара !")
