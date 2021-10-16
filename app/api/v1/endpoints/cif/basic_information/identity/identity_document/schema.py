from datetime import datetime
from typing import List

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.schemas.cif import (
    FingerPrint, IdentityDocumentType, PlaceOfIssue
)
from app.api.v1.schemas.utils import (
    District, Gender, Nationality, Province, Ward
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
    fingerprint: List[FingerPrint]


# II. Thông tin mặt sau CMND, CCCD
class BackSideInformation(BaseSchema):
    identity_image_url: str = Field(...)
    fingerprint: List[FingerPrint]
    updated_at: str = Field(...)
    updated_by: str = Field(...)


# III. Phân tích OCR -> 1. Giấy tờ định danh (CMND)
class IdentityCardDocumentRes(BaseSchema):
    identity_number: str = Field(...)
    issued_date: str = Field(...)
    place_of_issue: PlaceOfIssue
    expired_date: str = Field(...)


# III. Phân tích OCR -> 2. Thông tin cơ bản
class IdentityBasicInformationRes(BaseSchema):
    id: str = Field(...)
    full_name_vn: str = Field(...)
    gender: Gender
    date_of_birth: str = Field(...)
    nationality: Nationality
    province: Province
    identity_characteristic: str = Field(...)  # CMND
    father_full_name_vn: str = Field(...)  # CMND
    mother_full_name_vn: str = Field(...)  # CMND


# III. Phân tích OCR -> 3. Thông tin địa chỉ -> Nơi thường trú/ Địa chỉ liên hệ
class AddressRes(BaseSchema):
    province: Province
    district: District
    ward: Ward
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
    place_of_issue: PlaceOfIssue
    expired_date: str = Field(...)
    mrz_content: str = Field(...)  # CCCD
    qr_code_content: str = Field(...)  # CCCD


class CitizenBasicInformationRes(BaseSchema):
    id: str = Field(...)
    full_name_vn: str = Field(...)
    gender: Gender
    date_of_birth: str = Field(...)
    nationality: Nationality
    province: Province


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
    gender: Gender
    date_of_birth: str = Field(...)
    nationality: Nationality
    place_of_birth: Province
    identity_card_number: str = Field(...)
    mrz_content: str = Field(...)


class PassportDocumentRes(BaseSchema):
    identity_number: str = Field(...)
    issued_date: str = Field(...)
    place_of_issue: PlaceOfIssue
    expired_date: str = Field(...)


# III. Phân tích OCR (HC)
class OCRResultRes(BaseSchema):
    identity_document: PassportDocumentRes
    basic_information: PassportBasicInformationRes


########################################################################################################################
# response detail giấy tờ định danh
########################################################################################################################

class IdentityCardDetailRes(BaseSchema):
    identity_document_type: IdentityDocumentType
    frontside_information: FrontSideInformation
    backside_information: BackSideInformation
    ocr_result: IdentityCardOCRResultRes


class CitizenCardDetailRes(BaseSchema):
    identity_document_type: IdentityDocumentType
    frontside_information: FrontSideInformation
    backside_information: BackSideInformation
    ocr_result: CitizenOCRResultRes


class PassportDetailRes(BaseSchema):
    identity_document_type: IdentityDocumentType
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
