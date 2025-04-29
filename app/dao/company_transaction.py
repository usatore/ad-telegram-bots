from app.dao.base import BaseDAO
from app.models import BloggerTransaction, CompanyTransaction, Company
from app.database import async_session_maker
from app.dao.utils import dao_exception_handler
from sqlalchemy import select
from datetime import datetime


class CompanyTransactionDAO(BaseDAO):
    model = CompanyTransaction

    @classmethod
    @dao_exception_handler(CompanyTransaction)
    async def create_deposit(cls, company_id: int, money_amount: int):
        """
        Создаёт транзакцию на пополнение баланса компании.
        Баланс изменится только после одобрения транзакции.
        """
        async with async_session_maker() as session:
            new_transaction = CompanyTransaction(
                company_id=company_id,
                money_amount=money_amount,
                transaction_type=True,  # True — пополнение (deposit)
            )
            session.add(new_transaction)
            await session.commit()
            return new_transaction

    @classmethod
    @dao_exception_handler(CompanyTransaction)
    async def approve_deposit(cls, transaction_id: int):
        """
        Одобряет пополнение счёта компании.
        """
        async with async_session_maker() as session:
            transaction = await session.get(CompanyTransaction, transaction_id)
            if not transaction:
                raise ValueError("Transaction not found")

            if not transaction.transaction_type:
                raise ValueError("Only deposit transactions can be approved")

            if transaction.approved:
                raise ValueError("Transaction already approved")

            company = await session.get(Company, transaction.company_id)
            if not company:
                raise ValueError("Company not found")

            # Применяем пополнение
            company.money_balance += transaction.money_amount
            transaction.approved = True

            await session.commit()
            return transaction



