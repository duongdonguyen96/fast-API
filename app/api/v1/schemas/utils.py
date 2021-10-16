from pydantic import Field

from app.api.base.schema import BaseSchema


class Dropdown(BaseSchema):
    id: str = Field(..., description='`Chuỗi định danh`')
    code: str = Field(..., description='`Mã`')
    name: str = Field(..., description='`Tên`')


class Gender(Dropdown):
    pass


class Nationality(Dropdown):
    pass


class Province(Dropdown):
    pass


class District(Dropdown):
    pass


class Ward(Dropdown):
    pass
