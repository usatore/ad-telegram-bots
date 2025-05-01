from aiogram import Bot, Dispatcher
from app.config import settings
import asyncio
from app.storage import blogger_storage

# Импорт всех роутеров блогера
from app.handlers.blogger.admin_chat import router as router_blogger_admin_chat
from app.handlers.blogger.create_profile import router as router_blogger_create_profile
from app.handlers.blogger.main_menu import router as router_blogger_main_menu
from app.handlers.blogger.get_campaigns import router as router_blogger_get_campaigns


async def run_blogger_bot():
    bot = Bot(token=settings.BLOGGER_BOT_TOKEN)
    dp = Dispatcher(storage=blogger_storage)

    dp.include_routers(
        router_blogger_admin_chat,
        router_blogger_create_profile,
        router_blogger_main_menu,
        router_blogger_get_campaigns,
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__=='__main__':
    asyncio.run(run_blogger_bot())