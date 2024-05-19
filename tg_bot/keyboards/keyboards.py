from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def main_menu() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="About me", callback_data="about_me")],
        [InlineKeyboardButton(text="Admin", callback_data="admin")],
        [InlineKeyboardButton(text="Kurslar", callback_data="cources")],
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    return keyboard


async def go_back() -> InlineKeyboardMarkup:
    title = "Go back"

    buttons = [[InlineKeyboardButton(text=title, callback_data="go_back")]]

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    return keyboard


async def cources() -> InlineKeyboardMarkup:

    buttons = [
        [InlineKeyboardButton(text="Standart", callback_data="go_back")],
        [InlineKeyboardButton(text="Premium", callback_data="go_back")],
        [InlineKeyboardButton(text="Vip", callback_data="go_back")],
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    return keyboard