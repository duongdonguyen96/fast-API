from typing import List

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.schemas.cif import AddressRequest, AddressResponse
from app.api.v1.schemas.utils import DropdownRequest, DropdownResponse


class CardTypeResponse(BaseSchema):
    id: str = Field(..., description="id")
    code: str = Field(..., description="code")
    name: str = Field(..., description="Tên loại thẻ")
    source_code: str = Field(..., description="Mã source")
    promo_code: str = Field(..., description="Mã promo")
    active_flag: bool = Field(..., description="cờ hoạt động")


class NameOnCardResponse(BaseSchema):
    last_name_on_card: str = Field(..., description="Họ")
    middle_name_on_card: str = Field(..., description="tên lót")
    first_name_on_card: str = Field(..., description="tên")


class MainAndSubCardNumberResponse(BaseSchema):
    number_part_1: str = Field(..., description="4 số đầu trên thẻ")
    number_part_2: str = Field(..., description="4 số thứ 2 trên thẻ")
    number_part_3: str = Field(..., description="4 số thứ 3 trên thẻ")
    number_part_4: str = Field(..., description="4 số cuối trên thẻ")


class IssueDebitCardResponse(BaseSchema):
    register_flag: bool = Field(..., description="Đăng kí thẻ ghi nợ, `True`: đăng kí, `False`: không đăng kí ")
    physical_card_type: bool = Field(..., description="TÍnh vật lý, `True`: thẻ vật lý, `False`: thẻ phi vật lý")
    physical_issuance_type: DropdownResponse = Field(..., description="Hình thức phát hành")
    customer_type: DropdownResponse = Field(..., description="Nhóm khách hàng")
    payment_online_flag: bool = Field(..., description="Mở chức năng thanh toán online, `True`: có, `False`: không")
    branch_of_card: DropdownResponse = Field(..., description="Thương hiệu thẻ")
    issuance_fee: DropdownResponse = Field(..., description="Phí phat hành thẻ")
    annual_fee: DropdownResponse = Field(..., description="Phí thường niên")
    debit_card_types: List[CardTypeResponse] = Field(..., description="Danh sách loại thẻ phát hành")


class InformationDebitCardResponse(BaseSchema):
    name_on_card: NameOnCardResponse = Field(..., description="Tên trên thẻ")
    main_card_number: MainAndSubCardNumberResponse = Field(..., description="Số thẻ chính")
    card_image_url: str = Field(..., description="Url hình ảnh thẻ")


class CardDeliveryAddressResponse(BaseSchema):
    scb_delivery_address_flag: bool = Field(..., description="Địa chỉ nhận tại SCB. "
                                                             "`True`: tại SCB, "
                                                             "`Fasle`:địa chỉ khác")
    scb_branch: DropdownResponse = Field(..., description=" chi nhánh scb nhận thẻ")
    delivery_address: AddressResponse = Field(..., descripion="Địa chỉ nhân thẻ")
    note: str = Field(..., description="ghi chú")


class SubDebitCardResponse(BaseSchema):
    id: str = Field(..., description="Id thẻ phụ")
    name: str = Field(..., description="Tên thẻ phụ")
    cif_number: str = Field(..., description="Số cif")
    name_on_card: NameOnCardResponse = Field(..., description="Tên trên thẻ")
    physical_card_type: bool = Field(..., description="TÍnh vật lý, `True`: thẻ vật lý, `False`: thẻ phi vật lý")
    card_issuance_type: DropdownResponse = Field(..., description="Hình thức phát hành")
    payment_online_flag: bool = Field(..., description="Mở chức năng thanh toán online, `True`: có, `False`: không")
    card_delivery_address: CardDeliveryAddressResponse = Field(..., description="Địa chỉ giao nhận thẻ")
    sub_card_number: MainAndSubCardNumberResponse = Field(..., description="Số thẻ phụ")
    card_image_url: str = Field(..., description="Url hình ảnh thẻ ")


