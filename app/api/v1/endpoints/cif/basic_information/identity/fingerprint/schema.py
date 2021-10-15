from typing import List

from app.api.base.base_schema import CustomBaseModel


class HandSide(CustomBaseModel):
    id: str
    code: str
    name: str


class FingerType(CustomBaseModel):
    id: str
    code: str
    name: str


class Fingerprint(CustomBaseModel):
    image_url: str
    hand_side: HandSide
    finger_type: FingerType


class DocumentRes(CustomBaseModel):
    fingerprint_1: List[Fingerprint]
    fingerprint_2: List[Fingerprint]
