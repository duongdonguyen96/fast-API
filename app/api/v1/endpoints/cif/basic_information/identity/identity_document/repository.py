from typing import Union

from sqlalchemy import select, and_, desc
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.api.v1.endpoints.cif.basic_information.identity.identity_document.schema_request import (
    CitizenCardSaveRequest, IdentityCardSaveRequest, PassportSaveRequest
)
from app.third_parties.oracle.models.cif.basic_information.contact.model import CustomerAddress
from app.third_parties.oracle.models.cif.basic_information.identity.model import CustomerIdentity, \
    CustomerIdentityImage, CustomerCompareImage
from app.third_parties.oracle.models.cif.basic_information.model import Customer
from app.third_parties.oracle.models.cif.basic_information.personal.model import CustomerIndividualInfo
from app.third_parties.oracle.models.master_data.address import AddressProvince, AddressCountry, AddressType, \
    AddressDistrict, AddressWard
from app.third_parties.oracle.models.master_data.customer import CustomerGender
from app.third_parties.oracle.models.master_data.identity import CustomerIdentityType, PlaceOfIssue, HandSide, \
    FingerType
from app.third_parties.oracle.models.master_data.others import Currency, Nation, Religion
from app.utils.constant.cif import (
    CIF_ID_TEST, IDENTITY_DOCUMENT_TYPE, IDENTITY_DOCUMENT_TYPE_CITIZEN_CARD,
    IDENTITY_DOCUMENT_TYPE_IDENTITY_CARD, RESIDENT_ADDRESS_CODE, CONTACT_ADDRESS_CODE, IDENTITY_FRONT_SIDE,
    IDENTITY_BACK_SIDE
)
from app.utils.error_messages import (
    ERROR_CIF_ID_NOT_EXIST, ERROR_IDENTITY_DOCUMENT_NOT_EXIST
)
from app.utils.functions import now

