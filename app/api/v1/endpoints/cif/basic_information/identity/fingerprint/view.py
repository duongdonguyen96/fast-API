from fastapi import APIRouter, Depends, Path
from starlette import status

from app.api.base.schema import ResponseData
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.cif.basic_information.identity.fingerprint.controller import (
    CtrFingerPrint
)
from app.api.v1.endpoints.cif.basic_information.identity.fingerprint.schema import (
    FingerPrintResponse
)
from app.api.v1.endpoints.user.schema import UserInfoResponse
from app.utils.swagger import swagger_response

router = APIRouter()


@router.post(
    path="/",
    name="1. GTĐD - C. Vân tay",
    description="Create",
    responses=swagger_response(
        response_model=ResponseData[UserInfoResponse],
        success_status_code=status.HTTP_200_OK
    ),
)
async def view_create_identity_document(current_user=Depends(get_current_user_from_header())):
    data = {}
    return ResponseData[UserInfoResponse](**data)


@router.get(
    path="/",
    name="1. GTĐD - C. Vân tay",
    description="Detail",
    responses=swagger_response(
        response_model=ResponseData[FingerPrintResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_retrieve_fingerprint(
        cif_id: str = Path(...),
        current_user=Depends(get_current_user_from_header())
):
    fingerprint_info = await CtrFingerPrint().ctr_get_fingerprint(cif_id)
    return ResponseData[FingerPrintResponse](**fingerprint_info)
