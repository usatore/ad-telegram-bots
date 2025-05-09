from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_balance_menu_keyboard(company_id: int, balance: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"💳 Пополнить баланс ({balance})",
                    callback_data="add_deposit",
                )
            ],
            [
                InlineKeyboardButton(
                    text="📜 История всех транзакций",
                    callback_data="get_company_transactions",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="📈 История пополнений",
                    callback_data="get_company_deposits",
                ),
                InlineKeyboardButton(
                    text="📉 История списаний",
                    callback_data="get_company_withdrawals",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Главное меню",
                    callback_data="main_menu",
                )
            ],
        ]
    )
