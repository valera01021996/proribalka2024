from config import bot, dp
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from keyboards.main_menu_keyboards import *
from database.tools.product_tools import ProductTools


# @dp.message_handler(state="*", commands=["start"])
# async def show_main_menu(message: Message, state: FSMContext):
#     chat_id = message.chat.id
#     current_state = await state.get_state()
#     if current_state is None:
#         return
#     await state.finish()
#     await bot.send_message(chat_id, "Добро пожаловать в магазин \"PROрыбалка\" !", reply_markup=generate_main_menu())


@dp.message_handler(Text(equals="🏘   Главное меню"), state="*")
async def show_main_menu(message: Message, state: FSMContext):
    chat_id = message.chat.id
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await bot.send_message(chat_id, "Главное меню", reply_markup=generate_main_menu())


@dp.message_handler(Text(equals="✅   Начать заказ"))
async def show_categories_menu(message: Message):
    chat_id = message.chat.id
    await bot.send_message(chat_id, "Выберите категорию товара: ", reply_markup=await generate_categories_menu())


@dp.message_handler(state=MenuLevels.categories_menu)
async def show_subcategories_menu(message: Message, state: FSMContext):
    chat_id = message.chat.id
    await state.update_data(category_name=message.text)
    if message.text == "◀   Назад":
        await state.finish()
        await bot.send_message(chat_id, "Главное меню", reply_markup=generate_main_menu())

    elif message.text in ("Катушки", "Коптилки", "Пули", "Садки и Подсаки", "Сушилка для Рыбы"):
        await bot.send_message(chat_id, "Выберите бренд товара",
                               reply_markup=await generate_brands_menu_without_subcategories(message.text))

    elif message.text in ("Креветочницы", "Подарочные Сертификаты PROрыбалка", "Рогатки"):
        await bot.send_message(chat_id, "Выберите товар", reply_markup=await generate_products_menu(message.text))

    elif message.text in ProductTools.CATEGORIES:
        await state.reset_state(with_data=False)
        await bot.send_message(chat_id, "Прошу выберите категорию товара",
                               reply_markup=await generate_subcategories_menu(message.text))


@dp.message_handler(state=MenuLevels.subcategories_menu)
async def show_brands_menu(message: Message, state: FSMContext):
    chat_id = message.chat.id
    data = await state.get_data()
    await state.update_data(subcategory_name=message.text)
    category_name = data["category_name"]
    subcategory_name = message.text
    if message.text == "◀   Назад":
        await state.reset_state(with_data=False)
        await bot.send_message(chat_id, "Выберите категорию товара", reply_markup=await generate_categories_menu())

    elif message.text in ProductTools.SUBCATEGORIES and DBTools().product_tools.get_brands(subcategory_name) == ['']:
        await bot.send_message(chat_id, "Выберите товар",
                               reply_markup=await generate_products_menu_with_subcategories(category_name,
                                                                                            subcategory_name))

    elif message.text in ProductTools.SUBCATEGORIES:
        print("Работает !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!11")
        await bot.send_message(chat_id, "Выберите бренд", reply_markup=await generate_brands_menu(message.text))


@dp.message_handler(state=MenuLevels.brands_menu)
async def show_series_menu(message: Message, state: FSMContext):
    chat_id = message.chat.id
    await state.update_data(brand_name=message.text)
    data = await state.get_data()
    category_name = data["category_name"]
    subcategory_name = ""
    try:
        subcategory_name = data["subcategory_name"]
    except Exception as ex:
        print(f"Выбран товар без подкатегории: {ex}")
    brand_name = message.text
    print(message.text)
    if message.text == "◀   Назад":
        if category_name in ("Катушки", "Коптилки", "Пули", "Садки и Подсаки", "Сушилка для Рыбы"):
            await bot.send_message(chat_id, "Выберите категорию товара", reply_markup=await generate_categories_menu())
        else:
            await bot.send_message(chat_id, "Выберите подкатегорию товара",
                                   reply_markup=await generate_subcategories_menu(category_name))
    elif message.text in ProductTools.BRANDS and DBTools().product_tools.get_series_without_subcategory(category_name,
                                                                                                        brand_name) == [
        ''] and category_name in ("Катушки", "Коптилки", "Пули", "Садки и Подсаки", "Сушилка для Рыбы"):
        await bot.send_message(chat_id, "Выберите товар",
                               reply_markup=await generate_products_menu_without_subcategories(category_name,
                                                                                               brand_name))


    elif message.text in ProductTools.BRANDS and DBTools().product_tools.get_series(subcategory_name, brand_name) == [
        '']:
        await bot.send_message(chat_id, "Выберите товар",
                               reply_markup=await generate_products_menu_with_brands(subcategory_name, brand_name))


    elif message.text in ProductTools.BRANDS and category_name in (
            "Катушки", "Коптилки", "Пули", "Садки и Подсаки", "Сушилка для Рыбы"):
        await bot.send_message(chat_id, "Выберите серию товара",
                               reply_markup=await generate_series_menu_without_subcategories(category_name, brand_name))

    else:
        await bot.send_message(chat_id, "Выберите серию товара",
                               reply_markup=await generate_series_menu(subcategory_name, brand_name))


