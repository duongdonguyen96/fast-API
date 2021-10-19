from pydantic import Field

from app.api.base.schema import BaseSchema


class Face(BaseSchema):
    identity_image_id: str = Field(..., description='Mã hình ảnh định danh của khách hàng')
    image_url: str = Field(..., description='Hình ảnh định danh của khách hàng')
    created_at: str = Field(..., description='Ngày tạo')
    similar_percent: int = Field(..., description='Số phần trăm đối chiếu')


class FacesResponse(BaseSchema):
    date: str = Field(..., description='Ngày tạo ảnh khuôn mặt')
    faces: list[Face] = Field(..., description='Danh sách ảnh khuôn mặt')
