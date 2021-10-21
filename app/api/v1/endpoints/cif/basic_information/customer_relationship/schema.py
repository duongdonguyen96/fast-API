from datetime import date
from typing import List

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.schemas.cif import AddressResponse
from app.api.v1.schemas.utils import DropdownRequest, DropdownResponse


########################################################################################################################
# Response
########################################################################################################################
# Thông tin mối quan hệ khách hàng -> Danh sách mối quan hệ khách hàng -> I. Thông tin cơ bản
class BasicInformationResponse(BaseSchema):
    cif_number: str = Field(..., description="Số CIF")
    customer_relationship: DropdownResponse = Field(..., description="Mối quan hệ với khách hàng")
    full_name_vn: str = Field(..., description="Họ và tên")
    date_of_birth: date = Field(..., description="Ngày sinh")
    gender: DropdownResponse = Field(..., description="Giới tính")
    nationality: DropdownResponse = Field(..., description="Quốc tịch")
    telephone_number: str = Field(..., description="Số ĐT bàn")
    mobile_number: str = Field(..., description="Số ĐTDĐ")


# Thông tin mối quan hệ khách hàng -> Danh sách mối quan hệ khách hàng -> II. Giấy tờ định danh
class IdentityDocumentResponse(BaseSchema):
    identity_number: str = Field(..., description="Số CMND/CCCD/Hộ chiếu")
    issued_date: date = Field(..., description="Ngày cấp")
    expired_date: date = Field(..., description="Ngày hết hạn")
    place_of_issue: DropdownResponse = Field(..., description="Nơi cấp")


# Thông tin mối quan hệ khách hàng -> Danh sách mối quan hệ khách hàng -> III. Thông tin địa chỉ
class AddressInformationResponse(BaseSchema):
    resident_address: AddressResponse = Field(..., description="Cờ có mối quan hệ khách hàng không")
    contact_address: AddressResponse = Field(..., description="Cờ có mối quan hệ khách hàng không")


# Thông tin mối quan hệ khách hàng -> Danh sách mối quan hệ khách hàng
class CustomerRelationshipResponse(BaseSchema):
    id: str = Field(..., description="ID mối quan hệ khách hàng")
    avatar_url: str = Field(..., description="URL avatar mối quan hệ khách hàng")
    basic_information: BasicInformationResponse = Field(..., description="I. Thông tin cơ bản")
    identity_document: IdentityDocumentResponse = Field(..., description="II. Giấy tờ định danh")
    address_information: AddressInformationResponse = Field(..., description="III. Thông tin địa chỉ")


# Thông tin mối quan hệ khách hàng
class DetailCustomerRelationshipResponse(BaseSchema):
    customer_relationship_flag: bool = Field(..., description="Cờ có người mối quan hệ khách hàng không")
    number_of_customer_relationship: int = Field(..., description="Số mối quan hệ khách hàng")
    relationships: List[CustomerRelationshipResponse] = Field(..., description="Danh sách mối quan hệ khách hàng")


########################################################################################################################
# Request Body
########################################################################################################################
# Thông tin mối quan hệ khách hàng
class SaveCustomerRelationshipRequest(BaseSchema):
    cif_number: str = Field(..., description="Số CIF")
    customer_relationship: DropdownRequest = Field(..., description="Mối quan hệ với khách hàng")
