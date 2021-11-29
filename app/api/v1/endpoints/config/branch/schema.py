from pydantic import Field

from app.api.base.schema import BaseSchema


class BranchDropdownResponse(BaseSchema):
    id: str = Field(..., description='`id chi nhánh`')
    code: str = Field(..., description='`Mã chi nhánh`')
    name: str = Field(..., description='`Tên chi nh`ánh')
    address: str = Field(..., description='`Địa chỉ chi nh ánh`')
