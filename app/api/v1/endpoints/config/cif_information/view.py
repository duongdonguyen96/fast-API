from typing import List

from fastapi import APIRouter, Depends
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.config.cif_information.controller import CtrCifInfo
from app.api.v1.schemas.utils import DropdownResponse

router = APIRouter()


@router.get(
    path="/customer-classification/",
    name="Customer Classification",
    description="Lấy dữ liệu config đối tượng khách hàng",
    responses=swagger_response(
        response_model=ResponseData[List[DropdownResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_customer_classification_info(
        current_user=Depends(get_current_user_from_header())
):
    customer_classification_info = await CtrCifInfo(current_user).ctr_customer_classification_info()
    return ResponseData[List[DropdownResponse]](**customer_classification_info)


@router.get(
    path="/customer-economic-profession/",
    name="Customer Economic Profession",
    description="Lấy dữ liệu mã ngành kinh tế",
    responses=swagger_response(
        response_model=ResponseData[List[DropdownResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_customer_economic_profession_info(
        current_user=Depends(get_current_user_from_header())
):
    customer_economic_profession_info = await CtrCifInfo(current_user).ctr_customer_economic_profession_info()
    return ResponseData[List[DropdownResponse]](**customer_economic_profession_info)


@router.get(
    path="/kyc-level/",
    name="KYC Level",
    description="Lấy dữ liệu KYC level",
    responses=swagger_response(
        response_model=ResponseData[List[DropdownResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_kyc_level_info(
        current_user=Depends(get_current_user_from_header())
):
    kyc_level_info = await CtrCifInfo(current_user).ctr_kyc_level_info()
    return ResponseData[List[DropdownResponse]](**kyc_level_info)
