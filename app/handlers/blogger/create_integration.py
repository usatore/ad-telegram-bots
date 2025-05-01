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
from app.states.states import BloggerIntegrationStates
from app.dao.company import CompanyDAO
from app.utils.admin_chat import create_integration_admin_message

router = Router()


@router.callback_query(F.data.startswith("create_integration_for:"))
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

    await state.set_state(BloggerIntegrationStates.waiting_for_load_materials)
    await state.update_data(blogger_id=blogger_id, campaign_id=campaign_id)

    await callback.answer(
        "Интеграция успешно создана. Пришлите материалы следующим сообщением"
    )


@router.message(BloggerIntegrationStates.waiting_for_load_materials)
async def process_materials(message: Message, state: FSMContext):
    """Обрабатывает материалы, отправленные блоггером для интеграции."""
    data = await state.get_data()
    blogger_id = data.get("blogger_id")
    campaign_id = data.get("campaign_id")

    materials = {}

    if message.text:
        materials["text"] = message.text
    else:
        materials["text"] = None

    if message.photo:
        materials["photo"] = message.photo[-1].file_id
    else:
        materials["photo"] = None

    if message.video:
        materials["video"] = message.video.file_id
    else:
        materials["video"] = None

    await state.update_data(materials=materials)

    submit_button = InlineKeyboardButton(
        text="Отправить на проверку", callback_data="submit_for_materials"
    )
    submit_markup = InlineKeyboardMarkup(inline_keyboard=[[submit_button]])

    await message.answer(
        "Материалы успешно загружены. Нажмите кнопку ниже, чтобы отправить на проверку.",
        reply_markup=submit_markup,
    )


@router.callback_query(
    BloggerIntegrationStates.waiting_for_load_materials,
    F.data == "submit_for_materials",
)
async def process_check_submission(
    bot: Bot, callback: CallbackQuery, state: FSMContext
):
    """Обработчик кнопки отправки на проверку."""
    await callback.answer()

    data = await state.get_data()
    materials = data.get("materials", {})

    blogger_id = data.get("blogger_id")
    campaign_id = data.get("campaign_id")

    if not any(materials.values()):
        await callback.message.edit_text(
            "Материалы не были загружены, пожалуйста, загрузите их."
        )
        return

    # Получаем интеграцию по blogger_id и campaign_id
    integration = await IntegrationDAO.get_one_or_none(
        blogger_id=blogger_id, campaign_id=campaign_id
    )

    if not integration:
        await callback.message.edit_text("Интеграция не найдена.")
        return

    # Обновляем материалы
    updated_integration = await IntegrationDAO.update_materials(
        integration_id=integration.id, materials=materials
    )

    if not updated_integration:
        await callback.message.edit_text("Не удалось обновить материалы интеграции.")
        return

    # Получаем компанию через интеграцию
    company = await CompanyDAO.get_one_or_none(id=integration.company_id)
    campaign = await CampaignDAO.get_one_or_none(id=integration.campaign_id)

    # Формируем сообщение для админов с кнопками
    accept_button = InlineKeyboardButton(
        text="Принять", callback_data=f"approve_{integration.id}"
    )
    reject_button = InlineKeyboardButton(
        text="Отказать", callback_data=f"reject_{integration.id}"
    )

    admin_markup = InlineKeyboardMarkup(
        inline_keyboard=[[accept_button, reject_button]]
    )

    admin_message = (
        f"Новая интеграция для проверки:\n\n"
        f"Блоггер: @{callback.from_user.username}\n"
        f"Полное имя: {callback.from_user.full_name}\n\n"
        f"Кампания: {campaign.name}\n"
        f"ТЗ кампании: {campaign.description}\n\n"
        f"Интеграция ID: {integration.id}\n"
        f"Статус: Ожидает проверки"
    )

    await bot.send_message(
        chat_id=settings.ADMIN_CHAT_ID, text=admin_message, reply_markup=admin_markup
    )

    # Очищаем состояние
    await state.clear()

    await callback.message.edit_text(
        "Материалы успешно отправлены на проверку. Ожидайте ответа."
    )


@router.callback_query(F.data.startswith("approve_"))
async def approve_integration_materials(callback: CallbackQuery, bot: Bot):
    """Обработчик принятия интеграции."""
    integration_id = int(callback.data.split("_")[1])

    # Обновляем статус интеграции на "Принята"
    integration = await IntegrationDAO.get_one_or_none(id=integration_id)
    if integration:
        await IntegrationDAO.update_integration_status(integration_id, "accepted")
        await callback.answer("Интеграция принята!")
    else:
        await callback.answer("Интеграция не найдена.")

    await callback.message.delete()


@router.callback_query(F.data.startswith("reject_"))
async def reject_integration(callback: CallbackQuery, bot: Bot):
    """Обработчик отказа от интеграции с указанием причины."""
    integration_id = int(callback.data.split("_")[1])

    # Запрашиваем причину отказа
    await callback.message.edit_text("Укажите причину отказа:")

    # Обработчик сообщения с причиной отказа
    @router.message(BloggerIntegrationStates.waiting_for_rejection_reason)
    async def process_rejection_reason(message: Message, state: FSMContext):
        rejection_reason = message.text

        # Обновляем статус интеграции на "Отказана" и добавляем причину
        integration = await IntegrationDAO.get_one_or_none(id=integration_id)
        if integration:
            await IntegrationDAO.update_integration_status(
                integration_id, "rejected", rejection_reason
            )
            await message.answer(f"Интеграция отклонена по причине: {rejection_reason}")
        else:
            await message.answer("Интеграция не найдена.")

        # Очищаем состояние
        await state.clear()
