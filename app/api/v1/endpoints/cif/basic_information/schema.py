from datetime import date
from typing import Optional

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.schemas.cif import RelationshipResponse
########################################################################################################################
# Response
########################################################################################################################
# Thông tin chi tiết người giám hộ hoặc người có quan hệ với khách hàng qua mã CIF
# Response Model kế thừa từ RelationshipResponse (Model dùng chung)
from app.api.v1.schemas.utils import DropdownResponse


class BasicInformationResponse(BaseSchema):
    cif_number: str = Field(..., description="Số CIF")
    full_name_vn: str = Field(..., description="Họ và tên")
    date_of_birth: date = Field(..., description="Ngày sinh")
    gender: DropdownResponse = Field(..., description="Giới tính")
    nationality: DropdownResponse = Field(..., description="Quốc tịch")
    telephone_number: Optional[str] = Field(..., description="Số ĐT bàn")
    mobile_number: Optional[str] = Field(..., description="Số ĐTDĐ")
    email: Optional[str] = Field(..., description="Email")


class DetailRelationshipResponse(RelationshipResponse):
    basic_information: BasicInformationResponse = Field(..., description="I. Thông tin cơ bản")

########################################################################################################################
# Request Body
########################################################################################################################
