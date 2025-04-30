from aiogram.types import CallbackQuery, Message
from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from app.dao.blogger import BloggerDAO

router = Router()


# Хендлер на нажатие кнопки "Удалить мой профиль"
@router.callback_query(F.data == "delete_blogger_profile")
async def delete_blogger_profile(callback: CallbackQuery, state: FSMContext):
    """Удаляем профиль пользователя сразу после нажатия кнопки."""
    user_id = callback.from_user.id

    # Проверяем, существует ли блоггер с таким Telegram ID
    blogger = await BloggerDAO.get_one_or_none(telegram_id=user_id)

    if not blogger:
        await callback.answer("Ваш профиль не найден.")
        return

    # Удаляем профиль блоггера
    await BloggerDAO.delete(blogger.id)

    # Уведомляем пользователя о том, что его профиль удален
    await callback.answer("Ваш профиль был успешно удален.")