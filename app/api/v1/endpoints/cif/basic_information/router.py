from fastapi import APIRouter

from app.api.v1.endpoints.cif.basic_information.identity import \
    router as views_step_i_1

router_step = APIRouter()

# step I. Thông tin cá nhân -> 1. Giấy tờ định danh
router_step.include_router(
    router=views_step_i_1.router_sub_step,
    prefix="/identity", tags=['[CIF] I. TTCN']
)
