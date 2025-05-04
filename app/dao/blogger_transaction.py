from app.dao.base import BaseDAO
from app.models import BloggerTransaction


class BloggerTransactionDAO(BaseDAO):
    model = BloggerTransaction
