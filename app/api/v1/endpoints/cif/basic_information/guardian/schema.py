from typing import List

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.schemas.cif import AddressResponse
from app.api.v1.schemas.utils import DropdownResponse


class BasicInformationResponse(BaseSchema):
    cif_number: str = Field(..., description="Số CIF")
    customer_relationship: DropdownResponse = Field(..., description="Mối quan hệ với khách hàng")
    full_name_vn: str = Field(..., description="Họ và tên")
    date_of_birth: str = Field(..., description="Ngày sinh")
    gender: DropdownResponse = Field(..., description="Giới tính")
    nationality: DropdownResponse = Field(..., description="Quốc tịch")
    telephone_number: str = Field(..., description="Số ĐT bàn")
    mobile_number: str = Field(..., description="Số ĐTDĐ")
    email: str = Field(..., description="Email")


class IdentityDocumentResponse(BaseSchema):
    identity_number: str = Field(..., description="Số CMND/CCCD/Hộ chiếu")
    issued_date: str = Field(..., description="Ngày cấp")
    expired_date: str = Field(..., description="Ngày hết hạn")
    place_of_issue: DropdownResponse = Field(..., description="Nơi cấp")


class AddressInformationResponse(BaseSchema):
    resident_address: AddressResponse = Field(..., description="Cờ có người giám hộ không")
    contact_address: AddressResponse = Field(..., description="Cờ có người giám hộ không")


class GuardianResponse(BaseSchema):
    id: str = Field(..., description="ID người giám hộ")
    avatar_url: str = Field(..., description="URL avatar người giám hộ")
    basic_information: BasicInformationResponse = Field(..., description="I. Thông tin cơ bản")
    identity_document: IdentityDocumentResponse = Field(..., description="II. Giấy tờ định danh")
    address_information: AddressInformationResponse = Field(..., description="III. Thông tin địa chỉ")


class DetailGuardianResponse(BaseSchema):
    guardian_flag: bool = Field(..., description="Cờ có người giám hộ không")
    number_of_guardian: int = Field(..., description="Số người giám hộ")
    guardians: List[GuardianResponse] = Field(..., description="Danh sách người giám hộ")
