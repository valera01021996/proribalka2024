from config import bot, dp
from aiogram.dispatcher.filters import Text
from aiogram.types import Message
from database.tools import DBTools


@dp.message_handler(Text(equals="💳   Накопитель"))
async def show_bonus(message: Message):
    chat_id = message.chat.id
    phone_number = DBTools().drive_tools.select_phone_number_of_user(chat_id)
    try:
        bonus = DBTools().drive_tools.select_bonus_of_user(phone_number)
        await bot.send_message(chat_id, f"У вас накопилось : {bonus}")
    except Exception as ex:
        print(ex)
        await bot.send_message(chat_id, "Нет бонусов по вашему номеру телефона.")
