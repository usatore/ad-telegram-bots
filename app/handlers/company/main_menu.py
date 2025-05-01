# app/handlers/company/main_menu.py
from app.dao.company import CompanyDAO
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from app.keyboards.company.main_menu import get_main_menu_keyboard  # Импортируем клавиатуру main_menu

router = Router()


@router.message(CommandStart())
async def process_command_start_for_company(message: Message):
    # Получаем компанию или None, если она не существует
    company = await CompanyDAO.get_one_or_none(telegram_id=message.from_user.id)

    if not company:
        company = await CompanyDAO.create_company(telegram_id=message.from_user.id)

    await message.answer(
    "Добро пожаловать в компанию-бот! Здесь вы можете создать рекламную кампанию или управлять существующими.",
    reply_markup = get_main_menu_keyboard(company_id=company.id))
