import functools
from aiogram.types import Update

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.config import settings

# В данный момент ничего отсюда не используется
# Идея была в том чтобы валидировать что админ кликает по кнопкам предназначенным для админ-чата

def extract_user_id(update: Update) -> int:
    """Извлекает user_id из update, если найден нужный объект."""
    # Список атрибутов, которые могут содержать .from_user.id
    update_paths = [
        "message",
        "edited_message",
        "callback_query",
        "inline_query",
        "chosen_inline_result",
        "shipping_query",
        "pre_checkout_query",
        "poll_answer",
        "my_chat_member",
        "chat_member",
        "chat_join_request",
    ]  # не хватает путей ловить апдейты из сообщений от админа в админчате

    for path in update_paths:
        # Используем getattr, чтобы безопасно получить атрибут
        user = getattr(getattr(update, path, None), "from_user", None)
        if user is not None:
            return user.id


# в админчате пока не работает
def for_admin(func):
    """Декоратор для проверки прав доступа администратора."""

    @functools.wraps(func)
    async def wrapper(update, *args, **kwargs):
        user_id = extract_user_id(update)

        # Проверка на администратора
        if user_id not in settings.ADMIN_IDS:
            # Логируем или выводим сообщение
            print(f"Unauthorized access attempt by user {user_id}")
            return

        # Если пользователь админ, выполняем основную логику
        return await func(update, *args, **kwargs)

    return wrapper
