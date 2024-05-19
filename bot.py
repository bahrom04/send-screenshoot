import os
import asyncio
import logging
import django
from dotenv import load_dotenv


load_dotenv()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from tg_bot.config import main



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
