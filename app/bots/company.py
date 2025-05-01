from aiogram import Bot, Dispatcher
from app.config import settings
from app.storage import company_storage
import asyncio

# Импорт всех роутеров компании
from app.handlers.company.main_menu import router as router_company_main_menu
from app.handlers.company.get_campaigns import router as router_company_get_campaigns
from app.handlers.company.create_campaign import (
    router as router_company_create_campaign,
)
from app.handlers.company.admin_chat import router as router_company_admin_chat


async def run_company_bot():
    bot = Bot(token=settings.COMPANY_BOT_TOKEN)
    dp = Dispatcher(storage=company_storage)

    dp.include_routers(
        router_company_main_menu,
        router_company_get_campaigns,
        router_company_create_campaign,
        router_company_admin_chat,
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(run_company_bot())
