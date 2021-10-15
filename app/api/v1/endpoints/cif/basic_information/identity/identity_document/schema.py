from typing import List

from pydantic import Field

from app.api.base.base_schema import CustomBaseModel
from app.utils.constant.utils import FingerPrintRes, IdentityDocumentTypeRes, GenderRes, PlaceOfIssueRes, \
    NationalityRes, ProvinceRes, DistrictRes, WardRes


class FrontsideInformationRes(CustomBaseModel):
    identity_image_url: str = Field(...)
    face_compare_image_url: str = Field(...)
    similar_percent: int = Field(...)


class BacksideInformationRes(CustomBaseModel):
    identity_image_url: str = Field(...)
    fingerprint: List[FingerPrintRes]
    updated_at: str = Field(...)
    updated_by: str = Field(...)


class AddressRes(CustomBaseModel):
    province: ProvinceRes
    district: DistrictRes
    ward: WardRes
    number_and_street: str = Field(...)


class AddressInformationRes(CustomBaseModel):
    resident_address: AddressRes
    contact_address: AddressRes


# CMND
class IdentityCardDocumentRes(CustomBaseModel):
    identity_number: str = Field(...)
    issued_date: str = Field(...)
    place_of_issue: PlaceOfIssueRes
    expired_date: str = Field(...)


class IdentityBasicInformationRes(CustomBaseModel):
    id: str = Field(...)
    full_name_vn: str = Field(...)
    gender: GenderRes
    date_of_birth: str = Field(...)
    nationality: NationalityRes
    province: ProvinceRes
    identity_characteristic: str = Field(...)   # CMND
    father_full_name_vn: str = Field(...)       # CMND
    mother_full_name_vn: str = Field(...)       # CMND


class IdentityCardOCRResultRes(CustomBaseModel):
    identity_document: IdentityCardDocumentRes
    basic_information: IdentityBasicInformationRes
    address_information: AddressInformationRes


class IdentityCardDocumentRes(CustomBaseModel):
    identity_document_type: IdentityDocumentTypeRes
    frontside_information: FrontsideInformationRes
    backside_information: BacksideInformationRes
    ocr_result: IdentityCardOCRResultRes


# CCCD
class CitizenCardRes(CustomBaseModel):
    identity_number: str = Field(...)
    issued_date: str = Field(...)
    place_of_issue: PlaceOfIssueRes
    expired_date: str = Field(...)
    mrz_content: str = Field(...)       # CCCD
    qr_code_content: str = Field(...)   # CCCD


class CitizenBasicInformationRes(CustomBaseModel):
    id: str = Field(...)
    full_name_vn: str = Field(...)
    gender: GenderRes
    date_of_birth: str = Field(...)
    nationality: NationalityRes
    province: ProvinceRes


class CitizenOCRResultRes(CustomBaseModel):
    identity_document: CitizenCardRes
    basic_information: CitizenBasicInformationRes
    address_information: AddressInformationRes


class CitizenCardDocumentRes(CustomBaseModel):
    identity_document_type: IdentityDocumentTypeRes
    frontside_information: FrontsideInformationRes
    backside_information: BacksideInformationRes
    ocr_result: CitizenOCRResultRes


# HC
class PassportBasicInformationRes(CustomBaseModel):
    full_name_vn: str = Field(...)
    gender: GenderRes
    date_of_birth: str = Field(...)
    nationality: NationalityRes
    place_of_birth: ProvinceRes
    identity_card_number: str = Field(...)
    mrz_content: str = Field(...)


class PassportDocumentRes(CustomBaseModel):
    identity_number: str = Field(...)
    issued_date: str = Field(...)
    place_of_issue: PlaceOfIssueRes
    expired_date: str = Field(...)


class OCRResultRes(CustomBaseModel):
    identity_document: PassportDocumentRes
    basic_information: PassportBasicInformationRes


class PassportInformationRes(CustomBaseModel):
    identity_image_url: str = Field(...)
    face_compare_image_url: str = Field(...)
    similar_percent: int = Field(...)
    fingerprint: List[FingerPrintRes]


class PassportRes(CustomBaseModel):
    identity_document_type: IdentityDocumentTypeRes
    passport_information: PassportInformationRes
    ocr_result: OCRResultRes
