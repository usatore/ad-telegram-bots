from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


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