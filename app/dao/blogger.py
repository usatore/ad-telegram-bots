from app.dao.base import BaseDAO
from app.models import Blogger
from app.database import async_session_maker
from app.dao.utils import dao_exception_handler
from sqlalchemy import select


class BloggerDAO(BaseDAO):
    model = Blogger

    @classmethod
    @dao_exception_handler(model)
    async def create_blogger(cls, telegram_id: int, profile_links: list):
        """
        Создаёт блоггера с указанным Telegram ID и ссылками на профили.
        """
        async with async_session_maker() as session:
            # Проверяем, существует ли блоггер с таким Telegram ID
            existing_blogger = await session.execute(
                select(cls.model).filter_by(telegram_id=telegram_id)
            )
            if existing_blogger.scalars().first():
                raise ValueError(
                    f"Blogger with telegram_id {telegram_id} already exists"
                )

            # Создаём нового блоггера
            new_blogger = Blogger(telegram_id=telegram_id, profile_links=profile_links)
            session.add(new_blogger)
            await session.commit()
            # await session.refresh(new_blogger)
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
    async def update_blogger_profile_links(
        cls, blogger_id: int, new_profile_links: list
    ):
        """
        Обновляет профили блоггера по его ID.
        """
        async with async_session_maker() as session:
            blogger = await session.get(Blogger, blogger_id)
            if not blogger:
                raise ValueError(f"Blogger with id {blogger_id} not found")

            blogger.profile_links = new_profile_links
            await session.commit()
            return blogger
