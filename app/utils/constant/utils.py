from pydantic import Field

from app.api.base.base_schema import CustomBaseModel


class IdentityDocumentTypeRes(CustomBaseModel):
    id: str = Field(...)
    code: str = Field(...)
    name: str = Field(...)


class HandSideRes(CustomBaseModel):
    id: str = Field(...)
    code: str = Field(...)
    name: str = Field(...)


class FingerTypeRes(CustomBaseModel):
    id: str = Field(...)
    code: str = Field(...)
    name: str = Field(...)


class PlaceOfIssueRes(CustomBaseModel):
    id: str = Field(...)
    code: str = Field(...)
    name: str = Field(...)


class GenderRes(CustomBaseModel):
    id: str = Field(...)
    code: str = Field(...)
    name: str = Field(...)


class NationalityRes(CustomBaseModel):
    id: str = Field(...)
    code: str = Field(...)
    name: str = Field(...)


class ProvinceRes(CustomBaseModel):
    id: str = Field(...)
    code: str = Field(...)
    name: str = Field(...)


class DistrictRes(CustomBaseModel):
    id: str = Field(...)
    code: str = Field(...)
    name: str = Field(...)


class WardRes(CustomBaseModel):
    id: str = Field(...)
    code: str = Field(...)
    name: str = Field(...)


class FingerPrintRes(CustomBaseModel):
    id: str = Field(...)
    image_url: str = Field(...)
    hand_side: HandSideRes
    finger_type: FingerTypeRes
