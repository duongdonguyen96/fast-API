from datetime import datetime
from typing import List

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.schemas.utils import DropdownRequest, DropdownResponse

########################################################################################################################
# Request
########################################################################################################################


class CategoryDropdownRequest(DropdownRequest):
    active_flag: bool = Field(False, description='`False`: Có. `True`: Không')


class DocumentsRequest(BaseSchema):
    id: str = Field(..., description='Mã biểu mẫu')
    name: str = Field(..., description='Tên biểu mẫu')
    url: str = Field(..., description='Đường dẫn biểu mẫu')
    version: str = Field(..., description='Phiên bản biểu mẫu')
    content_type: str = Field(..., description='Loại biểu mẫu')
    size: str = Field(..., description='Kích thước biểu mẫu')
    folder: str = Field(..., description='Thư mục biểu mẫu')
    note: str = Field(..., description='Mô tả biểu mẫu')


class DocumentsListRequest(BaseSchema):
    language_type: DropdownRequest = Field(..., description='Ngôn ngữ biểu mẫu')
    documents: List[DocumentsRequest] = Field(..., description='Thông tin biểu mẫu `FATCA`')


class FatcaRequest(BaseSchema):
    fatca_information: List[CategoryDropdownRequest] = Field(..., description='Danh mục `FATCA`')
    documents_list: List[DocumentsListRequest] = Field(..., description='Danh sách biểu mẫu `FATCA`')


########################################################################################################################
# Response
########################################################################################################################

class CategoryDropdownResponse(DropdownResponse):
    active_flag: bool = Field(False, description='`False`: Có. `True`: Không')


class DocumentsResponse(BaseSchema):
    id: str = Field(..., description='Mã biểu mẫu')
    name: str = Field(..., description='Tên biểu mẫu')
    url: str = Field(..., description='Đường dẫn biểu mẫu')
    active_flag: bool = Field(..., description='Trạng thái biểu mẫu')
    version: str = Field(..., description='Phiên bản biểu mẫu')
    content_type: str = Field(..., description='Loại biểu mẫu')
    size: str = Field(..., description='Kích thước biểu mẫu')
    folder: str = Field(..., description='Thư mục biểu mẫu')
    created_by: str = Field(..., description='Người tạo biểu mẫu')
    created_at: datetime = Field(..., description='Thời gian tạo biểu mẫu')
    updated_by: str = Field(..., description='Người cập nhật biểu mẫu')
    updated_at: datetime = Field(..., description='Thời gian cập nhật biểu mẫu')
    note: str = Field(..., description='Mô tả biểu mẫu')


class DocumentsListResponse(BaseSchema):
    language_type: DropdownResponse = Field(..., description='Ngôn ngữ biểu mẫu')
    documents: List[DocumentsResponse] = Field(..., description='Thông tin biểu mẫu `FATCA`')


class FatcaResponse(BaseSchema):
    fatca_information: List[CategoryDropdownResponse] = Field(..., description='Danh mục `FATCA`')
    documents_list: List[DocumentsListResponse] = Field(..., description='Danh sách biểu mẫu `FATCA`')
