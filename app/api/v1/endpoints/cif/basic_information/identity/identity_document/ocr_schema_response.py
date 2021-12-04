from datetime import date
from typing import Optional

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.schemas.utils import DropdownResponse

# Thông tin dùng chung
########################################################################################################################


# I. Thông tin mặt trước CMND, CCCD
class FrontSideIdentityCitizenCardResponse(BaseSchema):
    identity_image_url: str = Field(..., description="URL hình ảnh mặt trước CMND/CCCD")


class AddressResponse(BaseSchema):
    province: Optional[DropdownResponse] = Field(..., description="Tỉnh/Thành phố")
    district: Optional[DropdownResponse] = Field(..., description="Quận/Huyện")
    ward: Optional[DropdownResponse] = Field(..., description="Phường/Xã")
    number_and_street: Optional[str] = Field(..., description="Số nhà, tên đường")


# III. Phân tích OCR -> 3. Thông tin địa chỉ CMND, CCCD
class OCRAddressIdentityCitizenCardResponse(BaseSchema):
    resident_address: AddressResponse = Field(..., description="Nơi thường trú")
    contact_address: AddressResponse = Field(..., description="Địa chỉ liên hệ")


########################################################################################################################
# Giấy tờ định danh - CMND
########################################################################################################################
# III. Phân tích OCR -> 1. Giấy tờ định danh (CMND)
class OCRFrontSideDocumentIdentityCardResponse(BaseSchema):
    identity_number: Optional[str] = Field(..., description="Số GTĐD")
    expired_date: Optional[date] = Field(..., description="Có giá trị đến")


# III. Phân tích OCR -> 2. Thông tin cơ bản (CMND)
class OCRFrontSideBasicInfoIdentityCardResponse(BaseSchema):
    full_name_vn: Optional[str] = Field(..., description="Họ và tên")
    date_of_birth: Optional[date] = Field(..., description="Ngày sinh")
    nationality: DropdownResponse = Field(..., description="Quốc tịch")
    province: Optional[DropdownResponse] = Field(..., description="Quê quán")


# III. Phân tích OCR (CMND)
class OCRResultIdentityCardResponse(BaseSchema):
    identity_document: OCRFrontSideDocumentIdentityCardResponse = Field(..., description="Giấy tờ định danh")
    basic_information: OCRFrontSideBasicInfoIdentityCardResponse = Field(..., description="Thông tin cơ bản")
    address_information: OCRAddressIdentityCitizenCardResponse = Field(..., description="Thông tin địa chỉ")


# RESPONSE CMND
class OCRFrontSideIdentityCardResponse(BaseSchema):
    front_side_information: FrontSideIdentityCitizenCardResponse = Field(..., description="Thông tin mặt trước")
    ocr_result: OCRResultIdentityCardResponse = Field(..., description="Phân tích OCR")


########################################################################################################################
# Giấy tờ định danh - Hộ chiếu
########################################################################################################################

# I. Thông tin Hộ chiếu
class InformationPassportResponse(BaseSchema):
    identity_image_url: str = Field(..., description="URL hình ảnh Hộ chiếu")


# II. Phân tích OCR -> 1. Giấy tờ định danh (Hộ Chiếu)
class OCRDocumentPassportResponse(BaseSchema):
    identity_number: Optional[str] = Field(..., description="Số GTĐD")
    issued_date: Optional[date] = Field(..., description="Ngày cấp")
    place_of_issue: Optional[DropdownResponse] = Field(..., description="Nơi cấp")
    expired_date: Optional[date] = Field(..., description="Có giá trị đến")
    passport_type: Optional[DropdownResponse] = Field(..., description="Loại")
    passport_code: Optional[DropdownResponse] = Field(..., description="Mã số")


# II. Phân tích OCR -> 2. Thông tin cơ bản (Hộ Chiếu)
class OCRBasicInfoPassportResponse(BaseSchema):
    full_name_vn: Optional[str] = Field(..., description="Họ và tên")
    gender: Optional[DropdownResponse] = Field(..., description="Giới tính")
    date_of_birth: Optional[date] = Field(..., description="Ngày sinh")
    nationality: Optional[DropdownResponse] = Field(..., description="Quốc tịch")
    place_of_birth: Optional[DropdownResponse] = Field(..., description="Nơi sinh")
    identity_card_number: Optional[str] = Field(..., description="Số CMND")
    mrz_content: Optional[str] = Field(None, description="Mã MRZ")


# II. Phân tích OCR (HC)
class OCRResultPassportResponse(BaseSchema):
    identity_document: OCRDocumentPassportResponse = Field(..., description="Giấy tờ định danh")
    basic_information: OCRBasicInfoPassportResponse = Field(..., description="Thông tin cơ bản")


# RESPONSE HC
class OCRPassportResponse(BaseSchema):
    passport_information: InformationPassportResponse = Field(..., description="Thông tin hộ chiếu")
    ocr_result: OCRResultPassportResponse = Field(..., description="Phân tích OCR")

########################################################################################################################
