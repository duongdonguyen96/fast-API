from typing import Optional

from pydantic import Field

from app.api.base.schema import BaseSchema


class DropdownResponse(BaseSchema):
    id: str = Field(..., description='`Chuỗi định danh`')
    code: str = Field(..., description='`Mã`')
    name: str = Field(..., description='`Tên`')


class OptionalDropdownResponse(BaseSchema):
    id: Optional[str] = Field(..., description='`Chuỗi định danh`')
    code: Optional[str] = Field(..., description='`Mã`')
    name: Optional[str] = Field(..., description='`Tên`')


class DropdownRequest(BaseSchema):
    id: str = Field(..., min_length=1, description='`Chuỗi định danh`')


class OpionalDropdownRequest(BaseSchema):
    id: Optional[str] = Field(..., description='`Chuỗi định danh`')


########################################################################################################################
# Response save
########################################################################################################################
class SaveSuccessResponse(BaseSchema):
    cif_id: str = Field(..., description='Id CIF ảo')
