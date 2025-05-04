from aiogram import Bot, Dispatcher
from app.config import settings
from app.storage import company_storage
import asyncio
from app.logger import logger

# Импорт всех роутеров компании
from app.handlers.company.main_menu import router as router_company_main_menu
from app.handlers.company.get_campaigns import router as router_company_get_campaigns
from app.handlers.company.create_campaign import router as router_company_create_campaign
from app.handlers.company.balance import router as router_company_balance
from app.handlers.company.admin_chat.new_campaign import router as router_company_new_campaign
from app.handlers.company.add_deposit import router as router_company_add_deposit
from app.handlers.company.admin_chat.new_deposit import router as router_company_new_deposit


async def run_company_bot():
    try:
        bot = Bot(token=settings.COMPANY_BOT_TOKEN)
        dp = Dispatcher(storage=company_storage)

        logger.info("🚀 Подключение роутеров компании...")
        dp.include_routers(
            router_company_main_menu,
            router_company_get_campaigns,
            router_company_create_campaign,
            router_company_new_campaign,
            router_company_add_deposit,
            router_company_balance,
            router_company_new_deposit,
        )
        logger.info("✅ Роутеры компании успешно подключены.")

        logger.info("Запуск опроса бота...")
        await dp.start_polling(bot)
        logger.info("✅ Опрос бота запущен.")
    except Exception as e:
        logger.exception("❌ Ошибка при запуске бота")
        raise


if __name__ == "__main__":
    logger.info("Запуск бота...")
    asyncio.run(run_company_bot())
    logger.info("🚨 Бот завершил работу.")
