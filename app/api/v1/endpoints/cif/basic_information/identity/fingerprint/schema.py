from typing import List

from app.api.base.schema import BaseSchema
from app.api.v1.schemas.cif import FingerPrintResponse


class FingerRequest(BaseSchema):
    pass


class FingerPrintResponse(BaseSchema):
    fingerprint_1: List[FingerPrintResponse]
    fingerprint_2: List[FingerPrintResponse]
