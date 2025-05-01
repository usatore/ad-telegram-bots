from pydantic_settings import BaseSettings, SettingsConfigDict
from app.logger import logger


class Settings(BaseSettings):
    COMPANY_BOT_TOKEN: str
    BLOGGER_BOT_TOKEN: str

    ADMIN_CHAT_ID: int
    ADMIN_IDS: list[int]

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    LOG_LEVEL: str

    REDIS_HOST: str
    REDIS_PORT: int

    @property
    def DB_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


try:
    settings = Settings()
    logger.info("✅ Настройки успешно загружены из .env")
    logger.debug(f"DB_HOST: {settings.DB_HOST}, DB_PORT: {settings.DB_PORT}")
    logger.debug(
        f"REDIS_HOST: {settings.REDIS_HOST}, REDIS_PORT: {settings.REDIS_PORT}"
    )
    logger.debug(f"ADMIN_CHAT_ID: {settings.ADMIN_CHAT_ID}")
    logger.debug(f"ADMIN_IDS: {settings.ADMIN_IDS}")
except Exception:
    logger.exception("❌ Ошибка при загрузке настроек из .env")
    raise
