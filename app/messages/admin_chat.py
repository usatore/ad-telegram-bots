from app.config import settings
import functools
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def create_publication_links_admin_message(
    username: str,
    full_name: str,
    integration_id: int,
    campaign_id: int,
    description: dict,
    publication_links: list,
    views_count: int = 0,
    materials: dict = None,
) -> tuple[str, InlineKeyboardMarkup]:

    if materials is None:
        materials = {}

    desc_lines = [f"{key}: {value}" for key, value in description.items()]
    mat_lines = [f"{key}: {value}" for key, value in materials.items()]

    admin_text = (
        f"🔗 *Ссылки на публикации от блоггера*\n\n"
        f"Блоггер: @{username}\n"
        f"Полное имя: {full_name}\n\n"
        f"Кампания ID: {campaign_id}\n"
        f"Описание кампании:\n" + "\n".join(desc_lines) + "\n\n"
        f"Интеграция ID: {integration_id}\n"
        f"Ссылки: {publication_links or '—'}\n"
        f"Просмотры: {views_count}\n"
        f"Материалы:\n" + "\n".join(mat_lines) + "\n\n"
        f"Статус: Ожидает проверки"
    )

    accept_button = InlineKeyboardButton(
        text="✅ Принять",
        callback_data=f"approve_integration_done:{integration_id}",
    )
    reject_button = InlineKeyboardButton(
        text="❌ Отклонить", callback_data=f"reject_integration:{integration_id}"
    )

    admin_markup = InlineKeyboardMarkup(
        inline_keyboard=[[accept_button, reject_button]]
    )

    return admin_text, admin_markup


def create_integration_admin_message(
    username: str,
    full_name: str,
    integration_id: int,
    campaign_id: int,
    description: dict,
    materials: dict,
) -> tuple[str, InlineKeyboardMarkup]:
    desc_lines = [f"{key}: {value}" for key, value in description.items()]
    mat_lines = [f"{key}: {value}" for key, value in materials.items()]

    admin_text = (
        f"Новая интеграция для проверки:\n\n"
        f"Блоггер: @{username}\n"
        f"Полное имя: {full_name}\n\n"
        f"Кампания ID: {campaign_id}\n"
        f"ТЗ кампании:\n" + "\n".join(desc_lines) + "\n\n"
        f"Материалы:\n" + "\n".join(mat_lines) + "\n\n"
        f"Интеграция ID: {integration_id}\n"
        f"Статус: Ожидает проверки"
    )

    accept_button = InlineKeyboardButton(
        text="✅ Принять",
        callback_data=f"approve_integration_materials:{integration_id}",
    )
    reject_button = InlineKeyboardButton(
        text="❌ Отклонить", callback_data=f"reject_integration:{integration_id}"
    )

    admin_markup = InlineKeyboardMarkup(
        inline_keyboard=[[accept_button, reject_button]]
    )

    return admin_text, admin_markup


def create_deposit_admin_message(
    company_transaction_id: int,
    company_id: int,
    telegram_id: int,
    username: str,
    full_name: str,
    deposit_amount: float,
) -> tuple[str, InlineKeyboardMarkup]:
    """
    Формирует сообщение и клавиатуру для отправки в админский чат при пополнении.

    Args:
        company_transaction_id: ID транзакции.
        company_id: ID компании.
        telegram_id: Telegram ID пользователя.
        username: Username пользователя (@username или None).
        full_name: Полное имя пользователя (или None).
        deposit_amount: Сумма пополнения.

    Returns:
        Tuple[str, InlineKeyboardMarkup]: Текст сообщения и клавиатура.
    """

    admin_message = (
        f"💰 *Новое пополнение на проверку*\n"
        f"Сумма: *{deposit_amount:.2f}₽*\n"
        f"ID транзакции: `{company_transaction_id}`\n\n"
        f"Пользователь: @{username or 'не указан'} ({full_name or 'не указано'})\n"
        f"Telegram ID: `{telegram_id}`\n"
        f"Компания ID: `{company_id}`"
    )

    approve_button = InlineKeyboardButton(
        text="✅ Подтвердить", callback_data=f"approve_deposit:{company_transaction_id}"
    )
    reject_button = InlineKeyboardButton(
        text="❌ Отклонить", callback_data=f"reject_deposit:{company_transaction_id}"
    )

    admin_markup = InlineKeyboardMarkup(
        inline_keyboard=[[approve_button, reject_button]]
    )

    return admin_message, admin_markup


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
