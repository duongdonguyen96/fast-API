from typing import List

from fastapi import APIRouter, Depends
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.config.staff.controller import CtrConfigStaff
from app.api.v1.endpoints.config.staff.schema import EmployeeDropdownResponse
from app.api.v1.schemas.utils import DropdownResponse

router = APIRouter()


@router.get(
    path="/staff-type/",
    name="Staff Type",
    description="Lấy dữ liệu loại nhân viên",
    responses=swagger_response(
        response_model=ResponseData[List[DropdownResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_staff_type_info(
        current_user=Depends(get_current_user_from_header())
):
    staff_type_info = await CtrConfigStaff(current_user).ctr_staff_type_info()
    return ResponseData[List[DropdownResponse]](**staff_type_info)


@router.get(
    path="/company-position/",
    name="Company Position",
    description="Lấy dữ liệu chức vụ",
    responses=swagger_response(
        response_model=ResponseData[List[DropdownResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_position_info(
        current_user=Depends(get_current_user_from_header())
):
    position_info = await CtrConfigStaff(current_user).ctr_position_info()
    return ResponseData[List[DropdownResponse]](**position_info)


@router.get(
    path="/sale-staff/",
    name="Sale Staff",
    description="Lấy dữ liệu nhân viên trực tiếp",
    responses=swagger_response(
        response_model=ResponseData[List[EmployeeDropdownResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_sale_staff_info(
        current_user=Depends(get_current_user_from_header())
):
    sale_staff_info = await CtrConfigStaff(current_user).ctr_sale_staff_info()
    return ResponseData[List[EmployeeDropdownResponse]](**sale_staff_info)


@router.get(
    path="/indirect-sale-staff/",
    name="Indirect Sale Staff",
    description="Lấy dữ liệu nhân viên gián tiếp",
    responses=swagger_response(
        response_model=ResponseData[List[EmployeeDropdownResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_indirect_sale_staff_info(
        current_user=Depends(get_current_user_from_header())
):
    indirect_sale_staff_info = await CtrConfigStaff(current_user).ctr_indirect_sale_staff_info()
    return ResponseData[List[EmployeeDropdownResponse]](**indirect_sale_staff_info)
