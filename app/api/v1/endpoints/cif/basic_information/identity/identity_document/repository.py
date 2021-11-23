from datetime import date
from typing import Union

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.api.v1.endpoints.cif.basic_information.identity.identity_document.schema_request import (
    CitizenCardSaveRequest, IdentityCardSaveRequest, PassportSaveRequest
)
from app.api.v1.endpoints.cif.repository import repos_update_basic_information_identity, \
    repos_create_basic_information_identity
from app.third_parties.oracle.models.cif.basic_information.model import Customer
from app.third_parties.oracle.models.master_data.address import AddressType
from app.utils.constant.cif import (
    CIF_ID_TEST, IDENTITY_DOCUMENT_TYPE, IDENTITY_DOCUMENT_TYPE_CITIZEN_CARD,
    IDENTITY_DOCUMENT_TYPE_IDENTITY_CARD, RESIDENT_ADDRESS_CODE, CONTACT_ADDRESS_CODE, UNCOMPLETED, ACTIVED
)
from app.utils.error_messages import (
    ERROR_CIF_ID_NOT_EXIST, ERROR_IDENTITY_DOCUMENT_NOT_EXIST
)
from app.utils.functions import now, calculate_age, raise_does_not_exist_string
from app.utils.vietnamese_converted import vietnamese_converted, split_name, make_short_name

