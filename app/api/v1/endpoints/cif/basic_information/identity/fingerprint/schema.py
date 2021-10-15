from typing import List

from app.api.base.schema import BaseSchema


class HandSide(BaseSchema):
    id: str
    code: str
    name: str


class FingerType(BaseSchema):
    id: str
    code: str
    name: str


class FingerPrint(BaseSchema):
    image_url: str
    hand_side: HandSide
    finger_type: FingerType


class FingerPrintRes(BaseSchema):
    fingerprint_1: List[FingerPrint]
    fingerprint_2: List[FingerPrint]
