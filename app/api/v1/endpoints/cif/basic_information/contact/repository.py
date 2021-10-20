from app.api.base.repository import ReposReturn
from app.utils.constant.cif import CIF_ID_TEST
from app.utils.error_messages import ERROR_CIF_ID_NOT_EXIST
from app.utils.functions import now

DOMESTIC_CONTACT_INFORMATION_DETAIL = {
    "resident_address": {
        "domestic_flag": True,
        "domestic_address": {
            "country": {
                "id": "1",
                "code": "VN",
                "name": "Việt Nam"
            },
            "number_and_street": "96 Hùng Vương",
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
            }
        },
        "foreign_address": {
            "country": {
                "id": None,
                "code": None,
                "name": None
            },
            "address_1": None,
            "address_2": None,
            "province": {
                "id": None,
                "code": None,
                "name": None
            },
            "state": {
                "id": None,
                "code": None,
                "name": None
            },
            "zip_code": {
                "id": None,
                "code": None,
                "name": None
            }
        }
    },
    "contact_address": {
        "resident_address_flag": False,
        "country": {
            "id": "1",
            "code": "VN",
            "name": "Việt Nam"
        },
        "number_and_street": "927 Trần Hưng Đạo",
        "province": {
            "id": "1",
            "code": "HCM",
            "name": "Hồ Chí Minh"
        },
        "district": {
            "id": "5",
            "code": "Q5",
            "name": "Quận 5"
        },
        "ward": {
            "id": "1",
            "code": "P1",
            "name": "Phường 1"
        }
    },
    "career_information": {
        "career": {
            "id": "1",
            "code": "XD",
            "name": "Xây dựng"
        },
        "average_income_amount": {
            "id": "1",
            "code": "LT10",
            "name": ">10 triệu"
        },
        "company_name": "Công ty ABC",
        "company_phone": "0215469874",
        "company_position": {
            "id": "1",
            "code": "NV",
            "name": "Nhân viên"
        },
        "company_address": "Số 20, Hẻm 269, Lý Tự Trọng"
    }
}

FOREIGN_CONTACT_INFORMATION_DETAIL = {
    "resident_address": {
        "domestic_flag": False,
        "domestic_address": {
            "country": {
                "id": None,
                "code": None,
                "name": None
            },
            "number_and_street": None,
            "province": {
                "id": None,
                "code": None,
                "name": None
            },
            "district": {
                "id": None,
                "code": None,
                "name": None
            },
            "ward": {
                "id": None,
                "code": None,
                "name": None
            }
        },
        "foreign_address": {
            "country": {
                "id": "1",
                "code": "USA",
                "name": "The United States of America"
            },
            "address_1": "",
            "address_2": "",
            "province": {
                "id": "1",
                "code": "LA",
                "name": "Los Angeles"
            },
            "state": {
                "id": "1",
                "code": "CALI",
                "name": "California"
            },
            "zip_code": {
                "id": "1",
                "code": "90001",
                "name": "90001"
            }
        }
    },
    "contact_address": {
        "resident_address_flag": False,
        "country": {
            "id": "1",
            "code": "VN",
            "name": "Việt Nam"
        },
        "number_and_street": "927 Trần Hưng Đạo",
        "province": {
            "id": "1",
            "code": "HCM",
            "name": "Hồ Chí Minh"
        },
        "district": {
            "id": "5",
            "code": "Q5",
            "name": "Quận 5"
        },
        "ward": {
            "id": "1",
            "code": "P1",
            "name": "Phường 1"
        }
    },
    "career_information": {
        "career": {
            "id": "1",
            "code": "XD",
            "name": "Xây dựng"
        },
        "average_income_amount": {
            "id": "1",
            "code": "LT10",
            "name": ">10 triệu"
        },
        "company_name": "Công ty ABC",
        "company_phone": "0215469874",
        "company_position": {
            "id": "1",
            "code": "NV",
            "name": "Nhân viên"
        },
        "company_address": "Số 20, Hẻm 269, Lý Tự Trọng"
    }
}


async def repos_get_detail_contact_information(cif_id: str) -> ReposReturn:
    if cif_id != CIF_ID_TEST:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc='cif_id')

    return ReposReturn(data=DOMESTIC_CONTACT_INFORMATION_DETAIL)


async def repos_save_contact_information(
        cif_id: str,
        created_by
) -> ReposReturn:
    if cif_id != CIF_ID_TEST:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc='cif_id')

    return ReposReturn(data={
        "cif_id": cif_id,
        "created_at": now(),
        "created_by": created_by
    })
