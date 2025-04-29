from app.dao.base import BaseDAO
from app.models import BloggerTransaction, CompanyTransaction
from app.database import async_session_maker
from app.dao.utils import dao_exception_handler
from sqlalchemy import select


class CompanyTransactionDAO(BaseDAO):
    model = CompanyTransaction


class BloggerTransactionDAO(BaseDAO):
    model = BloggerTransaction