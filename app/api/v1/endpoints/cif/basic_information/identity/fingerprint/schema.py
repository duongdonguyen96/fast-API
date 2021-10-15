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


class Fingerprint(BaseSchema):
    image_url: str
    hand_side: HandSide
    finger_type: FingerType


class DocumentRes(BaseSchema):
    fingerprint_1: List[Fingerprint]
    fingerprint_2: List[Fingerprint]


class FingerReq(BaseSchema):
    fingerprint_1: List[Fingerprint]
    fingerprint_2: List[Fingerprint]
