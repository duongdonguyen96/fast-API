from fastapi import APIRouter, Body, Depends
from starlette import status

from app.api.base.oauth import get_current_user
from app.api.base.schema import ResponseData, AuthenticationRes, Authentication, UserInfo
from app.api.base.swagger import swagger_response

from app.api.v1.endpoints.train.customer.controller import CtrUser
from app.api.v1.endpoints.train.customer.examples import (
    DATA_EXAMPLE_CREATE_USER, DATA_EXAMPLE_CHANGE_PASSWORD_USER
)
from app.api.v1.endpoints.train.customer.schema import (CreateUserRq, CreateUserRes, ChangePassWord)
from typing import List, Optional
from app.api.base.schema import PaginationRequest

router = APIRouter()


@router.post(
    path="/login/",
    name="login",
    description="Login",
    responses=swagger_response(
        response_model=ResponseData[AuthenticationRes],
        success_status_code=status.HTTP_200_OK
    ),
)
async def view_login(
        user: Authentication = Body(...),
        current_user=None
        # current_user=Depends(get_current_user_from_header())
):
    data = await CtrUser(current_user).ctr_login(user)
    return ResponseData[AuthenticationRes](**data)


@router.post(
    path="/",
    name="User",
    description="Tạo user",
    responses=swagger_response(
        response_model=ResponseData[CreateUserRes],
        success_status_code=status.HTTP_200_OK
    ),
)
async def view_create_user(
        user: CreateUserRq = Body(..., example=DATA_EXAMPLE_CREATE_USER),
        current_user=None
        # current_user=Depends(get_current_user_from_header())
):
    user = await CtrUser(current_user).ctr_create_user(user)

    return ResponseData[CreateUserRes](**user)


@router.post(
    path="/all_users",
    name="User",
    description="Lấy tất cả user",
    responses=swagger_response(
        response_model=ResponseData[List[CreateUserRes]],
        success_status_code=status.HTTP_200_OK,
    ),
)
async def view_get_all_user(
        params: Optional[PaginationRequest],
        current_user: UserInfo = Depends(get_current_user),
):
    users = await CtrUser(current_user).get_all_user(params=params)
    return users
    # return ResponseData[List[CreateUserRes]](**all_users)


@router.put(
    path="/change_password",
    name="User",
    description="Đổi mật khẩu",
    responses=swagger_response(
        response_model=str,
        success_status_code=status.HTTP_200_OK,
        # success_examples='Thay đổi mật khẩu thành công!'
    ),
)
async def view_change_password(
        # current_user=Depends(get_current_user_from_header())
        user: ChangePassWord = Body(..., example=DATA_EXAMPLE_CHANGE_PASSWORD_USER),
        current_user=None
):
    status = await CtrUser(current_user).change_password(user=user)
    return status
