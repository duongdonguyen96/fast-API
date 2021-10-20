from typing import List

from fastapi import APIRouter, Depends, Path
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.cif.basic_information.identity.sub_identity_document.controller import (
    CtrSubIdentityDocument
)
from app.api.v1.endpoints.cif.basic_information.identity.sub_identity_document.schema import (
    SubIdentityDetailResponse, SubIdentityDocumentRequest
)
from app.api.v1.schemas.utils import SaveSuccessResponse

router = APIRouter()


@router.post(
    path="/",
    name="1. GTĐD - E. GTĐD phụ",
    description="Lưu lại I. TTCN - Giấy tờ định danh - E. Giấy tờ định danh phụ",
    responses=swagger_response(
        response_model=ResponseData[SaveSuccessResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_create_sub_identity_card(
        sub_identity_document_requests: List[SubIdentityDocumentRequest],
        cif_id: str = Path(..., description='Id CIF ảo'),
        current_user=Depends(get_current_user_from_header())
):
    sub_identity_save_info = await CtrSubIdentityDocument(current_user).save_sub_identity_document(
        sub_identity_document_requests=sub_identity_document_requests,
        cif_id=cif_id
    )
    return ResponseData[SaveSuccessResponse](**sub_identity_save_info)


@router.get(
    path="/",
    name="1. GTĐD - E. GTĐD phụ",
    description="Chi tiết I. TTCN - Giấy tờ định danh - E. Giấy tờ định danh phụ",
    responses=swagger_response(
        response_model=ResponseData[List[SubIdentityDetailResponse]],
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
    return ResponseData[List[SubIdentityDetailResponse]](**sub_identity_document_info)
