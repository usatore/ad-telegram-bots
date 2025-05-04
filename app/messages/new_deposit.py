from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


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

