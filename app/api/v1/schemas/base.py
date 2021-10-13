from uuid import UUID

import orjson
from pydantic import BaseModel
from pydantic.generics import GenericModel
from pydantic.json import timedelta_isoformat
from pydantic.schema import datetime, timedelta


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class CustomBaseModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
        json_encoders = {
            datetime: lambda v: int(v.timestamp()),
            timedelta: timedelta_isoformat
        }

    def set_uuid(self, uuid: [str, UUID]):
        object.__setattr__(self, 'uuid', uuid)


class CustomGenericModel(CustomBaseModel, GenericModel):
    pass
