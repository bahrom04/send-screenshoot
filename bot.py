import os
import asyncio
import logging
import django
from dotenv import load_dotenv


load_dotenv()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()


from tg_bot.config import bot, dp

async def main() -> None:
    # Dispatcher is a root router
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
