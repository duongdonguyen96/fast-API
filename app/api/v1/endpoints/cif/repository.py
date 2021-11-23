from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from typing import List
from app.api.base.repository import ReposReturn
from app.third_parties.oracle.models.cif.basic_information.identity.model import (
    CustomerIdentity
)
from app.third_parties.oracle.models.cif.basic_information.model import (
    Customer
)
from app.third_parties.oracle.models.master_data.identity import ImageType
from app.third_parties.oracle.models.master_data.others import HrmEmployee
from app.utils.constant.cif import CIF_ID_TEST, IDENTITY_DOCUMENT_TYPE_PASSPORT, RESIDENT_ADDRESS_CODE, \
    CONTACT_ADDRESS_CODE
from app.utils.error_messages import ERROR_CIF_ID_NOT_EXIST
from app.utils.functions import dropdown


async def repos_get_initializing_customer(cif_id: str, session: Session) -> ReposReturn:
    customer = session.execute(
        select(
            Customer
        ).filter(
            Customer.id == cif_id,
            Customer.complete_flag == 0
        )
    ).scalar()
    if not customer:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc='cif_id')

    return ReposReturn(data=customer)


async def repos_get_hrm_employees(hrm_employee_ids: List[str], session: Session) -> ReposReturn:
    hrm_employees = session.execute(
        select(
            HrmEmployee
        ).filter(
            HrmEmployee.id.in_(hrm_employee_ids)
        )
    ).scalars().all()
    if len(hrm_employees) != len(hrm_employee_ids):
        return ReposReturn(is_error=True, detail="employee is not exist", loc="staff_id")

    return ReposReturn(data=hrm_employees)


async def repos_get_cif_info(cif_id: str) -> ReposReturn:
    if cif_id == CIF_ID_TEST:
        return ReposReturn(data={
            "self_selected_cif_flag": True,
            "cif_number": "123456789",
            "customer_classification": {
                "id": "fd01b796-5ad1-4161-8e2c-2abe41390deb",
                "code": "CN",
                "name": "Cá nhân"
            },
            "customer_economic_profession": {
                "id": "b860d25e-0db2-496b-8bb7-76d6838d191a",
                "code": "KT1",
                "name": "Mã ngành KT"
            },
            "kyc_level": {
                "id": "24152d4a-13c8-4720-a92d-2f2e784af6af",
                "code": "LV1",
                "name": "Level 1"
            }
        }
        )
    else:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc='cif_id')


async def repos_profile_history(cif_id: str) -> ReposReturn:
    if cif_id == CIF_ID_TEST:
        return ReposReturn(data=[
            {

                "created_date": "string",
                "logs":

                    [

                        {
                            "user_id": "string",
                            "full_name": "string",
                            "user_avatar_url": "string",
                            "id": "string",
                            "created_at": "2019-08-24T14:15:22Z",
                            "content": "string"
                        },
                        {
                            "user_id": "string",
                            "full_name": "string",
                            "user_avatar_url": "string",
                            "id": "string",
                            "created_at": "2019-08-24T14:15:22Z",
                            "content": "string"
                        }
                    ]

            },
            {

                "created_date": "string",
                "logs":

                    [

                        {
                            "user_id": "string",
                            "full_name": "string",
                            "user_avatar_url": "string",
                            "id": "string",
                            "created_at": "2019-08-24T14:15:22Z",
                            "content": "string"
                        },
                        {
                            "user_id": "string",
                            "full_name": "string",
                            "user_avatar_url": "string",
                            "id": "string",
                            "created_at": "2019-08-24T14:15:22Z",
                            "content": "string"
                        }
                    ]
            }
        ]
        )
    else:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc='cif_id')


