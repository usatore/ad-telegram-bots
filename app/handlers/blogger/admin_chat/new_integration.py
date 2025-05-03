from aiogram.types import CallbackQuery, Message
from aiogram import Router, Bot, F
from app.dao.integration import IntegrationDAO

from aiogram.fsm.context import FSMContext
from app.states.admin import AdminRejectIntegration


router = Router()



@router.callback_query(F.data.startswith("approve_integration_materials:"))
async def approve_integration_materials(callback: CallbackQuery, bot: Bot):
    """Обработчик принятия интеграции."""
    integration_id = int(callback.data.split(":")[1])
    print(integration_id)

    # Обновляем статус интеграции на "Принята"
    integration = await IntegrationDAO.get_one_or_none(id=integration_id)
    if integration:
        await IntegrationDAO.approve_integration_materials(integration_id=integration_id)
        await callback.message.answer("Интеграция принята!")
    else:
        await callback.answer("Интеграция не найдена.")



@router.callback_query(F.data.startswith("reject_integration:"))
async def reject_integration(callback: CallbackQuery, bot: Bot):
    """Обработчик отказа от интеграции с указанием причины."""
    integration_id = int(callback.data.split(":")[1])

    # Запрашиваем причину отказа
    await callback.message.edit_text("Укажите причину отказа:")


  # Обработчик сообщения с причиной отказа
    @router.message(AdminRejectIntegration.waiting_for_reason)
    async def process_reason_and_delete_integration(message: Message, state: FSMContext):


        # Обновляем статус интеграции на "Отказана" и добавляем причину
        integration = await IntegrationDAO.get_one_or_none(id=integration_id)
        if integration:
            await IntegrationDAO.delete(id=integration_id)
            await message.answer(f"Интеграция отклонена по причине: {message.text}")
        else:
            await message.answer("Интеграция не найдена.")

        # Очищаем состояние
        await state.clear()
