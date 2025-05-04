from aiogram import Bot, Dispatcher
from app.config import settings
import asyncio
from app.storage import blogger_storage
from app.logger import logger

# Импорт всех роутеров блогера
from app.handlers.blogger.admin_chat.new_blogger import (
    router as router_blogger_admin_chat_new_blogger,
)
from app.handlers.blogger.admin_chat.new_integration import (
    router as router_blogger_admin_chat_new_integration,
)
from app.handlers.blogger.create_profile import router as router_blogger_create_profile
from app.handlers.blogger.main_menu import router as router_blogger_main_menu
from app.handlers.blogger.get_campaigns import router as router_blogger_get_campaigns
from app.handlers.blogger.create_integration import (
    router as router_blogger_create_integration,
)
from app.handlers.blogger.get_integrations import (
    router as router_blogger_get_integrations,
)
from app.handlers.blogger.send_publication_links import (
    router as router_blogger_send_publication_links,
)


async def run_blogger_bot():
    try:
        bot = Bot(token=settings.BLOGGER_BOT_TOKEN)
        dp = Dispatcher(storage=blogger_storage)

        logger.info("🚀 Подключение роутеров блогера...")
        dp.include_routers(
            router_blogger_admin_chat_new_blogger,
            router_blogger_admin_chat_new_integration,
            router_blogger_create_profile,
            router_blogger_main_menu,
            router_blogger_get_campaigns,
            router_blogger_create_integration,
            router_blogger_get_integrations,
            router_blogger_send_publication_links,
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
