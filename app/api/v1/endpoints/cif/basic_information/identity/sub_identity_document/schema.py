from datetime import date
from typing import List

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.schemas.utils import DropdownRequest, DropdownResponse


########################################################################################################################
# Response
########################################################################################################################
# Response Chi tiết GTĐD phụ -> Phân tích OCR
class SubIdentityOCRResultResponse(BaseSchema):
    sub_identity_number: str = Field(..., description="Số GTĐD")
    symbol: str = Field(None, description="Ký hiệu")
    full_name_vn: str = Field(..., description="Họ và tên")
    date_of_birth: date = Field(..., description="Ngày sinh")
    passport_number: str = Field(..., description="Số hộ chiếu")
    place_of_issue: DropdownResponse = Field(..., description="Nơi cấp")
    expired_date: date = Field(..., description="Có giá trị đến")
    issued_date: date = Field(..., description="Ngày cấp")


# Response Chi tiết GTĐD phụ
class SubIdentityDetailResponse(BaseSchema):
    id: str = Field(..., description="ID GTĐD phụ")
    name: str = Field(..., description="Tên GTĐD phụ")
    sub_identity_document_type: DropdownResponse = Field(..., description="Loại GTĐD phụ")
    sub_identity_document_image_url: str = Field(..., description="I. Thông tin giấy tờ")
    ocr_result: SubIdentityOCRResultResponse = Field(..., description="II. Phân tích OCR")


# Hình ảnh trong lịch sử
class IdentityImage(BaseSchema):
    image_url: str = Field(..., description="URL hình ảnh định danh")


# Lịch sử thay đổi giấy tờ định danh phụ
class LogResponse(BaseSchema):
    reference_flag: bool = Field(..., description="Cờ giấy tờ định danh phụ dùng để so sánh với hình gốc")
    created_date: date = Field(..., description="Ngày ghi log")
    identity_document_type: DropdownResponse = Field(..., description="Loại giấy tờ định danh phụ")
    identity_images: List[IdentityImage] = Field(..., description="Danh sách hình ảnh")


########################################################################################################################
# Request
########################################################################################################################
# Request Body Lưu GTĐD phụ -> Phân tích OCR
class SubIdentityOCRResultRequest(SubIdentityOCRResultResponse):
    place_of_issue: DropdownRequest = Field(..., description="Nơi cấp")


# Request Body Lưu GTĐD phụ
class SubIdentityDocumentRequest(BaseSchema):
    name: str = Field(..., description="Tên GTĐD phụ")
    sub_identity_document_type: DropdownRequest = Field(..., description="Loại GTĐD phụ")
    ocr_result: SubIdentityOCRResultRequest = Field(..., description="II. Phân tích OCR")