IDENTITY_CARD_INFO = {
    "identity_document_type": {
        "id": "0",
        "code": "CMND",
        "name": "Chứng minh nhân dân"
    },
    "frontside_information": {
        "identity_image_url": "https://example.com/example.jpg",
        "face_compare_image_url": "https://example.com/example.jpg",
        "similar_percent": 94
    },
    "backside_information": {
        "identity_image_url": "https://example.com/example.jpg",
        "fingerprint": [
            {
                "image_url": "https://example.com/example.jpg",
                "hand_side": {
                    "id": "1",
                    "code": "TAYTRAI",
                    "name": "Tay trái"
                },
                "finger_type": {
                    "id": "1",
                    "code": "NGONTRO",
                    "name": "Ngón trỏ"
                }
            },
            {
                "image_url": "https://example.com/example.jpg",
                "hand_side": {
                    "id": "1",
                    "code": "TAYTRAI",
                    "name": "Tay trái"
                },
                "finger_type": {
                    "id": "1",
                    "code": "NGONTRO",
                    "name": "Ngón trỏ"
                }
            },
            {
                "image_url": "https://example.com/example.jpg",
                "hand_side": {
                    "id": "1",
                    "code": "TAYPHAI",
                    "name": "Tay phải"
                },
                "finger_type": {
                    "id": "1",
                    "code": "NGONTRO",
                    "name": "Ngón trỏ"
                }
            },
            {
                "image_url": "https://example.com/example.jpg",
                "hand_side": {
                    "id": "1",
                    "code": "TAYPHAI",
                    "name": "Tay phải"
                },
                "finger_type": {
                    "id": "1",
                    "code": "NGONTRO",
                    "name": "Ngón trỏ"
                }
            }
        ],
        "updated_at": "2021-09-15 15:23:45",
        "updated_by": "Nguyễn Anh Đào"
    },
    "ocr_result": {
        "identity_document": {
            "identity_number": "361963424",
            "issued_date": "2021-02-18",
            "place_of_issue": {
                "id": "1",
                "code": "CT",
                "name": "Cần Thơ"
            },
            "expired_date": "2021-02-18"
        },
        "basic_information": {
            "id": "1",
            "full_name_vn": "Lê Phương Thảo",
            "gender": {
                "id": "1",
                "code": "NU",
                "name": "Nữ"
            },
            "date_of_birth": "1990-08-12",
            "nationality": {
                "id": "1",
                "code": "VN",
                "name": "Việt Nam"
            },
            "province": {
                "id": "1",
                "code": "CT",
                "name": "Cần Thơ"
            },
            "ethnic": {
                "id": "1",
                "code": "KINH",
                "name": "Kinh"
            },
            "religion": {
                "id": "1",
                "code": "KHONG",
                "name": "Không"
            },
            "identity_characteristic": "",
            "father_full_name_vn": "Lê Tuấn Ngọc",
            "mother_full_name_vn": "Trần Phương Thảo"
        },
        "address_information": {
            "resident_address": {
                "province": {
                    "id": "1",
                    "code": "CT",
                    "name": "Cần Thơ"
                },
                "district": {
                    "id": "1",
                    "code": "PH",
                    "name": "Phụng Hiệp"
                },
                "ward": {
                    "id": "1",
                    "code": "TL",
                    "name": "Tân Long"
                },
                "number_and_street": "25 Đường Long Thới-12-54"
            },
            "contact_address": {
                "province": {
                    "id": "1",
                    "code": "CT",
                    "name": "Cần Thơ"
                },
                "district": {
                    "id": "1",
                    "code": "PH",
                    "name": "Phụng Hiệp"
                },
                "ward": {
                    "id": "1",
                    "code": "TL",
                    "name": "Tân Long"
                },
                "number_and_street": "25 Đường Long Thới-12-54"
            }
        }
    }
}
CITIZEN_CARD_INFO = {
    "identity_document_type": {
        "id": "1",
        "code": "CCCD",
        "name": "Căn cước công dân"
    },
    "frontside_information": {
        "identity_image_url": "https://example.com/example.jpg",
        "face_compare_image_url": "https://example.com/example.jpg",
        "similar_percent": 94
    },
    "backside_information": {
        "identity_image_url": "https://example.com/example.jpg",
        "fingerprint": [
            {
                "image_url": "https://example.com/example.jpg",
                "hand_side": {
                    "id": "1",
                    "code": "TAYTRAI",
                    "name": "Tay trái"
                },
                "finger_type": {
                    "id": "1",
                    "code": "NGONTRO",
                    "name": "Ngón trỏ"
                }
            },
            {
                "id": "2",
                "image_url": "https://example.com/example.jpg",
                "hand_side": {
                    "id": "1",
                    "code": "TAYTRAI",
                    "name": "Tay trái"
                },
                "finger_type": {
                    "id": "1",
                    "code": "NGONTRO",
                    "name": "Ngón trỏ"
                }
            },
            {
                "id": "3",
                "image_url": "https://example.com/example.jpg",
                "hand_side": {
                    "id": "1",
                    "code": "TAYPHAI",
                    "name": "Tay phải"
                },
                "finger_type": {
                    "id": "1",
                    "code": "NGONTRO",
                    "name": "Ngón trỏ"
                }
            },
            {
                "id": "4",
                "image_url": "https://example.com/example.jpg",
                "hand_side": {
                    "id": "1",
                    "code": "TAYPHAI",
                    "name": "Tay phải"
                },
                "finger_type": {
                    "id": "1",
                    "code": "NGONTRO",
                    "name": "Ngón trỏ"
                }
            }
        ],
        "updated_at": "2021-09-15 15:23:45",
        "updated_by": "Nguyễn Anh Đào"
    },
    "ocr_result": {
        "identity_document": {
            "identity_number": "361963424",
            "issued_date": "2021-02-18",
            "place_of_issue": {
                "id": "2",
                "code": "HCDS",
                "name": "Cục hành chính về trật tự xã hội"
            },
            "expired_date": "2021-02-07",
            "mrz_content": "IDVNM~079195236~8~079197258639~<< "
                           "122909199~X~Nu~23092031~X~VNM<<<<<<<<<<<~4Tran~<<~Minh~<~Huyen~<<<….",
            "qr_code_content": "079087007923||Nguyễn Thái Anh |27061987|Nam|236/11 Lê Thị Hồng, Phường 17, Gò Vấp, "
                               "TPHCM | 21022021 "
        },
        "basic_information": {
            "id": "1",
            "full_name_vn": "Nguyễn Phạm Thông",
            "gender": {
                "id": "2",
                "code": "NAM",
                "name": "Nam"
            },
            "date_of_birth": "1994-02-07",
            "nationality": {
                "id": "1",
                "code": "VN",
                "name": "Việt Nam"
            },
            "province": {
                "id": "2",
                "code": "HN",
                "name": "Hà Nội"
            },
            "identity_characteristic": "Sẹo chấm cách 2.5 so với trán"
        },
        "address_information": {
            "resident_address": {
                "province": {
                    "id": "1",
                    "code": "CT",
                    "name": "Cần Thơ"
                },
                "district": {
                    "id": "1",
                    "code": "PH",
                    "name": "Phụng Hiệp"
                },
                "ward": {
                    "id": "1",
                    "code": "TL",
                    "name": "Tân Long"
                },
                "number_and_street": "25 Đường Long Thới-12-54"
            },
            "contact_address": {
                "province": {
                    "id": "1",
                    "code": "CT",
                    "name": "Cần Thơ"
                },
                "district": {
                    "id": "1",
                    "code": "PH",
                    "name": "Phụng Hiệp"
                },
                "ward": {
                    "id": "1",
                    "code": "TL",
                    "name": "Tân Long"
                },
                "number_and_street": "25 Đường Long Thới-12-54"
            }
        }
    }
}
PASSPORT_INFO = {
    "identity_document_type": {
        "id": "2",
        "code": "HC",
        "name": "Hộ chiếu"
    },
    "passport_information": {
        "identity_image_url": "https://example.com/example.jpg",
        "face_compare_image_url": "https://example.com/example.jpg",
        "similar_percent": 94,
        "fingerprint": [
            {
                "image_url": "https://example.com/example.jpg",
                "hand_side": {
                    "id": "1",
                    "code": "TAYTRAI",
                    "name": "Tay trái"
                },
                "finger_type": {
                    "id": "1",
                    "code": "NGONTRO",
                    "name": "Ngón trỏ"
                }
            },
            {
                "image_url": "https://example.com/example.jpg",
                "hand_side": {
                    "id": "1",
                    "code": "TAYTRAI",
                    "name": "Tay trái"
                },
                "finger_type": {
                    "id": "1",
                    "code": "NGONTRO",
                    "name": "Ngón trỏ"
                }
            },
            {
                "image_url": "https://example.com/example.jpg",
                "hand_side": {
                    "id": "1",
                    "code": "TAYPHAI",
                    "name": "Tay phải"
                },
                "finger_type": {
                    "id": "1",
                    "code": "NGONTRO",
                    "name": "Ngón trỏ"
                }
            },
            {
                "image_url": "https://example.com/example.jpg",
                "hand_side": {
                    "id": "1",
                    "code": "TAYPHAI",
                    "name": "Tay phải"
                },
                "finger_type": {
                    "id": "1",
                    "code": "NGONTRO",
                    "name": "Ngón trỏ"
                }
            }
        ]
    },
    "ocr_result": {
        "identity_document": {
            "identity_number": "361963424",
            "issued_date": "2021-02-18",
            "place_of_issue": {
                "id": "1",
                "code": "CT",
                "name": "Cần Thơ"
            },
            "expired_date": "2021-02-18",
            "passport_type": {
                "id": "1",
                "code": "P",
                "name": "P"
            },
            "passport_code": {
                "id": "1",
                "code": "VNM",
                "name": "VNM"
            }
        },
        "basic_information": {
            "full_name_vn": "Lê Phương Thảo",
            "gender": {
                "id": "1",
                "code": "NU",
                "name": "Nữ"
            },
            "date_of_birth": "1990-08-12",
            "nationality": {
                "id": "1",
                "code": "VN",
                "name": "Việt Nam"
            },
            "place_of_birth": {
                "id": "1",
                "code": "CT",
                "name": "Cần Thơ"
            },
            "identity_card_number": "123214512321",
            "mrz_content": "P<VNM~Tran<<Minh<Huyen<<<<<...SoHC~<~X~VNM~29081999~X~Nu~ 29082029~X~079197005852~<~X"
        }
    }
}
IDENTITY_LOGS_INFO = [
    {
        "reference_flag": True,
        "created_date": "2021-02-18",
        "identity_document_type": {
            "id": "1",
            "code": "CMND",
            "name": "Chứng minh nhân dân"
        },
        "identity_images": [
            {
                "image_url": "https://example.com/example.jpg"
            },
            {
                "image_url": "https://example.com/example.jpg"
            }
        ]
    },
    {
        "reference_flag": False,
        "created_date": "2021-02-18",
        "identity_document_type": {
            "id": "2",
            "code": "CCCD",
            "name": "Căn cước công dân"
        },
        "identity_images": [
            {
                "image_url": "https://example.com/example.jpg"
            },
            {
                "image_url": "https://example.com/example.jpg"
            }
        ]
    },
    {
        "reference_flag": False,
        "created_date": "2021-02-18",
        "identity_document_type": {
            "id": "3",
            "code": "HC",
            "name": "Hộ chiếu"
        },
        "identity_images": [
            {
                "image_url": "https://example.com/example.jpg"
            }
        ]
    }
]


