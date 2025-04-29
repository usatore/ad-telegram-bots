from app.dao.base import BaseDAO
from app.models import Blogger
from app.database import async_session_maker
from app.dao.utils import dao_exception_handler
from sqlalchemy import select


class CompanyDAO(BaseDAO):
    model = Blogger

    @classmethod
    @dao_exception_handler(model)
    async def create_blogger(
            cls,
            telegram_id: int,
            profile_links: list,
    ):

        async with async_session_maker() as session: