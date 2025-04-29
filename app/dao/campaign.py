from app.dao.base import BaseDAO
from app.models import Campaign, Company
from app.database import async_session_maker
from app.dao.utils import dao_exception_handler

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
        async with async_session_maker() as session:
            company = await session.get(Company, company_id)
            if not company:
                raise ValueError("Company not found")
            if company.money_balance <= 0:
                raise ValueError("Insufficient balance to create a campaign")

            new_campaign = Campaign(
                company_id=company_id,
                description=description,
                view_price=view_price
            )
            session.add(new_campaign)
            await session.commit()
            return new_campaign



    @classmethod
    @dao_exception_handler(model)
    async def approve_campaign(cls, campaign_id: int):
        async with async_session_maker() as session:
            pass
