from datetime import datetime
from typing import List

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.schemas.utils import DropdownResponse


class CifInformationResponse(BaseSchema):
    self_selected_cif_flag: bool = Field(..., description='Cờ CIF thông thường/ tự chọn. '
                                                          '`False`: thông thường. '
                                                          '`True`: tự chọn')
    cif_number: str = Field(..., description='Số CIF yêu cầu')
    customer_classification: DropdownResponse = Field(..., description='Đối tượng khách hàng')
    customer_economic_profession: DropdownResponse = Field(..., description='Mã ngành KT')
    kyc_level: DropdownResponse = Field(..., description='Cấp độ KYC')


# ################################### lịch sử hồ sơ (log)####################################3
class ProfileHistoryOfDayResponse(BaseSchema):
    user_id: str = Field(..., description="Id người dùng")
    full_name: str = Field(..., description="Tên đầy đủ của người dùng ")
    user_avatar_url: str = Field(..., description="Url ảnh đại diện của người dùng")
    id: str = Field(..., description="Id log")
    created_at: datetime = Field(..., description="Thời gian tạo")
    content: str = Field(..., description="Nội dung log ")


class CifProfileHistoryResponse(BaseSchema):
    created_date: str = Field(..., description="Ngày tạo")
    logs: List[ProfileHistoryOfDayResponse] = Field(..., description="Danh sách log trong 1 ngày ")
