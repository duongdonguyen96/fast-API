from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn, auto_commit
from app.third_parties.oracle.models.cif.basic_information.model import (
    Customer
)
from app.third_parties.oracle.models.cif.e_banking.model import (
    EBankingInfo, EBankingInfoAuthentication,
    EBankingReceiverNotificationRelationship, EBankingRegisterBalance,
    EBankingRegisterBalanceNotification, EBankingRegisterBalanceOption,
    TdAccount
)
from app.third_parties.oracle.models.cif.payment_account.model import (
    CasaAccount
)
from app.third_parties.oracle.models.master_data.account import AccountType
from app.third_parties.oracle.models.master_data.customer import (
    CustomerContactType, CustomerRelationshipType
)
from app.third_parties.oracle.models.master_data.e_banking import (
    EBankingNotification
)
from app.third_parties.oracle.models.master_data.others import (
    MethodAuthentication
)
from app.utils.constant.cif import (
    CIF_ID_TEST, EBANKING_ACCOUNT_TYPE_CHECKING, EBANKING_ACCOUNT_TYPE_SAVING
)
from app.utils.error_messages import ERROR_CIF_ID_NOT_EXIST
from app.utils.functions import dropdown, now


@auto_commit
async def repos_save_e_banking_data(
        cif_id: str,
        insert_data,
        created_by: str,
        session: Session,
) -> ReposReturn:
    # clear old data
    e_banking_reg_balance = session.execute(select(
        EBankingRegisterBalance
    ).filter(
        EBankingRegisterBalance.customer_id == cif_id,
    )).first()

    session.execute(delete(
        EBankingReceiverNotificationRelationship
    ).filter(
        EBankingReceiverNotificationRelationship.e_banking_register_balance_casa_id == e_banking_reg_balance.EBankingRegisterBalance.id,
    ))

    session.execute(delete(e_banking_reg_balance))

    session.execute(delete(
        EBankingRegisterBalanceOption
    ).filter(
        EBankingRegisterBalanceOption.customer_id == cif_id,
    ))

    session.execute(delete(
        EBankingRegisterBalanceNotification
    ).filter(
        EBankingRegisterBalanceNotification.customer_id == cif_id,
    ))

    e_banking_info = session.execute(select(
        EBankingInfo
    ).filter(
        EBankingInfo.customer_id == cif_id,
    )).first()

    session.execute(delete(
        EBankingInfoAuthentication
    ).filter(
        EBankingInfoAuthentication.e_banking_info_id == e_banking_info.EBankingInfo.id,
    ))

    session.execute(delete(e_banking_info.EBankingInfo))

    session.bulk_save_objects(insert_data)
    return ReposReturn(data={
        "cif_id": cif_id,
        "created_at": now(),
        "created_by": created_by
    })


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


