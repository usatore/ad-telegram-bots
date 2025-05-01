from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from app.dao.campaign import CampaignDAO
from app.keyboards.company.main_menu import get_main_menu_keyboard  # Импортируем клавиатуру main_menu

router = Router()


@router.callback_query(F.data.startswith("get_campaigns_for_company:"))
async def get_campaigns_for_company(callback: CallbackQuery):
    """Отображает список кампаний компании с кнопками удаления."""
    company_id = int(callback.data.split(":")[-1])

    campaigns = await CampaignDAO.get_all(company_id=company_id)

    if not campaigns:
        await callback.answer("У вас пока нет созданных кампаний.", reply_markup=get_main_menu_keyboard(company_id=callback.from_user.id))
        return

    for campaign in campaigns:
        text = (
            f"🆔 Кампания ID: {campaign.id}\n"
            f"📄 Описание: {campaign.description}\n"
            f"💸 Цена за просмотр: {campaign.view_price} ₽"
        )

        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🗑 Удалить кампанию",
                        callback_data=f"delete_campaign:{campaign.id}"
                    )
                ]
            ]
        )

        await callback.message.answer(text, reply_markup=markup)
