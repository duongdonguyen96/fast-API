from typing import List

from fastapi import APIRouter, Depends, Query
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.customer_service.controller import CtrKSS
from app.api.v1.endpoints.customer_service.schema import (
    KSSResponse, QueryParamsKSSRequest, StatisticsMonth
)

router = APIRouter()


@router.get(
    path="/",
    name="Kiểm Soát Sau",
    description="Truy suất danh sách hậu kiểm",
    responses=swagger_response(
        response_model=ResponseData[KSSResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_list_kss(
        query_params: QueryParamsKSSRequest = Depends(),
        current_user=Depends(get_current_user_from_header())  # noqa
):
    kss_response = await CtrKSS().ctr_get_list_kss(
        query_params=query_params
    )

    return ResponseData[KSSResponse](**kss_response)


@router.get(
    path="/statistics/months/",
    name="Thống kê theo tháng",
    description="Thống kê theo tháng",
    responses=swagger_response(
        response_model=ResponseData[List[StatisticsMonth]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_list_statistics_month(
        months: str = Query(None, description='Số tháng', nullabe=True),
        current_user=Depends(get_current_user_from_header())  # noqa
):
    statistics_month_response = await CtrKSS().ctr_statistics(
        months=months
    )

    return ResponseData[List[StatisticsMonth]](**statistics_month_response)