async def repos_customer_information(cif_id: str) -> ReposReturn:
    if cif_id != CIF_ID_TEST:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc='cif_id')

    return ReposReturn(data={
        "customer_id": "1",
        "status": {
            "id": "1",
            "code": "code",
            "name": "MỞ",
            "active_flag": True
        },
        "cif_number": "2541352",
        "avatar_url": "http://example.com/example.jpg",
        "customer_classification": {
            "id": "1",
            "code": "CANHAN",
            "name": "Cá nhân"
        },
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
        "issued_date": "2019-02-02",
        "expired_date": "2032-02-02",
        "date_of_birth": "2002-02-02",
        "nationality": {
            "id": "1",
            "code": "VN",
            "name": "VIỆT NAM"
        },
        "marital_status": {
            "id": "1",
            "code": "DOCTHAN",
            "name": "Độc thân"
        },
        "customer_class": {
            "id": "1",
            "code": "DIAMOND",
            "name": "Diamond"
        },
        "credit_rating": {
            "id": "1",
            "code": "CODE",
            "name": "BBB"
        },
        "address": "144 Nguyễn Thị Minh Khai, Phường Bến Nghé, Quận 1, TPHCM",
        "total_number_of_participant": 3,
        "employees": [
            {
                "id": "1",
                "full_name_vn": "AAAAAA",
                "avatar_url": "http://example.com/example.jpg",
                "user_name": "username",
                "email": "asdfgh@gmail.com",
                "job_title": "chức danh",
                "department_id": "Khối VH&CN"
            },
            {
                "id": "2",
                "full_name_vn": "AAAAAA",
                "avatar_url": "http://example.com/example.jpg",
                "user_name": "username",
                "email": "asdfgh@gmail.com",
                "job_title": "chức danh",
                "department_id": "Khối VH&CN"
            },
            {
                "id": "3",
                "full_name_vn": "AAAAAA",
                "avatar_url": "http://example.com/example.jpg",
                "user_name": "username",
                "email": "asdfgh@gmail.com",
                "job_title": "chức danh",
                "department_id": "Khối VH&CN"
            }
        ]
    })


async def repos_get_last_identity(cif_id: str, session: Session):
    identity = session.execute(
        select(
            CustomerIdentity
        ).filter(CustomerIdentity.customer_id == cif_id).order_by(desc(CustomerIdentity.maker_at))
    ).scalars().first()

    if not identity:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc="cif_id")
    return ReposReturn(data=identity)


async def repos_get_image_type(image_type: str, session: Session) -> ReposReturn:
    image_type = session.execute(
        select(
            ImageType
        ).filter(ImageType.code == image_type)
    ).scalar()

    if not image_type:
        return ReposReturn(is_error=True, msg='ERROR_IMAGE_TYPE_NOT_EXIST', loc='image_type')

    return ReposReturn(data=image_type)