async def repos_get_e_banking_data(cif_id: str, session: Session) -> ReposReturn:
    e_banking_register_balance = session.execute(select(
        EBankingRegisterBalance,
        EBankingRegisterBalanceNotification,
        EBankingNotification,
        EBankingReceiverNotificationRelationship,
        CustomerRelationshipType
    ).join(
        EBankingRegisterBalanceNotification,
        EBankingRegisterBalance.id == EBankingRegisterBalanceNotification.eb_reg_balance_id
    ).join(
        EBankingReceiverNotificationRelationship,
        EBankingRegisterBalance.id == EBankingReceiverNotificationRelationship.e_banking_register_balance_casa_id
    ).join(
        CustomerRelationshipType,
        EBankingReceiverNotificationRelationship.relationship_type_id == CustomerRelationshipType.id
    ).join(
        EBankingNotification, EBankingRegisterBalanceNotification.eb_notify_id == EBankingNotification.id
    ).filter(
        EBankingRegisterBalance.customer_id == cif_id,
    )).all()

    checking_registration_info, saving_registration_info = {}, {}
    for register in e_banking_register_balance:
        if register.EBankingRegisterBalance.e_banking_register_account_type == EBANKING_ACCOUNT_TYPE_CHECKING:
            if not checking_registration_info.get(register.EBankingRegisterBalance.account_id):
                checking_registration_info[
                    register.EBankingRegisterBalance.account_id] = register.EBankingRegisterBalance.__dict__
                checking_registration_info[register.EBankingRegisterBalance.account_id]["notifications"] = [
                    register.EBankingNotification]
                checking_registration_info[register.EBankingRegisterBalance.account_id]["relationships"] = [{
                    "info": register.EBankingReceiverNotificationRelationship,
                    "relation_type": register.CustomerRelationshipType
                }]
            else:
                checking_registration_info[register.EBankingRegisterBalance.account_id]["notifications"].append(
                    register.EBankingNotification)
                checking_registration_info[register.EBankingRegisterBalance.account_id]["relationships"].append({
                    "info": register.EBankingReceiverNotificationRelationship,
                    "relation_type": register.CustomerRelationshipType
                })
        else:
            if not saving_registration_info.get(register.EBankingRegisterBalance.account_id):
                saving_registration_info[
                    register.EBankingRegisterBalance.account_id] = register.EBankingRegisterBalance.__dict__
                checking_registration_info[register.EBankingRegisterBalance.account_id]["notifications"] = [
                    register.EBankingNotification]
                checking_registration_info[register.EBankingRegisterBalance.account_id]["relationships"] = [{
                    "info": register.EBankingReceiverNotificationRelationship,
                    "relation_type": register.CustomerRelationshipType
                }]
            else:
                checking_registration_info[register.EBankingRegisterBalance.account_id]["notifications"].append(
                    register.EBankingNotification)
                checking_registration_info[register.EBankingRegisterBalance.account_id]["relationships"].append({
                    "info": register.EBankingReceiverNotificationRelationship,
                    "relation_type": register.CustomerRelationshipType
                })

    contact_types = session.execute(
        select(
            EBankingRegisterBalanceOption,
            CustomerContactType,
        ).outerjoin(
            EBankingRegisterBalanceOption,
            CustomerContactType.id == EBankingRegisterBalanceOption.customer_contact_type_id
        ).filter(
            EBankingRegisterBalanceOption.customer_id == cif_id
        )
    ).all()

    # Get e-banking information
    auth_method_query = session.execute(
        select(
            EBankingInfo,
            EBankingInfoAuthentication,
            MethodAuthentication
        ).outerjoin(
            EBankingInfoAuthentication,
            MethodAuthentication.id == EBankingInfoAuthentication.method_authentication_id
        ).join(
            EBankingInfo,
            EBankingInfoAuthentication.e_banking_info_id == EBankingInfo.id
        ).filter(
            EBankingInfo.customer_id == cif_id
        )
    ).all()

    account_info = {}
    for auth_method in auth_method_query:
        if auth_method.EBankingInfo:
            account_info["register_flag"] = True
            account_info["account_name"] = auth_method.EBankingInfo.account_name
            account_info["charged_account_id"] = auth_method.EBankingInfo.account_payment_fee
            account_info["method_active_password"] = auth_method.EBankingInfo.method_active_password_id
            break

    return ReposReturn(data={
        "change_of_balance_payment_account": {
            "register_flag": True if checking_registration_info else False,
            # TODO: hỏi lại chỗ này có trả danh sách các loại contact luôn không?
            "customer_contact_types": [
                {
                    "id": contact_type.CustomerContactType.id,
                    "name": contact_type.CustomerContactType.name,
                    "group": contact_type.CustomerContactType.group,
                    "description": contact_type.CustomerContactType.description,
                    "checked_flag": True if contact_type.EBankingRegisterBalanceOption else False
                } for contact_type in contact_types if contact_type.EBankingRegisterBalanceOption.e_banking_register_account_type == EBANKING_ACCOUNT_TYPE_CHECKING
            ],
            "register_balance_casas": [
                {
                    "account_id": registration_info['account_id'],
                    "checking_account_name": registration_info['name'],
                    "primary_phone_number": registration_info['mobile_number'],
                    "full_name_vn": registration_info['full_name'],
                    "notification_casa_relationships": [
                        {
                            "id": relationship["info"].id,
                            "mobile_number": relationship["info"].mobile_number,
                            "full_name_vn": relationship["info"].full_name,
                            "relationship_type": dropdown(relationship["relation_type"])
                        } for relationship in registration_info['relationships']
                    ],
                    "e_banking_notifications": [
                        {
                            **dropdown(notification),
                            "checked_flag": True
                        } for notification in registration_info['notifications']
                    ]
                } for registration_info in checking_registration_info.values()
            ]
        },
        # Mở CIF nên không có tài khoản tiết kiệm
        "change_of_balance_saving_account": {
            "register_flag": False,
            "customer_contact_types": [
                {
                    "id": contact_type.CustomerContactType.id,
                    "name": contact_type.CustomerContactType.name,
                    "group": contact_type.CustomerContactType.group,
                    "description": contact_type.CustomerContactType.description,
                    "checked_flag": True if contact_type.EBankingRegisterBalanceOption else False
                } for contact_type in contact_types if contact_type.EBankingRegisterBalanceOption.e_banking_register_account_type == EBANKING_ACCOUNT_TYPE_SAVING
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
                **account_info,
                "method_authentication": [
                    {
                        **dropdown(method.MethodAuthentication),
                        "checked_flag": True if method.EBankingInfo else False
                    } for method in auth_method_query
                ],
            },
            # Mở CIF không có phần này
            # "optional_e_banking_account": {
            #     "reset_password_flag": None,
            #     "active_account_flag": None,
            #     "note": None,
            #     "updated_by": None,
            #     "updated_at": None
            # }
        }
    })


