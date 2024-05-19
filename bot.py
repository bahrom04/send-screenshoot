import os
import asyncio
import logging
import django
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

# Setup Django
django.setup()

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from tg_bot.handlers.echo import echo_router
from tg_bot.handlers.client import start_router

# Get the bot token from environment variables
TOKEN = os.getenv("BOT_TOKEN")

async def main() -> None:
    # Dispatcher is a root router
    dp = Dispatcher()
    # Register all the routers from handlers package
    dp.include_routers(
        start_router,
        echo_router,
    )

    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
