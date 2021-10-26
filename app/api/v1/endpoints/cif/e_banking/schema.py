from datetime import date, datetime
from typing import List, Optional

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.schemas.utils import DropdownRequest, DropdownResponse

########################################################################################################################
# Response
########################################################################################################################


########################################################################################################################
# Response
########################################################################################################################
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
    register_balance_casas: List[RegisterBalanceCasa] = Field(..., description='Thông tin tài khoản nhận thông báo')


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
    updated_at: datetime = Field(..., description='Cập nhật vào lúc, format dạng: `YYYY-mm-dd HH:MM:SS`',
                                 example='2021-15-12 06:07:08')


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


################################################################
# Danh sách tài khoản thanh toán
################################################################
class ListBalancePaymentAccountResponse(BaseSchema):
    id: str = Field(..., description='Mã định danh tài khoản thanh toán')
    name: str = Field(..., description='Số tài khoản thanh toán')
    product: str = Field(..., description='Tên sản phẩm tài khoản thanh toán')
    checked_flag: bool = Field(..., description='Trạng thái. `False`: Không. `True`: Có')


# Chi tiết cấp lại mật khẩu E-Banking call center -> I. Thông tin cá nhân khách hàng -> 1. Hình thức nhận mật khẩu mới
class EBankingResetPasswordMethod(DropdownResponse):
    checked_flag: bool = Field(..., description="Cờ xác nhận hình thức nhận mật khẩu")


# Chi tiết cấp lại mật khẩu E-Banking call center -> I. Thông tin cá nhân khách hàng
class PersonalCustomerInformationResponse(BaseSchema):
    id: str = Field(..., description="ID")
    cif_number: str = Field(..., description="Số CIF")
    customer_classification: DropdownResponse = Field(..., description="Loại khách hàng (VD: Cá Nhân)")
    avatar_url: str = Field(..., description="URL Avatar khách hàng")
    full_name: str = Field(..., description="Tên khách hàng không dấu")
    gender: DropdownResponse = Field(..., description="Giới tính")
    email: str = Field(..., description="Email")
    mobile_number: str = Field(..., description="Số điện thoại")
    identity_number: str = Field(..., description="CMND/CCCD")
    place_of_issue: DropdownResponse = Field(..., description="Nơi cấp")
    issued_date: date = Field(..., description="Ngày cấp")
    expired_date: date = Field(..., description="Ngày hết hạn")
    address: str = Field(..., description="Địa chỉ")
    e_banking_reset_password_method: List[EBankingResetPasswordMethod] = Field(
        ..., description="1. Hình thức nhận mật khẩu mới"
    )
    e_banking_account_name: str = Field(..., description="2. Tên đăng nhập")


# Chi tiết cấp lại mật khẩu E-Banking call center -> II. Danh sách câu hỏi -> I. Câu hỏi cơ bản 1
# -> 1. Loại thẻ(tên thẻ, màu thẻ)
class BranchOfCardResponse(DropdownResponse):
    color: DropdownResponse = Field(..., description="Màu thẻ")


# Chi tiết cấp lại mật khẩu E-Banking call center -> II. Danh sách câu hỏi -> I. Câu hỏi cơ bản 1
class BasicQuestion1Response(BaseSchema):
    branch_of_card: BranchOfCardResponse = Field(..., description="1. Loại thẻ(tên thẻ, màu thẻ)")
    sub_card_number: str = Field(..., description="2. Số lượng thẻ phụ")
    mobile_number: str = Field(..., description="3. SĐT đăng ký dịch vụ")
    branch: DropdownResponse = Field(..., description="4. Đơn vị đăng ký dịch vụ/ mở TK")
    method_authentication: DropdownResponse = Field(..., description="5. Hình thức xác thực mật khẩu")
    e_banking_account_name: str = Field(..., description="6. Tên đăng nhập IB/MB")


# Chi tiết cấp lại mật khẩu E-Banking call center -> II. Danh sách câu hỏi -> II. Câu hỏi cơ bản 2 -> 2. Hạn mức thẻ
class CreditLimitResponse(BaseSchema):
    value: str = Field(..., description="Hạn mức đã sử dụng của Thẻ tín dụng")
    currency: DropdownResponse = Field(..., description="Loại tiền")


