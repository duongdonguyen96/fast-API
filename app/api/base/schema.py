from typing import Dict, Generic, List, TypeVar, Union
from uuid import UUID

import orjson
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel
from pydantic.schema import date, datetime

from app.utils.functions import date_to_string, datetime_to_string

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


class CreatedUpdatedBaseModel(BaseSchema):
    created_at: datetime = Field(..., description='Tạo mới vào lúc, format dạng: `dd/mm/YYYY HH:MM:SS`',
                                 example='15/12/2021 06:07:08')

    created_by: str = Field(..., description='Tạo mới bởi')

    updated_at: datetime = Field(..., description='Cập nhật vào lúc, format dạng: `dd/mm/YYYY HH:MM:SS`',
                                 example='15/12/2021 06:07:08')

    updated_by: str = Field(..., description='Cập nhật vào lúc')


class Error(BaseSchema):
    loc: str = None
    msg: str = None
    detail: str = None


class PagingResponse(BaseSchema, GenericModel, Generic[TypeX]):
    data: List[TypeX]
    errors: List[Error] = []
    total_item = 0
    total_page = 0
    current_page = 0


class ResponseData(BaseSchema, GenericModel, Generic[TypeX]):
    data: TypeX = None
    errors: List[Error] = []


class ResponseError(BaseSchema):
    data: Union[Dict, List] = None
    errors: List[Error]
