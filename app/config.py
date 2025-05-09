from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    COMPANY_BOT_TOKEN: str
    BLOGGER_BOT_TOKEN: str

    ADMIN_CHAT_ID: int

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


settings = Settings()
