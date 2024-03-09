from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from config import bot, dp
from aiogram.types import Message, MediaGroup, InputMediaPhoto, InputFile, ContentType
from database.tools import DBTools
from keyboards.admin_keyboards import *
from keyboards.main_menu_keyboards import generate_main_menu
from aiogram.dispatcher.filters import Text
from aiogram import types
from config import ADMINISTRATORS


class Form(StatesGroup):
    waiting_for_text = State()
    waiting_for_photos = State()


media = MediaGroup()


@dp.message_handler(commands=["proribalka"])
async def admin_panel(message: Message):
    chat_id = message.chat.id
    if chat_id not in ADMINISTRATORS:
        return await message.reply("У вас нет доступа !")
    await Form.waiting_for_text.set()
    await message.reply("Введите текст для сообщения:")
    # await bot.send_message(chat_id, "Что будем делать ?", reply_markup=generate_admin_keyboard())

@dp.message_handler(state=Form.waiting_for_text, content_types=types.ContentTypes.TEXT)
async def process_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['common_text'] = message.text
    await Form.waiting_for_photos.set()
    await message.reply("Теперь отправьте фотографии. Когда закончите, напишите или нажмите /done.")




@dp.message_handler(state=Form.waiting_for_photos, content_types=types.ContentTypes.PHOTO)
async def process_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'photos' not in data:
            data['photos'] = []
        data['photos'].append(message.photo[-1].file_id)
    await message.reply("Фотография добавлена. Добавьте еще или напишите /done.")



@dp.message_handler(state=Form.waiting_for_photos, commands='done')
async def process_done(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        common_text = data['common_text']
        photos = data.get('photos', [])
        chat_ids = DBTools().admin_tools.select_all_chat_ids()

    if not photos:
        await message.reply("Фотографии не были отправлены.")
    elif len(photos) == 1:
        for chat_id in chat_ids:
            await bot.send_photo(chat_id[0], photo=photos[0], caption=common_text)
    else:
        media = types.MediaGroup()
        media.attach_photo(photos[0], caption=common_text)
        for photo_id in photos[1:]:
            media.attach_photo(photo_id)
        for chat_id in chat_ids:
            await bot.send_media_group(chat_id[0], media=media)

    await state.finish()
