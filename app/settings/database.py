import json
import os

from loguru import logger

ORACLE_CONFIG = {
    "host": os.getenv("ORACLE_HOST"),
    "port": os.getenv("ORACLE_PORT"),
    "username": os.getenv("ORACLE_USERNAME"),
    "password": os.getenv("ORACLE_PASSWORD"),
    "service_name": os.getenv("ORACLE_SERVICE_NAME")
}

MONGO_CONFIG = {
    "host": os.getenv("MONGO_HOST"),
    "port": os.getenv("MONGO_PORT"),
    "username": os.getenv("MONGO_USERNAME"),
    "password": os.getenv("MONGO_PASSWORD"),
    "database": os.getenv("MONGO_DATABASE"),
}
