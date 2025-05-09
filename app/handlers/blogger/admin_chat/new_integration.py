from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.dao.blogger import BloggerDAO
from app.dao.integration import IntegrationDAO
from app.states.admin import AdminRejectIntegration

router = Router()


@router.callback_query(F.data.startswith("approve_integration_materials:"))
async def approve_integration_materials(callback: CallbackQuery, bot: Bot):
    await callback.answer()
    try:
        integration_id = int(callback.data.split(":")[1])
    except (IndexError, ValueError):
        await callback.message.answer("Некорректный формат данных.")
        return

    integration = await IntegrationDAO.get_one_or_none(id=integration_id)
    if not integration:
        await callback.message.answer("Интеграция не найдена.")
        return

    await IntegrationDAO.approve_integration_materials(integration_id=integration_id)

    blogger = await BloggerDAO.get_one_or_none(id=integration.blogger_id)
    if blogger:
        await bot.send_message(
            chat_id=blogger.telegram_id,
            text=f"✅ Материалы интеграции (ID {integration_id}) приняты!",
        )

    await callback.message.answer(
        f"Материалы интеграции (ID {integration_id}) приняты!", reply_markup=None
    )


@router.callback_query(F.data.startswith("reject_integration:"))
async def reject_integration(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await callback.answer()

    integration_id = int(callback.data.split(":")[1])

    await state.set_state(AdminRejectIntegration.waiting_for_reason)
    await state.update_data(integration_id=integration_id)
    await callback.message.answer("Введите причину отклонения интеграции:")


@router.message(AdminRejectIntegration.waiting_for_reason)
async def process_reason_and_delete_integration(
    message: Message, bot: Bot, state: FSMContext
):

    data = await state.get_data()
    integration_id = data.get("integration_id")

    integration = await IntegrationDAO.get_one_or_none(id=integration_id)
    if not integration:
        await message.answer("Интеграция не найдена.")
        await state.clear()
        return

    await IntegrationDAO.delete(id=integration_id)

    blogger = await BloggerDAO.get_one_or_none(id=integration.blogger_id)
    if blogger:
        await bot.send_message(
            chat_id=blogger.telegram_id,
            text=f"❌ Ваша интеграция (ID {integration_id}) отклонена и удалена по причине: {message.text}",
        )

    await message.answer(
        f"Интеграция (ID {integration_id}) отклонена и удалена по причине: {message.text}"
    )
    await state.clear()


@router.callback_query(F.data.startswith("approve_integration_done:"))
async def approve_integration_done(callback: CallbackQuery, bot: Bot):
    await callback.answer()

    integration_id = int(callback.data.split(":")[1])

    integration = await IntegrationDAO.approve_integration_done(integration_id)

    blogger = await BloggerDAO.get_one_or_none(id=integration.blogger_id)
    if blogger:
        await bot.send_message(
            chat_id=blogger.telegram_id,
            text=f"✅ Ваша интеграция (ID {integration_id}) принята как выполненная! Спасибо!",
        )

    await callback.message.answer(
        f"Интеграция (ID {integration_id}) подтверждена как выполненная."
    )
