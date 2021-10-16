from pydantic import Field

from app.api.base.schema import BaseSchema


class UserInfoRes(BaseSchema):
    user_id: str = Field(..., description='Id người dùng')
    username: str = Field(..., description='Tên đăng nhập')
    full_name_vn: str = Field(..., description='Họ và tên người dùng')
    avatar_url: str = Field(..., description='Link avatar')


class AuthRes(BaseSchema):
    token: str = Field(..., description='Token dùng cho các API khác')
    user_info: UserInfoRes = Field(..., description='Thông tin người dùng')


EXAMPLE_RES_FAIL_LOGIN = {
    "ex1": {
        "summary": "Không gửi đúng basic auth",
        "value": {
            "data": "null",  # do FastAPI đang generate file openapi.json với option bỏ qua None nên tạm thời để vậy
            "errors": [
                {
                    "loc": "null",
                    "msg": "null",
                    "detail": "Not authenticated"
                }
            ]
        }
    },
    "ex2": {
        "summary": "Sai tên đăng nhập hoặc mật khẩu",
        "value": {
            "data": "null",  # do FastAPI đang generate file openapi.json với option bỏ qua None nên tạm thời để vậy
            "errors": [
                {
                    "loc": "username, password",
                    "msg": "USERNAME_OR_PASSWORD_INVALID",
                    "detail": "Username or password is invalid"
                }
            ]
        }
    }
}

EXAMPLE_RES_SUCCESS_DETAIL_USER = {
    "ex1": {
        "summary": "Lấy thông tin thành công",
        "value": {
            "data": {
                "user_id": "9651cdfd9a9a4eb691f9a3a125ac46b0",
                "username": "dev1",
                "full_name_vn": "Developer 1",
                "avatar_url": "cdn/users/avatar/dev1.jpg"
            },
            "errors": []
        }
    }
}
