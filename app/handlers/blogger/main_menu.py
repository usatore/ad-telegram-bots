from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart

from app.dao.blogger import BloggerDAO
from app.keyboards.blogger.main_menu import get_main_menu_keyboard

router = Router()


@router.callback_query(F.data == "main_menu")
async def on_main_menu_callback(callback: CallbackQuery):
    await callback.answer()

    blogger = await BloggerDAO.get_one_or_none(telegram_id=callback.from_user.id)
    if not blogger:
        await callback.answer("Блогер не найден.", show_alert=True)
        return

    await callback.message.edit_text(
        text="\u2063",
        reply_markup=get_main_menu_keyboard(balance=1337),
    )


@router.message(F.text == "Главное меню")
async def get_main_menu(message: Message):
    await message.delete()


    await message.answer(
        text="\u2063",
        reply_markup=get_main_menu_keyboard(balance=1337),
    )


@router.message(CommandStart())
async def process_command_start(message: Message):
    #blogger = await BloggerDAO.get_one_or_none(telegram_id=message.from_user.id)
    #if not blogger:
        #blogger = await BloggerDAO.create(telegram_id=message.from_user.id)

    main_menu_keyboard = [[KeyboardButton(text="Главное меню")]]

    reply_keyboard = ReplyKeyboardMarkup(
        keyboard=main_menu_keyboard,
        resize_keyboard=True,
        row_width=1,
    )

    await message.answer(
        "👋 Добро пожаловать в бот-блогера!\nВы можете найти кампании, создавать интеграции и зарабатывать.",
        reply_markup=reply_keyboard,
    )
