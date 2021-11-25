from fastapi import APIRouter

from app.api.v1.endpoints.config.address import view as views_address_info
from app.api.v1.endpoints.config.cif_information import view as views_cif_info
from app.api.v1.endpoints.config.hand import view as views_hand_info
from app.api.v1.endpoints.config.passport import view as views_passport_info
from app.api.v1.endpoints.config.personal import view as views_personal_info

router = APIRouter()

router.include_router(router=views_hand_info.router)

router.include_router(router=views_cif_info.router)

router.include_router(router=views_address_info.router)

router.include_router(router=views_personal_info.router)

router.include_router(router=views_passport_info.router)
