import os
import requests

from asgiref.sync import sync_to_async

from aiogram import Router
from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


from tg_bot.keyboards.keyboards import (
    main_menu,
    go_back,
    cources,
    payment_button,
    confirm_decline_buttons,
)

from users.models import User, UserPayment, Plan

from utils import static
from dotenv import load_dotenv


load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
ADMIN = os.getenv("ADMIN")
ADMIN_USER_NAME = os.getenv("ADMIN_USER_NAME")
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

start_router = Router()


async def download_telegram_file(file_id, destination):
    file_info = await bot.get_file(file_id)
    file_path = file_info.file_path
    file_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"

    response = requests.get(file_url)
    response.raise_for_status()

    # Construct the full file path
    file_name = os.path.join(destination, os.path.basename(file_path))

    # Save the file
    with open(file_name, "wb") as f:
        f.write(response.content)

    return file_name


# Helper function to show payment details
async def show_payment_details(callback_query: CallbackQuery, plan_title, plan_amount):
    title = static.payment_info(plan=plan_title, amount=plan_amount)
    # photo = FSInputFile(path="utils/images/carta.jpg", filename="carta")
    await callback_query.message.answer(text=title)


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
    v = lambda payment_status: (
        "Tasdiqlangan" if payment_status == True else "Tasdiqlanmagan"
    )

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

    # Plans
    if callback_data.startswith("plan_"):
        plan_name = callback_data.split("_")[1]
        plan_title = plan_name.capitalize()
        if plan_title == "Plus18":
            await callback_query.message.answer(
                text=static.cources_info,
                reply_markup=await payment_button(plan_title=plan_title),
            )
        if plan_title == "Professionalkurs":
            await callback_query.message.answer(
                text=static.cources_info,
                reply_markup=await payment_button(plan_title=plan_title),
            )

        else:
            await callback_query.message.answer(
                f"Iltimos {plan_title} kursi uchun to'lov chekini jo'nating"
            )

    # Payment
    if callback_data.startswith("pay_"):
        plan_name = callback_data.split("_")[1]
        plan_title = plan_name.capitalize()

        if plan_title == "Plus18":
            await show_payment_details(callback_query, "18+", "1 300 000")
            await callback_query.message.answer(
                f"Iltimos 18+ kursi uchun to'lov chekini jo'nating"
            )
        if plan_title == "Professionalkurs":
            await show_payment_details(callback_query, "Pro Kurs", "2 300 000")
            await callback_query.message.answer(
                f"Iltimos Pro Kurs kursi uchun to'lov chekini jo'nating"
            )

        # Store the selected plan in the user's session
        user = await User.get_user(callback_query.message)
        plan = await sync_to_async(Plan.objects.get)(title=plan_title)

        await sync_to_async(
            User.objects.filter(user_id=callback_query.message.chat.id).update
        )(current_plan=plan)

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
            chat_id=ADMIN,
            text="Foydalanuvchiga xabar jonatildi",
        )

        # Update user payment status
        await sync_to_async(UserPayment.objects.filter(user=user_id).update)(
            is_verified=True
        )

        await bot.send_message(
            chat_id=user_id,
            text="To‘lov uchun rahmat. To‘lov admin tomonidan tasdiqlandi☺️",
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
        photo = FSInputFile(path="utils/images/uravo.jpg", filename="aboutme")
        await bot.send_photo(
            chat_id=callback_query.from_user.id,
            caption=static.about_me_title,
            photo=photo,
            reply_markup=await go_back(),
        )

    elif callback_data == "admin":
        await callback_query.message.edit_text(
            text=ADMIN_USER_NAME, reply_markup=await go_back()
        )

    elif callback_data == "cources":
        photo = FSInputFile(path="utils/images/kurslarim.png", filename="tariflar")
        await bot.send_photo(
            chat_id=callback_query.from_user.id,
            photo=photo,
            reply_markup=await cources(),
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
    # Get the user's current plan
    current_plan = await sync_to_async(
        User.objects.filter(user_id=message.chat.id).values_list("current_plan", flat=True).first
    )()

    photo_file_id = message.photo[-1].file_id

    payment = await sync_to_async(UserPayment.objects.filter(user=user).update)(
        user=user, plan=current_plan, screenshot=photo_file_id
    )
    # universal path
    root_dir = os.getcwd()
    photo_path = await download_telegram_file(
        photo_file_id, os.path.join(root_dir, "rasm/")
    )

    caption = f"""{message.from_user.full_name} tomonidan to'lov cheki yuborildi
Username: (@{message.from_user.username})
userID: {message.chat.id}"""
    try:
        await bot.send_photo(
            chat_id=ADMIN,
            photo=photo_file_id,
            caption=caption,
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="To'lovni tasdiqlash",
                            callback_data=f"confirm_{user.user_id}",
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="To'lovni rad etish",
                            callback_data=f"decline_{user.user_id}",
                        )
                    ],
                ]
            ),
        )
    except Exception as e:
        await message.answer("error")
    await message.answer(
        "To‘lovni tasdiqlash uchun adminga yuborildi. Javob kelishini kuting🙏🏼"
    )
