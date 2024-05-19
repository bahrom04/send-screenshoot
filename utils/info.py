from aiogram.types import Message


def extract_user_data_from_update(message: Message) -> list:
    """ python-telegram-bot's Update instance --> User info """
    """
    id=1107759940 is_bot=False first_name='Bahrom' 
    last_name=None username='bahrombek19' 
    language_code='en' is_premium=None 
    added_to_attachment_menu=None can_join_groups=None 
    can_read_all_group_messages=None 
    supports_inline_queries=None 
    can_connect_to_business=None"""

    user = message.from_user

    return list(
        user_id=user["id"],
        is_blocked_bot=False,
        **{
            k: user[k]
            for k in ["username", "first_name", "last_name", "language_code"]
            if k in user and user[k] is not None
        },
    )