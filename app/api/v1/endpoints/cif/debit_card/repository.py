from app.api.base.repository import ReposReturn
from app.api.v1.endpoints.cif.debit_card.schema import DebitCardRequest
from app.utils.constant.cif import CIF_ID_TEST
from app.utils.error_messages import ERROR_CIF_ID_NOT_EXIST
from app.utils.functions import now


async def repos_debit_card(cif_id: str) -> ReposReturn:
    if cif_id == CIF_ID_TEST:
        return ReposReturn(data={
            "issue_debit_card": {
                "register_flag": True,
                "physical_card_type": True,
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


async def repos_add_debit_card(cif_id: str, debt_card_req: DebitCardRequest)->ReposReturn: # noqa
    if cif_id == CIF_ID_TEST:
        return ReposReturn(data={
            'created_at': now(),
            'created_by': 'system',
            'updated_at': now(),
            'updated_by': 'system'
        })
    else:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc="cif_id")
