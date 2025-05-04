from aiogram.fsm.storage.redis import DefaultKeyBuilder, Redis, RedisStorage

from app.config import settings

company_redis = Redis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=1, decode_responses=True
)
blogger_redis = Redis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=2, decode_responses=True
)

company_storage = RedisStorage(
    company_redis, key_builder=DefaultKeyBuilder(prefix="company")
)
blogger_storage = RedisStorage(
    blogger_redis, key_builder=DefaultKeyBuilder(prefix="blogger")
)
