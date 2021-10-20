from datetime import date, datetime
from typing import List

from pydantic import Field

from app.api.base.schema import BaseSchema


class Face(BaseSchema):
    identity_image_id: str = Field(..., description='Mã hình ảnh định danh của khách hàng')
    image_url: str = Field(..., description='Hình ảnh định danh của khách hàng')
    created_at: datetime = Field(..., description='Ngày tạo')
    similar_percent: int = Field(..., description='Số phần trăm đối chiếu')


class FacesResponse(BaseSchema):
    created_date: date = Field(..., description='Ngày tạo ảnh khuôn mặt')
    faces: List[Face] = Field(..., description='Danh sách ảnh khuôn mặt')
