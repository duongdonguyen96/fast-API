GET_E_BANKING_SUCCESS = {
    "example": {
        "value": {
            "data": {
                "change_of_balance_payment_account": {
                    "register_flag": True,
                    "customer_contact_types": [
                        {
                            "id": "EMAIL",
                            "name": "BE_TEST1",
                            "group": "BE_TEST1",
                            "description": "test",
                            "checked_flag": True
                        }
                    ],
                    "register_balance_casas": [
                        {
                            "account_id": "D2349720A6641CDFE0530100007F9CCE",
                            "checking_account_name": "Nguyện Văn A",
                            "primary_phone_number": "0987654321",
                            "full_name_vn": "TRẦN THỊ PHƯƠNG DUNG1",
                            "notification_casa_relationships": [
                                {
                                    "id": "D2FE65C942762C46E0530100007FDFFC",
                                    "mobile_number": "string",
                                    "full_name_vn": "string",
                                    "relationship_type": {
                                        "id": "FRIENDS",
                                        "code": "FRIENDS",
                                        "name": "FRIENDS"
                                    }
                                }
                            ],
                            "e_banking_notifications": [
                                {
                                    "id": "TTTK",
                                    "code": "TTTK",
                                    "name": "Tất toán tài khoản",
                                    "checked_flag": True
                                }
                            ]
                        }
                    ]
                },
                "change_of_balance_saving_account": {
                    "register_flag": False,
                    "customer_contact_types": [
                        {
                            "id": "EMAIL",
                            "name": "BE_TEST1",
                            "group": "BE_TEST1",
                            "description": "test",
                            "checked_flag": True
                        }
                    ],
                    "mobile_number": "2541365822",
                    "range": {
                        "td_accounts": [],
                        "page": 0,
                        "limit": 6,
                        "total_page": 0
                    },
                    "e_banking_notifications": []
                },
                "e_banking_information": {
                    "account_information": {
                        "register_flag": True,
                        "account_name": "string",
                        "charged_account_id": None,
                        "method_active_password": "EMAIL",
                        "method_authentication": [
                            {
                                "id": "D29A4A5600A9AB9EE0530100007FF78A",
                                "code": "SMS",
                                "name": "SMS",
                                "checked_flag": True
                            }
                        ]
                    }
                }
            },
            "errors": []
        }
    }
}
