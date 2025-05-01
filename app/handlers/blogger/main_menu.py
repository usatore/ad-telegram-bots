from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart

router = Router()


@router.message(CommandStart())
async def process_command_start(message: Message):
    await message.answer(
        "Добро пожаловать в блоггер-бот! Здесь вы можете создать рекламную кампанию или управлять существующими."
    )