identity_info = {
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
        "fingerprint": [],
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


async def repos_get_detail(cif_id: str, identity_document_type_id: str, oracle_session: Session, current_user) -> ReposReturn:
    try:
        customer_identity_type, _ = oracle_session.execute(
            select(
                CustomerIdentityType,
                CustomerIdentity
            )
            .join(CustomerIdentity, CustomerIdentityType.id == CustomerIdentity.identity_type_id)
            .filter(CustomerIdentity.customer_id == cif_id, CustomerIdentityType.id == identity_document_type_id)
        ).one()
    except Exception as ex:
        return ReposReturn(is_error=True, msg=str(ex), loc='identity_document_type_id, cif_id')

    # Thông tin mặt trước
    try:
        _, customer_identity_image, customer_compare_image = oracle_session.execute(
            select(
                CustomerIdentity,
                CustomerIdentityImage,
                CustomerCompareImage
            )
            .join(CustomerIdentityImage, CustomerIdentityImage.identity_id == CustomerIdentity.id)
            .join(CustomerCompareImage, CustomerCompareImage.identity_id == CustomerIdentity.id, isouter=True)
            .order_by(desc(CustomerIdentity.updater_at))
            .filter(
                CustomerIdentity.customer_id == cif_id,
                CustomerIdentityType.id == identity_document_type_id,
                CustomerIdentityImage.identity_image_front_flag == IDENTITY_FRONT_SIDE
            )
        ).first()
        identity_info["frontside_information"] = {
            "identity_image_url": customer_identity_image.image_url,
            "face_compare_image_url": customer_compare_image.compare_image_url,
            "similar_percent": customer_compare_image.similar_percent
        }
    except Exception as ex:
        return ReposReturn(is_error=True, msg=str(ex), loc='front_side_information')

    # Thông tin mặt sau
    try:
        identity_backside_informations = oracle_session.execute(
            select(
                CustomerIdentity,
                CustomerIdentityImage,
                HandSide,
                FingerType
            )
            .join(CustomerIdentityImage, CustomerIdentityImage.identity_id == CustomerIdentity.id)
            .join(HandSide, CustomerIdentityImage.hand_side_id == HandSide.id)
            .join(FingerType, CustomerIdentityImage.finger_type_id == FingerType.id)
            .filter(
                CustomerIdentity.customer_id == cif_id,
                CustomerIdentity.identity_type_id == identity_document_type_id,
                CustomerIdentityImage.identity_image_front_flag == IDENTITY_BACK_SIDE
            )
        ).all()

    except Exception as ex:
        return ReposReturn(is_error=True, msg=str(ex), loc='back_side_information')

    for _, customer_identity_image, hand_side, finger_type in identity_backside_informations:
        if customer_identity_image.hand_side_id is None and customer_identity_image.finger_type_id is None:
            identity_info['backside_information']['identity_image_url'] = customer_identity_image.image_url
        else:
            identity_info['backside_information']['fingerprint'].append({
                "image_url": customer_identity_image.image_url,
                "hand_side": {
                    "id": hand_side.id,
                    "code": hand_side.code,
                    "name": hand_side.name
                },
                "finger_type": {
                    "id": finger_type.id,
                    "code": finger_type.code,
                    "name": finger_type.name,
                }
            })
    identity_info['backside_information']['updated_at'] = now()
    identity_info['backside_information']['updated_by'] = current_user.full_name_vn

    # Phân tích OCR -> Giấy tờ định danh
    try:
        ocr_customer_identity, ocr_place_of_issue = oracle_session.execute(
            select(
                CustomerIdentity,
                PlaceOfIssue
            )
            .join(PlaceOfIssue, PlaceOfIssue.id == CustomerIdentity.place_of_issue_id)
            .filter(CustomerIdentity.customer_id == cif_id)
        ).first()

    except Exception as ex:
        return ReposReturn(is_error=True, msg=str(ex), loc='ocr_result -> identity_document')


    # Phân tích OCR -> Thông tin cơ bản
    try:
        ocr_basic_info_customer, ocr_basic_info_customer_individual_info, ocr_basic_info_customer_gender, ocr_basic_info_customer_country, ocr_basic_info_customer_province, ocr_basic_info_customer_religion, ocr_basic_info_customer_nation = oracle_session.execute(
            select(
                Customer,
                CustomerIndividualInfo,
                CustomerGender,
                AddressCountry,
                AddressProvince,
                Religion,
                Nation
            )
            .join(CustomerIndividualInfo, Customer.id == CustomerIndividualInfo.customer_id)
            .filter(Customer.id == cif_id)
        ).first()
    except Exception as ex:
        return ReposReturn(is_error=True, msg=str(ex), loc='ocr_result -> basic_information')

    # Phân tích OCR -> Địa chi thường trú
    try:
        customer_resident_address, customer_resident_address_province, \
        customer_resident_address_district, customer_resident_address_ward, _ = oracle_session.execute(
            select(
                CustomerAddress,
                AddressProvince,
                AddressDistrict,
                AddressWard,
                AddressType
            )
            .join(AddressProvince, AddressProvince.id == CustomerAddress.address_province_id)
            .join(AddressDistrict, AddressDistrict.id == CustomerAddress.address_district_id)
            .join(AddressWard, AddressWard.id == CustomerAddress.address_ward_id)
            .join(AddressType, and_(
                AddressType.id == CustomerAddress.address_type_id, AddressType.code == RESIDENT_ADDRESS_CODE
            ))
            .filter(CustomerAddress.customer_id == cif_id)
        ).one()
    except Exception as ex:
        return ReposReturn(is_error=True, msg=str(ex), loc='ocr_result -> resident_address')

    # Phân tích OCR -> Địa chỉ liên lạc
    try:
        customer_contact_address, customer_contact_address_province, \
        customer_contact_address_district, customer_contact_address_ward, _ = oracle_session.execute(
            select(
                CustomerAddress,
                AddressProvince,
                AddressDistrict,
                AddressWard,
                AddressType
            )
            .join(AddressProvince, AddressProvince.id == CustomerAddress.address_province_id)
            .join(AddressDistrict, AddressDistrict.id == CustomerAddress.address_district_id)
            .join(AddressWard, AddressWard.id == CustomerAddress.address_ward_id)
            .join(AddressType, and_(
                AddressType.id == CustomerAddress.address_type_id,
                AddressType.code == CONTACT_ADDRESS_CODE
            ))
            .filter(CustomerAddress.customer_id == cif_id)
        ).one()
    except Exception as ex:
        return ReposReturn(is_error=True, msg=str(ex), loc='ocr_result -> contact_address')

    if identity_document_type_id not in IDENTITY_DOCUMENT_TYPE:
        return ReposReturn(is_error=True, msg=ERROR_IDENTITY_DOCUMENT_NOT_EXIST, loc='identity_document_type_id')

    if identity_document_type_id == IDENTITY_DOCUMENT_TYPE_IDENTITY_CARD:
        identity_info['identity_document_type'] = {
            "id": customer_identity_type.id,
            "code": customer_identity_type.code,
            "name": customer_identity_type.name
        }

        identity_info['ocr_result'] = {
            "identity_document": {
                "identity_number": ocr_customer_identity.identity_num,
                "issued_date": ocr_customer_identity.issued_date,
                "place_of_issue": {
                    "id": ocr_place_of_issue.id,
                    "code": ocr_place_of_issue.code,
                    "name": ocr_place_of_issue.name
                },
                "expired_date": ocr_customer_identity.expired_date
            },
            "basic_information": {
                "full_name_vn": ocr_basic_info_customer.full_name_vn,
                "gender": {
                    "id": ocr_basic_info_customer_gender.id,
                    "code": ocr_basic_info_customer_gender.code,
                    "name": ocr_basic_info_customer_gender.name
                },
                "date_of_birth": ocr_basic_info_customer_individual_info.date_of_birth,
                "nationality": {
                    "id": ocr_basic_info_customer_country.id,
                    "code": ocr_basic_info_customer_country.code,
                    "name": ocr_basic_info_customer_country.name,
                },
                "province": {
                    "id": ocr_basic_info_customer_province.id,
                    "code": ocr_basic_info_customer_province.code,
                    "name": ocr_basic_info_customer_province.name,
                },
                "ethnic": {
                    "id": ocr_basic_info_customer_nation.id,
                    "code": ocr_basic_info_customer_nation.code,
                    "name": ocr_basic_info_customer_nation.name
                },
                "religion": {
                    "id": ocr_basic_info_customer_religion.id,
                    "code": ocr_basic_info_customer_religion.code,
                    "name": ocr_basic_info_customer_religion.name
                },
                "identity_characteristic": ocr_basic_info_customer_individual_info.identifying_characteristics,
                "father_full_name_vn": ocr_basic_info_customer_individual_info.father_full_name,
                "mother_full_name_vn": ocr_basic_info_customer_individual_info.mother_full_name
            },
            "address_information": {
                "resident_address": {
                    "province": {
                        "id": customer_resident_address_province.id,
                        "code": customer_resident_address_province.code,
                        "name": customer_resident_address_province.name
                    },
                    "district": {
                        "id": customer_resident_address_district.id,
                        "code": customer_resident_address_district.code,
                        "name": customer_resident_address_district.name
                    },
                    "ward": {
                        "id": customer_resident_address_ward.id,
                        "code": customer_resident_address_ward.code,
                        "name": customer_resident_address_ward.name
                    },
                    "number_and_street": customer_resident_address.address
                },
                "contact_address": {
                    "province": {
                        "id": customer_contact_address_province.id,
                        "code": customer_contact_address_province.code,
                        "name": customer_contact_address_province.name
                    },
                    "district": {
                        "id": customer_contact_address_district.id,
                        "code": customer_contact_address_district.code,
                        "name": customer_contact_address_district.name
                    },
                    "ward": {
                        "id": customer_contact_address_ward.id,
                        "code": customer_contact_address_ward.code,
                        "name": customer_contact_address_ward.name
                    },
                    "number_and_street": customer_contact_address.address
                }
            }
        }
        return ReposReturn(data=identity_info)
    elif identity_document_type_id == IDENTITY_DOCUMENT_TYPE_CITIZEN_CARD:
        return ReposReturn(data=CITIZEN_CARD_INFO)
    else:
        return ReposReturn(data=PASSPORT_INFO)


async def repos_get_list_log(cif_id: str) -> ReposReturn:
    if cif_id != CIF_ID_TEST:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc='cif_id')

    return ReposReturn(data=IDENTITY_LOGS_INFO)


async def repos_save(
        identity_document_req: Union[IdentityCardSaveRequest, CitizenCardSaveRequest, PassportSaveRequest],
        created_by: str
):
    identity_document_type_id = identity_document_req.identity_document_type.id
    if identity_document_type_id not in IDENTITY_DOCUMENT_TYPE:
        return ReposReturn(is_error=True, msg=ERROR_IDENTITY_DOCUMENT_NOT_EXIST, loc='identity_document_type -> id')

    return ReposReturn(data={
        "cif_id": identity_document_req.cif_id,
        "created_at": now(),
        "created_by": created_by
    })
