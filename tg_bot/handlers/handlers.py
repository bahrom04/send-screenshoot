import os

from aiogram import Router
from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, FSInputFile, ContentType
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

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
                        text="Pay", callback_data=f"pay_{plan_title.lower()}"
                    )
                ]
            ]
        ),
    )


@start_router.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """

    u = await User.get_user_and_created(message)

    await message.answer(text=static.main_menu_title, reply_markup=await main_menu())


# @start_router.message()
# async def receive_payment_check(message: Message):
#     """
#     This handler receives payment check screenshots from the user
#     """
#     caption = f"Payment check from user {message.from_user.full_name} (@{message.from_user.username})."
#     await bot.send_photo(
#         chat_id=7148758895,
#         photo=message.photo[-1].file_id,
#         caption=caption,
#         reply_markup=await confirm_decline_buttons(message.from_user.id),
#     )
#     await message.answer(
#         "Your payment check has been sent to the admin for confirmation."
#     )


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
            f"Please send a screenshot of your payment for the {plan_title} plan."
        )
        user = await User.get_user(callback_query.message)
        user.plan = plan_title  # Store the selected plan
        await user.save()

        # user_payment = UserPayment(user=user, plan)

    elif callback_data.startswith("confirm_"):
        user_id = int(callback_data.split("_")[1])
        await bot.send_message(
            chat_id=user_id, text="Your payment has been confirmed. Thank you!"
        )
        await callback_query.message.edit_text("You have confirmed the payment.")

    elif callback_data.startswith("decline_"):
        user_id = int(callback_data.split("_")[1])
        await bot.send_message(
            chat_id=user_id, text="Your payment has been declined. Please try again."
        )
        await callback_query.message.edit_text("You have declined the payment.")

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
        await message.answer("Please send a valid photo of your payment receipt.")
        return

    photo_file_id = message.photo[-1].file_id

    # Save the image details to the Django model
    payment, created = await UserPayment.get_payment_and_created(
        message=message,
        plan_title=plan,
        photo_file_id=photo_file_id
    )

    caption = f"Payment check from user {message.from_user.full_name} (@{message.from_user.username}) for the {plan} plan."
    try:
        await bot.send_photo(
            chat_id=ADMIN_ID,
            photo=photo_file_id,
            caption=caption,
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="Confirm", callback_data=f"confirm_{user.user_id}")],
                    [InlineKeyboardButton(text="Decline", callback_data=f"decline_{user.user_id}")]
                ]
            )
        )
    except TelegramForbiddenError:
        await message.answer("Failed to send payment check to the admin. Please contact support.")
    await message.answer("Your payment check has been sent to the admin for confirmation.")
