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
    date_of_birth: str = Field(..., description="Ngày sinh")
    province: DropdownResponse = Field(..., description="Quốc gia")
    place_of_issue: DropdownResponse = Field(..., description="Nơi cấp")
    expired_date: str = Field(..., description="Có giá trị đến")
    issued_date: str = Field(..., description="Ngày cấp")


# Response Chi tiết GTĐD phụ
class SubIdentityDetailResponse(BaseSchema):
    id: str = Field(..., description="ID GTĐD phụ")
    name: str = Field(..., description="Tên GTĐD phụ")
    sub_identity_document_type: DropdownResponse = Field(..., description="Loại GTĐD phụ")
    sub_identity_document_image_url: str = Field(..., description="I. Thông tin giấy tờ")
    ocr_result: SubIdentityOCRResultResponse = Field(..., description="II. Phân tích OCR")


########################################################################################################################
# Request
########################################################################################################################
# Request Body Lưu GTĐD phụ -> Phân tích OCR
class SubIdentityOCRResultRequest(SubIdentityOCRResultResponse):
    province: DropdownRequest = Field(..., description="Quốc gia")
    place_of_issue: DropdownRequest = Field(..., description="Nơi cấp")


# Request Body Lưu GTĐD phụ
class SubIdentityDocumentRequest(SubIdentityDetailResponse):
    sub_identity_document_type: DropdownRequest = Field(..., description="Loại GTĐD phụ")
    ocr_result: SubIdentityOCRResultRequest = Field(..., description="II. Phân tích OCR")
