import asyncio
from aiogram import Bot, Dispatcher
from app.config import settings
from aiogram.fsm.storage.redis import RedisStorage, Redis


redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True)
storage = RedisStorage(redis=redis)


async def main():

    bot = Bot(token=settings.COMPANY_BOT_TOKEN)

    dp = Dispatcher(storage=storage)

    #dp.include_router(router_user)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())
