from typing import List

from app.api.base.schema import BaseSchema
from app.api.v1.schemas.cif import FingerPrint


class HandSide(BaseSchema):
    id: str
    code: str
    name: str


class FingerType(BaseSchema):
    id: str
    code: str
    name: str


class FingerReq(BaseSchema):
    fingerprint_1: List[FingerPrint]
    fingerprint_2: List[FingerPrint]


class FingerPrintRes(BaseSchema):
    fingerprint_1: List[FingerPrint]
    fingerprint_2: List[FingerPrint]
