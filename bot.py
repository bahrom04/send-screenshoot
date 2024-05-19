import asyncio
import logging
from dotenv import load_dotenv
from os import getenv

from tg_bot.handlers.echo import echo_router
from tg_bot.handlers.client import start_router

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

load_dotenv()
# Bot token can be obtained via https://t.me/BotFather
TOKEN = getenv("BOT_TOKEN")


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