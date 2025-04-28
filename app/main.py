import asyncio
from aiogram import Bot, Dispatcher
from app.config import settings
from app.handlers.user_handlers import router as router_user


async def main():

    bot = Bot(
        token=settings.BOT_TOKEN
    )

    dp = Dispatcher()

    dp.include_router(router_user)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

asyncio.run(main())