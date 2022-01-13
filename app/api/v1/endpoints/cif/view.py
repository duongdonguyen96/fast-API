from typing import List

from fastapi import APIRouter, Depends, Path
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.cif.controller import CtrCustomer
from app.api.v1.endpoints.cif.schema import (
    CheckExistCIFRequest, CheckExistCIFSuccessResponse,
    CifCustomerInformationResponse, CifInformationResponse,
    CifProfileHistoryResponse
)

router = APIRouter()


@router.get(
    path="/{cif_id}/",
    name="CIF",
    description="Lấy dữ liệu tab `THÔNG TIN CIF` của khách hàng",
    responses=swagger_response(
        response_model=ResponseData[CifInformationResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_cif_info(
        cif_id: str = Path(..., description='Id CIF ảo'),
        current_user=Depends(get_current_user_from_header())  # noqa
):
    cif_info = await CtrCustomer().ctr_cif_info(cif_id)
    return ResponseData[CifInformationResponse](**cif_info)


@router.get(
    path="/{cif_id}/log/",
    name="Profile history",
    description="Lấy dữ liệu tab `LỊCH SỬ HỒ SƠ` của khách hàng",
    responses=swagger_response(
        response_model=ResponseData[List[CifProfileHistoryResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_profile_history(
        cif_id: str = Path(..., description='Id CIF ảo'),
        current_user=Depends(get_current_user_from_header())
):
    profile_history = await CtrCustomer(current_user).ctr_profile_history(cif_id)
    return ResponseData[List[CifProfileHistoryResponse]](**profile_history)


@router.get(
    path="/{cif_id}/customer/",
    name="Customer Information",
    description="Lấy dữ liệu `THÔNG TIN` của khách hàng",
    responses=swagger_response(
        response_model=ResponseData[CifCustomerInformationResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_customer(
        cif_id: str = Path(..., description='Id CIF ảo'),
        current_user=Depends(get_current_user_from_header())
):
    customer_information_data = await CtrCustomer(current_user).ctr_customer_information(cif_id)
    return ResponseData[CifCustomerInformationResponse](**customer_information_data)


@router.post(
    path="/check-exist/",
    name="Kiểm tra tồn tại",
    description="Kiểm tra CIF có tồn tại hay không",
    responses=swagger_response(
        response_model=ResponseData[CheckExistCIFSuccessResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_check_exist_cif(
        request_body: CheckExistCIFRequest,
        current_user=Depends(get_current_user_from_header())
):
    check_exist_data = await CtrCustomer(current_user).ctr_check_exist_cif(cif_number=request_body.cif_number)
    return ResponseData[CheckExistCIFSuccessResponse](**check_exist_data)
