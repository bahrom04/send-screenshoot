from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def main_menu() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Men haqimda", callback_data="about_me")],
        [InlineKeyboardButton(text="Kurslar", callback_data="cources")],
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

    buttons = [
        [InlineKeyboardButton(text="«18+» kurs", callback_data="plan_Plus18")],
        [InlineKeyboardButton(text="Professional kurs", callback_data="plan_Professionalkurs")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    return keyboard


async def payment_button(plan_title: str) -> InlineKeyboardMarkup:

    buttons = [
        [
            InlineKeyboardButton(
                text="Kursga to'lov", callback_data=f"pay_{plan_title.lower()}"
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
