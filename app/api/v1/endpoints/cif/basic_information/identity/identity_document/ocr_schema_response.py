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
    province: Optional[DropdownResponse] = Field(..., description="Tỉnh/Thành phố", nullable=True)
    district: Optional[DropdownResponse] = Field(..., description="Quận/Huyện", nullable=True)
    ward: Optional[DropdownResponse] = Field(..., description="Phường/Xã", nullable=True)
    number_and_street: Optional[str] = Field(..., description="Số nhà, tên đường", nullable=True)


# III. Phân tích OCR -> 3. Thông tin địa chỉ CMND, CCCD
class OCRAddressIdentityCitizenCardResponse(BaseSchema):
    resident_address: AddressResponse = Field(..., description="Nơi thường trú")
    contact_address: AddressResponse = Field(..., description="Địa chỉ liên hệ")


########################################################################################################################
# Giấy tờ định danh - CMND
########################################################################################################################
# III. Phân tích OCR -> 1. Giấy tờ định danh (CMND)
class OCRFrontSideDocumentIdentityCardResponse(BaseSchema):
    identity_number: Optional[str] = Field(..., description="Số GTĐD", nullable=True)


# III. Phân tích OCR -> 2. Thông tin cơ bản (CMND)
class OCRFrontSideBasicInfoIdentityCardResponse(BaseSchema):
    full_name_vn: Optional[str] = Field(..., description="Họ và tên", nullable=True)
    date_of_birth: Optional[date] = Field(..., description="Ngày sinh", nullable=True)
    nationality: DropdownResponse = Field(..., description="Quốc tịch")
    province: Optional[DropdownResponse] = Field(..., description="Quê quán", nullable=True)


# III. Phân tích OCR (CMND)
class OCRResultFrontSideIdentityCardResponse(BaseSchema):
    identity_document: OCRFrontSideDocumentIdentityCardResponse = Field(..., description="Giấy tờ định danh")
    basic_information: OCRFrontSideBasicInfoIdentityCardResponse = Field(..., description="Thông tin cơ bản")
    address_information: OCRAddressIdentityCitizenCardResponse = Field(..., description="Thông tin địa chỉ")


# RESPONSE CMND
class OCRFrontSideIdentityCardResponse(BaseSchema):
    front_side_information: FrontSideIdentityCitizenCardResponse = Field(..., description="Thông tin mặt trước")
    ocr_result: OCRResultFrontSideIdentityCardResponse = Field(...,
                                                               description="Phân tích OCR thông tin mặt trước CMND")


class BackSideIdentityCardResponse(BaseSchema):
    identity_image_url: Optional[str] = Field(..., description="URL hình ảnh mặt sau CMND", nullable=True)


class OCRBackSideIdentityDocumentIdentityCardResponse(BaseSchema):
    issued_date: Optional[date] = Field(..., description="Ngày cấp", nullable=True)
    place_of_issue: Optional[DropdownResponse] = Field(..., description="Nơi cấp", nullable=True)


class OCRBackSideBasicInformationIdentityCardResponse(BaseSchema):
    ethnic: Optional[DropdownResponse] = Field(..., description="Dân tộc", nullable=True)
    religion: Optional[DropdownResponse] = Field(..., description="Tôn giáo", nullable=True)
    identity_characteristic: Optional[str] = Field(..., description="Đặc điểm nhận dạng", nullable=True)


class OCRResultBackSideIdentityCardResponse(BaseSchema):
    identity_document: OCRBackSideIdentityDocumentIdentityCardResponse = Field(..., description="Giấy tờ định danh")
    basic_information: OCRBackSideBasicInformationIdentityCardResponse = Field(..., description="Thông tin cơ bản")


class OCRBackSideIdentityCardResponse(BaseSchema):
    back_side_information: BackSideIdentityCardResponse = Field(..., description="Thông tin mặt sau")
    ocr_result: OCRResultBackSideIdentityCardResponse = Field(..., description="Phân tích OCR mặt sau CMND")


########################################################################################################################
# Giấy tờ định danh - Hộ chiếu
########################################################################################################################

# I. Thông tin Hộ chiếu
class InformationPassportResponse(BaseSchema):
    identity_image_url: str = Field(..., description="URL hình ảnh Hộ chiếu")


# II. Phân tích OCR -> 1. Giấy tờ định danh (Hộ Chiếu)
class OCRDocumentPassportResponse(BaseSchema):
    identity_number: Optional[str] = Field(..., description="Số GTĐD", nullable=True)
    issued_date: Optional[date] = Field(..., description="Ngày cấp", nullable=True)
    place_of_issue: Optional[DropdownResponse] = Field(..., description="Nơi cấp", nullable=True)
    expired_date: Optional[date] = Field(..., description="Có giá trị đến", nullable=True)
    passport_type: Optional[DropdownResponse] = Field(..., description="Loại", nullable=True)
    passport_code: Optional[DropdownResponse] = Field(..., description="Mã số", nullable=True)


