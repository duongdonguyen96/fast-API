from typing import List

from fastapi import APIRouter
from starlette import status

from app.api.v1.controllers.config.config import CtrConfig
from app.api.v1.schemas.response import ResponseData
from app.utils.swagger import swagger_response

router = APIRouter()

