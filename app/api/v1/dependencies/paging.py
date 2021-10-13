from enum import Enum

from fastapi import Depends
from pydantic import Field
from pydantic.main import BaseModel


class OrderBy(str, Enum):
    asc = "asc"
    desc = "desc"


class Paging(BaseModel):
    order_by: OrderBy = OrderBy.asc
    limit: int = Field(20, gt=0)
    page: int = Field(1, gt=0)


def get_paging(paging=Depends(Paging)):
    return paging
