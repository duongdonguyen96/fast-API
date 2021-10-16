from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.schemas.utils import Dropdown


# Đối tượng khách hàng
class CustomerClassification(Dropdown):
    pass


# Mã ngành KT
class CustomerEconomicProfession(Dropdown):
    pass


# Cấp độ KYC
class KYCLevel(Dropdown):
    pass


# Loại giấy tờ định danh
class IdentityDocumentType(Dropdown):
    pass


class PlaceOfIssue(Dropdown):
    pass


class HandSide(Dropdown):
    pass


class FingerType(Dropdown):
    pass


class FingerPrint(BaseSchema):
    id: str = Field(...)
    image_url: str = Field(...)
    hand_side: HandSide
    finger_type: FingerType
