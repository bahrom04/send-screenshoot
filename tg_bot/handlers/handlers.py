import os
import requests

from asgiref.sync import sync_to_async

from aiogram import Router
from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, FSInputFile, ContentType
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from django.conf import settings

from tg_bot.keyboards.keyboards import (
    main_menu,
    go_back,
    cources,
    payment_button,
    confirm_decline_buttons,
)

from utils import static
from users.models import User, UserPayment

from dotenv import load_dotenv


load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

start_router = Router()


async def download_telegram_file(file_id, destination):
    file_info = await bot.get_file(file_id)
    file_path = file_info.file_path
    file_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"

    response = requests.get(file_url)
    response.raise_for_status()

    # Ensure the destination directory exists
    if not os.path.exists(destination):
        os.makedirs(destination)

    # Construct the full file path
    file_name = os.path.join(destination, os.path.basename(file_path))

    # Save the file
    with open(file_name, "wb") as f:
        f.write(response.content)

    return file_name


# Helper function to show payment details
async def show_payment_details(callback_query: CallbackQuery, plan_title, plan_amount):
    title = static.payment_info(plan=plan_title, amount=plan_amount)
    photo = FSInputFile(path="utils/images/carta.jpg", filename="carta")
    await bot.send_photo(
        chat_id=callback_query.message.chat.id,
        photo=photo,
        caption=title,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Pay",
                        callback_data=f"pay_{plan_title.lower()}_{callback_query.message.chat.id}",
                    )
                ]
            ]
        ),
    )


@start_router.message(Command("profil"))
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/profil` command
    """

    u = await sync_to_async(list)(
        User.objects.filter(user_id=message.chat.id).values("user_id", "username")
    )
    payment = await sync_to_async(list)(
        UserPayment.objects.filter(user=u[0]["user_id"]).values("is_verified")
    )
    payment_status = payment[0]["is_verified"]
    v = lambda payment_status: "Tasdiqlangan" if payment_status==True else "Tasdiqlanmagan"

    title = f"""
    ID: {u[0]["user_id"]}
    username: @{u[0]["username"]}
    
    Tolvol: {v}
    """
    await message.answer(text=title)


@start_router.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """

    u = await User.get_user_and_created(message)

    await message.answer(text=static.main_menu_title, reply_markup=await main_menu())


@start_router.callback_query()
async def main_callback_query(callback_query: CallbackQuery, bot: Bot):
    """
    This handler receives callback queries from inline keyboards
    """
    callback_data = callback_query.data

    if callback_data.startswith("plan_"):
        plan_name = callback_data.split("_")[1]
        plan_title = plan_name.capitalize()
        if plan_title == "Standart":
            await show_payment_details(callback_query, "Standart", "399 000")
        elif plan_title == "Premium":
            await show_payment_details(callback_query, "Premium", "599 000")
        elif plan_title == "Vip":
            await show_payment_details(callback_query, "VIP", "2 499 000")

    elif callback_data.startswith("pay_"):
        plan_name = callback_data.split("_")[1]
        plan_title = plan_name.capitalize()
        await callback_query.message.answer(
            f"Iltimos {plan_title} uchun to'lov chekini jo'nating"
        )
        # Store the selected plan in the user's session
        user = await User.get_user(callback_query.message)
        if await sync_to_async(UserPayment.objects.filter(user=user).exists)():
            pass
        else:
            await sync_to_async(UserPayment.objects.create)(
                user=user,
            )

    elif callback_data.startswith("confirm_"):
        user_id = int(callback_data.split("_")[1])
        # user = await User.get_user(callback_query.message)

        await bot.send_message(
            chat_id="7148758895",
            text="Foydalanuvchiga xabar jonatildi",
        )

        # Update user payment status
        await sync_to_async(UserPayment.objects.filter(user=user_id).update)(
            is_verified=True
        )

        await bot.send_message(
            chat_id=user_id, text="To'lov uchun rahmat. To'lov admin tomonidan tasdiqlandi"
        )

    elif callback_data.startswith("decline_"):
        user_id = int(callback_data.split("_")[1])
        user = await User.get_user(callback_query.message)

        # Update user payment status
        await sync_to_async(UserPayment.objects.filter(user=user_id).update)(
            is_verified=False
        )
        await bot.send_message(
            chat_id=user_id, text="Tolovingiz admin tomonidan bekor qilindi"
        )

    if callback_data == "about_me":
        await callback_query.message.edit_text(
            text=static.about_me_title, reply_markup=await go_back()
        )

    elif callback_data == "admin":
        await callback_query.message.edit_text(
            text=static.admin_contact, reply_markup=await go_back()
        )

    elif callback_data == "cources":
        photo = FSInputFile(path="utils/images/tariflar-test.jpeg", filename="tariflar")
        await bot.send_photo(
            chat_id=callback_query.from_user.id,
            photo=photo,
            reply_markup=await cources(),
            caption=static.cources_info,
        )

    elif callback_data == "go_back":
        await callback_query.message.answer(
            text=static.main_menu_title, reply_markup=await main_menu()
        )

    # Acknowledge the callback query to remove the loading spinner
    await callback_query.answer()


@start_router.message()
async def receive_payment_check(message: Message):
    """
    This handler receives payment check screenshots from the user
    """
    if not message.photo:
        await message.answer("Iltimos to'lov ckekini yuboring")
        return

    user = await User.get_user(message)

    photo_file_id = message.photo[-1].file_id

    payment = await sync_to_async(UserPayment.objects.filter(user=user).update)(
        user=user, screenshot=photo_file_id
    )

    photo_path = await download_telegram_file(
        photo_file_id, "/Users/bahrom04/workplace/django/nadia-kurs/rasm/"
    )

    caption = f'''{message.from_user.full_name} tomonidan to'lov cheki yuborildi
    Username: (@{message.from_user.username})
    userID: {message.chat.id}'''
    try:
        await bot.send_photo(
            chat_id="7148758895",
            photo=photo_file_id,
            caption=caption,
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="To'lovni tasdiqlash", callback_data=f"confirm_{user.user_id}"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="To'lovni rad etish", callback_data=f"decline_{user.user_id}"
                        )
                    ],
                ]
            ),
        )
    except Exception as e:
        await message.answer(
            "Failed to send payment check to the admin. Please contact support."
        )
    await message.answer(
        "To'lovni tasdiqlash uchun adminga yuborildi. Javob kelishini kuting"
    )
