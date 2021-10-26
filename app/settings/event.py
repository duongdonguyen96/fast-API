from typing import Callable

from fastapi import FastAPI
from loguru import logger

from app.third_parties.services.card import ServiceCard
from app.third_parties.services.file import ServiceFile

service_file = ServiceFile()
service_card = ServiceCard()


def create_start_app_handler(app: FastAPI) -> Callable:  # noqa
    async def start_app():
        service_file.start()
        service_card.start()

    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable:  # noqa
    @logger.catch
    async def stop_app() -> None:
        await service_file.stop()
        await service_card.stop()

    return stop_app
