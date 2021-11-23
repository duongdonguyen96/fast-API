from typing import List, Union

from fastapi import APIRouter, Body, Depends, Path, Query
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.cif.basic_information.identity.identity_document.controller import (
    CtrIdentityDocument
)
from app.api.v1.endpoints.cif.basic_information.identity.identity_document.schema_request import (
    CitizenCardSaveRequest, IdentityCardSaveRequest, PassportSaveRequest
)
from app.api.v1.endpoints.cif.basic_information.identity.identity_document.schema_response import (
    CitizenCardDetailResponse, IdentityCardDetailResponse, LogResponse,
    PassportDetailResponse
)
from app.api.v1.schemas.utils import SaveSuccessResponse

router = APIRouter()


@router.get(
    path="/",
    name="1. GTĐD - A. GTĐD - Chi tiết",
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
async def view_detail(
        cif_id: str = Path(..., description='Id CIF ảo'),
        identity_document_type_id: str = Query(None, description='Code loại giấy tờ định danh'),
        current_user=Depends(get_current_user_from_header())
):
    ctr_identity_document = CtrIdentityDocument(current_user)

    detail_info = await ctr_identity_document.detail(
        cif_id=cif_id,
        identity_document_type_id=identity_document_type_id
    )

    return ResponseData[Union[IdentityCardDetailResponse, CitizenCardDetailResponse, PassportDetailResponse]](
        **detail_info
    )


@router.get(
    path="/log/",
    name="1. GTĐD - A. GTĐD - Lịch sử",
    description="Lịch sử",
    responses=swagger_response(
        response_model=ResponseData[List[LogResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_list_logs(
        cif_id: str = Path(..., description='Id CIF ảo'),
        current_user=Depends(get_current_user_from_header())
):
    ctr_identity_document = CtrIdentityDocument(current_user)

    logs_info = await ctr_identity_document.get_list_log(
        cif_id=cif_id
    )

    return ResponseData[List[LogResponse]](
        **logs_info
    )

########################################################################################################################

router_special = APIRouter()


@router_special.post(
    path="/basic-information/identity/identity-document/",
    name="1. GTĐD - A. GTĐD - Lưu",
    description="Lưu",
    responses=swagger_response(
        response_model=ResponseData[SaveSuccessResponse],
        success_status_code=status.HTTP_200_OK
    ),
    tags=['[CIF] I. TTCN']
)
async def view_save(
        identity_document_req: Union[IdentityCardSaveRequest, CitizenCardSaveRequest, PassportSaveRequest] = Body(
            ...
        ),
        current_user=Depends(get_current_user_from_header())
):
    save_info = await CtrIdentityDocument(current_user).save_identity(identity_document_req)
    return ResponseData[SaveSuccessResponse](**save_info)
