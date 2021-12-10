from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn, auto_commit
from app.third_parties.oracle.models.cif.debit_card.model import (
    CardDeliveryAddress, DebitCard
)
from app.utils.constant.cif import CIF_ID_TEST
from app.utils.error_messages import ERROR_CIF_ID_NOT_EXIST
from app.utils.functions import now


async def repos_debit_card(cif_id: str) -> ReposReturn:
    if cif_id == CIF_ID_TEST:
        return ReposReturn(data={
            "issue_debit_card": {
                "register_flag": True,
                "physical_card_type": [
                    {
                        "id": "1",
                        "code": "1",
                        "name": "Physic"
                    },
                    {
                        "id": "2",
                        "code": "2",
                        "name": "Non-Physic"
                    }
                ],
                "physical_issuance_type": {
                    "id": "1",
                    "code": "NORMAL",
                    "name": "Thông thường"
                },
                "customer_type": {
                    "id": "1",
                    "code": "1",
                    "name": "abc"
                },
                "payment_online_flag": True,
                "branch_of_card": {
                    "id": "123",
                    "code": "VISA",
                    "name": "VISA"
                },
                "issuance_fee": {
                    "id": "1",
                    "code": "FREE",
                    "name": "miễn phí"
                },
                "annual_fee": {
                    "id": "123",
                    "code": "FREE",
                    "name": "miễn phí"
                },
                "debit_card_types": [
                    {
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
            },
            "information_debit_card": {
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
            "card_delivery_address": {
                "scb_delivery_address_flag": True,
                "scb_branch": {
                    "id": 1,
                    "code": "BT",
                    "name": "Bình Tân"
                },
                "delivery_address": {
                    "province": {
                        "id": "1",
                        "code": "HCM",
                        "name": "Hồ Chí Minh"
                    },
                    "district": {
                        "id": "2",
                        "code": "BT",
                        "name": "Bình Tân"
                    },
                    "ward": {
                        "id": "3",
                        "code": "BHH",
                        "name": "Bình Hưng Hòa"
                    },
                    "number_and_street": "123/456/abc",
                },
                "note": "địa chỉ cơ quan"
            },
            "information_sub_debit_card": {
                "sub_debit_cards": [
                    {
                        "id": "234",
                        "name": "thẻ phụ 2",
                        "cif_number": "123456789",
                        "name_on_card": {
                            "first_name_on_card": "TRAN",
                            "middle_name_on_card": "THANH",
                            "last_name_on_card": "TUYEN"
                        },
                        "physical_card_type": True,
                        "card_issuance_type": {
                            "id": "1",
                            "code": "NORMAL",
                            "name": "Thông thường"
                        },
                        "payment_online_flag": True,
                        "card_delivery_address": {
                            "scb_delivery_address_flag": True,
                            "scb_branch": {
                                "id": 1,
                                "code": "BT",
                                "name": "Bình Tân"
                            },
                            "delivery_address": {
                                "province": {
                                    "id": "1",
                                    "code": "HCM",
                                    "name": "Hồ Chí Minh"
                                },
                                "district": {
                                    "id": "2",
                                    "code": "BT",
                                    "name": "Bình Tân"
                                },
                                "ward": {
                                    "id": "3",
                                    "code": "BHH",
                                    "name": "Bình Hưng Hòa"
                                },
                                "number_and_street": "123/456/abc",
                            },
                            "note": "string"
                        },
                        "sub_card_number": {
                            "number_part_1": "1234",
                            "number_part_2": "5678",
                            "number_part_3": "9875",
                            "number_part_4": "5781"
                        },
                        "card_image_url": "https://vi.wikipedia.org/wiki/Trang_Ch%C3%ADn"
                    }
                ],
                "total_sub_debit_card": 9
            }

        })
    else:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc="cif_id")


@auto_commit
async def repos_add_debit_card(
        cif_id: str,
        data_card_delivery_address,
        data_debit_card,
        list_sub_delivery_address,
        list_sub_debit_card,
        session: Session) -> ReposReturn:
    session.add_all([
        CardDeliveryAddress(**data_card_delivery_address),

        DebitCard(**data_debit_card),

    ])

    session.flush()
    session.bulk_save_objects(
        [CardDeliveryAddress(**list_sub_delivery_address) for list_sub_delivery_address in list_sub_delivery_address])
    session.bulk_save_objects([DebitCard(**list_sub_debit_card) for list_sub_debit_card in list_sub_debit_card])

    return ReposReturn(data={
        'created_at': now(),
        'created_by': 'system',
        'updated_at': now(),
        'updated_by': 'system'
    })


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
