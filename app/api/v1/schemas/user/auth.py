from pydantic import Field

from app.api.v1.schemas.base import CustomBaseModel


class AuthReq(CustomBaseModel):
    username: str = Field(...)
    password: str = Field(..., min_length=8)


class UserInfoRes(CustomBaseModel):
    user_id: str
    user_name: str
    full_name: str
    avatar_url: str


class AuthRes(CustomBaseModel):
    token: str
    user_info: UserInfoRes
