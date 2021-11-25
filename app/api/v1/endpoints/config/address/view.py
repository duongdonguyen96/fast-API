from typing import List

from fastapi import APIRouter, Depends, Path
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.config.address.controller import CtrAddress
from app.api.v1.schemas.utils import DropdownResponse

router = APIRouter()


@router.get(
    path="/province/{country_id}",
    name="Province",
    description="Lấy dữ liệu config tỉnh/thành phố",
    responses=swagger_response(
        response_model=ResponseData[List[DropdownResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_province_info(
        country_id: str = Path(..., description='Id country'),
        current_user=Depends(get_current_user_from_header())
):
    province_info = await CtrAddress(current_user).ctr_province_info(country_id=country_id)
    return ResponseData[List[DropdownResponse]](**province_info)


@router.get(
    path="/district/{province_id}",
    name="District",
    description="Lấy dữ liệu quận/huyện",
    responses=swagger_response(
        response_model=ResponseData[List[DropdownResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_district_info(
        province_id: str = Path(..., description='Id province'),
        current_user=Depends(get_current_user_from_header())
):
    district_info = await CtrAddress(current_user).ctr_district_info(province_id=province_id)
    return ResponseData[List[DropdownResponse]](**district_info)


@router.get(
    path="/ward/{district_id}",
    name="Ward",
    description="Lấy dữ liệu phường/xã",
    responses=swagger_response(
        response_model=ResponseData[List[DropdownResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_ward_info(
        district_id: str = Path(..., description='Id district'),
        current_user=Depends(get_current_user_from_header())
):
    ward_info = await CtrAddress(current_user).ctr_ward_info(district_id=district_id)
    return ResponseData[List[DropdownResponse]](**ward_info)


@router.get(
    path="/place-of-issue/{country_id}",
    name="Place Of Issue",
    description="Lấy dữ liệu nơi cấp",
    responses=swagger_response(
        response_model=ResponseData[List[DropdownResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_place_of_issue_info(
        country_id: str = Path(..., description='Id country'),
        current_user=Depends(get_current_user_from_header())
):
    place_of_issue_info = await CtrAddress(current_user).ctr_place_of_issue(country_id=country_id)
    return ResponseData[List[DropdownResponse]](**place_of_issue_info)


@router.get(
    path="/country/",
    name="Country",
    description="Lấy dữ liệu quê quán",
    responses=swagger_response(
        response_model=ResponseData[List[DropdownResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_country_info(
        current_user=Depends(get_current_user_from_header())
):
    country_info = await CtrAddress(current_user).ctr_country_info()
    return ResponseData[List[DropdownResponse]](**country_info)
