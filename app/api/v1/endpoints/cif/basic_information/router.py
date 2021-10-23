from fastapi import APIRouter

from app.api.v1.endpoints.cif.basic_information import \
    view as views_step_common
from app.api.v1.endpoints.cif.basic_information.contact import \
    view as views_step_i_3
from app.api.v1.endpoints.cif.basic_information.customer_relationship import \
    view as views_step_i_6
from app.api.v1.endpoints.cif.basic_information.fatca import \
    view as views_step_i_4
from app.api.v1.endpoints.cif.basic_information.guardian import \
    view as views_step_i_5
from app.api.v1.endpoints.cif.basic_information.identity import \
    router as routers_step_i_1
from app.api.v1.endpoints.cif.basic_information.personal import \
    view as views_step_i_2

router_step = APIRouter()

# step I. Thông tin cá nhân -> 1. Giấy tờ định danh
router_step.include_router(
    router=routers_step_i_1.router_sub_step,
    prefix="/identity"
)

# step I. Thông tin cá nhân -> 2. Thông tin cá nhân
router_step.include_router(
    router=views_step_i_2.router,
    prefix="/personal"
)

# step I. Thông tin cá nhân -> 3. Thông tin liên lạc
router_step.include_router(
    router=views_step_i_3.router,
    prefix="/contact"
)

# step I. Thông tin cá nhân -> 4. Thông tin FATCA
router_step.include_router(
    router=views_step_i_4.router,
    prefix="/fatca"
)

# step I. Thông tin cá nhân -> 5. Thông tin người giám hộ
router_step.include_router(
    router=views_step_i_5.router,
    prefix="/guardian"
)

# step I. Thông tin cá nhân -> 6. Thông tin người giám hộ
router_step.include_router(
    router=views_step_i_6.router,
    prefix="/customer-relationship"
)

router_step.include_router(
    router=views_step_common.router,
    prefix="/common",
    tags=["[CIF] Thông tin cơ bản - API dùng chung"]
)
