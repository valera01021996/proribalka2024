from config import bot, dp
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ContentType
from aiogram.dispatcher import FSMContext
from keyboards.order_keyboards import generate_request_contact_menu
from keyboards.main_menu_keyboards import *

class StartForm(StatesGroup):
    phone = State()


@dp.message_handler(Text(equals="💳   Накопитель"))
async def show_bonus(message: Message):
    chat_id = message.chat.id
    if DBTools().user_tools.get_phone_number(chat_id):

        phone_number = DBTools().drive_tools.select_phone_number_of_user(chat_id)
        try:
            bonus = int(DBTools().drive_tools.select_bonus_of_user(phone_number))
            formatted_bonus = f"{bonus:,}".replace(",", " ")
            await bot.send_message(chat_id, f"У вас накопилось : {formatted_bonus} баллов \nНапоминаем: 1 балл = 1 сум")
        except Exception as ex:
            print(ex)
            await bot.send_message(chat_id, "Нет бонусов по вашему номеру телефона.")

    else:
        await bot.send_message(chat_id, "Отправьте свой контакт", reply_markup=generate_request_contact_menu())
        await StartForm.phone.set()


@dp.message_handler(state=StartForm.phone, content_types=ContentType().CONTACT)
async def show_bonus(message: Message, state: FSMContext):
    chat_id = message.chat.id
    phone_number = message.contact.phone_number
    if phone_number[0] != "+":
        phone_number = "+" + phone_number
    print(phone_number)
    await register_phone_number(phone_number, chat_id)
    await state.finish()
    try:
        bonus = int(DBTools().drive_tools.select_bonus_of_user(phone_number))
        formatted_bonus = f"{bonus:,}".replace(",", " ")

        await bot.send_message(chat_id, f"У вас накопилось : {formatted_bonus} баллов \nНапоминаем: 1 балл = 1 сум",
                               reply_markup=generate_main_menu())
    except Exception as ex:
        print(ex)
        await bot.send_message(chat_id, "Нет бонусов по вашему номеру телефона.", reply_markup=generate_main_menu())


async def register_phone_number(phone_number, chat_id):
    DBTools().user_tools.save_phone_number(phone_number, chat_id)
