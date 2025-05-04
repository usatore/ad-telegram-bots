from aiogram.types import CallbackQuery, Message
from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from app.dao.blogger import BloggerDAO
from app.states.admin import AdminRejectBlogger


router = Router()


@router.callback_query(F.data.startswith("approve_blogger:"))
# @for_admin
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
        text="✅ Ваш профиль был одобрен администратором.\n Теперь вы получили доступ к рекламным кампаниям.",
    )

    await callback.message.edit_text(
        f"✅ Профиль блоггера (ID: {blogger.id}) одобрен.", reply_markup=None
    )


@router.callback_query(F.data.startswith("reject_blogger:"))
# @for_admin
async def reject_blogger(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    blogger_id = int(callback.data.split(":")[1])

    await state.set_state(AdminRejectBlogger.waiting_for_reason)
    await state.update_data(blogger_id=blogger_id)

    await callback.message.answer("✏️ Введите причину отклонения профиля блоггера:")
    print(await state.get_data())
    print(await state.get_state())


@router.message(AdminRejectBlogger.waiting_for_reason)
# @for_admin
async def process_reason_why_no_update_profile_links(
    message: Message, bot: Bot, state: FSMContext
):
    data = await state.get_data()
    blogger_id = data.get("blogger_id")

    blogger = await BloggerDAO.get_one_or_none(id=blogger_id)

    await bot.send_message(
        chat_id=blogger.telegram_id,
        text=f"❌ Ваши ссылки были не приняты администратором. Повторите действие. \nПричина: {message.text}",
    )

    await message.answer(
        f"❌ Ссылки блоггера (ID: {blogger_id}) отклонены.\nПричина: {message.text}"
    )

    await state.clear()
