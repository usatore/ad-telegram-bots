from aiogram.types import CallbackQuery, Message
from aiogram import Bot, F, Router
from app.dao.company import CompanyDAO
from app.dao.campaign import CampaignDAO
from aiogram.fsm.context import FSMContext
from app.states.states import CompanyAdminStates
from app.utils.admin_chat import for_admin

router = Router()


# Обработчик для кнопки "Принять"
@router.callback_query(F.data.startswith("approve_campaign:"))
@for_admin
async def approve_campaign(callback: CallbackQuery, bot: Bot):
    await callback.answer()
    try:
        campaign_id = int(callback.data.split(":")[1])
    except (IndexError, ValueError):
        await callback.message.answer("Некорректный формат данных.")
        return

    # Аппрувим кампанию
    campaign = await CampaignDAO.approve_campaign(campaign_id=campaign_id)
    if not campaign:
        await callback.message.answer("Кампания не найдена.")
        return

    # Уведомляем компанию
    company = await CompanyDAO.get_one_or_none(id=campaign.company_id)
    if company:
        await bot.send_message(
            chat_id=company.telegram_id,
            text=f"Ваша кампания (ID: {campaign_id})  опубликована, как только будут поступать рекламные интеграции от пользователей, вы будете получать ссылки на эти интеграции.!",
        )

    # Обновляем сообщение в админском чате
    await callback.message.edit_text(
        f"Кампания (ID: {campaign_id}) одобрена!", reply_markup=None
    )


# Обработчик для кнопки "Отклонить" запускает состояние на ввод причины
@router.callback_query(F.data.startswith("reject_campaign:"))
@for_admin
async def reject_campaign(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await callback.answer()
    try:
        campaign_id = int(callback.data.split(":")[1])
    except (IndexError, ValueError):
        await callback.message.answer("Некорректный формат данных.")
        return

    await state.update_data(campaign_id=campaign_id)
    await state.set_state(CompanyAdminStates.waiting_for_reason)

    await callback.message.edit_text("Введите причину отклонения кампании:")


@router.message(CompanyAdminStates.waiting_for_reason)
@for_admin  # Добавляем декоратор для проверки прав администратора
async def process_input_reason_and_delete_campaign(
    message: Message, state: FSMContext, bot: Bot
):
    """
    Обработчик ввода причины отклонения кампании.
    """

    if not message.text:
        await message.answer("Пожалуйста, введите причину текстом.")
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        return

    data = await state.get_data()
    campaign_id = data.get("campaign_id")

    # Удаляем кампанию из базы данных
    campaign = await CampaignDAO.delete(campaign_id=campaign_id)

    if not campaign:
        await message.answer("Кампания не найдена или уже удалена.")
        return

    # Находим компанию для уведомления компании
    company = await CompanyDAO.get_one_or_none(id=campaign.company_id)
    if company:
        await bot.send_message(
            chat_id=company.telegram_id,
            text=f"Ваша кампания (ID: {campaign_id}) отклонена и удалена по причине: {message.text}",
        )

    # Сообщаем администратору, что кампания была отклонена и удалена
    await message.answer(
        f"Кампания (ID: {campaign_id}) отклонена и удалена по причине: {message.text}"
    )
    await state.clear()
