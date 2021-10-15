import datetime
from typing import Union, Dict

from app.api.base.repository import ReposReturn
from app.utils.status.message import ERROR_IDENTITY_DOCUMENT_NOT_EXIST

IDENTITY_CARD_CIF_ID = "CMND123"
CITIZEN_CARD_CIF_ID = "CCCD123"
PASSPORT_CIF_ID = "PASSPORT123"
TYPE_IDENTITY_CARD = 0
TYPE_CITIZEN_CARD = 1
TYPE_PASSPORT = 2
IDENTITY_DOCUMENT_TYPES = [
    TYPE_IDENTITY_CARD,
    TYPE_CITIZEN_CARD,
    TYPE_PASSPORT
]
IDENTITY_CARD = "Chứng minh nhân dân"
CITIZEN_IDENTITY_CARD = "Căn cước công dân"
PASSPORT = "Hộ chiếu"
IDENTITY_DOCUMENT_TYPE = {
    TYPE_IDENTITY_CARD: IDENTITY_CARD,
    TYPE_CITIZEN_CARD: CITIZEN_IDENTITY_CARD,
    TYPE_PASSPORT: PASSPORT
}
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
                "id": "1",
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
            "issued_date": "18/02/2021",
            "place_of_issue": {
                "id": "1",
                "code": "CT",
                "name": "Cần Thơ"
            },
            "expired_date": ""
        },
        "basic_information": {
            "id": "1",
            "full_name_vn": "Lê Phương Thảo",
            "gender": {
                "id": "1",
                "code": "NU",
                "name": "Nữ"
            },
            "date_of_birth": "12/08/1990",
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
                "number_and_street": "54/12/25 Đường Long Thới"
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
                "number_and_street": "54/12/25 Đường Long Thới"
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
                "id": "1",
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
            "issued_date": "18/02/2021",
            "place_of_issue": {
                "id": "2",
                "code": "HCDS",
                "name": "Cục hành chính về trật tự xã hội"
            },
            "expired_date": "07/02/2021",
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
            "date_of_birth": "07/02/1994",
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
                "number_and_street": "54/12/25 Đường Long Thới"
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
                "number_and_street": "54/12/25 Đường Long Thới"
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
                "id": "1",
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
        ]
    },
    "ocr_result": {
        "identity_document": {
            "identity_number": "361963424",
            "issued_date": "18/02/2021",
            "place_of_issue": {
                "id": "1",
                "code": "CT",
                "name": "Cần Thơ"
            },
            "expired_date": "18/02/2021",
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
            "date_of_birth": "12/08/1990",
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


async def repos_get_detail_identity_document(cif_id: str) -> (bool, Union[str, Dict]):
    if cif_id == IDENTITY_CARD_CIF_ID:
        return ReposReturn(data=IDENTITY_CARD_INFO)
    elif cif_id == CITIZEN_CARD_CIF_ID:
        return ReposReturn(data=CITIZEN_CARD_INFO)
    elif cif_id == PASSPORT_CIF_ID:
        return ReposReturn(data=PASSPORT_INFO)
    else:
        return ReposReturn(is_error=True, msg=ERROR_IDENTITY_DOCUMENT_NOT_EXIST, loc='cif_id')


async def repos_save_identity_document(identity_card_document_req, created_by):
    identity_document_type_id = int(identity_card_document_req.identity_document_type.id)
    if identity_document_type_id in IDENTITY_DOCUMENT_TYPES:
        cif_id = identity_card_document_req.identity_document_type.code
        return ReposReturn(data={
            "cif_id": cif_id,
            "created_at": datetime.datetime.now(),
            "created_by": created_by
        })
    else:
        return ReposReturn(is_error=True, msg=ERROR_IDENTITY_DOCUMENT_NOT_EXIST, loc='cif_id')