# Chi tiết cấp lại mật khẩu E-Banking call center -> II. Danh sách câu hỏi -> II. Câu hỏi cơ bản 2
# -> 4. Câu hỏi bí mật/Người liên hệ
class SecretQuestionOrPersonalRelationshipResponse(BaseSchema):
    customer_relationship: DropdownResponse = Field(..., description="URL tài liệu đi kèm")
    mobile_number: str = Field(..., description="URL tài liệu đi kèm")


# Chi tiết cấp lại mật khẩu E-Banking call center -> II. Danh sách câu hỏi -> II. Câu hỏi cơ bản 2
class BasicQuestion2Response(BaseSchema):
    last_four_digits: str = Field(..., description="1. 4 số cuối của thẻ")
    credit_limit: CreditLimitResponse = Field(..., description="2. Hạn mức thẻ")
    email: str = Field(..., description="3. Email đăng ký")
    secret_question_or_personal_relationships: List[SecretQuestionOrPersonalRelationshipResponse] = Field(
        ..., description="4. Câu hỏi bí mật/ Người liên hệ")
    automatic_debit_status: str = Field(..., description="5. Tình trạng đăng ký trích nợ tự động")
    transaction_method_receiver: DropdownResponse = Field(..., description="6. Hình thức nhận sao kê")


class Nearest3rdSecureResponse(CreditLimitResponse):
    business_partner: DropdownResponse = Field(..., description="Đối tác kinh doanh")


# Chi tiết cấp lại mật khẩu E-Banking call center -> II. Danh sách câu hỏi -> III. Câu hỏi nâng cao
class AdvancedQuestionResponse(BaseSchema):
    used_limit_of_credit_card: CreditLimitResponse = Field(..., description="1. Hạn mức đã sử dụng của Thẻ tín dụng")
    nearest_3d_secure: Nearest3rdSecureResponse = Field(
        ..., description="2. Thông tin GD Thẻ tín dụng có 3D Secure gần nhất"
    )
    one_of_two_nearest_successful_transaction: str = Field(
        ..., description="""3. Thông tin 1 trong 2 GD phát sinh trong thành công gần nhất
        ( đối với thẻ ghi nợ, thẻ tín dụng, TKTT, dịch vụ IB/MB) """
    )
    nearest_successful_login_time: str = Field(
        ..., description="4. Thời gian đăng nhập dịch vụ IB/MB thành công gần nhất"
    )


# Chi tiết cấp lại mật khẩu E-Banking call center -> II. Danh sách câu hỏi
class QuestionResponse(BaseSchema):
    basic_question_1: BasicQuestion1Response = Field(..., description="I. Câu hỏi cơ bản 1")
    basic_question_2: BasicQuestion2Response = Field(..., description="II. Câu hỏi cơ bản 2")
    advanced_question: AdvancedQuestionResponse = Field(..., description="III. Câu hỏi nâng cao")


# Chi tiết cấp lại mật khẩu E-Banking call center -> IV. Kết luận
class ResultResponse(BaseSchema):
    confirm_current_transaction_flag: bool = Field(..., description="Cờ xác nhận thực hiện giao dịch")
    note: str = Field(..., description="Ghi chú")


# Chi tiết cấp lại mật khẩu E-Banking call center
class ResetPasswordEBankingResponse(BaseSchema):
    personal_customer_information: PersonalCustomerInformationResponse = Field(
        ..., description="I. Thông tin cá nhân khách hàng"
    )
    question: QuestionResponse = Field(..., description="II. Danh sách câu hỏi")
    document_url: str = Field(..., description="III. Phiếu yêu cầu của đơn vị - URL tài liệu đi kèm")
    result: ResultResponse = Field(..., description="IV. Kết luận")


########################################################################################################################
# Request
########################################################################################################################

class ContactTypeRequest(DropdownRequest):
    checked_flag: bool = Field(..., description='Trạng thái. `False`: Không. `True`: Có')


class NotificationCasaRelationshipRequest(BaseSchema):
    mobile_number: str = Field(..., description='Số điện thoại')
    full_name_vn: str = Field(..., description='Tên tiếng việt')
    relationship_type: DropdownRequest = Field(..., description='Mối quan hệ')


class EBankingNotificationRequest(DropdownRequest):
    checked_flag: bool = Field(..., description='Trạng thái. `False`: Không. `True`: Có')


