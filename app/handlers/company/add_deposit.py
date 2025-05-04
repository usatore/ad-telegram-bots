from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.config import settings
from app.dao.company import CompanyDAO
from app.dao.company_transaction import CompanyTransactionDAO
from app.messages.new_deposit import create_deposit_admin_message
from app.states.company import CompanyAddDeposit

router = Router()


@router.callback_query(F.data == "add_deposit")
async def process_add_deposit(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    # Показываем инструкцию по оплате
    await callback.message.answer(
        "💸 *Пополнение баланса*\n\n"
        "Пожалуйста, переведите деньги по следующим реквизитам:\n"
        "`0000 1111 2222 3333`\n\n"
        "После оплаты введите сумму, которую вы отправили:",
        parse_mode="Markdown",
    )

    await state.set_state(CompanyAddDeposit.waiting_for_deposit_amount)


@router.message(CompanyAddDeposit.waiting_for_deposit_amount)
async def process_deposit_amount(message: Message, state: FSMContext):
    try:
        deposit_amount = int(message.text)
        if deposit_amount <= 0:
            raise ValueError
    except ValueError:
        await message.answer("❌ Пожалуйста, введите корректную сумму целым числом")
        return

    company = await CompanyDAO.get_one_or_none(telegram_id=message.from_user.id)
    if not company:
        await message.answer("❌ Компания не найдена.")
        await state.clear()
        return

    deposit = await CompanyTransactionDAO.add_deposit(
        company_id=company.id, money_amount=deposit_amount
    )

    admin_text, admin_markup = create_deposit_admin_message(
        company_transaction_id=deposit.id,
        company_id=company.id,
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        full_name=message.from_user.full_name,
        deposit_amount=deposit_amount,
    )

    await message.bot.send_message(
        chat_id=settings.ADMIN_CHAT_ID, text=admin_text, reply_markup=admin_markup
    )

    # Очищаем состояние
    await state.clear()
