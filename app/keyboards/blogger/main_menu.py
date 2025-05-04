from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_main_menu_keyboard(balance: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📋 Доступные кампании", callback_data="get_campaigns"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📤 Мои интеграции", callback_data="get_integrations"
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"💰 Баланс {balance}", callback_data="balance"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔗 Отправить ссылки", callback_data="send_links"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📞 Поддержка", url="https://t.me/usatoresapiente"
                )
            ],
        ]
    )
