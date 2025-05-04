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