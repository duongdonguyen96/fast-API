from fastapi import APIRouter, Depends
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.customer_service.controller import CtrKSS
from app.api.v1.endpoints.customer_service.schema import (
    KSSResponse, QueryParamsKSSRequest, StatisticsProfilesResponse
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
        current_user = Depends(get_current_user_from_header())  # noqa
):
    kss_response = await CtrKSS().ctr_get_list_kss(
        query_params=query_params
    )

    return ResponseData[KSSResponse](**kss_response)


@router.get(
    path="/statistics/profiles/",
    name="Thống kê hồ sơ hậu kiểm",
    description="Thống kê hồ sơ hậu kiểm",
    responses=swagger_response(
        response_model=ResponseData[StatisticsProfilesResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_list_statistics_profiles(
        current_user = Depends(get_current_user_from_header())  # noqa
):
    statistics_profiles = await CtrKSS().ctr_get_statistics_profiles()

    return ResponseData[StatisticsProfilesResponse](**statistics_profiles)
