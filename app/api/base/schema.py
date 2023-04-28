from typing import Any, Generic, List, TypeVar
from uuid import UUID

import orjson
from pydantic import Field

from pydantic.schema import date, datetime

from app.utils.functions import date_to_string, datetime_to_string
from pydantic import BaseModel, conint
from typing import Optional, Generic, TypeVar

from pydantic.generics import GenericModel

TypeX = TypeVar("TypeX")


def orjson_dumps(v, *, default):
    # orjson.dumps returns bytes, to match standard json.dumps we need to decode
    return orjson.dumps(v, default=default).decode()


class BaseSchema(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
        json_encoders = {
            datetime: lambda dt: datetime_to_string(dt),
            date: lambda d: date_to_string(d)
        }

    def set_uuid(self, uuid: [str, UUID]):
        object.__setattr__(self, 'uuid', uuid)


class BaseGenericSchema(BaseSchema, GenericModel):
    pass


class Error(BaseSchema):
    loc: str = Field(..., description='Vị trí lỗi')
    msg: str = Field(..., description='Mã lỗi')
    detail: str = Field(..., description='Mô tả chi tiết')


class PagingResponse(BaseSchema, GenericModel, Generic[TypeX]):
    data: List[TypeX] = Field(..., description='Danh sách item')
    errors: List[Error] = []
    total_item: int = Field(..., description='Tổng số item có trong hệ thống')
    total_page: int = Field(..., description='Tổng số trang')
    current_page: int = Field(..., description='Số thứ tự trang hiện tại')


class PaginationRequest(BaseSchema):
    page_size: Optional[conint(gt=0, lt=1001)] = 10
    current_page: Optional[conint(gt=0)] = 1
    # sort_by: Optional[str] = 'id'
    # order: Optional[str] = 'desc'


class ResponseData(BaseSchema, GenericModel, Generic[TypeX]):
    data: TypeX = Field(..., description='Dữ liệu trả về khi success')
    errors: List[Error] = []


class ResponseError(BaseSchema):
    data: Any = None
    errors: List[Error] = Field(..., description='Lỗi trả về')


class UserInfo(BaseSchema):
    user_id: str = Field(..., description='user_id', example='103C76ECBBC144B7B589C6808C029016')
    username: str = Field(..., description='Tên tài khoản', example='ddonguyen')
    full_name: str = Field(..., description='Tên đầy đủ', example='Dương Đỗ Nguyên')
    email: str = Field(..., description='Thư điện tử', example='ddonguyen@cmc.com.vn')
    department_id: str = Field(None, description='Phòng ban', example='ddonguyen@cmc.com.vn')
    company_id: str = Field(None, description='Công ty', example='ddonguyen@cmc.com.vn')


class Authentication(BaseSchema):
    username: str = Field(..., description='Tài khoản', example='ddonguyen')
    password: str = Field(..., description='Mật khẩu', example='123456')


class AuthenticationRes(BaseSchema):
    access_token: str = Field(..., description='access_token', example='103C76ECBBC144B7B589C6808C029016')
    user_info: UserInfo
