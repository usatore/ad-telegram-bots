from functools import wraps

from sqlalchemy.exc import SQLAlchemyError

from app.logger import logger


def dao_exception_handler(model):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except SQLAlchemyError:
                msg = "Database Exc: Cannot perform operation"
                logger.error(msg, extra={"table": model.__tablename__}, exc_info=True)
                return None
            except Exception:
                msg = "Unknown Exc: Cannot perform operation"
                logger.error(msg, extra={"table": model.__tablename__}, exc_info=True)
                return None

        return wrapper

    return decorator


# Надо ловить ошибки чтобы было понятно какие
