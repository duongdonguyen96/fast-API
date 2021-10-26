from app.api.base.repository import ReposReturn
from app.utils.constant.cif import CIF_ID_TEST
from app.utils.error_messages import ERROR_CIF_ID_NOT_EXIST

DETAIL_RESET_PASSWORD_E_BANKING_DATA = {
    "personal_customer_information": {
        "id": "1234567",
        "cif_number": "1324567",
        "customer_classification": {
            "id": "1",
            "code": "CA_NHAN",
            "name": "Cá nhân"
        },
        "avatar_url": "example.com/example.jpg",
        "full_name": "TRAN MINH HUYEN",
        "gender": {
            "id": "1",
            "code": "NU",
            "name": "Nữ"
        },
        "email": "nhuxuanlenguyen153@gmail.com",
        "mobile_number": "0896524256",
        "identity_number": "079197005869",
        "place_of_issue": {
            "id": "1",
            "code": "HCM",
            "name": "TPHCM"
        },
        "issued_date": "2021-02-18",
        "expired_date": "2021-02-18",
        "address": "144 Nguyễn Thị Minh Khai, Phường Bến Nghé, Quận 1, TPHCM",
        "e_banking_reset_password_method": [
            {
                "id": "1",
                "code": "SMS",
                "name": "SMS",
                "checked_flag": False
            },
            {
                "id": "2",
                "code": "EMAIL",
                "name": "EMAIL",
                "checked_flag": True
            }
        ],
        "e_banking_account_name": "huyentranminh"
    },
    "question": {
        "basic_question_1": {
            "branch_of_card": {
                "id": "123",
                "code": "MASTERCARD",
                "name": "Mastercard",
                "color": {
                    "id": "123",
                    "code": "YELLOW",
                    "name": "Vàng"
                }
            },
            "sub_card_number": 2,
            "mobile_number": "0897528556",
            "branch": {
                "id": "0897528556",
                "code": "HO",
                "name": "Hội Sở"
            },
            "method_authentication": {
                "id": "1",
                "code": "SMS",
                "name": "SMS"
            },
            "e_banking_account_name": "huyentranminh"
        },
        "basic_question_2": {
            "last_four_digits": "1234",
            "credit_limit": {
                "value": "20000000",
                "currency": {
                    "id": "1",
                    "code": "VND",
                    "name": "Việt Nam Đồng"
                }
            },
            "email": "huyentranminh126@gmail.com",
            "secret_question_or_personal_relationships": [
                {
                    "customer_relationship": {
                        "id": "1",
                        "code": "MOTHER",
                        "name": "Mẹ"
                    },
                    "mobile_number": "0867589623"
                }
            ],
            "automatic_debit_status": "",
            "transaction_method_receiver": {
                "id": "1",
                "code": "EMAIL",
                "name": "Email"
            }
        },
        "advanced_question": {
            "used_limit_of_credit_card": {
                "value": "20000000",
                "currency": {
                    "id": "1",
                    "code": "VND",
                    "name": "Việt Nam Đồng"
                }
            },
            "nearest_3d_secure": {
                "business_partner": {
                    "id": "1",
                    "code": "GRAB",
                    "name": "Grab"
                },
                "value": "125000",
                "currency": {
                    "id": "1",
                    "code": "VND",
                    "name": "Việt Nam Đồng"
                }
            },
            "one_of_two_nearest_successful_transaction": "",
            "nearest_successful_login_time": ""
        }
    },
    "document_url": "example.com/example.pdf",
    "result": {
        "confirm_current_transaction_flag": True,
        "note": "Trả lời đầy đủ các câu hỏi"
    }
}


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
                                "code": "BO_ME",
                                "name": "Bố mẹ"
                            }
                        },
                        {
                            "id": "2",
                            "mobile_number": "2541365822",
                            "full_name_vn": "Trần văn B",
                            "relationship_type": {
                                "id": "1",
                                "code": "VO_CHONG",
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
                        "code": "VAN_TAY",
                        "name": "Vân tay",
                        "checked_flag": False
                    },
                    {
                        "id": "2",
                        "code": "KHUON_MAT",
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
                        "code": "SOFT_TOKEN",
                        "name": "SOFT TOKEN",
                        "checked_flag": True
                    },
                    {
                        "id": "5",
                        "code": "HARD_TOKEN",
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
    }
    )


async def repos_get_detail_reset_password(cif_id: str) -> ReposReturn:
    if cif_id != CIF_ID_TEST:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc='cif_id')

    return ReposReturn(data=DETAIL_RESET_PASSWORD_E_BANKING_DATA)
