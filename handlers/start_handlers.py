from config import bot, dp
from aiogram.types import Message, ContentType
from database.tools import DBTools
from keyboards.order_keyboards import generate_request_contact_menu
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from keyboards.main_menu_keyboards import *

class StartForm(StatesGroup):
    phone = State()


@dp.message_handler(state="*", commands=["start"])
async def start(message: Message, state: FSMContext):
    chat_id = message.chat.id
    username = message.from_user.username
    full_name = message.chat.full_name
    await state.finish()
    await register_user(username, full_name, chat_id)
    print("salam")
    await register_cart(chat_id)
    await bot.send_message(chat_id, f"Привет, {full_name}!\n\n"
                                    f"Добро пожаловать в магазин PROрыбалка!!!\n\n"
                                    f"Наш бот работает только на доставку 🚖.", reply_markup=generate_main_menu())



async def register_user(username: str, full_name: str, chat_id: int):
    DBTools().user_tools.register_user(username, full_name, chat_id)


async def register_cart(chat_id: int):
    user_id = DBTools().user_tools.get_user_id(chat_id)
    DBTools().cart_tools.register_cart(user_id)
