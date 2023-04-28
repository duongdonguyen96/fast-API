from fastapi import APIRouter

from app.api.v1.endpoints.train import router as routers_cif
from app.api.v1.endpoints.other_module import router as routers_other_module

router = APIRouter()

router.include_router(router=routers_cif.router_module, prefix="/train")

router.include_router(router=routers_other_module.router_module, prefix="/other_module")
