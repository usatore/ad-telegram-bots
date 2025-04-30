import asyncio
from aiogram import Bot, Dispatcher
from app.config import settings
from app.storage import company_storage, blogger_storage
from app.handlers.campaign_creation_handlers import router as router_campaign_creation


async def main():

    bot = Bot(token=settings.COMPANY_BOT_TOKEN)

    dp = Dispatcher(storage=company_storage)

    dp.include_router(router_campaign_creation)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())
