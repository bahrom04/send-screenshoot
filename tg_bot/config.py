from aiogram import Dispatcher

from tg_bot.handlers.handlers import start_router,bot



dp = Dispatcher()

dp.include_routers(start_router)


async def main() -> None:
    # Dispatcher is a root router
    await dp.start_polling(bot)
