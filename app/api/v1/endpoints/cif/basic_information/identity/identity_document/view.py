from typing import Union

from fastapi import APIRouter, Depends, Path, Query, Body
from starlette import status

from app.api.base.schema import ResponseData
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.cif.basic_information.identity.identity_document.controller import (
    CtrIdentityDocument
)
from app.api.v1.endpoints.cif.basic_information.identity.identity_document.schema import (
    CitizenCardDetailResponse, CitizenCardSaveRequest, IdentityCardDetailResponse,
    IdentityCardSaveRequest, IdentityDocumentSaveSuccessResponse, PassportDetailResponse,
    PassportSaveRequest, EXAMPLE_REQUEST_SAVE_IDENTITY_DOCUMENT
)
from app.utils.swagger import swagger_response

router = APIRouter()


@router.get(
    path="/",
    name="1. GTĐD - A. GTĐD",
    description="Chi tiết",
    responses=swagger_response(
        response_model=Union[
            ResponseData[IdentityCardDetailResponse],
            ResponseData[CitizenCardDetailResponse],
            ResponseData[PassportDetailResponse]
        ],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_detail_identity_card(
        cif_id: str = Path(..., description='Id CIF ảo'),
        identity_document_type_code: str = Query(None, description='Code loại giấy tờ định danh'),
        current_user=Depends(get_current_user_from_header())
):
    ctr_identity_document = CtrIdentityDocument(current_user)

    identity_document_info = await ctr_identity_document.detail_identity_document(
        cif_id=cif_id,
        identity_document_type_code=identity_document_type_code
    )

    return ResponseData[Union[IdentityCardDetailResponse, CitizenCardDetailResponse, PassportDetailResponse]](
        **identity_document_info
    )

########################################################################################################################

router_special = APIRouter()


@router_special.post(
    path="/basic-information/identity/identity-document/",
    name="1. GTĐD - A. GTĐD",
    description="Lưu",
    responses=swagger_response(
        response_model=ResponseData[IdentityDocumentSaveSuccessResponse],
        success_status_code=status.HTTP_200_OK
    ),
    tags=['[CIF] I. TTCN']
)
async def view_create(
        identity_document_req: Union[IdentityCardSaveRequest, CitizenCardSaveRequest, PassportSaveRequest] = Body(
            ...,
            examples=EXAMPLE_REQUEST_SAVE_IDENTITY_DOCUMENT,
        ),
        current_user=Depends(get_current_user_from_header())
):
    identity_save_info = await CtrIdentityDocument(current_user).save_identity_document(identity_document_req)
    return ResponseData[IdentityDocumentSaveSuccessResponse](**identity_save_info)
