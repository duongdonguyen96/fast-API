from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.schemas.utils import DropdownRequest, DropdownResponse


class AddressResponse(BaseSchema):
    province: DropdownResponse = Field(..., description="Tỉnh/Thành phố")
    district: DropdownResponse = Field(..., description="Quận/Huyện")
    ward: DropdownResponse = Field(..., description="Phường/Xã")
    number_and_street: str = Field(..., description="Số nhà, tên đường")


class AddressRequest(BaseSchema):
    province: DropdownResponse = Field(..., description="Tỉnh/Thành phố")
    district: DropdownResponse = Field(..., description="Quận/Huyện")
    ward: DropdownResponse = Field(..., description="Phường/Xã")
    number_and_street: str = Field(..., description="Số nhà, tên đường")


class FingerPrintResponse(BaseSchema):
    image_url: str = Field(..., description='Ảnh bàn tay')
    hand_side: DropdownResponse = Field(..., description='Loại bàn tay')
    finger_type: DropdownResponse = Field(..., description='Loại ngón tay')


class FingerPrintRequest(BaseSchema):
    image_url: str = Field(..., description="URL hình ảnh vân tay")
    hand_side: DropdownRequest = Field(..., description="Bàn tay")
    finger_type: DropdownRequest = Field(..., description="Ngón tay")
