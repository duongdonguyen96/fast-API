from fastapi import APIRouter

from app.api.v1.endpoints.cif import view as views_cif_info
from app.api.v1.endpoints.cif.basic_information import router as views_step_1
from app.api.v1.endpoints.cif.basic_information.identity.identity_document import \
    view as views_step_i_1_a

router_module = APIRouter()

# step I. Thông tin cá nhân
router_module.include_router(router=views_step_1.router_step, prefix="/{cif_id}/basic-information")

# router đặc biệt, do không sử dụng prefix có path param là {cif_id}
router_module.include_router(router=views_step_i_1_a.router_special, prefix="")

# router của thông tin cif
router_module.include_router(router=views_cif_info.router, tags=["CIF information"])
