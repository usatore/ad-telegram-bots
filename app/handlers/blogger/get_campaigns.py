from aiogram.types import (
    CallbackQuery,
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram import Router, Bot, F
from app.dao.integration import IntegrationDAO  # Если у тебя есть DAO для интеграций
from app.dao.blogger import BloggerDAO
from app.dao.campaign import CampaignDAO
from app.config import settings

router = Router()


# Хендлер для кнопки "Получить кампании для блоггера"
@router.callback_query(F.data.startswith("get_campaigns_for:"))
async def get_campaigns_for_blogger(callback: CallbackQuery, bot: Bot):
    """Обработчик для получения доступных рекламных кампаний для блоггера."""
    # Извлекаем blogger_id из данных callback
    try:
        blogger_id = int(callback.data.split(":")[1])
    except (IndexError, ValueError):
        await callback.answer("Некорректный формат данных.")
        return

    # Получаем блоггера по ID
    blogger = await BloggerDAO.get_one_or_none(id=blogger_id)
    if not blogger:
        await callback.answer("Блоггер не найден.")
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
            callback_data=f"create_integration_for:{blogger.id}:{campaign.id}",  # Данные для создания интеграции
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
