from pydantic import Field

from app.api.base.schema import BaseSchema


class EmployeeDropdownResponse(BaseSchema):
    id: str = Field(..., description='`Mã nhân viên`')
    fullname_vn: str = Field(..., description='`Tên nhân viên`')
