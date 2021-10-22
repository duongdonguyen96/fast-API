from typing import Optional

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.schemas.utils import (
    DropdownRequest, DropdownResponse, OpionalDropdownRequest,
    OptionalDropdownResponse
)


########################################################################################################################
# Response
########################################################################################################################
# Chi tiết tài khoản thanh toán -> Tài khoản của tổ chức chi lương
class CasaAccountResponse(BaseSchema):
    id: Optional[str] = Field(..., description="ID tài khoản của tổ chức chi lương")
    account_number: Optional[str] = Field(..., description="Số tài khoản của tổ chức chi lương")


# Chi tiết tài khoản thanh toán
class PaymentAccountResponse(BaseSchema):
    self_selected_account_flag: bool = Field(..., description="""Cờ tự chọn số tài khoản
                                                              \nSố tài khoản thường => `False`
                                                              \nSố tài khoản yêu cầu => `True`""")
    currency: DropdownResponse = Field(..., description="Loại tiền")
    account_type: DropdownResponse = Field(..., description="Gói tài khoản")
    account_class: DropdownResponse = Field(..., description="Loại hình tài khoản")
    account_structure_type_level_1: OptionalDropdownResponse = Field(..., description="Kiểu kiến trúc cấp 1")
    account_structure_type_level_2: OptionalDropdownResponse = Field(..., description="Kiểu kiến trúc cấp 2")
    account_structure_type_level_3: OptionalDropdownResponse = Field(..., description="Kiểu kiến trúc cấp 3")
    casa_account: CasaAccountResponse = Field(..., description="Số tài khoản")
    account_salary_organization_account: str = Field(..., description="Tài khoản của tổ chức chi lương")
    account_salary_organization_name: Optional[str] = Field(..., description="Chủ tài khoản chi lương")


########################################################################################################################
# Request Body
########################################################################################################################
# Chi tiết tài khoản thanh toán
class CasaAccountRequest(BaseSchema):
    account_number: Optional[str] = Field(None, description="Số tài khoản của tổ chức chi lương")


class SavePaymentAccountRequest(BaseSchema):
    self_selected_account_flag: bool = Field(..., description="""Cờ tự chọn số tài khoản
                                                              \nSố tài khoản thường => `False`
                                                              \nSố tài khoản yêu cầu => `True`""")
    currency: DropdownRequest = Field(..., description="Loại tiền")
    account_type: DropdownRequest = Field(..., description="Gói tài khoản")
    account_class: DropdownRequest = Field(..., description="Loại hình tài khoản")
    account_structure_type_level_1: OpionalDropdownRequest = Field(None, description="Kiểu kiến trúc cấp 1")
    account_structure_type_level_2: OpionalDropdownRequest = Field(None, description="Kiểu kiến trúc cấp 2")
    account_structure_type_level_3: OpionalDropdownRequest = Field(None, description="Kiểu kiến trúc cấp 3")
    casa_account: CasaAccountRequest = Field(None, description="Số tài khoản")
    account_salary_organization_account: str = Field(None, description="Tài khoản của tổ chức chi lương")
