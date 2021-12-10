from sqlalchemy import select
from sqlalchemy.orm import Session, aliased

from app.api.base.repository import ReposReturn
from app.api.v1.endpoints.cif.debit_card.schema import DebitCardRequest
from app.third_parties.oracle.models.cif.basic_information.model import (
    Customer
)
from app.third_parties.oracle.models.cif.debit_card.model import (
    CardDeliveryAddress, DebitCard
)
from app.third_parties.oracle.models.master_data.address import (
    AddressDistrict, AddressProvince, AddressWard
)
from app.third_parties.oracle.models.master_data.card import (
    BrandOfCard, CardIssuanceFee, CardIssuanceType, CardType
)
from app.third_parties.oracle.models.master_data.customer import CustomerType
from app.third_parties.oracle.models.master_data.others import Branch
from app.utils.constant.cif import CIF_ID_TEST
from app.utils.error_messages import ERROR_CIF_ID_NOT_EXIST
from app.utils.functions import dropdown, now


<<<<<<< HEAD
async def repos_debit_card(cif_id: str) -> ReposReturn:
    if cif_id == CIF_ID_TEST:
        return ReposReturn(data={
            "issue_debit_carxd": {
                "register_flag": True,
                "physical_card_type": True,
                "physical_issuance_type": {
                    "id": "1",
                    "code": "NORMAL",
                    "name": "Thông thường"
                },
                "customer_type": {
=======
async def repos_debit_card(cif_id: str, session: Session) -> ReposReturn:

    branch_province = aliased(AddressProvince, name='branch_province')
    branch_district = aliased(AddressDistrict, name='branch_district')
    branch_ward = aliased(AddressWard, name='branch_ward')

    list_debit_card_info_engine = select(
        DebitCard,
        CardType,
        CardIssuanceType,
        CustomerType,
        BrandOfCard,
        CardIssuanceFee,
        Branch,
        branch_province,
        branch_district,
        branch_ward,
        CardDeliveryAddress,
        AddressWard,
        AddressDistrict,
        AddressProvince,
    ).join(
        CustomerType, DebitCard.customer_type_id == CustomerType.id
    ).join(
        CardType, DebitCard.card_type_id == CardType.id
    ).join(
        CardIssuanceType, DebitCard.card_type_id == CardIssuanceType.id
    ).join(
        BrandOfCard, DebitCard.card_type_id == BrandOfCard.id
    ).join(
        CardIssuanceFee, DebitCard.card_issuance_fee_id == CardIssuanceFee.id
    ).join(
        CardDeliveryAddress, DebitCard.card_delivery_address_id == CardDeliveryAddress.id
    ).outerjoin(
        Branch, CardDeliveryAddress.branch_id == Branch.id
    ).outerjoin(
        branch_province, Branch.province_id == branch_province.id
    ).outerjoin(
        branch_district, Branch.district_id == branch_district.id
    ).outerjoin(
        branch_ward, Branch.ward_id == branch_ward.id
    ).outerjoin(
        AddressWard, CardDeliveryAddress.ward_id == AddressWard.id,
    ).outerjoin(
        AddressDistrict, CardDeliveryAddress.district_id == AddressDistrict.id
    ).outerjoin(
        AddressProvince, CardDeliveryAddress.province_id == AddressProvince.id
    ).filter(
        DebitCard.customer_id == cif_id,
        DebitCard.active_flag == 1,
    )

    list_debit_card_info = session.execute(list_debit_card_info_engine).all()
    if not list_debit_card_info:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc="cif_id")

    for debit_card_info, card_type, card_issuance_type, customer_type, branch_of_card, issuance_fee, branch, \
            branch_province, branch_district, branch_ward, card_delivery_address, \
            ward, district, province in list_debit_card_info:
        if branch is not None:
            delivery_address = {
                "province": dropdown(branch_province),
                "district": dropdown(branch_district),
                "ward": dropdown(branch_ward),
                "number_and_street": branch.address
            }
            scb_branch = dropdown(branch)
        else:
            delivery_address = {
                "province": dropdown(province),
                "district": dropdown(district),
                "ward": dropdown(ward),
                "number_and_street": card_delivery_address.card_delivery_address_address
            }
            scb_branch = None

        issue_debit_card = {
            "register_flag": debit_card_info.card_registration_flag,
            "physical_card_type": dropdown(card_type),
            "physical_issuance_type": dropdown(card_issuance_type),
            "customer_type": dropdown(customer_type),
            "payment_online_flag": debit_card_info.payment_online_flag,
            "branch_of_card": dropdown(branch_of_card),
            "issuance_fee": dropdown(issuance_fee),
            "annual_fee": dropdown(issuance_fee),
            "debit_card_types": [
                {
>>>>>>> c44ebff7dd794083041391289ef6719d372bb6c3
                    "id": "1",
                    "code": "MDTC1",
                    "name": "VISA",
                    "source_code": "DM407",
                    "promo_code": "P311",
                    "active_flag": True
                },
                {
                    "id": "2",
                    "code": "VSDB",
                    "name": "MASTER CARD",
                    "source_code": "DM407",
                    "promo_code": "P311",
                    "active_flag": False
                }
            ]
        }
        card_delivery_address = {
            "scb_branch": scb_branch,
            "delivery_address": delivery_address,
            "note": card_delivery_address.card_delivery_address_note
        }

        # query lấy ra thông tin thẻ phụ
        sub_branch_province = aliased(AddressProvince, name='sub_branch_province')
        sub_branch_district = aliased(AddressDistrict, name='sub_branch_district')
        sub_branch_ward = aliased(AddressWard, name='sub_branch_ward')
        sub_debit_card = aliased(DebitCard, name='sub_debit_card')

        list_sub_debit_card_info_engine = select(
            DebitCard,
            sub_debit_card,
            Customer,
            CardType,
            CardIssuanceType,
            BrandOfCard,
            Branch,
            sub_branch_province,
            sub_branch_district,
            sub_branch_ward,
            CardDeliveryAddress,
            AddressWard,
            AddressDistrict,
            AddressProvince,
        ).join(
            sub_debit_card, DebitCard.id == sub_debit_card.parent_card_id
        ).join(
            Customer, sub_debit_card.customer_id == Customer.id
        ).join(
            CardType, sub_debit_card.card_type_id == CardType.id
        ).join(
            CardIssuanceType, sub_debit_card.card_type_id == CardIssuanceType.id
        ).join(
            BrandOfCard, sub_debit_card.card_type_id == BrandOfCard.id
        ).join(
            CardDeliveryAddress, sub_debit_card.card_delivery_address_id == CardDeliveryAddress.id
        ).outerjoin(
            Branch, CardDeliveryAddress.branch_id == Branch.id
        ).outerjoin(
            sub_branch_province, Branch.province_id == sub_branch_province.id
        ).outerjoin(
            sub_branch_district, Branch.district_id == sub_branch_district.id
        ).outerjoin(
            sub_branch_ward, Branch.ward_id == sub_branch_ward.id
        ).outerjoin(
            AddressWard, CardDeliveryAddress.ward_id == AddressWard.id,
        ).outerjoin(
            AddressDistrict, CardDeliveryAddress.district_id == AddressDistrict.id
        ).outerjoin(
            AddressProvince, CardDeliveryAddress.province_id == AddressProvince.id
        ).filter(
            DebitCard.customer_id == cif_id,
            sub_debit_card.active_flag == 1,
            Customer.complete_flag == 1,
        )

        list_sub_debit_card_info = session.execute(list_sub_debit_card_info_engine).all()

        sub_debit_cards = []
        for _, sub_debit_card_info, customer, sub_card_type, sub_card_issuance_type, \
                sub_branch_of_card, sub_branch, sub_branch_province, sub_branch_district, sub_branch_ward, \
                sub_card_delivery_address, sub_ward, sub_district, sub_province in list_sub_debit_card_info:
            if sub_branch is not None:
                delivery_address = {
                    "province": dropdown(sub_branch_province),
                    "district": dropdown(sub_branch_district),
                    "ward": dropdown(sub_branch_ward),
                    "number_and_street": sub_branch.address
                }
                scb_branch = dropdown(sub_branch)
            else:
                delivery_address = {
                    "province": dropdown(sub_province),
                    "district": dropdown(sub_district),
                    "ward": dropdown(sub_ward),
                    "number_and_street": sub_card_delivery_address.card_delivery_address_address
                }
                scb_branch = None

            sub_card_delivery_address = {
                "scb_branch": scb_branch,
                "delivery_address": delivery_address,
                "note": sub_card_delivery_address.card_delivery_address_note
            }

            sub_debit_card = {
                "id": sub_debit_card_info.id,
                "cif_number": customer.cif_number,
                "name_on_card": {  # chưa có api để gọi
                    "first_name_on_card": "TRAN",
                    "middle_name_on_card": "THANH",
                    "last_name_on_card": "TUYEN"
                },
                "physical_card_type": dropdown(sub_card_type),
                "card_issuance_type": dropdown(sub_card_issuance_type),
                "payment_online_flag": sub_debit_card_info.payment_online_flag,
                "card_delivery_address": sub_card_delivery_address,
                "sub_card_number": {  # chưa có api để gọi
                    "number_part_1": "1234",
                    "number_part_2": "5678",
                    "number_part_3": "9875",
                    "number_part_4": "5781"
                },
                "card_image_url": "https://vi.wikipedia.org/wiki/Trang_Ch%C3%ADn"

            }
            sub_debit_cards.append(sub_debit_card)
        return ReposReturn(data={
            "issue_debit_card": issue_debit_card,
            "information_debit_card": {  # chưa có api để gọi
                "name_on_card": {
                    "first_name_on_card": "TRAN",
                    "middle_name_on_card": "THANH",
                    "last_name_on_card": "TUYEN"
                },
                "main_card_number": {
                    "number_part_1": "1234",
                    "number_part_2": "5678",
                    "number_part_3": "9875",
                    "number_part_4": "5781"
                },
                "card_image_url": "https://vi.wikipedia.org/wiki/Trang_Ch%C3%ADn"
            },
            "card_delivery_address": card_delivery_address,
            "information_sub_debit_card": {
                "sub_debit_cards": sub_debit_cards,
                "total_sub_debit_card": len(sub_debit_cards)
            }

        })


async def repos_add_debit_card(cif_id: str, debt_card_req: DebitCardRequest) -> ReposReturn:  # noqa
    if cif_id == CIF_ID_TEST:
        return ReposReturn(data={
            'created_at': now(),
            'created_by': 'system',
            'updated_at': now(),
            'updated_by': 'system'
        })
    else:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc="cif_id")


async def repos_get_list_debit_card(
        cif_id: str,
        branch_of_card_id: str,  # noqa
        issuance_fee_id: str,  # noqa
        annual_fee_id: str  # noqa
) -> ReposReturn:
    if cif_id == CIF_ID_TEST:
        return ReposReturn(data=[
            {
                "id": "1",
                "code": "MDTC1",
                "name": "VISA",
                "source_code": "DM407",
                "promo_code": "P311",
            },
            {
                "id": "2",
                "code": "VSDB",
                "name": "MASTER CARD",
                "source_code": "DM407",
                "promo_code": "P311",
            }
        ]
        )
    else:
        ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc="cif_id")
