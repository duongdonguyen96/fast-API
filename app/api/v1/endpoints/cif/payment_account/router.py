from fastapi import APIRouter

from app.api.v1.endpoints.cif.payment_account.co_owner import \
    view as views_step_iii_b
from app.api.v1.endpoints.cif.payment_account.detail import \
    view as views_step_iii_a

router_step = APIRouter()

# step III. Tài khoản thanh toán -> A. Chi tiết tài khoản thanh toán
router_step.include_router(
    router=views_step_iii_a.router,
    prefix="/detail"
)

# step III. Tài khoản thanh toán -> B. Thông tin đồng sở hữu
router_step.include_router(
    router=views_step_iii_b.router,
    prefix="/co-owner"
)
