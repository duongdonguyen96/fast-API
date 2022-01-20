GET_E_BANKING_SUCCESS = {
    "example": {
        "value": {
            "data": {
                "data": {
                    "change_of_balance_payment_account": {
                        "register_flag": False,
                        "customer_contact_types": [],
                        "register_balance_casas": []
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
                            "get_initial_password_method": "Email",
                            "method_authentication": [
                                {
                                    "id": "VAN_TAY",
                                    "code": "VAN_TAY",
                                    "name": "Vân tay",
                                    "checked_flag": True
                                }
                            ],
                            "charged_account": None
                        },
                        "optional_e_banking_account": None
                    }
                },
                "errors": []
            },
            "errors": []
        }
    }
}

POST_E_BANKING = {
    "change_of_balance_payment_account": {
        "register_flag": False,
        "customer_contact_types": [
            {
                "id": "EMAIL",
                "checked_flag": True
            }
        ],
        "register_balance_casas": [
            {
                "account_id": "D2349720A6641CDFE0530100007F9CCE",
                "account_name": "Nguyện Văn A",
                "primary_phone_number": "0987654321",
                "notification_casa_relationships": [
                    {
                        "mobile_number": "string",
                        "full_name_vn": "string",
                        "relationship_type": {
                            "id": "FRIENDS"
                        }
                    }
                ],
                "e_banking_notifications": [
                    {
                        "id": "TTTK",
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
                "id": "EMAIL",
                "checked_flag": True
            }
        ],
        "mobile_number": "string",
        "range": {
            "td_accounts": [
                {
                    "id": "string",
                    "checked_flag": True
                }
            ]
        },
        "e_banking_notifications": [
            {
                "id": "BDSD",
                "checked_flag": True
            }
        ]
    },
    "e_banking_information": {
        "account_information": {
            "register_flag": True,
            "account_name": "string",
            "get_initial_password_method": "Email",
            "method_authentication": [
                {
                    "id": "VAN_TAY",
                    "name": "Vân tay",
                    "code": "VAN_TAY",
                    "checked_flag": True
                }
            ],
            "payment_fee": []
        }
    }
}
