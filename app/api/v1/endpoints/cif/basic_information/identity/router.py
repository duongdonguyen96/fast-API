from fastapi import APIRouter

from app.api.v1.endpoints.cif.basic_information.identity.face import \
    router as views_step_i_1_b
from app.api.v1.endpoints.cif.basic_information.identity.fingerprint import \
    router as views_step_i_1_c
from app.api.v1.endpoints.cif.basic_information.identity.identity_document import \
    router as views_step_i_1_a
from app.api.v1.endpoints.cif.basic_information.identity.signature import \
    router as views_step_i_1_d
from app.api.v1.endpoints.cif.basic_information.identity.sub_identity_document import \
    router as views_step_i_1_e

router_sub_step = APIRouter()

router_sub_step.include_router(router=views_step_i_1_a.router, prefix="/identity-document")

router_sub_step.include_router(router=views_step_i_1_b.router, prefix="/face")

router_sub_step.include_router(router=views_step_i_1_c.router, prefix="/fingerprint")

router_sub_step.include_router(router=views_step_i_1_d.router, prefix="/signature")

router_sub_step.include_router(router=views_step_i_1_e.router, prefix="/sub-identity-document")
