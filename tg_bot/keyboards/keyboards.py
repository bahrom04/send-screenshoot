from asgiref.sync import sync_to_async

from users.models import Plan

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# Keyboard button queries from django model
@sync_to_async
def get_plan_title():
    return list(Plan.objects.all().values_list("title", flat=True).order_by("-created_at"))


async def main_menu() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="About us", callback_data="about_me")],
        [InlineKeyboardButton(text="Courses/Lectures", callback_data="cources")],
        [InlineKeyboardButton(text="Admin", callback_data="admin")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    return keyboard


async def go_back() -> InlineKeyboardMarkup:
    title = "Ortga"

    buttons = [[InlineKeyboardButton(text=title, callback_data="go_back")]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    return keyboard


async def cources() -> InlineKeyboardMarkup:
    titles = await get_plan_title()
    
    buttons = []

    for title in titles:
        callback_title = title.replace(" ", "_")
        buttons.append([InlineKeyboardButton(text=title, callback_data=f"plan_{callback_title}")])

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    return keyboard


async def payment_button(plan_title: str) -> InlineKeyboardMarkup:

    buttons = [
        [
            InlineKeyboardButton(
                text="Pay", callback_data=f"pay_{plan_title}"
            )
        ]
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    return keyboard


async def confirm_decline_buttons(user_id: int) -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(text="Confirm", callback_data=f"confirm_{user_id}"),
        InlineKeyboardButton(text="Decline", callback_data=f"decline_{user_id}"),
    ]
    return InlineKeyboardMarkup(inline_keyboard=[buttons])
