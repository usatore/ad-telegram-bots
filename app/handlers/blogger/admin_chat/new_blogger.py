from aiogram.types import CallbackQuery, Message
from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from app.dao.blogger import BloggerDAO
from app.states.admin import AdminRejectBlogger
from app.messages.admin_chat import for_admin

router = Router()


@router.callback_query(F.data.startswith("approve_blogger:"))
#@for_admin
async def approve_blogger(callback: CallbackQuery, bot: Bot):
    await callback.answer()

    try:
        blogger_id = int(callback.data.split(":")[1])
    except (IndexError, ValueError):
        await callback.message.answer("❗ Некорректный формат данных.")
        return

    blogger = await BloggerDAO.approve_blogger(blogger_id=blogger_id)
    if not blogger:
        await callback.message.answer("❗ Блоггер не найден.")
        return

    await bot.send_message(
        chat_id=blogger.telegram_id,
        text="✅ Ваш профиль был одобрен администратором. Ожидайте рекламных интеграций.",
    )

    await callback.message.edit_text(
        f"✅ Профиль блоггера (ID: {blogger.id}) одобрен.", reply_markup=None
    )


@router.callback_query(F.data.startswith("reject_blogger:"))
#@for_admin
async def reject_blogger(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    blogger_id = int(callback.data.split(":")[1])

    await state.set_state(AdminRejectBlogger.waiting_for_reason)
    await state.update_data(blogger_id=blogger_id)

    await callback.message.answer("✏️ Введите причину отклонения профиля блоггера:")
    print(await state.get_data())
    print(await state.get_state())


@router.message(AdminRejectBlogger.waiting_for_reason)
#@for_admin
async def process_reason_and_delete_blogger(message: Message, bot: Bot, state: FSMContext):
    print('ya v process reject reason')
    data = await state.get_data()
    blogger_id = data.get("blogger_id")

    blogger = await BloggerDAO.delete(id=blogger_id)
    print(blogger)
    await bot.send_message(
        chat_id=blogger.telegram_id,
        text=f"❌ Ваш профиль был отклонён и удалён администратором.\nПричина: {message.text}"
    )
    print('ya tut')

    await message.answer(
        f"❌ Профиль блоггера (ID: {blogger_id}) отклонён и удалён.\nПричина: {message.text}"
    )

    await state.clear()
