from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def create_profile_links_admin_message(
    blogger_id: int,
    telegram_id: int,
    username: str,
    full_name: str,
    profile_links: list[str],
) -> tuple[str, InlineKeyboardMarkup]:
    """
    Формирует сообщение и клавиатуру для отправки в админский чат по запросу на создание профиля блоггера.

    Args:
        blogger: Объект блоггера (Blogger).
        telegram_id: Telegram ID пользователя.
        username: Имя пользователя в Telegram (@username или None).
        full_name: Полное имя пользователя (или None).
        profile_links: Список ссылок на профили блоггера.

    Returns:
        Tuple[str, InlineKeyboardMarkup]: Текст сообщения и клавиатура.
    """

    # Формируем текст сообщения
    admin_message = (
        f"Новая заявка на профиль блоггера (ID: {blogger_id})\n"
        f"Пользователь: @{username or 'не указан'} ({full_name or 'не указан'})\n"
        f"Telegram ID: {telegram_id}\n"
        f"Ссылки на профили:\n" + "\n".join(profile_links) + "\n"
        f"Профиль ожидает одобрения.\n"
    )

    # Создаем кнопки
    approve_button = InlineKeyboardButton(
        text="Одобрить", callback_data=f"approve_blogger:{blogger_id}"
    )
    reject_button = InlineKeyboardButton(
        text="Отклонить", callback_data=f"reject_blogger:{blogger_id}"
    )

    admin_markup = InlineKeyboardMarkup(
        inline_keyboard=[[approve_button, reject_button]]
    )

    return admin_message, admin_markup