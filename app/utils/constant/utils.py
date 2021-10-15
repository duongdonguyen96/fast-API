from pydantic import Field

from app.api.base.schema import BaseSchema


class IdentityDocumentTypeRes(BaseSchema):
    id: str = Field(...)
    code: str = Field(...)
    name: str = Field(...)


class HandSideRes(BaseSchema):
    id: str = Field(...)
    code: str = Field(...)
    name: str = Field(...)


class FingerTypeRes(BaseSchema):
    id: str = Field(...)
    code: str = Field(...)
    name: str = Field(...)


class PlaceOfIssueRes(BaseSchema):
    id: str = Field(...)
    code: str = Field(...)
    name: str = Field(...)


class GenderRes(BaseSchema):
    id: str = Field(...)
    code: str = Field(...)
    name: str = Field(...)


class NationalityRes(BaseSchema):
    id: str = Field(...)
    code: str = Field(...)
    name: str = Field(...)


class ProvinceRes(BaseSchema):
    id: str = Field(...)
    code: str = Field(...)
    name: str = Field(...)


class DistrictRes(BaseSchema):
    id: str = Field(...)
    code: str = Field(...)
    name: str = Field(...)


class WardRes(BaseSchema):
    id: str = Field(...)
    code: str = Field(...)
    name: str = Field(...)


class FingerPrintRes(BaseSchema):
    id: str = Field(...)
    image_url: str = Field(...)
    hand_side: HandSideRes
    finger_type: FingerTypeRes
