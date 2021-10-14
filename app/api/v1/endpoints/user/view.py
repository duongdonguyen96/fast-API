from fastapi import APIRouter, Depends
from starlette import status

from app.api.base.schema import ResponseData
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.user.controller import CtrUser
from app.api.v1.endpoints.user.schema import AuthReq, AuthRes, UserInfoRes
from app.utils.swagger import swagger_response

router = APIRouter()


@router.post(
    path="/login/",
    name="Login",
    description="Đăng nhập",
    responses=swagger_response(
        response_model=ResponseData[AuthRes],
        success_status_code=status.HTTP_200_OK
    ),
)
async def view_login(login_req: AuthReq):
    data = await CtrUser().ctr_login(login_req)
    return ResponseData[AuthRes](**data)


@router.get(
    path="/me/",
    name="Detail current user",
    description="Lấy thông tin user hiện tại",
    responses=swagger_response(
        response_model=ResponseData[UserInfoRes],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_retrieve_current_user(
        current_user=Depends(get_current_user_from_header())
):
    user_info = await CtrUser(current_user).ctr_get_current_user_info()
    return ResponseData[UserInfoRes](**user_info)


@router.get(
    path="/{user_id}/",
    name="Detail",
    description="Lấy thông tin user",
    responses=swagger_response(
        response_model=ResponseData[UserInfoRes],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_retrieve_user(
        user_id: str,
        current_user=Depends(get_current_user_from_header())  # noqa
):
    user_info = await CtrUser().ctr_get_user_info(user_id)
    return ResponseData[UserInfoRes](**user_info)
