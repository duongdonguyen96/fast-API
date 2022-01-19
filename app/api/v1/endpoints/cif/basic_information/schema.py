from datetime import date
from typing import Optional

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.schemas.cif import OptionalAddressResponse
########################################################################################################################
# Response
########################################################################################################################
# Thông tin chi tiết người giám hộ hoặc người có quan hệ với khách hàng qua mã CIF
from app.api.v1.schemas.utils import OptionalDropdownResponse


# I. Thông tin cơ bản
class BasicInformationResponse(BaseSchema):
    cif_number: Optional[str] = Field(..., description="Số CIF")
    full_name_vn: Optional[str] = Field(..., description="Họ và tên")
    date_of_birth: Optional[date] = Field(..., description="Ngày sinh")
    gender: OptionalDropdownResponse = Field(..., description="Giới tính")
    nationality: OptionalDropdownResponse = Field(..., description="Quốc tịch")
    telephone_number: Optional[str] = Field(..., description="Số ĐT bàn")
    mobile_number: Optional[str] = Field(..., description="Số ĐTDĐ")
    email: Optional[str] = Field(..., description="Email")


# II. Giấy tờ định danh
class IdentityDocumentResponse(BaseSchema):
    identity_number: Optional[str] = Field(..., description="Số CMND/CCCD/Hộ chiếu")
    issued_date: Optional[date] = Field(..., description="Ngày cấp")
    expired_date: Optional[date] = Field(..., description="Ngày hết hạn")
    place_of_issue: OptionalDropdownResponse = Field(..., description="Nơi cấp")


# III. Thông tin địa chỉ
class AddressInformationResponse(BaseSchema):
    resident_address: OptionalAddressResponse = Field(..., description="Địa chỉ thường trú")
    contact_address: OptionalAddressResponse = Field(..., description="Địa chỉ liên hệ")


class DetailRelationshipResponse(BaseSchema):
    basic_information: BasicInformationResponse = Field(..., description="I. Thông tin cơ bản")
    identity_document: IdentityDocumentResponse = Field(..., description="II. Giấy tờ định danh")
    address_information: AddressInformationResponse = Field(..., description="III. Thông tin địa chỉ")

########################################################################################################################
# Request Body
########################################################################################################################
