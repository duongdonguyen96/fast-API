from typing import Optional

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.schemas.utils import DropdownRequest


class EmployeeDropdownResponse(BaseSchema):
    id: str = Field(..., description='`Mã nhân viên`')
    fullname_vn: str = Field(..., description='`Tên nhân viên`')


class OtherInformationResponse(BaseSchema):
    legal_agreement_flag: bool = Field(..., description="cờ thỏa thuận pháp lý `True`: có , `False`: không ")
    advertising_marketing_flag: bool = Field(
        ...,
        description="Cờ đồng ý nhận SMS, Email tiếp thị quảng cáo từ SCB. "
                    "`True`: có, "
                    "`False`: không."
    )
    sale_staff: Optional[EmployeeDropdownResponse] = Field(..., description="Mã nhân viên kinh doanh")
    indirect_sale_staff: Optional[EmployeeDropdownResponse] = Field(..., description="Mã nhân viên kinh doanh gián tiếp")


class OtherInformationUpdateRequest(BaseSchema):
    legal_agreement_flag: bool = Field(..., description="cờ thỏa thuận pháp lý `True`: có , `False`: không ")
    advertising_marketing_flag: bool = Field(
        ...,
        description="Cờ đồng ý nhận SMS, Email tiếp thị quảng cáo từ SCB. "
                    "`True`: có, "
                    "`False`: không."
    )
    sale_staff: DropdownRequest = Field(..., description="Mã nhân viên kinh doanh")
    indirect_sale_staff: DropdownRequest = Field(..., description="Mã nhân viên kinh doanh gián tiếp")
