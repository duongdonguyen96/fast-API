from fastapi import APIRouter, Depends, Path
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.cif.basic_information.identity.signature.controller import (
    CtrSignature
)
from app.api.v1.endpoints.cif.basic_information.identity.signature.schema import (
    SignaturesSuccessResponse
)
from app.api.v1.endpoints.user.schema import UserInfoResponse

router = APIRouter()


@router.post(
    path="/",
    name="1. GTĐD - D. Chữ ký",
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
    name="1. GTĐD - D. Chữ ký",
    description="Lấy dữ liệu tab `CHỮ KÝ` của khách hàng",
    responses=swagger_response(
        response_model=ResponseData[SignaturesSuccessResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_retrieve_user(
        cif_id: str = Path(...),
        current_user=Depends(get_current_user_from_header())
):
    signature_data = await CtrSignature(current_user).ctr_get_signature(cif_id)
    return ResponseData[SignaturesSuccessResponse](**signature_data)
