from fastapi import APIRouter

from app.api.v1.endpoints.config import router as views_config
from app.api.v1.endpoints.user import router as views_user

router = APIRouter()

router.include_router(router=views_user.router, prefix="/account", tags=["User"])

router.include_router(router=views_config.router, prefix="/config", tags=["Configs"])
