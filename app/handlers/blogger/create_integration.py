from aiogram.types import (
    CallbackQuery,
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram import Router, Bot, F
from app.dao.integration import IntegrationDAO
from app.dao.blogger import BloggerDAO
from app.dao.campaign import CampaignDAO
from app.config import settings
from aiogram.fsm.context import FSMContext
from app.states.blogger import BloggerCreateIntegration
from app.messages.new_integration import create_integration_admin_message

router = Router()


@router.callback_query(F.data.startswith("create_integration:"))
async def create_integration(callback: CallbackQuery, bot: Bot, state: FSMContext):
    """Обработчик для начала процесса интеграции между блоггером и кампанией."""
    try:
        blogger_id, campaign_id = map(int, callback.data.split(":")[1:])
    except (IndexError, ValueError):
        await callback.answer("Некорректный формат данных.")
        return

    blogger = await BloggerDAO.get_one_or_none(id=blogger_id)
    if not blogger:
        await callback.answer("Блоггер не найден.")
        return

    campaign = await CampaignDAO.get_one_or_none(id=campaign_id)
    if not campaign:
        await callback.answer("Кампания не найдена.")
        return

    existing_integration = await IntegrationDAO.get_one_or_none(
        blogger_id=blogger.id, campaign_id=campaign.id
    )
    if existing_integration:
        await callback.answer("Блоггер уже сделал интеграцию на эту кампанию.")
        return

    integration = await IntegrationDAO.create_integration(
        blogger_id=blogger.id,
        campaign_id=campaign.id,  # создаем интеграцию в БД без материалов (пустой словарь materials по дефолту)
    )

    if not integration:
        await callback.answer("Не удалось создать интеграцию.")
        return

    await state.set_state(BloggerCreateIntegration.waiting_for_load_materials)
    await state.update_data(blogger_id=blogger_id, campaign_id=campaign_id)

    await callback.message.answer("Пришлите материалы следующим сообщением")


@router.message(BloggerCreateIntegration.waiting_for_load_materials)
async def process_materials(message: Message, state: FSMContext):
    """Обрабатывает материалы, отправленные блоггером для интеграции."""
    data = await state.get_data()
    blogger_id = data.get("blogger_id")
    campaign_id = data.get("campaign_id")

    materials = {}

    if message.text:
        materials["text"] = message.text
    if message.photo:
        materials["photo"] = message.photo[-1].file_id
    if message.video:
        materials["video"] = message.video.file_id

    await state.update_data(materials=materials)

    submit_button = InlineKeyboardButton(
        text="Отправить на проверку", callback_data="submit_for_materials"
    )
    submit_markup = InlineKeyboardMarkup(inline_keyboard=[[submit_button]])

    await message.answer(
        "Материалы успешно загружены. Нажмите кнопку ниже, чтобы отправить на проверку.",
        reply_markup=submit_markup,
    )


@router.callback_query(F.data == "submit_for_materials")
async def submit_for_materials(callback: CallbackQuery, state: FSMContext):
    """Обработчик кнопки отправки на проверку."""
    await callback.answer()

    data = await state.get_data()
    materials = data.get("materials", {})
    message_id = data.get("materials_message_id")  # ID сообщения с материалами

    blogger_id = data.get("blogger_id")
    campaign_id = data.get("campaign_id")

    if not any(materials.values()):
        await callback.message.edit_text(
            "Материалы не были загружены, пожалуйста, загрузите их."
        )
        return

    integration = await IntegrationDAO.get_one_or_none(
        blogger_id=blogger_id, campaign_id=campaign_id
    )

    if not integration:
        await callback.message.edit_text("Интеграция не найдена.")
        return

    await IntegrationDAO.update_materials(
        integration_id=integration.id, materials=materials
    )

    campaign = await CampaignDAO.get_one_or_none(id=integration.campaign_id)

    admin_text, admin_markup = create_integration_admin_message(
        username=callback.from_user.username,
        full_name=callback.from_user.full_name,
        integration_id=integration.id,
        campaign_id=campaign.id,
        description=campaign.description,
        materials=materials,
    )

    # Пересылаем сообщение с материалами в админ-чат
    if message_id:
        try:
            await callback.bot.forward_message(
                chat_id=settings.ADMIN_CHAT_ID,
                from_chat_id=callback.message.chat.id,
                message_id=message_id,
            )
        except Exception as e:
            await callback.message.answer(
                f"Не удалось переслать сообщение с материалами: {e}"
            )

    # Отправляем сообщение с описанием интеграции и кнопками
    await callback.bot.send_message(
        chat_id=settings.ADMIN_CHAT_ID, text=admin_text, reply_markup=admin_markup
    )

    await state.clear()

    await callback.message.edit_text(
        "Материалы успешно отправлены на проверку. Ожидайте ответа."
    )
