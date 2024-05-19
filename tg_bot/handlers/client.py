from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from tg_bot.keyboards.client import main_menu, go_back
from tg_bot.keyboards import static
from users.models import User

start_router = Router()


@start_router.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    print("------------------------")
    print(message.from_user)
    print("------------------------")
    u = User.get_user_and_created(message)
    
    await message.answer(text=static.main_menu_title, reply_markup=await main_menu())


@start_router.callback_query()
async def main_callback_query(callback_query: CallbackQuery):
    """
    This handler receives callback queries from inline keyboards
    """
    callback_data = callback_query.data  # Get the callback data

    if callback_data == "about_me":
        await callback_query.message.edit_text(
            text=static.about_me_title, reply_markup=await go_back()
        )
    elif callback_data == "admin":
        await callback_query.message.edit_text(
            text=static.admin_contact, reply_markup=await go_back()
        )
    elif callback_data == "go_back":
        await callback_query.message.answer(
            text=static.main_menu_title, reply_markup=await main_menu()
        )

    # Acknowledge the callback query to remove the loading spinner
    await callback_query.answer()
