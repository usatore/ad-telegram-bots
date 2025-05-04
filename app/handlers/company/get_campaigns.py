from aiogram import Router, F
from aiogram.types import CallbackQuery
from app.dao.campaign import CampaignDAO
from app.dao.company import CompanyDAO
from app.dao.integration import IntegrationDAO

router = Router()

@router.callback_query(F.data == 'get_campaigns')
async def get_campaigns(callback: CallbackQuery):
    await callback.answer()

    company = await CompanyDAO.get_one_or_none(telegram_id=callback.from_user.id)
    if not company:
        await callback.message.answer("Компания не найдена.")
        return

    campaigns = await CampaignDAO.get_all(company_id=company.id)
    if not campaigns:
        await callback.message.answer("У вас пока нет созданных кампаний.")
        return

    for campaign in campaigns:
        # Описание кампании
        description_text = "\n".join(
            [f"🔑 {key}: {value}" for key, value in campaign.description.items()]
        )
        status = "✅ Одобрена" if campaign.approved else "⛔ Не одобрена"

        text = (
            f"🆔 Кампания ID: {campaign.id}\n"
            f"📄 Описание:\n{description_text}\n"
            f"💸 Цена за просмотр: {campaign.view_price} ₽\n"
            f"📊 Статус: {status}"
        )


        ''' # Ошибка с 'lazy', надо разобраться
        # Получаем интеграции по этой кампании
        integrations = await IntegrationDAO.get_all(campaign_id=campaign.id)

        if integrations:
            text += "\n\n🔗 Интеграции:\n"
            for integration in integrations:
                blogger = integration.blogger
                blogger_username = f"@{blogger.username}" if blogger.username else "—"
                status_icon = "✅ Done" if integration.done else "🟡 Approved"
                links = integration.publication_links or []
                links_text = "\n".join([f"🔗 {link}" for link in links]) if links else "—"

                text += (
                    f"\n👤 Блоггер ID: {blogger.id}, {blogger_username}\n"
                    f"📎 Статус: {status_icon}\n"
                    f"{links_text}\n"
                )
        '''

        await callback.message.answer(text)
