from aiogram.types import CallbackQuery, Message
from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from app.states.states import BloggerStates
from app.utils.admin_chat import for_admin  # Декоратор для проверки прав
from app.dao.blogger import BloggerDAO
from app.config import settings
from app.utils.admin_chat import create_profile_links_admin_message


router = Router()


# Хендлер на нажатие кнопки "Создать профиль блоггера"
@router.callback_query(F.data == "create_blogger_profile")
@for_admin
async def process_input_profile_links(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Пожалуйста, отправьте ссылку на профиль блоггера:")

    telegram_id = callback.from_user.id
    await state.update_data(telegram_id=telegram_id)
    await state.set_state(BloggerStates.waiting_for_profile_links)


# Хендлер на ввод profile ссылок блоггера
@router.message(BloggerStates.waiting_for_profile_links)
@for_admin
async def process_profile_links(message: Message, state: FSMContext, bot: Bot):
    if not message.text:
        await message.answer("Пожалуйста, введите ссылки построчно.")
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        return

    profile_links = [line.strip() for line in message.text.splitlines() if line.strip()]
    if not profile_links:
        await message.answer("Вы не указали ни одной корректной ссылки.")
        return

    data = await state.get_data()

    # Создаем профиль блоггера (еще не проверенный)
    blogger = await BloggerDAO.create_blogger(
        telegram_id=message.from_user.id, profile_links=profile_links
    )

    await message.answer(
        f"Профиль блоггера с Telegram ID {blogger.telegram_id} отправлен на проверку.\n"
        f"Ссылки:\n" + "\n".join(profile_links)
    )

    username = message.from_user.username
    full_name = message.from_user.full_name

    admin_message, admin_markup = create_profile_links_admin_message(
        blogger=blogger,
        username=username,
        full_name=full_name,
        profile_links=profile_links,
    )

    await bot.send_message(
        chat_id=settings.ADMIN_CHAT_ID, text=admin_message, reply_markup=admin_markup
    )

    await state.clear()
