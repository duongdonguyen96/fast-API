from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.schemas.utils import DropdownResponse, DropdownRequest


# III. Phân tích OCR -> 3. Thông tin địa chỉ -> Nơi thường trú/ Địa chỉ liên hệ (CMND)
class AddressResponse(BaseSchema):
    province: DropdownResponse = Field(..., description="Tỉnh/Thành phố")
    district: DropdownResponse = Field(..., description="Quận/Huyện")
    ward: DropdownResponse = Field(..., description="Phường/Xã")
    number_and_street: str = Field(..., description="Số nhà, tên đường")


# III. Phân tích OCR -> 2. Thông tin địa chỉ -> Chi tiết từng địa chỉ
class AddressRequest(AddressResponse):
    province: DropdownRequest = Field(..., description="Tỉnh/Thành phố")
    district: DropdownRequest = Field(..., description="Quận/Huyện")
    ward: DropdownRequest = Field(..., description="Phường/Xã")


class FingerPrintResponse(BaseSchema):
    image_url: str = Field(..., description='Ảnh bàn tay')
    hand_side: DropdownResponse = Field(..., description='Loại bàn tay')
    finger_type: DropdownResponse = Field(..., description='Loại ngón tay')


class FingerPrintRequest(BaseSchema):
    image_url: str = Field(..., description="URL hình ảnh vân tay")
    hand_side: DropdownRequest = Field(..., description="Bàn tay")
    finger_type: DropdownRequest = Field(..., description="Ngón tay")
