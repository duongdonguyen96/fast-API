from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.schemas.utils import DropdownResponse


# Đối tượng khách hàng
class CustomerClassificationResponse(DropdownResponse):
    pass


# Mã ngành KT
class CustomerEconomicProfessionResponse(DropdownResponse):
    pass


# Cấp độ KYC
class KYCLevelResponse(DropdownResponse):
    pass


# Loại giấy tờ định danh
class IdentityDocumentTypeResponse(DropdownResponse):
    pass


class PlaceOfIssueResponse(DropdownResponse):
    pass


class HandSideResponse(DropdownResponse):
    pass


class FingerTypeResponse(DropdownResponse):
    pass


class FingerPrintResponse(BaseSchema):
    image_url: str = Field(..., description='Ảnh bàn tay')
    hand_side: DropdownResponse = Field(..., description='Bàn tay')
    finger_type: DropdownResponse = Field(..., description='Ngón tay')
