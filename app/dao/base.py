from sqlalchemy import select, delete
from app.database import async_session_maker
from app.dao.utils import dao_exception_handler


class BaseDAO:
    model = None

    @classmethod
    @dao_exception_handler(model)
    async def get_all(cls, **filter_by):
        async with async_session_maker() as session:

            query = select(cls.model).filter_by(**filter_by)
            #   query = select(cls.model.__table__.columns).filter_by(**filter_by)

            result = await session.execute(query)

            # return result.mappings().all()
            return result.scalars().all()

    @classmethod
    @dao_exception_handler(model)
    async def get_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:

            query = select(cls.model).filter_by(**filter_by)
            #   query = select(cls.model.__table__.columns).filter_by(**filter_by)

            result = await session.execute(query)

            #   return result.mappings().one_or_none()
            return result.scalars().one_or_none()

    @classmethod
    @dao_exception_handler(model)
    async def delete(cls, **filter_by):
        """
        Удаляет запись из таблицы на основе фильтров.
        Если запись не найдена, возвращает None.
        """
        async with async_session_maker() as session:
            # Получаем первую запись по фильтрам
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            record = result.scalars().first()

            if not record:
                return None  # Если записи нет, возвращаем None

            # Удаляем запись из базы данных
            delete_query = delete(cls.model).filter_by(**filter_by)
            await session.execute(delete_query)
            await session.commit()  # Коммитим транзакцию

            return record  # Возвращаем (первую) удаленную запись, (удаляются все отфильтрованные))
