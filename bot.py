import os
import asyncio
import logging
import django
from dotenv import load_dotenv

load_dotenv()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

# Setup Django
django.setup()

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from tg_bot.handlers.handlers import start_router

TOKEN = os.getenv("BOT_TOKEN")


async def main() -> None:
    # Dispatcher is a root router
    dp = Dispatcher()
    dp.include_routers(
        start_router,
    )

    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
