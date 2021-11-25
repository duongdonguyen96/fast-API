from fastapi import APIRouter

from app.api.v1.endpoints.config.cif_information import view as views_cif_info
from app.api.v1.endpoints.config.hand import view as views_hand_side_info

router = APIRouter()

router.include_router(router=views_hand_side_info.router)

router.include_router(router=views_cif_info.router)
