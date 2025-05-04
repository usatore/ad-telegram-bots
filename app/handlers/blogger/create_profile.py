from aiogram.types import CallbackQuery, Message
from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from app.states.blogger import BloggerSendProfileLinks
from app.dao.blogger import BloggerDAO
from app.config import settings
from app.messages.admin_chat import create_profile_links_admin_message


router = Router()


# Хендлер на нажатие кнопки "Отправить ссылки"
@router.callback_query(F.data == "send_links")
async def process_profile_links(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Пожалуйста, отправьте ссылку на профиль блоггера:")
    await state.update_data(telegram_id=callback.from_user.id)
    await state.set_state(BloggerSendProfileLinks.waiting_for_profile_links)


# Хендлер на ввод profile ссылок блоггера
@router.message(BloggerSendProfileLinks.waiting_for_profile_links)
async def process_profile_links(message: Message, state: FSMContext, bot: Bot):
    if not message.text:
        await message.answer("Отклонено")
        await message.delete()
        await state.clear()
        return

    profile_links = [line.strip() for line in message.text.splitlines() if line.strip()]
    if not profile_links:
        await message.answer("Вы не указали ни одной корректной ссылки.")
        await message.delete()
        await state.clear()
        return

    data = await state.get_data()

    blogger = await BloggerDAO.get_one_or_none(telegram_id=message.from_user.id)
    if not blogger:
        blogger = await BloggerDAO.create_blogger(
            telegram_id=message.from_user.id, profile_links=profile_links
        )
    else:
        blogger.approved = False
        blogger = await BloggerDAO.update_profile_links(
            blogger_id=blogger.id,
            new_profile_links=profile_links,
        )

    await message.answer(
        f"Профиль блоггера с Telegram ID {blogger.telegram_id} отправлен на проверку.\n"
        f"Ссылки:\n" + "\n".join(profile_links)
    )

    username = message.from_user.username
    full_name = message.from_user.full_name

    admin_message, admin_markup = create_profile_links_admin_message(
        blogger_id=blogger.id,
        telegram_id=blogger.telegram_id,
        username=username,
        full_name=full_name,
        profile_links=profile_links,
    )

    await bot.send_message(
        chat_id=settings.ADMIN_CHAT_ID, text=admin_message, reply_markup=admin_markup
    )

    await state.clear()
