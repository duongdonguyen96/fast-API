from fastapi import APIRouter, Depends
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.customer_service.controller import CtrKSS
from app.api.v1.endpoints.customer_service.schema import (
    KSSResponse, PostControlResponse, QueryParamsKSSRequest
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
    path="/customer/postcontrol/{postcheck_uuid}/",
    name="Thông tin hậu kiểm của khách hàng",
    description="Thông tin hậu kiểm của khách hàng",
    responses=swagger_response(
        response_model=ResponseData[PostControlResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_list_post_control(
        postcheck_uuid: str, # noqa
        current_user=Depends(get_current_user_from_header())  # noqa
):
    post_control_response = await CtrKSS().ctr_get_post_control()

    return ResponseData[PostControlResponse](**post_control_response)
