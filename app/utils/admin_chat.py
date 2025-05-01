from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from app.models import Campaign, Company
from app.config import settings
import functools
from app.models import Integration
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from app.dao.blogger import Blogger


def create_integration_admin_message(
    integration: Integration,
    blogger: Blogger,
    username: str,
    full_name: str,
    materials: dict,
) -> tuple[str, InlineKeyboardMarkup]:
    """
    Формирует сообщение и клавиатуру для отправки в админский чат о создании материалов интеграции.

    Args:
        integration: Объект интеграции (Integration).
        blogger: Объект блоггера (Blogger).
        username: Имя пользователя в Telegram (@username или None).
        full_name: Полное имя пользователя (или None).
        materials: Материалы интеграции, хранящиеся в виде словаря.

    Returns:
        Tuple[str, InlineKeyboardMarkup]: Текст сообщения и клавиатура.
    """
    # Формируем текст сообщения
    admin_message = (
        f"Новая интеграция для проверки (ID: {integration.id})\n"
        f"Блоггер: @{username or 'не указан'} ({full_name or 'не указан'})\n"
        f"Telegram ID: {blogger.telegram_id}\n"
        f"Интеграция ID: {integration.id}\n"
        f"Материалы:\n"
        f"- Текст: {materials.get('text', 'не предоставлен')}\n"
        f"- Видео: {materials.get('video', 'не предоставлено')}\n"
        f"- Фото: {materials.get('photo', 'не предоставлено')}\n"
        f"Интеграция ожидает одобрения.\n"
    )

    # Создаем кнопки для админа
    approve_button = InlineKeyboardButton(
        text="Одобрить", callback_data=f"approve_integration:{integration.id}"
    )
    reject_button = InlineKeyboardButton(
        text="Отклонить", callback_data=f"reject_integration:{integration.id}"
    )

    admin_markup = InlineKeyboardMarkup(
        inline_keyboard=[[approve_button, reject_button]]
    )

    return admin_message, admin_markup


def create_profile_links_admin_message(
    blogger: Blogger,
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
        f"Новая заявка на профиль блоггера (ID: {blogger.id})\n"
        f"Пользователь: @{username or 'не указан'} ({full_name or 'не указан'})\n"
        f"Telegram ID: {blogger.telegram_id}\n"
        f"Ссылки на профили:\n" + "\n".join(profile_links) + "\n"
        f"Профиль ожидает одобрения.\n"
    )

    # Создаем кнопки
    approve_button = InlineKeyboardButton(
        text="Одобрить", callback_data=f"approve_blogger:{blogger.id}"
    )
    reject_button = InlineKeyboardButton(
        text="Отклонить", callback_data=f"reject_blogger:{blogger.id}"
    )

    admin_markup = InlineKeyboardMarkup(
        inline_keyboard=[[approve_button, reject_button]]
    )

    return admin_message, admin_markup


def create_campaign_admin_message(
    campaign_id: int,
    company_id: int,
    telegram_id: int,
    username: str,
    full_name: str,
    description: dict,
    view_price: int,
) -> tuple[str, InlineKeyboardMarkup]:
    """
    Формирует сообщение и клавиатуру для отправки в админский чат.

    Args:
        campaign: Объект кампании (Campaign).
        company: Объект компании (Company).
        telegram_id: Telegram ID пользователя.
        username: Имя пользователя в Telegram (@username или None).
        full_name: Полное имя пользователя (или None).
        description: Словарь с данными кампании.

    Returns:
        Tuple[str, InlineKeyboardMarkup]: Текст сообщения и клавиатура.
    """

    # Формируем текст сообщения
    admin_message = (
        f"Новая кампания на проверку (ID: {campaign_id})\n"
        f"Пользователь: @{username or 'не указан'} ({full_name or 'не указан'})\n"
        f"Telegram ID: {telegram_id}\n"
        f"Компания ID: {company_id}\n"
        f"Цена за просмотр: {view_price} руб.\n"
        f"Детали кампании:\n"
        f"- Тип контента: {description.get('content_type', 'не указан')}\n"
        f"- Соцсети: {description.get('social_networks', 'не указаны')}\n"
        f"- Приоритет аудитории: {description.get('audience_priority', 'не указан')}\n"
        f"- Тип продукта: {description.get('product_type', 'не указан')}\n"
        f"- Ссылка: {description.get('website_link', 'не указана')}\n"
        f"- Способ связи: {description.get('contact_method', 'не указан')}\n"
        f"- Стиль рекламы: {description.get('advertising_style', 'не указан')}"
    )

    # Создаем кнопки
    approve_button = InlineKeyboardButton(
        text="Принять", callback_data=f"approve_campaign:{campaign_id}"
    )
    reject_button = InlineKeyboardButton(
        text="Отказать", callback_data=f"reject_campaign:{campaign_id}"
    )

    admin_markup = InlineKeyboardMarkup(
        inline_keyboard=[[approve_button, reject_button]]
    )

    return admin_message, admin_markup


def extract_user_id(update) -> int:
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
    ]

    for path in update_paths:
        # Используем getattr, чтобы безопасно получить атрибут
        user = getattr(getattr(update, path, None), "from_user", None)
        if user is not None:
            return user.id


def for_admin(func):
    """Декоратор для проверки прав доступа администратора."""

    @functools.wraps(func)
    async def wrapper(update, *args, **kwargs):
        user_id = extract_user_id(update)

        # Проверка на администратора
        if user_id not in settings.ADMIN_IDS:
            # Логируем или выводим сообщение
            print(f"Unauthorized access attempt by user {user_id}")
            return  # Можно добавить return с сообщением или выводом ошибки, если нужно

        # Если пользователь админ, выполняем основную логику
        return await func(update, *args, **kwargs)

    return wrapper
