from aiogram.types import Message, CallbackQuery


def extract_user_data_from_update(message: Message) -> dict:
    """Extract user info from a Message instance."""
    user = message.from_user
    if user is None:
        return {}

    return {
        "user_id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "language_code": user.language_code,
    }


def extract_user_data_from_callback(callabck_query: CallbackQuery) -> dict:
    """Extract user info from a Message instance."""
    user = callabck_query

    if user is None:
        return {}

    return {
        "user_id": user.id,
        "first_name": user.message.from_user.first_name,
        "last_name": user.message.from_user.last_name,
        "username": user.message.from_user.username,
        "language_code": user.message.from_user.language_code,
    }
