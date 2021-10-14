from pydantic import Field

from app.api.base.schema import BaseSchema


class AuthReq(BaseSchema):
    username: str = Field(...)
    password: str = Field(..., min_length=8)


class UserInfoRes(BaseSchema):
    user_id: str
    user_name: str
    full_name: str
    avatar_url: str


class AuthRes(BaseSchema):
    token: str
    user_info: UserInfoRes
