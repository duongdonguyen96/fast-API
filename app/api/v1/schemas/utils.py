from pydantic import Field

from app.api.base.schema import BaseSchema


class DropdownResponse(BaseSchema):
    id: str = Field(..., description='`Chuỗi định danh`')
    code: str = Field(..., description='`Mã`')
    name: str = Field(..., description='`Tên`')


class DropdownRequest(BaseSchema):
    id: str = Field(..., description='`Chuỗi định danh`')


class GenderResponse(DropdownResponse):
    pass


class GenderRequest(DropdownRequest):
    pass


class NationalityResponse(DropdownResponse):
    pass


class ProvinceResponse(DropdownResponse):
    pass


class DistrictResponse(DropdownResponse):
    pass


class WardResponse(DropdownResponse):
    pass
