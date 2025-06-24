import logging
from logging import Logger
from logging.config import dictConfig

from app.core.config import settings

LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] %(levelname)s \
                  in %(module)s:%(lineno)d - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": settings.LOG_LEVEL,
            "stream": "ext://sys.stdout",
        }
    },
    "root": {
        "handlers": ["console"],
        "level": settings.LOG_LEVEL,
    },
}


def setup_logging() -> None:
    dictConfig(LOG_CONFIG)

    for uvicorn_logger in ("uvicorn", "uvicorn.error", "uvicorn.access"):
        logger = logging.getLogger(uvicorn_logger)
        logger.handlers = []
        logger.propagate = True


def get_logger(name: str) -> Logger:
    return logging.getLogger(name)


setup_logging()
