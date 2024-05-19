import os

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from dotenv import load_dotenv

from tg_bot.handlers.handlers import start_router


load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

dp.include_routers(start_router)