async def repos_get_detail(cif_id: str, identity_document_type_id: str) -> ReposReturn:
    if cif_id != CIF_ID_TEST:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc='cif_id')

    if identity_document_type_id not in IDENTITY_DOCUMENT_TYPE:
        return ReposReturn(is_error=True, msg=ERROR_IDENTITY_DOCUMENT_NOT_EXIST, loc='identity_document_type_id')

    if identity_document_type_id == IDENTITY_DOCUMENT_TYPE_IDENTITY_CARD:
        return ReposReturn(data=IDENTITY_CARD_INFO)
    elif identity_document_type_id == IDENTITY_DOCUMENT_TYPE_CITIZEN_CARD:
        return ReposReturn(data=CITIZEN_CARD_INFO)
    else:
        return ReposReturn(data=PASSPORT_INFO)


async def repos_get_list_log(cif_id: str) -> ReposReturn:
    if cif_id != CIF_ID_TEST:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc='cif_id')

    return ReposReturn(data=IDENTITY_LOGS_INFO)


async def repos_save_identity(
        identity_document_req: Union[IdentityCardSaveRequest, CitizenCardSaveRequest, PassportSaveRequest],
        save_by: str,
        session: Session
):
    cif_number = identity_document_req.cif_id
    identity_document_type_id = identity_document_req.identity_document_type.id
    frontside_information_identity_image_url = identity_document_req.frontside_information.identity_image_url
    frontside_information_compare_image_url = identity_document_req.frontside_information.face_compare_image_url
    backside_information_identity_image_url = identity_document_req.frontside_information.face_compare_image_url
    # RULE: identity_number
    identity_number = identity_document_req.ocr_result.identity_document.identity_number
    issued_date = identity_document_req.ocr_result.identity_document.issued_date
    expired_date = identity_document_req.ocr_result.identity_document.expired_date
    full_name_vn = identity_document_req.ocr_result.basic_information.full_name_vn
    full_name = vietnamese_converted(full_name_vn)
    first_name, middle_name, last_name = split_name(full_name)
    date_of_birth = identity_document_req.ocr_result.basic_information.date_of_birth
    identity_characteristic = identity_document_req.ocr_result.basic_information.identity_characteristic
    father_full_name_vn = identity_document_req.ocr_result.basic_information.father_full_name_vn
    mother_full_name_vn = identity_document_req.ocr_result.basic_information.mother_full_name_vn
    contact_address_number_and_street = identity_document_req.ocr_result.address_information.contact_address.number_and_street
    resident_address_number_and_street = identity_document_req.ocr_result.address_information.resident_address.number_and_street

    place_of_issue_id = identity_document_req.ocr_result.identity_document.place_of_issue.id
    gender_id = identity_document_req.ocr_result.basic_information.gender.id
    nationality_id = identity_document_req.ocr_result.basic_information.nationality.id
    province_id = identity_document_req.ocr_result.basic_information.province.id
    ethnic_id = identity_document_req.ocr_result.basic_information.ethnic.id
    religion_id = identity_document_req.ocr_result.basic_information.religion.id
    resident_address_province_id = identity_document_req.ocr_result.address_information.resident_address.province.id
    resident_address_district_id = identity_document_req.ocr_result.address_information.resident_address.district.id
    resident_address_ward_id = identity_document_req.ocr_result.address_information.resident_address.ward.id
    contact_address_province_id = identity_document_req.ocr_result.address_information.contact_address.province.id
    contact_address_district_id = identity_document_req.ocr_result.address_information.contact_address.district.id
    contact_address_ward_id = identity_document_req.ocr_result.address_information.contact_address.ward.id

    saving_customer = {
        "full_name": full_name,
        "full_name_vn": full_name_vn,
        "first_name": first_name,
        "middle_name": middle_name,
        "last_name": last_name,
        "short_name": make_short_name(full_name),
        "active_flag": ACTIVED,
        "open_cif_at": now(),
        "open_branch_id": "000",  # TODO
        "kyc_level_id": "KYC_1",  # TODO

        "customer_category_id": "D0682B44BEB3830EE0530100007F1DDC",  # TODO
        "customer_economic_profession_id": "D0682B44BE6D830EE0530100007F1DDC",  # TODO
        "nationality_id": nationality_id,
        "customer_classification_id": "1",  # TODO
        "customer_status_id": "1",  # TODO
        "channel_id": "1",  # TODO
        "avatar_url": None,
        "complete_flag": UNCOMPLETED
    }

    customer_identity = {
        "identity_type_id": identity_document_type_id,
        "identity_num": identity_number,
        "issued_date": issued_date,
        "expired_date": expired_date,
        "place_of_issue_id": place_of_issue_id,
        "maker_at": now(),
        "maker_id": save_by,
        "updater_at": now(),
        "updater_id": save_by
    }
    under_15_year_old_flag = True if calculate_age(date.today(), date_of_birth) < 15 else False
    customer_individual_info = {
        "gender_id": gender_id,
        "place_of_birth_id": province_id,
        "country_of_birth_id": nationality_id,
        "religion_id": religion_id,
        "nation_id": ethnic_id,
        "date_of_birth": date_of_birth,
        "under_15_year_old_flag": under_15_year_old_flag,
        "identifying_characteristics": identity_characteristic,
        "father_full_name": father_full_name_vn,
        "mother_full_name": mother_full_name_vn
    }
    
    resident_address = session.execute(
        select(AddressType).filter(AddressType.code == RESIDENT_ADDRESS_CODE)
    ).scalars().first()
    if not resident_address:
        return ReposReturn(is_error=True, msg=raise_does_not_exist_string("Resident Address"), loc="resident_address")
    customer_resident_address = {
        "address_type_id": resident_address.id,
        "address_country_id": nationality_id,
        "address_province_id": resident_address_province_id,
        "address_district_id": resident_address_district_id,
        "address_ward_id": resident_address_ward_id,
        "address": resident_address_number_and_street
    }
    
    contact_address = session.execute(
        select(AddressType).filter(AddressType.code == CONTACT_ADDRESS_CODE)
    ).scalars().first()
    if not contact_address:
        return ReposReturn(is_error=True, msg=raise_does_not_exist_string("Contact Address"), loc="contact_address")
    customer_contact_address = {
        "address_type_id": contact_address.id,
        "address_country_id": nationality_id,
        "address_province_id": contact_address_province_id,
        "address_district_id": contact_address_district_id,
        "address_ward_id": contact_address_ward_id,
        "address": contact_address_number_and_street
    }

    # Kiểm tra cif có tồn tại hay không, có thì cập nhật không là tạo mới
    customer = session.execute(
        select(Customer).filter(Customer.cif_number == cif_number)
    ).scalars().first()

    # Update
    if customer:
        # Cập nhật 1 cif_number đã tồn tại
        customer_id = await repos_update_basic_information_identity(
            customer,
            customer_identity,
            customer_individual_info,
            customer_resident_address,
            customer_contact_address,
            saving_customer,
            session
        )

    # Create
    else:
        customer_id = await  repos_create_basic_information_identity(
            cif_number,
            saving_customer,
            customer_individual_info,
            customer_resident_address,
            customer_contact_address,
            customer_identity,
            frontside_information_identity_image_url,
            frontside_information_compare_image_url,
            backside_information_identity_image_url,
            save_by,
            session
        )

    return ReposReturn(data={
        "cif_id": customer_id
    })
