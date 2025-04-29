from sqlalchemy import select
from app.database import async_session_maker
from app.dao.utils import dao_exception_handler

class BaseDAO:
    model = None

    @classmethod
    @dao_exception_handler(model)
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:

            query = select(cls.model).filter_by(**filter_by)
        #   query = select(cls.model.__table__.columns).filter_by(**filter_by)

            result = await session.execute(query)

        #   return result.mappings().all()
            return result.scalars().all()


    @classmethod
    @dao_exception_handler(model)
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:

            query = select(cls.model).filter_by(**filter_by)
        #   query = select(cls.model.__table__.columns).filter_by(**filter_by)

            result = await session.execute(query)

        #   return result.mappings().one_or_none()
            return result.scalars().one_or_none()
