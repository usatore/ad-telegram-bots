from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_main_menu_keyboard(company_id: int, balance: int) -> InlineKeyboardMarkup:

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📋 Мои кампании",
                    callback_data=f"get_campaigns_for_company:{company_id}",
                )
            ],
            [
                InlineKeyboardButton(
                    text="➕ Создать кампанию", callback_data="create_campaign"
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"💰 Баланс {balance}", callback_data="balance_menu"
                )
            ],
            [InlineKeyboardButton(text="📊 Статистика", callback_data="stats")],
            [
                InlineKeyboardButton(
                    text="🆘 Поддержка", url="https://t.me/usatoresapiente"
                )
            ],
        ]
    )
