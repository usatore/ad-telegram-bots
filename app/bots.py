import asyncio
from aiogram import Bot, Dispatcher
from app.config import settings
from app.storage import company_storage, blogger_storage
from app.handlers.company.main_menu import router as router_company_main_menu
from app.handlers.blogger.admin_chat import router as router_blogger_admin_chat
from app.handlers.blogger.create_profile import router as router_blogger_create_profile
from app.handlers.blogger.main_menu import router as router_blogger_main_menu


async def run_company_bot():
    bot = Bot(token=settings.COMPANY_BOT_TOKEN)

    dp = Dispatcher(storage=company_storage)

    dp.include_router(router_company_main_menu)

    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot)


async def run_blogger_bot():
    bot = Bot(token=settings.BLOGGER_BOT_TOKEN)

    dp = Dispatcher(
        storage=blogger_storage
    )

    dp.include_router(router_blogger_admin_chat)
    dp.include_router(router_blogger_create_profile)
    dp.include_router(router_blogger_main_menu)

    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot)
