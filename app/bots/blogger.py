from aiogram import Bot, Dispatcher
from app.config import settings
import asyncio
from app.storage import blogger_storage
from app.logger import logger

# Импорт всех роутеров блогера
from app.handlers.blogger.admin_chat.new_blogger import router as router_blogger_admin_chat
from app.handlers.blogger.create_profile import router as router_blogger_create_profile
from app.handlers.blogger.main_menu import router as router_blogger_main_menu
from app.handlers.blogger.get_campaigns import router as router_blogger_get_campaigns
from app.handlers.blogger.create_integration import router as router_blogger_create_integration

async def run_blogger_bot():
    try:
        bot = Bot(token=settings.BLOGGER_BOT_TOKEN)
        dp = Dispatcher(storage=blogger_storage)


        logger.info("🚀 Подключение роутеров блогера...")
        dp.include_routers(
            router_blogger_admin_chat,
            router_blogger_create_profile,
            router_blogger_main_menu,
            router_blogger_get_campaigns,
            router_blogger_create_integration
        )
        logger.info("✅ Роутеры блогера успешно подключены.")


        logger.info("Запуск опроса бота...")
        await dp.start_polling(bot)
        logger.info("✅ Опрос бота запущен.")
    except Exception as e:
        logger.exception("❌ Ошибка при запуске бота")
        raise


if __name__ == "__main__":
    logger.info("Запуск бота...")
    asyncio.run(run_blogger_bot())
    logger.info("🚨 Бот завершил работу.")
