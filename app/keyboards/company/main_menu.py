from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_main_menu_keyboard(company_id: int, balance: int) -> InlineKeyboardMarkup:

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📋 Мои кампании",
                    callback_data="get_campaigns",
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
