from app.dao.base import BaseDAO
from app.models import Integration, Blogger, Campaign
from app.database import async_session_maker
from app.dao.utils import dao_exception_handler
from sqlalchemy import select


class IntegrationDAO(BaseDAO):
    model = Integration

    @classmethod
    @dao_exception_handler(Integration)
    async def create_integration(
        cls,
        blogger_id: int,
        campaign_id: int,
        materials: dict,
    ):
        """
        Создаёт интеграцию между блоггером и кампанией.
        Устанавливает связь между блоггером и кампанией с указанными публикациями.
        """
        async with async_session_maker() as session:
            # Проверяем, существует ли блоггер
            blogger = await session.get(Blogger, blogger_id)
            if not blogger:
                raise ValueError("Blogger not found")

            # Проверяем, существует ли кампания
            campaign = await session.get(Campaign, campaign_id)
            if not campaign:
                raise ValueError("Campaign not found")

            # Проверяем, не существует ли уже интеграция
            existing_integration = await session.execute(
                select(Integration).filter(
                    Integration.blogger_id == blogger_id,
                    Integration.campaign_id == campaign_id,
                )
            )
            if existing_integration.scalars().first():
                raise ValueError("Integration already exists")

            # Создаем новую интеграцию
            new_integration = Integration(
                blogger_id=blogger_id,
                campaign_id=campaign_id,
                materials=materials,
            )

            session.add(new_integration)
            await session.commit()
            return new_integration

    @classmethod
    @dao_exception_handler(Integration)
    async def approve_integration_materials(cls, integration_id: int):
        """
        Утверждает интеграцию.
        """
        async with async_session_maker() as session:
            integration = await session.get(Integration, integration_id)
            if not integration:
                raise ValueError("Integration not found")

            if integration.approved:
                raise ValueError("Integration materials already approved")

            # Утверждаем интеграцию (в смысле материалы)
            integration.approved = True
            await session.commit()
            return integration

    @classmethod
    @dao_exception_handler(Integration)
    async def approve_integration_is_done(cls, integration_id: int):
        """
        Подтверждает, что блоггер выполнил интеграцию (опубликовал контент).
        Устанавливает флаг done = True.
        """
        async with async_session_maker() as session:
            integration = await session.get(Integration, integration_id)
            if not integration:
                raise ValueError("Integration not found")

            if not integration.approved:
                raise ValueError("Materials not yet approved")

            if integration.done:
                raise ValueError("Integration already marked as done")

            integration.done = True
            await session.commit()
            return integration

    @classmethod
    @dao_exception_handler(Integration)
    async def update_materials(cls, integration_id: int, materials: dict):
        """
        Обновляет материалы у интеграции.
        """
        async with async_session_maker() as session:
            integration = await session.get(Integration, integration_id)
            if integration:
                integration.materials = materials
                await session.commit()
            return integration

'''
    @classmethod
    @dao_exception_handler(Integration)
    async def get_integrations_for_blogger(cls, blogger_id: int):
        """
        Возвращает все интеграции для конкретного блоггера.
        """
        async with async_session_maker() as session:
            integrations = await session.execute(
                select(Integration).filter(Integration.blogger_id == blogger_id)
            )
            return integrations.scalars().all()


 Думаю, что не приходится так как можно использовать get_all(**filter_by).
Но если функционал расширится то пригодится.

    @classmethod
    @dao_exception_handler(Integration)
    async def get_integrations_for_campaign(cls, campaign_id: int):
        """
        Возвращает все интеграции для конкретной кампании.
        """
        async with async_session_maker() as session:
            integrations = await session.execute(
                select(Integration).filter(Integration.campaign_id == campaign_id)
            )
            return integrations.scalars().all()
'''
