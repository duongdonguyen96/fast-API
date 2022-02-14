from typing import List

from fastapi import APIRouter, Body, Depends
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.config.payment_account.detail.controller import (
    CtrConfigPaymentDetail
)
from app.api.v1.endpoints.config.payment_account.detail.schema import (
    AccountStructureTypeRequest
)
from app.api.v1.schemas.utils import DropdownResponse

router = APIRouter()


@router.get(
    path="/account-structure-type/",
    name="Account Structure Type",
    description="Lấy dữ liệu các Kiểu kiến trúc",
    responses=swagger_response(
        response_model=ResponseData[List[DropdownResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_account_structure_type_info(
        request_body: AccountStructureTypeRequest = Body(...),
        current_user=Depends(get_current_user_from_header())
):
    account_structure_type_infos = await CtrConfigPaymentDetail(current_user).ctr_account_structure_type_info(
        level=request_body.level,
        parent_id=request_body.parent_id
    )
    return ResponseData[List[DropdownResponse]](**account_structure_type_infos)
