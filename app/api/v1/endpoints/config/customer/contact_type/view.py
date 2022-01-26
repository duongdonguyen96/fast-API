from typing import List

from fastapi import APIRouter, Depends
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.config.customer.contact_type.controller import (
    CtrConfigContactType
)
from app.api.v1.schemas.utils import DropdownResponse

router = APIRouter()


@router.get(
    path="/customer-contact-type/",
    name="Customer Contact Type",
    description="Lấy dữ liệu Hình thức kích hoạt mật khẩu lần đầu/ Hình thức liên hệ",
    responses=swagger_response(
        response_model=ResponseData[List[DropdownResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_customer_contact_type_info(
        current_user=Depends(get_current_user_from_header())
):
    customer_contact_type_infos = await CtrConfigContactType(current_user).ctr_customer_contact_type_info()
    return ResponseData[List[DropdownResponse]](**customer_contact_type_infos)
