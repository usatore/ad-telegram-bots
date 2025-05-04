from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.dao.campaign import CampaignDAO
from app.dao.company import CompanyDAO
from app.dao.company_transaction import CompanyTransactionDAO
from app.messages.admin_chat import for_admin
from app.states.admin import AdminRejectCampaign

router = Router()


@router.callback_query(F.data.startswith("approve_deposit:"))
async def approve_deposit(callback: CallbackQuery, bot: Bot):
    company_transaction_id = int(callback.data.split(":")[1])

    # Получаем транзакцию
    deposit = await CompanyTransactionDAO.get_one_or_none(id=company_transaction_id)
    if not deposit:
        await callback.answer("❗ Транзакция не найдена.")
        return

    # Подтверждаем транзакцию
    await CompanyTransactionDAO.approve_deposit(transaction_id=company_transaction_id)

    company_id = deposit.company_id

    company = await CompanyDAO.get_one_or_none(id=company_id)

    # Уведомляем пользователя
    await bot.send_message(
        chat_id=company.telegram_id,
        text=f"✅ Ваше пополнение на сумму {deposit.money_amount} было подтверждено администратором",
    )

    await callback.answer("✅ Пополнение подтверждено.")
    await callback.message.edit_reply_markup()


@router.callback_query(F.data.startswith("reject_deposit:"))
async def reject_deposit(callback: CallbackQuery, bot: Bot):
    company_transaction_id = int(callback.data.split(":")[1])

    # Получаем транзакцию
    deposit = await CompanyTransactionDAO.get_one_or_none(id=company_transaction_id)
    if not deposit:
        await callback.answer("❗ Транзакция не найдена.")
        return

    # Получаем компанию по ID (чтобы не использовать ленивую загрузку)
    company = await CompanyDAO.get_one_or_none(id=deposit.company_id)

    # Удаляем транзакцию
    await CompanyTransactionDAO.delete(id=company_transaction_id)

    # Уведомляем пользователя
    await bot.send_message(
        chat_id=company.telegram_id,
        text=f"❌ Ваше пополнение на сумму {deposit.money_amount} было отклонено администратором.",
    )

    await callback.answer("❌ Пополнение отклонено.")
    await callback.message.edit_reply_markup()
