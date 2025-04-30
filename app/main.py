import asyncio
from aiogram import Bot, Dispatcher
from app.config import settings



async def main():

    bot = Bot(
        token=settings.COMPANY_BOT_TOKEN
    )

    dp = Dispatcher()

    dp.include_router(router_user)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

asyncio.run(main())