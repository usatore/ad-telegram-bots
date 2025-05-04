from aiogram import F, Router
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from app.dao.blogger import BloggerDAO
from app.dao.campaign import CampaignDAO
from app.dao.integration import IntegrationDAO

router = Router()


@router.callback_query(F.data == "get_integrations")
async def get_integrations(callback: CallbackQuery):
    """Обработчик для получения интеграций блоггера."""

    blogger = await BloggerDAO.get_one_or_none(telegram_id=callback.from_user.id)
    if not blogger:
        await callback.answer(
            "Вы еще не создали профиль блоггера. Отправьте ссылки на проверку"
        )
        return

    integrations = await IntegrationDAO.get_all(blogger_id=blogger.id)
    if not integrations:
        await callback.answer("У вас пока нет интеграций.")
        return

    for integration in integrations:
        campaign = await CampaignDAO.get_one_or_none(id=integration.campaign_id)

        integration_status = "✅ Одобрено" if integration.approved else "🕒 На проверке"
        is_done = "✔️ Выполнено" if integration.done else "❌ Не выполнено"

        text = (
            f"Интеграция ID: {integration.id}\n"
            f"Кампания: {campaign.description if campaign else '❓ Не найдена'}\n"
            f"Ссылки: {integration.publication_links or '—'}\n"
            f"Просмотры: {integration.views_count or 0}\n"
            f"Статус: {integration_status}, {is_done}"
        )

        markup = None
        if integration.approved and not integration.done:
            button = InlineKeyboardButton(
                text="Отправить ссылки на публикации",
                callback_data=f"send_publication_links:{integration.id}",
            )
            markup = InlineKeyboardMarkup(inline_keyboard=[[button]])

        await callback.message.answer(text, reply_markup=markup)
