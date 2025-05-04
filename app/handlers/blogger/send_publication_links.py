from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from app.states.blogger import BloggerSendPublicationLinks
from app.config import settings
from app.dao.integration import IntegrationDAO
from app.dao.blogger import BloggerDAO
from app.dao.campaign import CampaignDAO
from app.messages.admin_chat import create_publication_links_admin_message


router = Router()


@router.callback_query(F.data.startswith("send_publication_links:"))
async def send_publication_links(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    integration_id = int(callback.data.split(":")[1])

    await state.set_state(BloggerSendPublicationLinks.waiting_for_publication_links)
    await state.update_data(integration_id=integration_id)

    await callback.message.answer(
        "Пожалуйста, отправьте ссылки на публикации (одним сообщением)."
    )


@router.message(BloggerSendPublicationLinks.waiting_for_publication_links)
async def process_publication_links(message: Message, state: FSMContext, bot: Bot):
    """Обрабатывает отправленные блоггером ссылки на публикации."""
    data = await state.get_data()
    integration_id = data.get("integration_id")

    if not integration_id:
        await message.answer(
            "Ошибка: не удалось найти ID интеграции. Попробуйте снова."
        )
        return

    links_list = [
        line.strip() for line in message.text.strip().splitlines() if line.strip()
    ]

    # Сохраняем список в базу
    await IntegrationDAO.update_publication_links(integration_id, links_list)

    integration = await IntegrationDAO.get_one_or_none(id=integration_id)
    blogger = await BloggerDAO.get_one_or_none(id=integration.blogger_id)
    campaign = await CampaignDAO.get_one_or_none(id=integration.campaign_id)

    description = campaign.description if campaign else {}
    materials = integration.materials if integration else {}
    views_count = integration.views_count if integration else 0

    admin_text, admin_markup = create_publication_links_admin_message(
        username=message.from_user.username,
        full_name=message.from_user.full_name,
        integration_id=integration_id,
        campaign_id=campaign.id if campaign else 0,
        description=description,
        materials=materials,
        publication_links=links_list,
        views_count=views_count,
    )

    await bot.send_message(
        chat_id=settings.ADMIN_CHAT_ID, text=admin_text, reply_markup=admin_markup
    )

    await message.answer("Ссылки отправлены на проверку администратору.")
    await state.clear()
