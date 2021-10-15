from typing import Dict, Generic, List, TypeVar, Union
from uuid import UUID

import orjson
from pydantic import BaseModel
from pydantic.generics import GenericModel
from pydantic.json import timedelta_isoformat
from pydantic.schema import datetime, timedelta

TypeX = TypeVar("TypeX")


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class BaseSchema(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
        json_encoders = {
            datetime: lambda v: int(v.timestamp()),
            timedelta: timedelta_isoformat
        }

    def set_uuid(self, uuid: [str, UUID]):
        object.__setattr__(self, 'uuid', uuid)


class BaseGenericSchema(BaseSchema, GenericModel):
    pass


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
