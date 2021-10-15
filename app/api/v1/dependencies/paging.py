from enum import Enum

from fastapi.params import Query
from pydantic.main import BaseModel


class OrderBy(str, Enum):
    asc = "asc"
    desc = "desc"


class PaginationParams(BaseModel):
    order_by: OrderBy = OrderBy.asc
    limit: int = Query(50, ge=1, description="Page size")
    page: int = Query(1, ge=1, description="Page number")

    @property
    def offset(self):
        return self.limit * (self.page - 1)
