from datetime import date
from typing import List

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.schemas.cif import AddressRequest, AddressResponse
from app.api.v1.schemas.utils import DropdownRequest, DropdownResponse


########################################################################################################################
# Response
########################################################################################################################
# Thông tin người giám hộ -> Danh sách người giám hộ -> I. Thông tin cơ bản
class BasicInformationResponse(BaseSchema):
    cif_number: str = Field(..., description="Số CIF")
    customer_relationship: DropdownResponse = Field(..., description="Mối quan hệ với khách hàng")
    full_name_vn: str = Field(..., description="Họ và tên")
    date_of_birth: date = Field(..., description="Ngày sinh")
    gender: DropdownResponse = Field(..., description="Giới tính")
    nationality: DropdownResponse = Field(..., description="Quốc tịch")
    telephone_number: str = Field(..., description="Số ĐT bàn")
    mobile_number: str = Field(..., description="Số ĐTDĐ")
    email: str = Field(..., description="Email")


# Thông tin người giám hộ -> Danh sách người giám hộ -> II. Giấy tờ định danh
class IdentityDocumentResponse(BaseSchema):
    identity_number: str = Field(..., description="Số CMND/CCCD/Hộ chiếu")
    issued_date: date = Field(..., description="Ngày cấp")
    expired_date: date = Field(..., description="Ngày hết hạn")
    place_of_issue: DropdownResponse = Field(..., description="Nơi cấp")


# Thông tin người giám hộ -> Danh sách người giám hộ -> III. Thông tin địa chỉ
class AddressInformationResponse(BaseSchema):
    resident_address: AddressResponse = Field(..., description="Cờ có người giám hộ không")
    contact_address: AddressResponse = Field(..., description="Cờ có người giám hộ không")


# Thông tin người giám hộ -> Danh sách người giám hộ
class GuardianResponse(BaseSchema):
    id: str = Field(..., description="ID người giám hộ")
    avatar_url: str = Field(..., description="URL avatar người giám hộ")
    basic_information: BasicInformationResponse = Field(..., description="I. Thông tin cơ bản")
    identity_document: IdentityDocumentResponse = Field(..., description="II. Giấy tờ định danh")
    address_information: AddressInformationResponse = Field(..., description="III. Thông tin địa chỉ")


# Thông tin người giám hộ
class DetailGuardianResponse(BaseSchema):
    guardian_flag: bool = Field(..., description="Cờ có người giám hộ không")
    number_of_guardian: int = Field(..., description="Số người giám hộ")
    guardians: List[GuardianResponse] = Field(..., description="Danh sách người giám hộ")


########################################################################################################################
# Request Body
########################################################################################################################
# Thông tin người giám hộ -> Danh sách người giám hộ -> I. Thông tin cơ bản
class BasicInformationRequest(BasicInformationResponse):
    customer_relationship: DropdownRequest = Field(..., description="Mối quan hệ với khách hàng")
    gender: DropdownRequest = Field(..., description="Giới tính")
    nationality: DropdownRequest = Field(..., description="Quốc tịch")


# Thông tin người giám hộ -> Danh sách người giám hộ -> II. Giấy tờ định danh
class IdentityDocumentRequest(IdentityDocumentResponse):
    place_of_issue: DropdownRequest = Field(..., description="Nơi cấp")


# Thông tin người giám hộ -> Danh sách người giám hộ -> III. Thông tin địa chỉ
class AddressInformationRequest(BaseSchema):
    resident_address: AddressRequest = Field(..., description="Cờ có người giám hộ không")
    contact_address: AddressRequest = Field(..., description="Cờ có người giám hộ không")


# Thông tin người giám hộ -> Danh sách người giám hộ
class GuardianRequest(GuardianResponse):
    basic_information: BasicInformationRequest = Field(..., description="I. Thông tin cơ bản")
    identity_document: IdentityDocumentRequest = Field(..., description="II. Giấy tờ định danh")
    address_information: AddressInformationRequest = Field(..., description="III. Thông tin địa chỉ")


# Thông tin người giám hộ
class SaveGuardianRequest(DetailGuardianResponse):
    guardians: List[GuardianRequest] = Field(..., description="Danh sách người giám hộ")