async def repos_get_identity_info(
        identities,
        identity_document_type_id,
):
    customer, identity, individual_info, _, _, identity_type, _, _, _, place_of_issue, gender, country, province, _, \
    _, nation, religion, passport_type, passport_code = identities[0]
    address_information = {
        "resident_address": {
            "province": {
                "id": "",
                "code": "",
                "name": ""
            },
            "district": {
                "id": "",
                "code": "",
                "name": ""
            },
            "ward": {
                "id": "",
                "code": "",
                "name": ""
            },
            "number_and_street": ""
        },
        "contact_address": {
            "province": {
                "id": "",
                "code": "",
                "name": ""
            },
            "district": {
                "id": "",
                "code": "",
                "name": ""
            },
            "ward": {
                "id": "",
                "code": "",
                "name": ""
            },
            "number_and_street": ""
        }
    }
    identity_document = {
        "identity_number": "",
        "issued_date": "2000-01-01",
        "place_of_issue": {
            "id": "",
            "code": "",
            "name": ""
        },
        "expired_date": "2000-01-01",
        # HC
        "passport_type": {
            "id": "",
            "code": "",
            "name": ""
        },
        "passport_code": {
            "id": "",
            "code": "",
            "name": ""
        }
    }
    basic_information = {
        "id": "",
        "full_name_vn": "",
        "gender": {
            "id": "",
            "code": "",
            "name": ""
        },
        "date_of_birth": "2000-01-01",
        "nationality": {
            "id": "",
            "code": "",
            "name": ""
        },
        "province": {
            "id": "",
            "code": "",
            "name": ""
        },
        "ethnic": {
            "id": "",
            "code": "",
            "name": ""
        },
        "religion": {
            "id": "",
            "code": "",
            "name": ""
        },
        "identity_characteristic": "",
        "father_full_name_vn": "",
        "mother_full_name_vn": "",
        # HC
        "place_of_birth": {
            "id": "",
            "code": "",
            "name": ""
        },
        "identity_card_number": ""
    }
    backside_information = {
        "identity_image_url": "",
        "fingerprint": [
            {
                "image_url": "",
                "hand_side": {
                    "id": "",
                    "code": "",
                    "name": ""
                },
                "finger_type": {
                    "id": "",
                    "code": "",
                    "name": ""
                }
            }
        ],
        "updated_at": "2000-01-01 00:00:00",
        "updated_by": ""
    }
    passport_information = {
        "identity_image_url": "",
        "face_compare_image_url": "",
        "similar_percent": 00,
        "fingerprint": [
            {
                "image_url": "",
                "hand_side": {
                    "id": "",
                    "code": "",
                    "name": ""
                },
                "finger_type": {
                    "id": "",
                    "code": "",
                    "name": ""
                }
            }
        ]
    }
    identity_info = {
        "identity_document_type": {
            "id": "",
            "code": "",
            "name": ""
        },
        "frontside_information": {
            "identity_image_url": "",
            "face_compare_image_url": "",
            "similar_percent": 00
        },
        "backside_information": backside_information,
        "ocr_result": {
            "identity_document": identity_document,
            "basic_information": basic_information,
            "address_information": address_information
        },
        "passport_information": passport_information
    }
    # Loại giấy tờ định danh
    identity_info.update({
        "identity_document_type": dropdown(identity_type),
    })

    # Phân tích OCR -> Giấy tờ định danh
    identity_document.update({
        "identity_number": identity.identity_num,
        "issued_date": identity.issued_date,
        "place_of_issue": dropdown(place_of_issue),
        "expired_date": identity.expired_date,
        "mrz_content": identity.mrz_content,
        "qr_code_content": identity.qrcode_content,
    })
    # HC
    if identity_document_type_id == IDENTITY_DOCUMENT_TYPE_PASSPORT:
        identity_document.update({
            "passport_type": dropdown(passport_type),
            "passport_code": dropdown(passport_code)
        })

    # Phân tích OCR -> Thông tin cơ bản
    basic_information.update({
        "full_name_vn": customer.full_name_vn,
        "gender": dropdown(gender),
        "date_of_birth": individual_info.date_of_birth,
        "nationality": dropdown(country),
        "province": dropdown(province),
        "ethnic": dropdown(nation),
        "religion": dropdown(religion),
        "identity_characteristic": individual_info.identifying_characteristics,
        "father_full_name_vn": individual_info.father_full_name,
        "mother_full_name_vn": individual_info.mother_full_name,
        # HC
        "place_of_birth": dropdown(province),
        "identity_card_number": identity.identity_number_in_passport,
        "mrz_content": identity.mrz_content
    })

    fingerprint_list = []
    for _, _, _, customer_address, identity_image, _, compare_image, hand_side, finger_type, _, _, _, province, \
        district, ward, _, _, _, _ in identities:

        if identity_document_type_id != IDENTITY_DOCUMENT_TYPE_PASSPORT:
            # Mặt trước
            if identity_image.identity_image_front_flag == 1:
                identity_info.update({
                    "frontside_information": {
                        "identity_image_url": identity_image.image_url,
                        "face_compare_image_url": compare_image.compare_image_url,
                        "similar_percent": compare_image.similar_percent
                    }
                })
            # Mặt sau
            else:
                if identity_image.hand_side_id and identity_image.finger_type_id:
                    fingerprint = {
                        "image_url": identity_image.image_url,
                        "hand_side": dropdown(hand_side),
                        "finger_type": dropdown(finger_type)
                    }
                    if fingerprint not in fingerprint_list:
                        fingerprint_list.append(fingerprint)
                        backside_information.update({
                            "identity_image_url": identity_image.image_url,
                            "fingerprint": fingerprint_list,
                            "updated_at": identity_image.updater_at,
                            "updated_by": identity_image.updater_id
                        })

                backside_information.update({
                    "identity_image_url": identity_image.image_url,
                    "fingerprint": fingerprint_list,
                    "updated_at": identity_image.updater_at,
                    "updated_by": identity_image.updater_id
                })
        else:
            passport_information.update({
                "identity_image_url": identity_image.image_url
            })

        # Phân tích OCR -> Thông tin địa chỉ
        if customer_address.address_type_id == RESIDENT_ADDRESS_CODE:
            address_information['resident_address'].update({
                "province": dropdown(province),
                "district": dropdown(district),
                "ward": dropdown(ward),
                "number_and_street": customer_address.address
            })

        if customer_address.address_type_id == CONTACT_ADDRESS_CODE:
            address_information['contact_address'].update({
                "province": dropdown(province),
                "district": dropdown(district),
                "ward": dropdown(ward),
                "number_and_street": customer_address.address
            })

        if compare_image:
            passport_information.update({
                "face_compare_image_url": compare_image.compare_image_url,
                "similar_percent": compare_image.similar_percent
            })

        passport_information.update({
            "identity_image_url": identity_image.image_url,
            "fingerprint": fingerprint_list
        })

    identity_info.update({
        "identity_document": identity_document,
        "basic_information": basic_information,
        "address_information": address_information,
        "passport_information": passport_information
    })

    return identity_info
