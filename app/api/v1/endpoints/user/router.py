from fastapi import APIRouter
from starlette import status

from app.api.v1.controllers.user.ctr_user import CtrUser
from app.api.v1.schemas.response import ResponseData
from app.api.v1.schemas.user.auth import AuthReq, AuthRes, UserInfoRes
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
    path="/{user_id}/",
    name="Detail",
    description="Lấy thông tin user",
    responses=swagger_response(
        response_model=ResponseData[UserInfoRes],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_retrieve_user(user_id: str):
    user_info = await CtrUser().ctr_get_user_info(user_id)
    return ResponseData[UserInfoRes](**user_info)
