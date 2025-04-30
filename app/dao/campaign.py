from app.dao.base import BaseDAO
from app.models import Campaign, Company, Integration
from app.database import async_session_maker
from app.dao.utils import dao_exception_handler
from sqlalchemy import select


class CampaignDAO(BaseDAO):
    model = Campaign

    @classmethod
    @dao_exception_handler(model)
    async def create_campaign(
        cls,
        company_id: int,
        description: dict,
        view_price: int,
    ):
        """
        Создаёт новую кампанию, если у компании положительный баланс.

        Используется при создании рекламной кампании через Telegram-бот.
        """
        async with async_session_maker() as session:
            company = await session.get(Company, company_id)
            if not company:
                raise ValueError("Company not found")
            if company.money_balance <= 0:
                raise ValueError("Insufficient balance to create a campaign")

            new_campaign = Campaign(
                company_id=company_id, description=description, view_price=view_price
            )
            session.add(new_campaign)
            await session.commit()
            return new_campaign

    @classmethod
    @dao_exception_handler(model)
    async def approve_campaign(cls, campaign_id: int):
        """
        Утверждает кампанию, устанавливая ей approved = True.

        Используется администратором в Telegram-боте для ручного одобрения.
        """
        async with async_session_maker() as session:
            campaign = await session.get(Campaign, campaign_id)
            if campaign:
                campaign.approved = True
            await session.commit()
            return campaign

    @classmethod
    @dao_exception_handler(model)
    async def get_approved_campaigns_not_joined_by_blogger(cls, blogger_id: int):
        """
        Возвращает список утверждённых кампаний, в которых
        блоггер ещё не участвовал (нет интеграции).

        Используется в Telegram-боте, чтобы показать блоггеру только доступные кампании.
        """
        async with async_session_maker() as session:
            subquery = select(Integration.campaign_id).filter(
                Integration.blogger_id == blogger_id
            )

            query = (
                select(Campaign)
                .filter(Campaign.approved == True)
                .filter(Campaign.id.not_in(subquery))
            )

            result = await session.execute(query)
            return result.scalars().all()
