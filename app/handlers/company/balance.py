from app.dao.company import CompanyDAO
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import CommandStart
from app.keyboards.company.balance_menu import get_balance_menu_keyboard

router = Router()

@router.callback_query(F.data == "balance_menu")
async def get_balance_menu(callback: CallbackQuery):
    await callback.answer()

    company = await CompanyDAO.get_one_or_none(telegram_id=callback.from_user.id)
    if not company:
        await callback.message.answer("Компания не найдена.")
        return

    await callback.message.edit_text(
        text="\u2063",
        reply_markup=get_balance_menu_keyboard(balance=company.money_balance, company_id=company.id),
    )