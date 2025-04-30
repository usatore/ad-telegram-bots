from app.models import BloggerTransaction
from app.dao.base import BaseDAO


class BloggerTransactionDAO(BaseDAO):
    model = BloggerTransaction
