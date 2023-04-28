from fastapi import APIRouter

from app.api.v1.endpoints.other_module.customer import view as views_other_module

router_module = APIRouter()

router_module.include_router(
    router=views_other_module.router, prefix="/other_module", tags=["[OTHER_MODULE]"]
)