# II. Phân tích OCR -> 2. Thông tin cơ bản (Hộ Chiếu)
class OCRBasicInfoPassportResponse(BaseSchema):
    full_name_vn: Optional[str] = Field(..., description="Họ và tên", nullable=True)
    gender: Optional[DropdownResponse] = Field(..., description="Giới tính", nullable=True)
    date_of_birth: Optional[date] = Field(..., description="Ngày sinh", nullable=True)
    nationality: Optional[DropdownResponse] = Field(..., description="Quốc tịch", nullable=True)
    place_of_birth: Optional[DropdownResponse] = Field(..., description="Nơi sinh", nullable=True)
    identity_card_number: Optional[str] = Field(..., description="Số CMND", nullable=True)
    mrz_content: Optional[str] = Field(None, description="Mã MRZ", nullable=True)


# II. Phân tích OCR (HC)
class OCRResultPassportResponse(BaseSchema):
    identity_document: OCRDocumentPassportResponse = Field(..., description="Giấy tờ định danh")
    basic_information: OCRBasicInfoPassportResponse = Field(..., description="Thông tin cơ bản")


# RESPONSE HC
class OCRPassportResponse(BaseSchema):
    passport_information: InformationPassportResponse = Field(..., description="Thông tin hộ chiếu")
    ocr_result: OCRResultPassportResponse = Field(..., description="Phân tích OCR")


########################################################################################################################

########################################################################################################################
# Giấy tờ định danh - Hộ chiếu
########################################################################################################################

# III. Phân tích OCR (CCCD) -> Giấy tờ định danh
class OCRFrontSideDocumentCitizenCardResponse(OCRFrontSideDocumentIdentityCardResponse):
    expired_date: Optional[date] = Field(..., description="Có giá trị đến", nullable=True)


# III. Phân tích OCR (CCCD) -> Thông tin cơ bản
class OCRFrontSideBasicInfoCitizenCardResponse(OCRFrontSideBasicInfoIdentityCardResponse):
    gender: Optional[DropdownResponse] = Field(..., description="Giới tính", nullable=True)


# III. Phân tích OCR (CCCD)
class OCRResultFrontSideCitizenCardResponse(BaseSchema):
    identity_document: OCRFrontSideDocumentCitizenCardResponse = Field(..., description="Giấy tờ định danh")
    basic_information: OCRFrontSideBasicInfoCitizenCardResponse = Field(..., description="Thông tin cơ bản")
    address_information: OCRAddressIdentityCitizenCardResponse = Field(..., description="Thông tin địa chỉ")


class OCRFrontSideCitizenCardResponse(BaseSchema):
    front_side_information: FrontSideIdentityCitizenCardResponse = Field(..., description="Thông tin mặt trước")
    ocr_result: OCRResultFrontSideCitizenCardResponse = Field(...,
                                                              description="Phân tích OCR thông tin mặt trước CCCD")


class BackSideCitizenCardResponse(BaseSchema):
    identity_image_url: Optional[str] = Field(..., description="URL hình ảnh mặt sau CMND", nullable=True)


class OCRBackSideIdentityDocumentCitizenCardResponse(BaseSchema):
    issued_date: Optional[date] = Field(..., description="Ngày cấp", nullable=True)
    place_of_issue: Optional[DropdownResponse] = Field(..., description="Nơi cấp", nullable=True)
    mrz_content: Optional[str] = Field(..., description="Đặc điểm nhận dạng", nullable=True)


class OCRBackSideBasicInformationCitizenCardResponse(BaseSchema):
    identity_characteristic: Optional[str] = Field(..., description="Đặc điểm nhận dạng", nullable=True)


class OCRResultBackSideCitizenCardResponse(BaseSchema):
    identity_document: OCRBackSideIdentityDocumentCitizenCardResponse = Field(..., description="Giấy tờ định danh")
    basic_information: OCRBackSideBasicInformationCitizenCardResponse = Field(..., description="Thông tin cơ bản")


class OCRBackSideCitizenCardResponse(BaseSchema):
    back_side_information: BackSideCitizenCardResponse = Field(..., description="Thông tin mặt sau")
    ocr_result: OCRResultBackSideCitizenCardResponse = Field(..., description="Phân tích OCR mặt sau CCCD")
########################################################################################################################


########################################################################################################################
# So sánh khuôn mặt đối chiếu với khuôn mặt trên giấy tờ định danh
########################################################################################################################
class CompareSuccessResponse(BaseSchema):
    similar_percent: float = Field(
        ...,
        description="Tỉ lệ chính xác giữa khuôn mặt đối chiếu với khuôn mặt trên giấy tờ định danh"
    )
