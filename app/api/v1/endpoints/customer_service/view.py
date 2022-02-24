from typing import List

from fastapi import APIRouter, Depends, Query
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.customer_service.controller import CtrKSS
from app.api.v1.endpoints.customer_service.schema import (
    KSSResponse, QueryParamsKSSRequest, ZoneResponse
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
    path="/branch/",
    name="Danh sách đơn vị",
    description="Truy suất danh sách đơn vị",
    responses=swagger_response(
        response_model=ResponseData[List[ZoneResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_list_zone(
    zone_id: int = Query(None, description='Zone ID', nullable=True),
    current_user = Depends(get_current_user_from_header())  # noqa
):
    zone_response = await CtrKSS().ctr_get_list_zone(zone_id=zone_id)

    return ResponseData[List[ZoneResponse]](**zone_response)
