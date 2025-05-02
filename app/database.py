from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from app.config import settings
from app.logger import logger


logger.info("Подключение к базе данных...")
try:
    engine = create_async_engine(settings.DB_URL, echo=True)  # echo=True для SQL-логов
    async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
    logger.info(
        f"✅ Успешное подключение к базе данных: {settings.DB_HOST}:{settings.DB_PORT}"
    )
except Exception as e:
    logger.exception("❌ Ошибка при подключении к базе данных")
    raise


class Base(DeclarativeBase):
    pass