async def repos_get_list_balance_payment_account(cif_id: str, session: Session) -> ReposReturn:
    balance_payments = session.execute(
        select(
            CasaAccount,
            AccountType
        ).join(
            AccountType, CasaAccount.acc_type_id == AccountType.id
        ).filter(CasaAccount.customer_id == cif_id)
    ).all()

    if not balance_payments:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc="cif_id")

    response_data = [{
        "id": balance_payment.id,
        "account_number": balance_payment.case_account_number,
        "product_name": dropdown(account_type),
        "checked_flag": balance_payment.acc_active_flag
    } for balance_payment, account_type in balance_payments]

    return ReposReturn(data=response_data)


async def repos_get_detail_reset_password(cif_id: str) -> ReposReturn:
    if cif_id != CIF_ID_TEST:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc='cif_id')

    return ReposReturn(data=DETAIL_RESET_PASSWORD_E_BANKING_DATA)


async def repos_balance_saving_account_data(cif_id: str, session: Session) -> ReposReturn:
    saving_account = session.execute(
        select(
            Customer,
            TdAccount
        ).filter(Customer.id == cif_id)
    ).all()

    if not saving_account:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc="cif_id")

    response_data = [
        {
            "id": td_account.id,
            "account_number": td_account.td_account_number,
            "name": customer.full_name_vn,
            "checked_flag": td_account.active_flag

        } for customer, td_account in saving_account]

    return ReposReturn(data=response_data)


async def repos_get_detail_reset_password_teller(cif_id: str) -> ReposReturn:
    if cif_id != CIF_ID_TEST:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc='cif_id')

    return ReposReturn(data={
        "personal_customer_information": {
            "id": "1234567",
            "cif_number": "1324567",
            "customer_classification": {
                "id": "1",
                "code": "CANHAN",
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
            "issued_date": "2019-02-01",
            "expired_date": "2032-03-02",
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
        "document": {
            "id": "1",
            "name": "Biểu mẫu đề nghị cấp lại mật khẩu Ebanking",
            "url": "https://example.com/abc/pdf",
            "version": "1.0",
            "created_by": "Nguyễn Phúc",
            "created_at": "2020-02-01 08:40",
            "active_flag": True
        }
    })
