from datetime import datetime
from typing import List

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.schemas.cif import FingerPrintResponse


class TwoFingerPrintResponse(BaseSchema):
    fingerprint_1: List[FingerPrintResponse] = Field(..., description='Mẫu vân tay 1')
    fingerprint_2: List[FingerPrintResponse] = Field(..., description='Mẫu vân tay 2')


class FingerPrintSaveSuccessResponse(BaseSchema):
    cif_id: str = Field(..., description='Id CIF ảo')
    created_at: datetime = Field(..., description='Ngày và giờ')
    created_by: str = Field(..., description='Người tạo')