class InformationSubDebitCardResponse(BaseSchema):
    sub_debit_cards: List[SubDebitCardResponse] = Field(..., description="Danh sách thẻ phụ ")
    total_sub_debit_card: int = Field(..., description="Tổng số thẻ phụ ")


class DebitCardResponse(BaseSchema):
    issue_debit_card: IssueDebitCardResponse = Field(..., description="Phát hành thẻ ghi nợ ")
    information_debit_card: InformationDebitCardResponse = Field(..., description="Thông tin thẻ ")
    card_delivery_address: CardDeliveryAddressResponse = Field(..., description="Địa chỉ nhân thẻ ")
    information_sub_debit_card: InformationSubDebitCardResponse = Field(..., description="Thông tin thẻ phụ")


# ######################### request schema ###################################
class NameOnCardRequest(BaseSchema):
    middle_name_on_card: str = Field(..., description="tên lót")


class IssueDebitRequest(BaseSchema):
    register_flag: bool = Field(..., description="Đăng kí thẻ ghi nợ, `True`: đăng kí, `False`: không đăng kí ")
    physical_card_type: bool = Field(..., description="TÍnh vật lý, `True`: thẻ vật lý, `False`: thẻ phi vật lý")
    physical_issuance_type: DropdownRequest = Field(..., description="Hình thức phát hành")
    customer_type: DropdownRequest = Field(..., description="Nhóm khách hàng")
    payment_online_flag: bool = Field(..., description="Mở chức năng thanh toán online, `True`: có, `False`: không")
    branch_of_card: DropdownRequest = Field(..., description="Thương hiệu thẻ")
    issuance_fee: DropdownRequest = Field(..., description="Phí phat hành thẻ")
    annual_fee: DropdownRequest = Field(..., description="Phí thường niên")
    debit_card_type_id: str = Field(..., description="id loại thẻ phát hành")


class CardDeliveryAddressRequest(BaseSchema):
    scb_delivery_address_flag: bool = Field(..., description="Địa chỉ nhận tại SCB. "
                                                             "`True`: tại SCB, "
                                                             "`Fasle`:địa chỉ khác")
    scb_branch: DropdownRequest = Field(..., description=" chi nhánh scb nhận thẻ")
    delivery_address: AddressRequest = Field(..., descripion="Địa chỉ nhân thẻ")
    note: str = Field(..., description="ghi chú")


class SubDebitCardRequest(BaseSchema):
    cif_number: str = Field(..., description="Số cif")
    name_on_card: NameOnCardRequest = Field(..., description="Tên trên thẻ")
    physical_card_type: bool = Field(..., description="TÍnh vật lý, `True`: thẻ vật lý, `False`: thẻ phi vật lý")
    card_issuance_type: DropdownRequest = Field(..., description="Hình thức phát hành")
    payment_online_flag: bool = Field(..., description="Mở chức năng thanh toán online, `True`: có, `False`: không")
    card_delivery_address: CardDeliveryAddressRequest = Field(..., description="Địa chỉ giao nhận thẻ")


class InformationSubDebitCardRequest(BaseSchema):
    sub_debit_cards: List[SubDebitCardRequest] = Field(..., description="Danh sách thẻ phụ ")


class InformationDebitCardRequest(BaseSchema):
    name_on_card: NameOnCardRequest = Field(..., description="Tên trên thẻ")


class DebitCardRequest(BaseSchema):
    issue_debit_card: IssueDebitRequest = Field(..., description="Phát hành thẻ ghi nợ ")
    information_debit_card: InformationDebitCardRequest = Field(..., description="Thông tin thẻ ")
    card_delivery_address: CardDeliveryAddressRequest = Field(..., description="Địa chỉ nhân thẻ ")
    information_sub_debit_card: InformationSubDebitCardRequest = Field(..., description="Thông tin thẻ phụ")


class ListCardTypeResponse(BaseSchema):
    id: str = Field(..., description="id")
    code: str = Field(..., description="code")
    name: str = Field(..., description="Tên loại thẻ")
    source_code: str = Field(..., description="Mã source")
    promo_code: str = Field(..., description="Mã promo")
