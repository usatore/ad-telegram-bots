from aiogram.types import (
    CallbackQuery,
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram import Router, Bot, F
from app.dao.integration import IntegrationDAO
from app.dao.blogger import BloggerDAO
from app.dao.campaign import CampaignDAO
from app.config import settings

router = Router()


# Хендлер для кнопки "Получить кампании для блоггера"
@router.callback_query(F.data.startswith("get_campaigns"))
async def get_campaigns(callback: CallbackQuery, bot: Bot):
    """Обработчик для получения доступных рекламных кампаний для блоггера."""

    blogger = await BloggerDAO.get_one_or_none(telegram_id=callback.from_user.id)
    if not blogger:
        await callback.answer(
            "Вы еще не создали профиль блоггера. Отправьте ссылки на проверку"
        )
        return

    if not blogger.approved:
        await callback.answer("Ваши ссылки проверяются администратором, ожидайте...")
        return

    # Получаем кампании, которые доступны для блоггера
    campaigns = await CampaignDAO.get_approved_campaigns_not_joined_by_blogger(
        blogger_id=blogger.id
    )
    if not campaigns:
        await callback.answer("Нет доступных кампаний для интеграции.")
        return

    # Отправляем каждую кампанию отдельно с кнопкой "Сделать интеграцию"
    for campaign in campaigns:
        # Формируем кнопку для интеграции
        integration_button = InlineKeyboardButton(
            text=f"Сделать интеграцию с кампанией {campaign.id}",
            callback_data=f"create_integration:{blogger.id}:{campaign.id}",  # Данные для создания интеграции
        )

        # Создаем клавиатуру с кнопкой
        campaign_markup = InlineKeyboardMarkup(inline_keyboard=[[integration_button]])

        # Формируем сообщение с описанием и ценой кампании
        campaign_message = (
            f"Кампания ID: {campaign.id}\n"
            f"Описание: {campaign.description}\n"
            f"Цена: {campaign.view_price} ₽\n"
            "Нажмите кнопку ниже, чтобы сделать интеграцию."
        )

        # Отправляем сообщение с кнопкой
        await callback.message.answer(campaign_message, reply_markup=campaign_markup)
