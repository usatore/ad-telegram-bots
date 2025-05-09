from sqlalchemy import select

from app.dao.base import BaseDAO
from app.dao.utils import dao_exception_handler
from app.database import async_session_maker
from app.models import Company


class CompanyDAO(BaseDAO):
    model = Company

    @classmethod
    @dao_exception_handler(model)
    async def create_company(cls, telegram_id: int):

        async with async_session_maker() as session:
            query = select(cls.model).filter_by(telegram_id=telegram_id)
            result = await session.execute(query)

            """
            Добавили проверку на это в хенлере commandstart для компаний
            existing_company = result.scalars().first()
            if existing_company:
                raise ValueError("Company with this telegram_id already exists")
            """

            new_company = cls.model(telegram_id=telegram_id)
            session.add(new_company)
            await session.commit()
            return new_company