class RegisterBalanceCasaRequest(BaseSchema):
    mobile_number: str = Field(..., description='Số điện thoại')
    full_name_vn: str = Field(..., description='Tên tiếng việt ')
    primary_mobile_number: DropdownRequest = Field(..., description='Loại SĐT')
    notification_casa_relationships: List[NotificationCasaRelationshipRequest] = Field(..., description='Mối quan hê')
    e_banking_notifications: List[EBankingNotificationRequest] = Field(..., description='Tùy chọn thông báo')


class BalancePaymentAccountRequest(BaseSchema):
    register_flag: bool = Field(..., description='Trạng thái. `False`: Không. `True`: Có')
    customer_contact_types: List[ContactTypeRequest] = Field(..., description='Hình thức nhận thông báo')
    register_balance_casas: List[RegisterBalanceCasaRequest] = Field(...,
                                                                     description='Thông tin tài khoản nhận thông báo')


class AccountRequest(BaseSchema):
    number: str = Field(..., description='Số tài khoản')
    name: str = Field(..., description='Tên khách hàng')
    checked_flag: bool = Field(..., description='Trạng thái. `False`: Không. `True`: Có')


class TdAccountRequest(BaseSchema):
    td_accounts: List[AccountRequest] = Field(..., description='Danh sách số tài khoản tiết kiệm')


class BalanceSavingAccountRequest(BaseSchema):
    register_flag: bool = Field(..., description='Trạng thái. `False`: Không. `True`: Có')
    customer_contact_types: List[ContactTypeRequest] = Field(..., description='Hình thức nhận thông báo')
    mobile_number: str = Field(..., description='Số điện thoại')
    range: TdAccountRequest = Field(..., description='Phạm vi áp dụng')
    e_banking_notifications: List[EBankingNotificationRequest] = Field(..., description='Tùy chọn thông báo')


class ResetPasswordMethodRequest(DropdownRequest):
    checked_flag: bool = Field(..., description='Trạng thái. `False`: Không. `True`: Có')


class MethodAuthenticationRequest(DropdownRequest):
    checked_flag: bool = Field(..., description='Trạng thái. `False`: Không. `True`: Có')


class NumberRequest(BaseSchema):
    id: Optional[str] = Field(..., description='Mã tài khoản')
    name: Optional[str] = Field(..., description='Tài khoản')


class PaymentFeeRequest(DropdownRequest):
    checked_flag: bool = Field(..., description='Trạng thái. `False`: Không. `True`: Có')
    number: NumberRequest = Field(..., description='Tài khoản thanh toán')


class AccountInformationRequest(BaseSchema):
    register_flag: bool = Field(..., description='Trạng thái. `False`: Không. `True`: Có')
    account_name: str = Field(..., description='Tên đăng nhập')
    checked_flag: bool = Field(..., description='Trạng thái. `False`: Không. `True`: Có')
    e_banking_reset_password_methods: List[ResetPasswordMethodRequest] = Field(...,
                                                                               description='Hình thức nhận '
                                                                                           'mật khẩu kích hoạt')
    method_authentication: List[MethodAuthenticationRequest] = Field(..., description='Hình thức xác thực')
    payment_fee: List[PaymentFeeRequest] = Field(..., description='Thanh toán phí')


class OptionalEBankingAccountRequest(BaseSchema):
    reset_password_flag: bool = Field(..., description='Trạng thái. `False`: Không. `True`: Có')
    active_account_flag: bool = Field(..., description='Trạng thái. `False`: Không. `True`: Có')
    note: str = Field(..., description='Mô tả')


class AccountInformationEBankingRequest(BaseSchema):
    account_information: AccountInformationRequest = Field(..., description='Tài khoản E-Banking')
    optional_e_banking_account: OptionalEBankingAccountRequest = Field(..., description='Hình thức nhận thông báo')


class EBankingRequest(BaseSchema):
    change_of_balance_payment_account: BalancePaymentAccountRequest = Field(..., description='Tài khoản thanh toán')
    change_of_balance_saving_account: BalanceSavingAccountRequest = Field(..., description='Tài khoản tiết kiệm')
    e_banking_information: AccountInformationEBankingRequest = Field(..., description='Thông tin E-Banking')
