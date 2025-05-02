from aiogram.types import CallbackQuery, Message
from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from app.utils.admin_chat import for_admin
from app.dao.blogger import BloggerDAO
from app.states.states import BloggerAdminStates
from app.config import settings

router = Router()


@router.callback_query(F.data.startswith("approve_blogger:"))
@for_admin
async def approve_blogger(callback: CallbackQuery, bot: Bot):
    await callback.answer()
    try:
        blogger_id = int(callback.data.split(":")[1])
    except (IndexError, ValueError):
        await callback.message.answer("Некорректный формат данных.")
        return

    # Аппрувим ссылки блоггера
    blogger = await BloggerDAO.approve_blogger(blogger_id=blogger_id)
    if not blogger:
        await callback.message.answer("Блоггер не найден.")
        return

    await bot.send_message(
        chat_id=blogger.telegram_id,
        text=f"Ваш профиль блоггера был одобрен администратором!",
    )

    # Обновляем сообщение в админском чате
    await callback.message.edit_text(
        f"Ссылки блоггера (ID: {blogger.id}) одобрены!", reply_markup=None
    )


@router.callback_query(F.data.startswith("reject_blogger:"))
@for_admin
async def reject_blogger(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    try:
        blogger_id = int(callback.data.split(":")[1])
    except (IndexError, ValueError):
        await callback.message.answer("Некорректный формат данных.")
        return

    await state.update_data(blogger_id=blogger_id)
    await state.set_state(BloggerAdminStates.waiting_for_reason)

    await callback.message.edit_text("Введите причину отклонения профиля блоггера:")


@router.message(BloggerAdminStates.waiting_for_reason)
@for_admin
async def process_reject_reason_and_delete_blogger(
    message: Message, state: FSMContext, bot: Bot
):
    if not message.text:
        await message.answer("Пожалуйста, введите причину текстом.")
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        return

    data = await state.get_data()
    blogger_id = data.get("blogger_id")

    blogger = await BloggerDAO.delete(blogger_id=blogger_id)

    if not blogger:
        await message.answer("Блоггер не найден или уже удалён.")
        return

    # Уведомляем блоггера
    await bot.send_message(
        chat_id=blogger.telegram_id,
        text=f"Ваш профиль был отклонён и удалён администратором по причине: {message.text}",
    )

    # Подтверждаем удаление админу
    await message.answer(
        f"Профиль блоггера (ID: {blogger_id}) отклонён и удалён по причине: {message.text}"
    )
    await state.clear()
