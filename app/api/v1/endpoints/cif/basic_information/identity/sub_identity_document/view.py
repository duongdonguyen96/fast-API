from fastapi import APIRouter, Depends, Path
from starlette import status

from app.api.base.schema import ResponseData, PagingResponse
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.cif.basic_information.identity.sub_identity_document.controller import CtrSubIdentityDocument
from app.api.v1.endpoints.cif.basic_information.identity.sub_identity_document.schema import SubIdentityDetailResponse
from app.api.v1.endpoints.user.schema import UserInfoResponse

router = APIRouter()


@router.post(
    path="/",
    name="1. GTĐD - E. GTĐD phụ",
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
    name="1. GTĐD - E. GTĐD phụ",
    description="Chi tiết I. TTCN - Giấy tờ định danh - E. Giấy tờ định danh phụ",
    responses=swagger_response(
        response_model=ResponseData[SubIdentityDetailResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_detail_sub_identity_card(
        cif_id: str = Path(..., description='Id CIF ảo'),
        current_user=Depends(get_current_user_from_header())
):
    ctr_sub_identity_document = CtrSubIdentityDocument(current_user)

    sub_identity_document_info = await ctr_sub_identity_document.detail_sub_identity_document(
        cif_id=cif_id
    )
    return PagingResponse[SubIdentityDetailResponse](**sub_identity_document_info)
