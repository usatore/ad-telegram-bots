import logging
from app.config import settings

logger = logging.getLogger('app')
logger.setLevel(settings.LOG_LEVEL)

logHandler = logging.StreamHandler()
formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
