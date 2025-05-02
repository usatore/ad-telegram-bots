from app.dao.company import CompanyDAO
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import CommandStart
from app.keyboards.company.main_menu import get_main_menu_keyboard


router = Router()

@router.callback_query(F.data == "main_menu")
async def get_main_menu(callback: CallbackQuery):
    await callback.answer()

    # Получаем компанию из БД
    company = await CompanyDAO.get_one_or_none(telegram_id=callback.from_user.id)
    if not company:
        await callback.message.answer("Компания не найдена.")
        return

    # Отправляем новое сообщение с главным меню
    await callback.message.edit_text(
        text="\u2063",
        reply_markup=get_main_menu_keyboard(balance=company.money_balance, company_id=company.id),
    )



@router.message(CommandStart())
async def process_command_start(message: Message):

    # Получаем компанию или None, если она не существует
    company = await CompanyDAO.get_one_or_none(telegram_id=message.from_user.id)

    if not company:
        print(f"Компания с telegram_id={message.from_user.id} не найдена, создаем новую.")
        company = await CompanyDAO.create_company(telegram_id=message.from_user.id)

    # Ответ пользователю
    await message.answer(
        "👋 Добро пожаловать в компанию-бот!\nЗдесь вы можете создать рекламную кампанию или управлять существующими.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")]
        ])
    )



