from typing import List

from fastapi import APIRouter, Depends
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.config.identity_document.controller import (
    CtrConfigIdentityDocument
)
from app.api.v1.schemas.utils import DropdownResponse

router = APIRouter()


@router.get(
    path="/identity-document-type/",
    name="Identity Document Type",
    description="Lấy dữ liệu loại giấy tờ định danh",
    responses=swagger_response(
        response_model=ResponseData[List[DropdownResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_identity_type_info(
        current_user=Depends(get_current_user_from_header())
):
    identity_type_info = await CtrConfigIdentityDocument(current_user).ctr_identity_type_info()
    return ResponseData[List[DropdownResponse]](**identity_type_info)


@router.get(
    path="/sub-identity-document-type/",
    name="Sub Identity Document Type",
    description="Lấy dữ liệu loại giấy tờ định danh phụ ",
    responses=swagger_response(
        response_model=ResponseData[List[DropdownResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_sub_identity_type_info(
        current_user=Depends(get_current_user_from_header())
):
    sub_identity_type_info = await CtrConfigIdentityDocument(current_user).ctr_sub_identity_type_info()
    return ResponseData[List[DropdownResponse]](**sub_identity_type_info)
