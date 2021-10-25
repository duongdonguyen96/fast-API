from app.api.base.repository import ReposReturn
from app.utils.constant.cif import CIF_ID_TEST
from app.utils.error_messages import ERROR_CIF_ID_NOT_EXIST


async def repos_get_e_banking_data(cif_id: str) -> ReposReturn:
    if cif_id != CIF_ID_TEST:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc='cif_id')

    return ReposReturn(data={
        "change_of_balance_payment_account": {
            "register_flag": True,
            "customer_contact_types": [
                {
                    "id": "1",
                    "code": "OTT",
                    "name": "OTT",
                    "checked_flag": True
                },
                {
                    "id": "2",
                    "code": "SMS",
                    "name": "SMS",
                    "checked_flag": False
                }
            ],
            "register_balance_casas": [
                {
                    "id": "1",
                    "mobile_number": "25168385251",
                    "full_name_vn": "TRẦN MINH HUYỀN",
                    "primary_mobile_number": {
                        "id": "1",
                        "code": "code",
                        "name": "SDT Chính"
                    },
                    "notification_casa_relationships": [
                        {
                            "id": "1",
                            "mobile_number": "2541365822",
                            "full_name_vn": "Nguyễn văn Tèo",
                            "relationship_type": {
                                "id": "1",
                                "code": "BOME",
                                "name": "Bố mẹ"
                            }
                        },
                        {
                            "id": "2",
                            "mobile_number": "2541365822",
                            "full_name_vn": "Trần văn B",
                            "relationship_type": {
                                "id": "1",
                                "code": "VOCHONG",
                                "name": "Vợ chồng"
                            }
                        }
                    ],
                    "e_banking_notifications": [
                        {
                            "id": "1",
                            "code": "code",
                            "name": "Tất cả",
                            "checked_flag": True
                        },
                        {
                            "id": "2",
                            "code": "code",
                            "name": "Biến động số dư",
                            "checked_flag": True
                        },
                        {
                            "id": "3",
                            "code": "code",
                            "name": "Tất toán tài khoản",
                            "checked_flag": True
                        },
                        {
                            "id": "4",
                            "code": "code",
                            "name": "Rút tiền",
                            "checked_flag": True
                        },
                        {
                            "id": "5",
                            "code": "code",
                            "name": "Nộp tiền",
                            "checked_flag": True
                        }
                    ]
                }
            ]
        },
        "change_of_balance_saving_account": {
            "register_flag": True,
            "customer_contact_types": [
                {
                    "id": "1",
                    "code": "OTT",
                    "name": "OTT",
                    "checked_flag": True
                },
                {
                    "id": "2",
                    "code": "SMS",
                    "name": "SMS",
                    "checked_flag": False
                }
            ],
            "mobile_number": "2541365822",
            "range": {
                "td_accounts": [
                    {
                        "id": "1",
                        "number": "001_03042021_00000001",
                        "name": "Trần Văn Quốc Khánh",
                        "checked_flag": False
                    },
                    {
                        "id": "2",
                        "number": "001_03042021_00000001",
                        "name": "Võ văn tùng",
                        "checked_flag": True
                    },
                    {
                        "id": "3",
                        "number": "001_03042021_00000001",
                        "name": "Trần Thị Sen",
                        "checked_flag": True
                    },
                    {
                        "id": "1",
                        "number": "001_03042021_00000001",
                        "name": "Trần Văn Quốc Khánh",
                        "checked_flag": True
                    }
                ],
                "page": 2,
                "limit": 2,
                "total_page": 30
            },
            "e_banking_notifications": [
                {
                    "id": "1",
                    "code": "code",
                    "name": "Tất cả",
                    "checked_flag": True
                },
                {
                    "id": "2",
                    "code": "code",
                    "name": "Biến động số dư",
                    "checked_flag": True
                },
                {
                    "id": "3",
                    "code": "code",
                    "name": "Tất toán tài khoản",
                    "checked_flag": True
                },
                {
                    "id": "4",
                    "code": "code",
                    "name": "Rút tiền",
                    "checked_flag": True
                },
                {
                    "id": "5",
                    "code": "code",
                    "name": "Nộp tiền",
                    "checked_flag": True
                }
            ]
        },
        "e_banking_information": {
            "account_information": {
                "register_flag": True,
                "account_name": "0325614879",
                "checked_flag": True,
                "e_banking_reset_password_methods": [
                    {
                        "id": "1",
                        "code": "SMS",
                        "name": "SMS",
                        "checked_flag": True
                    },
                    {
                        "id": "2",
                        "code": "EMAIL",
                        "name": "Email",
                        "checked_flag": False
                    }
                ],
                "method_authentication": [
                    {
                        "id": "1",
                        "code": "VANTAY",
                        "name": "Vân tay",
                        "checked_flag": False
                    },
                    {
                        "id": "2",
                        "code": "KHUONMAT",
                        "name": "Khuôn mặt",
                        "checked_flag": False
                    },
                    {
                        "id": "3",
                        "code": "SMS",
                        "name": "SMS",
                        "checked_flag": True
                    },
                    {
                        "id": "4",
                        "code": "SOFTTOKEN",
                        "name": "SOFT TOKEN",
                        "checked_flag": True
                    },
                    {
                        "id": "5",
                        "code": "HARDTOKEN",
                        "name": "HARD TOKEN",
                        "checked_flag": True
                    }
                ],
                "payment_fee": [
                    {
                        "id": "1",
                        "name": "Trích từ tài khoản",
                        "checked_flag": True,
                        "number": {
                            "id": "1",
                            "name": "023587412599634"
                        }
                    },
                    {
                        "id": "2",
                        "name": "Tiền mặt",
                        "checked_flag": False,
                        "number": {
                            "id": None,
                            "name": None
                        }
                    }
                ]
            },
            "optional_e_banking_account": {
                "reset_password_flag": True,
                "active_account_flag": True,
                "note": "note",
                "updated_by": "Nguyễn Anh Đào",
                "updated_at": "2021-03-06 09:25:00"
            }
        }
    })


async def repos_get_list_balance_payment_account(cif_id: str) -> ReposReturn:
    if cif_id != CIF_ID_TEST:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc='cif_id')

    return ReposReturn(data=[
        {
            "id": "123",
            "name": "231231321",
            "product": "S-Free",
            "checked_flag": True
        },
        {
            "id": "2",
            "name": "213213123123",
            "product": "Lộc phát",
            "checked_flag": False
        }
    ])
