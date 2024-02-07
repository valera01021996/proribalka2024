from config import bot, dp, ADMINS
from aiogram.types import Message, ContentType
from aiogram.dispatcher.filters import Text
from database.tools import DBTools
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from keyboards.order_keyboards import *
from keyboards.main_menu_keyboards import generate_main_menu
from find_address import get_address_via_coords


class OrderForm(StatesGroup):
    cart_id = State()
    location = State()
    phone_number = State()
    confirm = State()


@dp.message_handler(Text(equals="🚖   Оформить заказ"))
async def create_order(message: Message):
    print("WORKING !")
    chat_id = message.chat.id
    user_id = DBTools().user_tools.get_user_id(chat_id)
    cart_id = DBTools().cart_tools.get_active_cart(user_id)[0]
    print(cart_id)
    await bot.send_message(chat_id, "Чтобы оформить заказ, вам нужно \n"
                                    "Заполнить: \n\n"
                                    "- Локация\n"
                                    "- Номер телефона\n", reply_markup=generate_request_location_menu())
    await OrderForm.location.set()


@dp.message_handler(state=OrderForm.location, content_types=ContentType().LOCATION)
async def check_location(message: Message, state: FSMContext):
    chat_id = message.chat.id
    async with state.proxy() as data:
        data["location"] = {
            "latitude": message.location.latitude,
            "longitude": message.location.longitude
        }
        print(type(data["location"]))
        await bot.send_message(chat_id, "Отправьте свой номер телефона", reply_markup=generate_request_contact_menu())
        await OrderForm.phone_number.set()


@dp.message_handler(state=OrderForm.phone_number, content_types=ContentType().CONTACT)
async def check_phone_number(message: Message, state: FSMContext):
    data = await state.get_data()
    chat_id = message.chat.id
    user_id = DBTools().user_tools.get_user_id(chat_id)
    cart_id = DBTools().cart_tools.get_active_cart(user_id)[0]
    phone_number = message.contact.phone_number
    await state.update_data(phone_number=phone_number)
    confirm_text = await formatted_message_for_confirm(data, cart_id, user_id, phone_number)
    await OrderForm.confirm.set()
    await bot.send_message(chat_id, confirm_text, reply_markup=generate_confirm_menu())


@dp.message_handler(state=OrderForm.confirm)
async def success_confirm(message: Message, state: FSMContext):
    data = await state.get_data()
    chat_id = message.chat.id
    full_name = message.chat.full_name
    user_id = DBTools().user_tools.get_user_id(chat_id)
    cart_products = DBTools().cart_tools.get_cart_products(user_id)
    cart_id = DBTools().cart_tools.get_active_cart(user_id)[0]
    print(cart_products)
    if message.text == "Да":
        await state.finish()
        text_admins = await formatted_message_for_admins(data, full_name, cart_products)
        await bot.send_message(chat_id, "Ваш заказ принят😊 Ожидайте звонка", reply_markup=generate_main_menu())
        for admin_id in ADMINS:
            await bot.send_message(admin_id, text_admins)
        DBTools().order_tools.create_order(cart_id)
        DBTools().cart_tools.change_order_status(cart_id)
        DBTools().cart_tools.register_cart(user_id)
        await minus_count(cart_products)
        DBTools().product_tools.delete_product()
    else:
        await message.answer("Заказ отменен !", reply_markup=generate_main_menu())
        await state.finish()


@dp.message_handler(state=OrderForm.location)
async def check_location(message: Message, state:FSMContext):
    chat_id = message.chat.id
    if message.text == "Отменить":
        await state.finish()
        await bot.send_message(chat_id, "Главное меню", reply_markup=generate_main_menu())

@dp.message_handler(state=OrderForm.phone_number)
async def check_location(message: Message, state:FSMContext):
    chat_id = message.chat.id
    if message.text == "Отменить":
        await state.finish()
        await bot.send_message(chat_id, "Главное меню", reply_markup=generate_main_menu())


async def formatted_message_for_confirm(data, cart_id, user_id, phone_number):
    address = await get_address(data)
    confirm = f"Ваш заказ № {cart_id}\n" \
              f"Ваш адрес: {address}\n" \
              f"Ваш номер телефона: {phone_number}\n\n"
    total = int()
    cart_products = DBTools().cart_tools.get_cart_products(user_id)
    i = 0
    for _, title, quantity, total_coast in cart_products:
        i += 1
        total += total_coast
        confirm += f"    {i}.{title}\n" \
                   f"      Количество: {quantity} шт.\n" \
                   f"      Стоимость: {total_coast} сум. \n\n"
    last_message = confirm + "Итого: " + str(total) + "сум"
    return last_message


async def get_address(data):
    longitude = str(data['location']['longitude'])
    latitude = str(data['location']['latitude'])
    coords = longitude + ',' + latitude
    address = await get_address_via_coords(coords)
    return address


async def formatted_message_for_admins(data, full_name: str, cart_products: list):
    address = await get_address(data)
    text = f"Новый заказ !\n" \
           f"От пользователя: {full_name}\n" \
           f"Адрес: {address}\n\n" \
           f"Номер телефона: {data['phone_number']}\n\n"
    i = 0
    total = int()
    for _, title, quantity, total_coast in cart_products:
        i += 1
        total += total_coast
        text += f"    {i}.{title}\n" \
                f"      Количество: {quantity} шт.\n" \
                f"      Стоимость: {total_coast} сум. \n\n"
    last_message = text + "Итого: " + str(total) + "сум"
    return last_message


async def minus_count(cart_products):
    for tpl in cart_products:
        _, title, count, _ = tpl
        DBTools().product_tools.minus_count_units_in_store(count, title)
