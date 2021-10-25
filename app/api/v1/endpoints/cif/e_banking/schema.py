from datetime import datetime
from typing import List, Optional

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.schemas.utils import DropdownResponse


class ContactTypeResponse(DropdownResponse):
    checked_flag: bool = Field(..., description='Trạng thái. `False`: Không. `True`: Có')


class NotificationCasaRelationshipResponse(BaseSchema):
    id: str = Field(..., description='Mã định danh')
    mobile_number: str = Field(..., description='Số điện thoại')
    full_name_vn: str = Field(..., description='Tên tiếng việt')
    relationship_type: DropdownResponse = Field(..., description='Mối quan hệ')


class EBankingNotificationResponse(DropdownResponse):
    checked_flag: bool = Field(..., description='Trạng thái. `False`: Không. `True`: Có')


class RegisterBalanceCasa(BaseSchema):
    id: str = Field(..., description='Mã định danh tài khoản')
    mobile_number: str = Field(..., description='Số điện thoại')
    full_name_vn: str = Field(..., description='Tên tiếng việt ')
    primary_mobile_number: DropdownResponse = Field(..., description='Loại SĐT')
    notification_casa_relationships: List[NotificationCasaRelationshipResponse] = Field(..., description='Mối quan hê')
    e_banking_notifications: List[EBankingNotificationResponse] = Field(..., description='Hình thức nhận thông báo')


class BalancePaymentAccountResponse(BaseSchema):
    register_flag: bool = Field(..., description='Trạng thái. `False`: Không. `True`: Có')
    customer_contact_types: List[ContactTypeResponse] = Field(..., description='Hình thức nhận thông báo')
    register_balance_casas: List[RegisterBalanceCasa] = Field(..., description='Thông tin tài khoảnh nhận thông báo')


class TdAccount(BaseSchema):
    id: str = Field(..., description='Mã định danh')
    number: str = Field(..., description='Số tài khoản')
    name: str = Field(..., description='Tên khách hàng')
    checked_flag: bool = Field(..., description='Trạng thái. `False`: Không. `True`: Có')


class TdAccountResponse(BaseSchema):
    td_accounts: List[TdAccount] = Field(..., description='Danh sách số tài khoản tiết kiệm')
    page: int = Field(..., description='Trang')
    limit: int = Field(..., description='Giới hạn')
    total_page: int = Field(..., description='Tổng số trang')


class BalanceSavingAccountResponse(BaseSchema):
    register_flag: bool = Field(..., description='Trạng thái. `False`: Không. `True`: Có')
    customer_contact_types: List[ContactTypeResponse] = Field(..., description='Hình thức nhận thông báo')
    mobile_number: str = Field(..., description='Số điện thoại')
    range: TdAccountResponse = Field(..., description='Phạm vi áp dụng')
    e_banking_notifications: List[EBankingNotificationResponse] = Field(..., description='Hình thức nhận thông báo')


class ResetPasswordMethodResponse(DropdownResponse):
    checked_flag: bool = Field(..., description='Trạng thái. `False`: Không. `True`: Có')


class MethodAuthenticationResponse(DropdownResponse):
    checked_flag: bool = Field(..., description='Trạng thái. `False`: Không. `True`: Có')


class NumberResponse(BaseSchema):
    id: Optional[str] = Field(..., description='Mã tài khoản')
    name: Optional[str] = Field(..., description='Tài khoản')


class PaymentFeeResponse(BaseSchema):
    id: str = Field(..., description='Mã thanh toán')
    name: str = Field(..., description='Tên thanh toán')
    checked_flag: bool = Field(..., description='Trạng thái. `False`: Không. `True`: Có')
    number: NumberResponse = Field(..., description='Tài khoản thanh toán')


class OptionalEBankingAccountResponse(BaseSchema):
    reset_password_flag: bool = Field(..., description='Trạng thái. `False`: Không. `True`: Có')
    active_account_flag: bool = Field(..., description='Trạng thái. `False`: Không. `True`: Có')
    note: str = Field(..., description='Mô tả')
    updated_by: str = Field(..., description='Người cập nhật')
    updated_at: datetime = Field(..., description='Ngày giờ cập nhật')


class AccountInformation(BaseSchema):
    register_flag: bool = Field(..., description='Trạng thái. `False`: Không. `True`: Có')
    account_name: str = Field(..., description='Tên đăng nhập')
    checked_flag: bool = Field(..., description='Trạng thái. `False`: Không. `True`: Có')
    e_banking_reset_password_methods: List[ResetPasswordMethodResponse] = Field(...,
                                                                                description='Hình thức nhận '
                                                                                            'mật khẩu kích hoạt')
    method_authentication: List[MethodAuthenticationResponse] = Field(..., description='Hình thức xác thực')
    payment_fee: List[PaymentFeeResponse] = Field(..., description='Thanh toán phí')


class AccountInformationResponse(BaseSchema):
    account_information: AccountInformation = Field(..., description='Tài khoản E-Banking')

    optional_e_banking_account: OptionalEBankingAccountResponse = Field(..., description='Hình thức nhận thông báo')


class EBankingResponse(BaseSchema):
    change_of_balance_payment_account: BalancePaymentAccountResponse = Field(..., description='Tài khoản thanh toán')
    change_of_balance_saving_account: BalanceSavingAccountResponse = Field(..., description='Tài khoản tiết kiệm')
    e_banking_information: AccountInformationResponse = Field(..., description='Thông tin E-Banking')