@dp.message_handler(state=MenuLevels.series_menu)
async def show_products_menu(message: Message, state: FSMContext):
    chat_id = message.chat.id
    data = await state.get_data()
    await state.update_data(serie_name=message.text)
    category_name = data["category_name"]
    subcategory_name = ""
    brand_name = ""
    serie_name = message.text
    try:
        subcategory_name = data["subcategory_name"]
    except Exception as ex:
        print(f"Ошибка {ex}")
    try:
        brand_name = data["brand_name"]
    except Exception as ex:
        print(f"Ошибка {ex}")

    if message.text == "◀   Назад" and category_name in (
            "Катушки", "Коптилки", "Пули", "Садки и Подсаки", "Сушилка для Рыбы"):
        await bot.send_message(chat_id, "Выберите бренд:",
                               reply_markup=await generate_brands_menu_without_subcategories(category_name))
    elif message.text == "◀   Назад":
        await bot.send_message(chat_id, "Выберите бренд:", reply_markup=await generate_brands_menu(subcategory_name))
    elif message.text in ProductTools.SERIES and DBTools().product_tools.get_types(category_name, brand_name,
                                                                                   serie_name) == ['']:
        await bot.send_message(chat_id, "Выберите продукт",
                               reply_markup=await generate_products_menu_with_series(category_name, brand_name,
                                                                                     serie_name))
    elif message.text in ProductTools.SERIES:
        await bot.send_message(chat_id, "Выберите тип товара",
                               reply_markup=await generate_types_menu(category_name, brand_name, serie_name))


@dp.message_handler(state=MenuLevels.types_menu)
async def show_types2_menu(message: Message, state: FSMContext):
    chat_id = message.chat.id
    data = await state.get_data()
    subcategory_name = ""
    await state.update_data(type_name=message.text)
    try:
        subcategory_name = data["subcategory_name"]
    except Exception as ex:
        print(ex)
    brand_name = data["brand_name"]
    serie_name = data["serie_name"]
    type_name = message.text
    await state.update_data(type_name=message.text)

    if message.text == "◀   Назад":
        await bot.send_message(chat_id, "Выберите серию",
                               reply_markup=await generate_series_menu(subcategory_name, brand_name))
    elif message.text in ProductTools.TYPES and DBTools().product_tools.get_types2(serie_name, type_name) == ['']:
        await bot.send_message(chat_id, "Выберите товар",
                               reply_markup=await generate_products_menu_with_types(serie_name, type_name))

    elif message.text in ProductTools.TYPES:
        await bot.send_message(chat_id, "Выберите второй тип",
                               reply_markup=await generate_types2_menu(serie_name, type_name))


@dp.message_handler(state=MenuLevels.types_menu2)
async def show_product_menu_with_types(message: Message, state: FSMContext):
    chat_id = message.chat.id
    await state.update_data(type2_name=message.text)
    data = await state.get_data()
    category_name = data["category_name"]
    brand_name = data["brand_name"]
    serie_name = data["serie_name"]
    type_name = data["type_name"]
    type_name2 = message.text
    if message.text == "◀   Назад":
        await bot.send_message(chat_id, "Выберите тип",
                               reply_markup=await generate_types_menu(category_name, brand_name, serie_name))

    elif message.text in ProductTools.TYPES2:
        await bot.send_message(chat_id, "Выберите товар",
                               reply_markup=await generate_products_menu_with_types2(type_name, type_name2))


