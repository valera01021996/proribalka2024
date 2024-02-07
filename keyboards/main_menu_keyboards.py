from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from database.tools import DBTools
from aiogram.dispatcher.filters.state import State, StatesGroup


class MenuLevels(StatesGroup):
    categories_menu = State()
    subcategories_menu = State()
    brands_menu = State()
    series_menu = State()
    products_menu = State()
    types_menu = State()
    types_menu2 = State()


def generate_main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(
        KeyboardButton(text="✅   Начать заказ")
    )
    markup.row(
        KeyboardButton(text="🛒   Корзина"),
        KeyboardButton(text="💳   Накопитель")
    )
    markup.row(
        KeyboardButton(text="✍   Оставить отзыв")
    )
    return markup


async def generate_categories_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    categories = DBTools().product_tools.get_categories()
    markup.add(*categories)
    markup.row(
        KeyboardButton(text="◀   Назад"),
        KeyboardButton(text="🏘   Главное меню")
    )
    await MenuLevels.categories_menu.set()
    return markup


async def generate_subcategories_menu(category_name: str):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    subcategories = DBTools().product_tools.get_subcategories(category_name)
    markup.add(*subcategories)
    markup.row(
        KeyboardButton(text="◀   Назад"),
        KeyboardButton(text="🏘   Главное меню")
    )
    await MenuLevels.subcategories_menu.set()
    return markup


async def generate_brands_menu(subcategory_name: str):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    brands = DBTools().product_tools.get_brands(subcategory_name)
    markup.add(*brands)
    markup.row(
        KeyboardButton(text="◀   Назад"),
        KeyboardButton(text="🏘   Главное меню")
    )
    await MenuLevels.brands_menu.set()
    return markup


async def generate_brands_menu_without_subcategories(category_name: str):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    brands = DBTools().product_tools.get_brands_without_subcategories(category_name)
    markup.add(*brands)
    markup.row(
        KeyboardButton(text="◀   Назад"),
        KeyboardButton(text="🏘   Главное меню")
    )
    await MenuLevels.brands_menu.set()
    return markup


async def generate_series_menu_without_subcategories(category_name: str, brand_name: str):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    series = DBTools().product_tools.get_series_without_subcategory(category_name, brand_name)
    markup.add(*series)
    markup.row(
        KeyboardButton(text="◀   Назад"),
        KeyboardButton(text="🏘   Главное меню")
    )
    await MenuLevels.series_menu.set()
    return markup


async def generate_series_menu(subcategory_name: str, brand_name: str):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    series = DBTools().product_tools.get_series(subcategory_name, brand_name)
    markup.add(*series)
    markup.row(
        KeyboardButton(text="◀   Назад"),
        KeyboardButton(text="🏘   Главное меню")
    )
    await MenuLevels.series_menu.set()
    return markup


async def generate_types_menu(category_name: str, brand_name: str, serie_name: str):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    types = DBTools().product_tools.get_types(category_name, brand_name, serie_name)
    markup.add(*types)
    markup.row(
        KeyboardButton(text="◀   Назад"),
        KeyboardButton(text="🏘   Главное меню")
    )
    await MenuLevels.types_menu.set()
    return markup


async def generate_types2_menu(serie_name: str, type_name: str):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    types2 = DBTools().product_tools.get_types2(serie_name, type_name)
    markup.add(*types2)
    markup.row(
        KeyboardButton(text="◀   Назад"),
        KeyboardButton(text="🏘   Главное меню")
    )
    await MenuLevels.types_menu2.set()
    return markup


async def generate_products_menu(category_name: str):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    products = DBTools().product_tools.get_products(category_name)
    markup.add(*products)
    markup.row(
        KeyboardButton(text="◀   Назад"),
        KeyboardButton(text="🏘   Главное меню")
    )
    await MenuLevels.products_menu.set()
    return markup


async def generate_products_menu_with_subcategories(category_name: str, subcategory_name: str):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    products = DBTools().product_tools.get_products_with_subcategories(category_name, subcategory_name)
    markup.add(*products)
    markup.row(
        KeyboardButton(text="◀   Назад"),
        KeyboardButton(text="🏘   Главное меню")
    )
    await MenuLevels.products_menu.set()
    return markup


async def generate_products_menu_without_subcategories(category_name: str, brand_name: str):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    products = DBTools().product_tools.get_products_without_subcategories(category_name, brand_name)
    markup.add(*products)
    markup.row(
        KeyboardButton(text="◀   Назад"),
        KeyboardButton(text="🏘   Главное меню")
    )
    await MenuLevels.products_menu.set()
    return markup


async def generate_products_menu_with_brands(subcategory_name: str, brand_name: str):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    products = DBTools().product_tools.get_products_with_brands(subcategory_name, brand_name)
    markup.add(*products)
    markup.row(
        KeyboardButton(text="◀   Назад"),
        KeyboardButton(text="🏘   Главное меню")
    )
    await MenuLevels.products_menu.set()
    return markup


async def generate_products_menu_with_series(brand_name: str, serie_name: str):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    products = DBTools().product_tools.get_products_with_series(brand_name, serie_name)
    markup.add(*products)
    markup.row(
        KeyboardButton(text="◀   Назад"),
        KeyboardButton(text="🏘   Главное меню")
    )
    await MenuLevels.products_menu.set()
    return markup


async def generate_products_menu_with_types(serie_name: str, type_name: str):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    products = DBTools().product_tools.get_products_with_types(serie_name, type_name)
    markup.add(*products)
    markup.row(
        KeyboardButton(text="◀   Назад"),
        KeyboardButton(text="🏘   Главное меню")
    )
    await MenuLevels.products_menu.set()
    return markup


async def generate_products_menu_with_types2(type_name: str, type_name2: str):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    products = DBTools().product_tools.get_products_with_types2(type_name, type_name2)
    markup.add(*products)
    markup.row(
        KeyboardButton(text="◀   Назад"),
        KeyboardButton(text="🏘   Главное меню")
    )
    await MenuLevels.products_menu.set()
    return markup


async def generate_detail_product_menu(product_id: int, units_in_store: int,
                                       current_qty: int = 0) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(text="-", callback_data=f"action_minus_{product_id}_{current_qty}_{units_in_store}"),
        InlineKeyboardButton(text=str(current_qty),
                             callback_data=f"action_current_{product_id}_{current_qty}_{units_in_store}"),
        InlineKeyboardButton(text="+", callback_data=f"action_plus_{product_id}_{current_qty}_{units_in_store}")
    )
    markup.row(
        InlineKeyboardButton(text="🚀   Добавить в корзину", callback_data=f"add-cart_{product_id}_{current_qty}")
    )
    await MenuLevels.products_menu.set()
    return markup
