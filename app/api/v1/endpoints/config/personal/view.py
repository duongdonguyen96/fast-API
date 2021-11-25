from typing import List

from fastapi import APIRouter, Depends
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.config.personal.controller import CtrConfigPersonal
from app.api.v1.schemas.utils import DropdownResponse

router = APIRouter()


@router.get(
    path="/gender/",
    name="Gender",
    description="Lấy dữ liệu giới tính",
    responses=swagger_response(
        response_model=ResponseData[List[DropdownResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gender_info(
        current_user=Depends(get_current_user_from_header())
):
    gender_info = await CtrConfigPersonal(current_user).ctr_gender_info()
    return ResponseData[List[DropdownResponse]](**gender_info)


@router.get(
    path="/nationality/",
    name="Nationality",
    description="Lấy dữ liệu quốc tịch",
    responses=swagger_response(
        response_model=ResponseData[List[DropdownResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_nationality_info(
        current_user=Depends(get_current_user_from_header())
):
    nationality_info = await CtrConfigPersonal(current_user).ctr_nationality_info()
    return ResponseData[List[DropdownResponse]](**nationality_info)


@router.get(
    path="/ethnic/",
    name="Ethnic",
    description="Lấy dữ liệu dân tộc ",
    responses=swagger_response(
        response_model=ResponseData[List[DropdownResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_ethnic_info(
        current_user=Depends(get_current_user_from_header())
):
    ethnic_info = await CtrConfigPersonal(current_user).ctr_ethnic_info()
    return ResponseData[List[DropdownResponse]](**ethnic_info)


@router.get(
    path="/religion/",
    name="Religion",
    description="Lấy dữ liệu tôn giáo ",
    responses=swagger_response(
        response_model=ResponseData[List[DropdownResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_religion_info(
        current_user=Depends(get_current_user_from_header())
):
    religion_info = await CtrConfigPersonal(current_user).ctr_religion_info()
    return ResponseData[List[DropdownResponse]](**religion_info)


@router.get(
    path="/honorific/",
    name="Honorific",
    description="Lấy dữ liệu danh xưng ",
    responses=swagger_response(
        response_model=ResponseData[List[DropdownResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_honorific_info(
        current_user=Depends(get_current_user_from_header())
):
    honorific_info = await CtrConfigPersonal(current_user).ctr_honorific_info()
    return ResponseData[List[DropdownResponse]](**honorific_info)


@router.get(
    path="/resident-status/",
    name="Resident Status",
    description="Lấy dữ liệu tình trạng cư trú ",
    responses=swagger_response(
        response_model=ResponseData[List[DropdownResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_resident_status_info(
        current_user=Depends(get_current_user_from_header())
):
    resident_status_info = await CtrConfigPersonal(current_user).ctr_resident_status_info()
    return ResponseData[List[DropdownResponse]](**resident_status_info)


@router.get(
    path="/marital-status/",
    name="Marital Status",
    description="Lấy dữ liệu tình trạng hôn nhân ",
    responses=swagger_response(
        response_model=ResponseData[List[DropdownResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_marital_status_info(
        current_user=Depends(get_current_user_from_header())
):
    marital_status_info = await CtrConfigPersonal(current_user).ctr_marital_status_info()
    return ResponseData[List[DropdownResponse]](**marital_status_info)


@router.get(
    path="/career/",
    name="Career",
    description="Lấy dữ liệu nghề nghiệp ",
    responses=swagger_response(
        response_model=ResponseData[List[DropdownResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_career_info(
        current_user=Depends(get_current_user_from_header())
):
    career_info = await CtrConfigPersonal(current_user).ctr_career_info()
    return ResponseData[List[DropdownResponse]](**career_info)


@router.get(
    path="/average-income-amount/",
    name="Average Income Amount",
    description="Lấy dữ liệu thu nhập trung bình trong 3 tháng gần nhất ",
    responses=swagger_response(
        response_model=ResponseData[List[DropdownResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_average_income_amount_info(
        current_user=Depends(get_current_user_from_header())
):
    average_income_amount_info = await CtrConfigPersonal(current_user).ctr_average_income_amount_info()
    return ResponseData[List[DropdownResponse]](**average_income_amount_info)


@router.get(
    path="/customer-relationship/",
    name="Customer Relationship",
    description="Lấy dữ liệu mối quan hệ khách hàng ",
    responses=swagger_response(
        response_model=ResponseData[List[DropdownResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_customer_relationship_info(
        current_user=Depends(get_current_user_from_header())
):
    customer_relationship_info = await CtrConfigPersonal(current_user).ctr_customer_relationship_info()
    return ResponseData[List[DropdownResponse]](**customer_relationship_info)
