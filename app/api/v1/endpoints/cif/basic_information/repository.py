from app.api.base.repository import ReposReturn
from app.utils.constant.cif import CIF_ID_TEST, RESIDENT_ADDRESS_CODE, CONTACT_ADDRESS_CODE, \
    IDENTITY_DOCUMENT_TYPE_PASSPORT
from app.utils.error_messages import ERROR_CIF_ID_NOT_EXIST
from app.utils.functions import dropdown

DETAIL_RELATIONSHIP_DATA = {
    "id": "1",
    "avatar_url": "https//example.com/example.jpg",
    "basic_information": {
        "cif_number": "1",
        "customer_relationship": {
            "id": "1",
            "code": "MOTHER",
            "name": "Mẹ"
        },
        "full_name_vn": "Nguyễn Anh Đào",
        "date_of_birth": "1990-08-12",
        "gender": {
            "id": "1",
            "code": "NU",
            "name": "Nữ"
        },
        "nationality": {
            "id": "1",
            "code": "VN",
            "name": "Việt Nam"
        },
        "telephone_number": "",
        "mobile_number": "0867589623",
        "email": "anhdao@gmail.com"
    },
    "identity_document": {
        "identity_number": "079190254791",
        "issued_date": "1990-12-08",
        "expired_date": "1990-12-08",
        "place_of_issue": {
            "id": "1",
            "code": "CAHCM",
            "name": "Công an TPHCM"
        }
    },
    "address_information": {
        "resident_address": {
            "number_and_street": "125 Võ Thị Sáu",
            "province": {
                "id": "1",
                "code": "HCM",
                "name": "Hồ Chí Minh"
            },
            "district": {
                "id": "3",
                "code": "Q3",
                "name": "Quận 3"
            },
            "ward": {
                "id": "8",
                "code": "P8",
                "name": "Phường 8"
            }
        },
        "contact_address": {
            "number_and_street": "120/6 Điện Biên Phủ",
            "province": {
                "id": "1",
                "code": "HCM",
                "name": "Hồ Chí Minh"
            },
            "district": {
                "id": "BT",
                "code": "BT",
                "name": "Quận Bình Thạnh"
            },
            "ward": {
                "id": "8",
                "code": "AP",
                "name": "Phường An Phước"
            }
        }
    }
}


async def repos_detail_relationship(cif_id: str, cif_number_need_to_find: str):
    if cif_id != CIF_ID_TEST:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc="cif_id")

    return ReposReturn(data=DETAIL_RELATIONSHIP_DATA)


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
