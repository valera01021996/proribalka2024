from dotenv import load_dotenv
import os
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

load_dotenv()

ADMINS = [
    -1001998831051,
    43031788,
    # 778133858,
    # 5112368258
    # -801039371
]

ADMINISTRATORS = [
    # 43031788,
    778133858,
    5112368258
]

bot = Bot(os.getenv("BOT_TOKEN"))
storage = RedisStorage2('10.10.10.149', 6379, db=5, password="Insider29")
dp = Dispatcher(bot, storage=storage)
