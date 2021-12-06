from typing import Optional

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.schemas.utils import (
    DropdownRequest, DropdownResponse, OpionalDropdownRequest,
    OptionalDropdownResponse
)


########################################################################################################################
# Response
########################################################################################################################
class DomesticAddressResponse(BaseSchema):
    country: OptionalDropdownResponse = Field(..., description="Quốc gia")
    province: OptionalDropdownResponse = Field(..., description="Tỉnh/Thành phố")
    district: OptionalDropdownResponse = Field(..., description="Quận/Huyện")
    ward: OptionalDropdownResponse = Field(..., description="Phường/Xã")
    number_and_street: str = Field(..., min_length=1, description="Số nhà, tên đường")


class ForeignAddressResponse(BaseSchema):
    country: OptionalDropdownResponse = Field(..., description="Quốc gia/Khu vực")
    address_1: Optional[str] = Field(..., description="Địa chỉ 1", nullable=True)
    address_2: Optional[str] = Field(..., description="Địa chỉ 2", nullable=True)
    province: OptionalDropdownResponse = Field(..., description="Thành phố")
    state: OptionalDropdownResponse = Field(..., description="Tỉnh/Bang")
    zip_code: str = Field(..., min_length=1, description="Mã bưu chính", nullable=True)


class ResidentAddressContactInformationResponse(BaseSchema):
    domestic_flag: bool = Field(..., description="""Cờ địa chỉ trong nước
    \n`flag` = `True` => Địa chỉ trong nước
    \n`flag` = `False` => Địa chỉ nước ngoài""")
    domestic_address: Optional[DomesticAddressResponse] = Field(..., description="Địa chỉ trong nước", nullable=True)
    foreign_address: Optional[ForeignAddressResponse] = Field(..., description="Địa chỉ nước ngoài", nullable=True)


class CareerInformationContactInformationResponse(BaseSchema):
    career: DropdownResponse = Field(..., description="Nghề nghiệp")
    average_income_amount: DropdownResponse = Field(..., description="Thu nhập BQ 3 tháng gần nhất")
    company_name: Optional[str] = Field(None, min_length=1, description="Tên cơ quan công tác")
    company_phone: Optional[str] = Field(None, min_length=1, description="Số điện thoại cơ quan")
    company_position: DropdownResponse = Field(None, description="Chức vụ")
    company_address: Optional[str] = Field(None, min_length=1, description="Địa chỉ cơ quan")


# Quốc gia ở địa chỉ liên lạc không bắt buộc nhập ở màn hình 01_03_03
class ContactAddressResponse(DomesticAddressResponse):
    resident_address_flag: bool = Field(..., description="Cờ giống địa chỉ thường trú")
    country: DropdownResponse = Field(None, description="Quốc gia")


class ContactInformationDetailResponse(BaseSchema):
    resident_address: ResidentAddressContactInformationResponse = Field(..., description="I. Địa chỉ thường trú")
    resident_address_active_flag: bool = Field(..., description="Cờ kích hoạt địa chỉ thường trú")
    # Địa chỉ liên lạc sẽ giống với thông tin của địa chỉ trong nước
    contact_address: ContactAddressResponse = Field(..., description="II. Địa chỉ liên lạc")
    contact_address_active_flag: bool = Field(..., description="Cờ kích hoạt địa chỉ liên lạc")
    career_information: CareerInformationContactInformationResponse = Field(..., description="III. Thông tin nghề "
                                                                                             "nghiệp")


########################################################################################################################
# Request Body
########################################################################################################################
class DomesticAddressRequest(BaseSchema):
    country: OpionalDropdownRequest = Field(..., description="Quốc gia")
    province: OpionalDropdownRequest = Field(..., description="Tỉnh/Thành phố")
    district: OpionalDropdownRequest = Field(..., description="Quận/Huyện")
    ward: OpionalDropdownRequest = Field(..., description="Phường/Xã")
    number_and_street: Optional[str] = Field(..., min_length=1, description="Số nhà, tên đường", nullable=True)


class ForeignAddressRequest(BaseSchema):
    country: OpionalDropdownRequest = Field(..., description="Quốc gia/Khu vực")
    address_1: Optional[str] = Field(..., description="Địa chỉ 1", nullable=True)
    address_2: Optional[str] = Field(..., description="Địa chỉ 2", nullable=True)
    province: OpionalDropdownRequest = Field(..., description="Thành phố")
    state: OpionalDropdownRequest = Field(..., description="Tỉnh/Bang")
    zip_code: Optional[str] = Field(..., description="Mã bưu chính", nullable=True)


class ResidentAddressContactInformationRequest(BaseSchema):
    domestic_flag: bool = Field(..., description="""Cờ địa chỉ trong nước
        \n`flag` = `True` => Địa chỉ trong nước
        \n`flag` = `False` => Địa chỉ nước ngoài""")
    domestic_address: Optional[DomesticAddressRequest] = Field(..., description="Địa chỉ trong nước")
    foreign_address: Optional[ForeignAddressRequest] = Field(..., description="Địa chỉ nước ngoài")


class ContactAddressRequest(BaseSchema):
    resident_address_flag: bool = Field(..., description="Cờ giống địa chỉ thường trú")
    province: DropdownRequest = Field(..., description="Tỉnh/Thành phố")
    district: DropdownRequest = Field(..., description="Quận/Huyện")
    ward: DropdownRequest = Field(..., description="Phường/Xã")
    number_and_street: str = Field(..., min_length=1, description="Số nhà, tên đường")


class CareerInformationContactInformationRequest(CareerInformationContactInformationResponse):
    career: DropdownRequest = Field(..., description="Nghề nghiệp")
    average_income_amount: DropdownRequest = Field(..., description="Nghề nghiệp")
    company_position: OpionalDropdownRequest = Field(None, description="Chức vụ", nullable=True)


class ContactInformationSaveRequest(BaseSchema):
    resident_address: Optional[ResidentAddressContactInformationRequest] = Field(
        ..., description="I. Địa chỉ thường trú", nullale=True)
    # Địa chỉ liên lạc sẽ giống với thông tin của địa chỉ trong nước
    contact_address: Optional[ContactAddressRequest] = Field(..., description="II. Địa chỉ liên lạc", nullale=True)
    career_information: CareerInformationContactInformationRequest = Field(
        ..., description="III. Thông tin nghề nghiệp")
