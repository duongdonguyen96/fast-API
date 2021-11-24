from datetime import date
from typing import List

from pydantic import Field

from app.api.base.schema import BaseSchema


class SignatureRequest(BaseSchema):
    identity_image_transaction_1: str = Field(..., description='Đường dẫn hình ảnh định danh chữ ký khách hàng')
    identity_image_transaction_2: str = Field(..., description='Đường dẫn hình ảnh định danh chữ ký khách hàng')


class SignaturesRequest(BaseSchema):
    customer_signatures: List[SignatureRequest] = Field(..., description='Hình ảnh chữ ký')


class SignaturesResponse(BaseSchema):
    identity_image_id: str = Field(..., description='Mã hình ảnh chữ ký của khách hàng')
    image_url: str = Field(..., description='Hình ảnh chữ ký của khách hàng')
    active_flag: bool = Field(..., description='Trạng thái hoạt động')


class CompareSignaturesResponse(BaseSchema):
    compare_image_url: str = Field(..., description='Hình ảnh đối chiếu')
    similar_percent: int = Field(..., description='Số phần trăm đối chiếu')


class SignaturesSuccessResponse(BaseSchema):
    created_date: date = Field(..., description='Ngày tạo')
    signature: List[SignaturesResponse] = Field(..., description='Danh sách ảnh khuôn mặt')
