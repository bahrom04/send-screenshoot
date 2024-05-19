from aiogram.types import Message


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
        "language_code": user.language_code
    }
