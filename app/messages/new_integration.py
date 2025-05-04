from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


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



