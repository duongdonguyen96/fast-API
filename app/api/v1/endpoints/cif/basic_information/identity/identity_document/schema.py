from datetime import datetime
from typing import List

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.schemas.cif import (
    FingerPrintResponse, IdentityDocumentTypeResponse, PlaceOfIssueResponse
)
from app.api.v1.schemas.utils import (
    DistrictResponse, GenderResponse, NationalityResponse, ProvinceResponse,
    WardResponse
)


# I. Thông tin mặt trước CMND, CCCD
class FrontSideInformation(BaseSchema):
    identity_image_url: str = Field(...)
    face_compare_image_url: str = Field(...)
    similar_percent: int = Field(...)


# I. Thông tin HC
class PassportInformationRes(BaseSchema):
    identity_image_url: str = Field(...)
    face_compare_image_url: str = Field(...)
    similar_percent: int = Field(...)
    fingerprint: List[FingerPrintResponse]


# II. Thông tin mặt sau CMND, CCCD
class BackSideInformation(BaseSchema):
    identity_image_url: str = Field(...)
    fingerprint: List[FingerPrintResponse]
    updated_at: str = Field(...)
    updated_by: str = Field(...)


# III. Phân tích OCR -> 1. Giấy tờ định danh (CMND)
class IdentityCardDocumentRes(BaseSchema):
    identity_number: str = Field(...)
    issued_date: str = Field(...)
    place_of_issue: PlaceOfIssueResponse
    expired_date: str = Field(...)


# III. Phân tích OCR -> 2. Thông tin cơ bản
class IdentityBasicInformationRes(BaseSchema):
    id: str = Field(...)
    full_name_vn: str = Field(...)
    gender: GenderResponse
    date_of_birth: str = Field(...)
    nationality: NationalityResponse
    province: ProvinceResponse
    identity_characteristic: str = Field(...)  # CMND
    father_full_name_vn: str = Field(...)  # CMND
    mother_full_name_vn: str = Field(...)  # CMND


# III. Phân tích OCR -> 3. Thông tin địa chỉ -> Nơi thường trú/ Địa chỉ liên hệ
class AddressRes(BaseSchema):
    province: ProvinceResponse
    district: DistrictResponse
    ward: WardResponse
    number_and_street: str = Field(...)


# III. Phân tích OCR -> 3. Thông tin địa chỉ
class AddressInformationRes(BaseSchema):
    resident_address: AddressRes
    contact_address: AddressRes


# III. Phân tích OCR (CMND)
class IdentityCardOCRResultRes(BaseSchema):
    identity_document: IdentityCardDocumentRes
    basic_information: IdentityBasicInformationRes
    address_information: AddressInformationRes


# CCCD
class CitizenCardRes(BaseSchema):
    identity_number: str = Field(...)
    issued_date: str = Field(...)
    place_of_issue: PlaceOfIssueResponse
    expired_date: str = Field(...)
    mrz_content: str = Field(...)  # CCCD
    qr_code_content: str = Field(...)  # CCCD


class CitizenBasicInformationRes(BaseSchema):
    id: str = Field(...)
    full_name_vn: str = Field(...)
    gender: GenderResponse
    date_of_birth: str = Field(...)
    nationality: NationalityResponse
    province: ProvinceResponse


class CitizenOCRResultRes(BaseSchema):
    identity_document: CitizenCardRes
    basic_information: CitizenBasicInformationRes
    address_information: AddressInformationRes


class CitizenCardCreateSuccessRes(BaseSchema):
    cif_id: str = Field(...)
    created_at: datetime
    created_by: str = Field(...)


# HC
class PassportBasicInformationRes(BaseSchema):
    full_name_vn: str = Field(...)
    gender: GenderResponse
    date_of_birth: str = Field(...)
    nationality: NationalityResponse
    place_of_birth: ProvinceResponse
    identity_card_number: str = Field(...)
    mrz_content: str = Field(...)


class PassportDocumentRes(BaseSchema):
    identity_number: str = Field(...)
    issued_date: str = Field(...)
    place_of_issue: PlaceOfIssueResponse
    expired_date: str = Field(...)


# III. Phân tích OCR (HC)
class OCRResultRes(BaseSchema):
    identity_document: PassportDocumentRes
    basic_information: PassportBasicInformationRes


########################################################################################################################
# response detail giấy tờ định danh
########################################################################################################################

class IdentityCardDetailRes(BaseSchema):
    identity_document_type: IdentityDocumentTypeResponse
    frontside_information: FrontSideInformation
    backside_information: BackSideInformation
    ocr_result: IdentityCardOCRResultRes


class CitizenCardDetailRes(BaseSchema):
    identity_document_type: IdentityDocumentTypeResponse
    frontside_information: FrontSideInformation
    backside_information: BackSideInformation
    ocr_result: CitizenOCRResultRes


class PassportDetailRes(BaseSchema):
    identity_document_type: IdentityDocumentTypeResponse
    passport_information: PassportInformationRes
    ocr_result: OCRResultRes


########################################################################################################################
# request body save giấy tờ định danh
########################################################################################################################

class IdentityCardSaveReq(IdentityCardDetailRes):
    cif_id: str


class CitizenCardSaveReq(CitizenCardDetailRes):
    cif_id: str


class PassportSaveReq(PassportDetailRes):
    cif_id: str


########################################################################################################################
# response save giấy tờ định danh
########################################################################################################################

class IdentityDocumentSaveSuccessRes(BaseSchema):
    cif_id: str = Field(...)
    created_at: datetime
    created_by: str = Field(...)
