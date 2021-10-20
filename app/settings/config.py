import logging
import os
import pathlib
import sys

from loguru import logger

from app.settings.logging_config import InterceptHandler

ROOT_APP = str(pathlib.Path(__file__).parent.absolute().parent)

APPLICATION = {
    "version": "1.0.0",
    "project_name": os.getenv("PROJECT_NAME", "CRM"),
    "secret_key": os.getenv("SECRET_KEY", ""),
    "debug": bool(os.getenv("DEBUG", True)),
    "allowed_hosts": list(os.getenv("ALLOWED_HOSTS", ["*"])),
}

DATETIME_INPUT_OUTPUT_FORMAT = '%Y-%m-%d %H:%M:%S'

DATE_INPUT_OUTPUT_FORMAT = '%Y-%m-%d'

TIME_INPUT_OUTPUT_FORMAT = '%H:%M:%S'

# logging configuration
LOGGING_LEVEL = logging.DEBUG if APPLICATION["debug"] else logging.INFO
LOGGERS = ("uvicorn.asgi", "uvicorn.access", "sqlalchemy.engine")  # noqa
logger.level("CUSTOM", no=15, color="<blue>", icon="@")
logger.level("SERVICE", no=200)

logging.getLogger().handlers = [InterceptHandler()]
# logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
for logger_name in LOGGERS:
    logging_logger = logging.getLogger(logger_name)
    logging_logger.handlers = [InterceptHandler(level=LOGGING_LEVEL)]

logger.configure(
    handlers=[
        {"sink": sys.stderr, "level": LOGGING_LEVEL},
        {
            "sink": sys.stderr,
            "level": 200,
            "format": "<blue>{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}</blue>",
        },
    ]
)
