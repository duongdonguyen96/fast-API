from typing import Dict, Generic, List, TypeVar, Union

from pydantic.generics import GenericModel

from app.api.base.base_schema import CustomBaseModel
from app.api.base.errors import Error

TypeX = TypeVar("TypeX")


class PagingResponse(CustomBaseModel, GenericModel, Generic[TypeX]):
    data: List[TypeX]
    errors: List[Error] = []
    total_items = 0
    total_page = 0
    current_page = 0


class ResponseData(CustomBaseModel, GenericModel, Generic[TypeX]):
    data: TypeX = None
    errors: List[Error] = []


class ResponseError(CustomBaseModel):
    data: Union[Dict, List] = None
    errors: List[Error]
