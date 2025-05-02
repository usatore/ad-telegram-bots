from app.dao.company import CompanyDAO
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, CallbackQuery
from aiogram.filters import CommandStart
from app.keyboards.company.main_menu import get_main_menu_keyboard

router = Router()

@router.callback_query(F.data == "main_menu")
async def on_main_menu_callback(callback: CallbackQuery):
    await callback.answer()

    company = await CompanyDAO.get_one_or_none(telegram_id=callback.from_user.id)
    if not company:
        await callback.answer("Компания не найдена.", show_alert=True)
        return

    await callback.message.edit_text(
        text="\u2063",
        reply_markup=get_main_menu_keyboard(balance=company.money_balance, company_id=company.id),
    )


@router.message(F.text == "Главное меню")
async def get_main_menu(message: Message):

    await message.delete()

    company = await CompanyDAO.get_one_or_none(telegram_id=message.from_user.id)
    if not company:
        await message.answer("Компания не найдена.")
        return

    await message.answer(
        text="\u2063",
        reply_markup=get_main_menu_keyboard(balance=company.money_balance, company_id=company.id),
    )

@router.message(CommandStart())
async def process_command_start(message: Message):
    # Получаем компанию или None, если она не существует
    company = await CompanyDAO.get_one_or_none(telegram_id=message.from_user.id)

    if not company:
        company = await CompanyDAO.create_company(telegram_id=message.from_user.id)

    main_menu_keyboard = [[KeyboardButton(text="Главное меню")]]


    # Создаём обычную клавиатуру с кнопкой "Главное меню"
    reply_keyboard = ReplyKeyboardMarkup(
        keyboard=main_menu_keyboard,
        resize_keyboard=True,
        row_width=1
    )


    # Ответ пользователю
    await message.answer(
        "👋 Добро пожаловать в компанию-бот!\nЗдесь вы можете создать рекламную кампанию или управлять существующими.",
        reply_markup=reply_keyboard
    )