@dp.message_handler(state=MenuLevels.products_menu)
async def show_product_detail(message: Message, state: FSMContext):
    data = await state.get_data()
    category_name = data["category_name"]
    subcategory_name = ""
    chat_id = message.chat.id
    brand_name = ""
    serie_name = ""
    type_name = ""
    try:
        subcategory_name = data["subcategory_name"]
    except Exception as ex:
        print(f"Ошибка {ex}")
    try:
        brand_name = data["brand_name"]
    except Exception as ex:
        print(f"Ошибка {ex}")
    try:
        serie_name = data["serie_name"]
    except Exception as ex:
        print(f"Ошибка {ex}")

    try:
        type_name = data["type_name"]
    except Exception as ex:
        print(f"Ошибка {ex}")

    if message.text in ProductTools.PRODUCTS:
        pk, product_name, description, image, price, quantity = DBTools().product_tools.get_product_detail_info(
            message.text)
        try:
            with open(image, "rb") as photo:
                await bot.send_photo(chat_id, photo, caption=f"<b>{product_name}</b>\n\n"
                                                             f"Цена : {price} сум\n\n"
                                                             f"{description}", parse_mode="HTML",
                                     reply_markup=await generate_detail_product_menu(pk, quantity))
        except Exception as ex:
            await bot.send_message(chat_id, f"<b>{product_name}</b>\n\n"
                                            f"Цена : {price} сум\n\n"
                                            f"{description}", parse_mode="HTML",
                                   reply_markup=await generate_detail_product_menu(pk, quantity))



    elif message.text == "◀   Назад" and category_name in (
            "Креветочницы", "Подарочные Сертификаты PROрыбалка", "Рогатки"):
        await bot.send_message(chat_id, "Выберите категорию товара", reply_markup=await generate_categories_menu())




    elif message.text == "◀   Назад" \
            and DBTools().product_tools.get_subcategories(category_name) == [
        ''] and DBTools().product_tools.get_series_without_subcategory(category_name, brand_name) != ['']:
        await bot.send_message(chat_id, "Выберите серию товара",
                               reply_markup=await generate_series_menu_without_subcategories(category_name, brand_name))

    elif message.text == "◀   Назад" and DBTools().product_tools.get_subcategories(category_name) == ['']:
        await bot.send_message(chat_id, "Выберите бренд товара",
                               reply_markup=await generate_brands_menu_without_subcategories(category_name))


    elif message.text == "◀   Назад" and DBTools().product_tools.get_brands(subcategory_name) == ['']:
        await bot.send_message(chat_id, "Выберите категорию товара",
                               reply_markup=await generate_subcategories_menu(category_name))


    elif message.text == "◀   Назад" and DBTools().product_tools.get_series(subcategory_name, brand_name) == ['']:
        await bot.send_message(chat_id, "Выберите бренд товара",
                               reply_markup=await generate_brands_menu(subcategory_name))


    elif message.text == "◀   Назад" and DBTools().product_tools.get_series(category_name,
                                                                            brand_name) != [
        ''] and DBTools().product_tools.get_types(category_name,
                                                  brand_name, serie_name) == ['']:
        await bot.send_message(chat_id, "Выберите серию товара",
                               reply_markup=await generate_series_menu(subcategory_name, brand_name))

    elif message.text == "◀   Назад" and DBTools().product_tools.get_types(category_name, brand_name,
                                                                           serie_name) != [
        ''] and DBTools().product_tools.get_types2(
        serie_name, type_name) == ['']:
        await bot.send_message(chat_id, "Выберите тип товара",
                               reply_markup=await generate_types_menu(category_name, brand_name, serie_name))

    elif message.text == "◀   Назад" and DBTools().product_tools.get_types2(serie_name, type_name) != ['']:
        await bot.send_message(chat_id, "Выберите второй тип",
                               reply_markup=await generate_types2_menu(serie_name, type_name))


@dp.callback_query_handler(
    lambda call: call.data.startswith("action"), state=MenuLevels.products_menu
)
async def edit_count_product(call: CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    _, action, product_id, current_qty, quantity = call.data.split("_")
    current_qty, quantity = int(current_qty), int(quantity)

    if action == "minus" and current_qty > 0:
        current_qty -= 1

    elif action == "minus" and current_qty <= 0:
        await bot.answer_callback_query(call.id, "Недопустимое значение !")
        return

    if action == "current":
        await bot.answer_callback_query(call.id, "Текущее количество")
        return

    if action == "plus" and current_qty < quantity:
        current_qty += 1

    elif action == "plus" and current_qty >= quantity:
        await bot.answer_callback_query(call.id, f"На складе есть : {current_qty}")
        return

    await bot.edit_message_reply_markup(chat_id, message_id, reply_markup=await generate_detail_product_menu(product_id,
                                                                                                             quantity,
                                                                                                             current_qty
                                                                                                             ))
