from sqlalchemy import select

from app.dao.base import BaseDAO
from app.dao.utils import dao_exception_handler
from app.database import async_session_maker
from app.models import Blogger


class BloggerDAO(BaseDAO):
    model = Blogger

    @classmethod
    @dao_exception_handler(model)
    async def create_blogger(cls, telegram_id: int,):

        async with async_session_maker() as session:

            new_blogger = Blogger(telegram_id=telegram_id)
            session.add(new_blogger)
            await session.commit()

            return new_blogger

    @classmethod
    @dao_exception_handler(model)
    async def approve_blogger(cls, blogger_id: int):
        """
        Аппрувит блоггера по ID (ставит approved=True если админ одобрил ссылки блоггера).
        """
        async with async_session_maker() as session:
            blogger = await session.get(cls.model, blogger_id)
            if blogger:
                blogger.approved = True
                await session.commit()
            return blogger

    @classmethod
    @dao_exception_handler(model)
    async def update_profile_links(cls, blogger_id: int, new_profile_links: list):
        """
        Обновляет профили блоггера по его ID и сбрасывает approved = False.
        """
        async with async_session_maker() as session:
            blogger = await session.get(Blogger, blogger_id)
            if not blogger:
                raise ValueError(f"Blogger with id {blogger_id} not found")

            blogger.profile_links = new_profile_links
            blogger.approved = False  # Меняем Статус на непроверенный админом
            await session.commit()
            return blogger

