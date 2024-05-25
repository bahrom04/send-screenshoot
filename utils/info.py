from aiogram.types import Message, CallbackQuery


def extract_user_data_from_update(message: Message) -> dict:
    """Extract user info from a Message instance."""
    user = message.chat
    if user is None:
        return {}

    return {
        "user_id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "language_code": message.from_user.language_code
    }


def extract_user_data_from_callback(callabck_query: CallbackQuery) -> dict:
    """Extract user info from a Message instance."""
    user = callabck_query.message.chat

    if user is None:
        return {}

    return {
        "user_id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "language_code": callabck_query.message.from_user.language_code,
    }
