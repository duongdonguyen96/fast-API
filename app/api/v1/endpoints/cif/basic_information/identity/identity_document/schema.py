from datetime import datetime
from typing import List

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.schemas.cif import FingerPrintResponse, FingerPrintRequest
from app.api.v1.schemas.utils import DropdownResponse, DropdownRequest


########################################################################################################################
# Thông tin dùng chung
########################################################################################################################
# I. Thông tin mặt trước CMND, CCCD
class FrontSideInformationResponse(BaseSchema):
    identity_image_url: str = Field(..., description="URL hình ảnh mặt trước CMND/CCCD")
    face_compare_image_url: str = Field(..., description="Hình ảnh chụp khuôn mặt")
    similar_percent: int = Field(..., description="Tỉ lệ so khớp với Hình ảnh chụp khuôn mặt")


# II. Thông tin mặt sau CMND, CCCD
class BackSideInformationResponse(BaseSchema):
    identity_image_url: str = Field(..., description="URL hình ảnh mặt sau CMND/CCCD")
    fingerprint: List[FingerPrintResponse] = Field(..., description="Vân tay")
    updated_at: str = Field(..., description="Thời gian cập nhật")
    updated_by: str = Field(..., description="Người cập nhật")


# III. Phân tích OCR -> 3. Thông tin địa chỉ -> Nơi thường trú/ Địa chỉ liên hệ (CMND)
class AddressResponse(BaseSchema):
    province: DropdownResponse = Field(..., description="Tỉnh/Thành phố")
    district: DropdownResponse = Field(..., description="Quận/Huyện")
    ward: DropdownResponse = Field(..., description="Phường/Xã")
    number_and_street: str = Field(..., description="Số nhà, tên đường")


# III. Phân tích OCR -> 3. Thông tin địa chỉ
class AddressInformationResponse(BaseSchema):
    resident_address: AddressResponse = Field(..., description="Nơi thường trú")
    contact_address: AddressResponse = Field(..., description="Địa chỉ liên hệ")


########################################################################################################################
# Giấy tờ định danh - CMND
########################################################################################################################
# III. Phân tích OCR -> 1. Giấy tờ định danh (CMND)
class IdentityCardDocumentResponse(BaseSchema):
    identity_number: str = Field(..., description="Số GTĐD")
    issued_date: str = Field(..., description="Ngày cấp")
    place_of_issue: DropdownResponse = Field(..., description="Nơi cấp")
    expired_date: str = Field(..., description="Có giá trị đến")


# III. Phân tích OCR -> 2. Thông tin cơ bản (CMND)
class IdentityBasicInformationResponse(BaseSchema):
    full_name_vn: str = Field(..., description="Họ và tên")
    gender: DropdownResponse = Field(..., description="Giới tính")
    date_of_birth: str = Field(..., description="Ngày sinh")
    nationality: DropdownResponse = Field(..., description="Quốc tịch")
    province: DropdownResponse = Field(..., description="Quê quán")
    ethnic: DropdownResponse = Field(None, description="Dân tộc")  # CMND
    religion: DropdownResponse = Field(None, description="Tôn giáo")  # CMND
    identity_characteristic: str = Field(None, description="Đặc điểm nhận dạng")  # CMND
    father_full_name_vn: str = Field(None, description="Họ tên cha")  # CMND
    mother_full_name_vn: str = Field(None, description="Họ tên mẹ")  # CMND


# III. Phân tích OCR (CMND)
class IdentityCardOCRResultResponse(BaseSchema):
    identity_document: IdentityCardDocumentResponse = Field(..., description="Giấy tờ định danh")
    basic_information: IdentityBasicInformationResponse = Field(..., description="Thông tin cơ bản")
    address_information: AddressInformationResponse = Field(..., description="Thông tin địa chỉ")


########################################################################################################################
# Giấy tờ định danh - CCCD
########################################################################################################################
# III. Phân tích OCR -> 1. Giấy tờ định danh
class CitizenCardResponse(BaseSchema):
    identity_number: str = Field(..., description="Số GTĐD")
    issued_date: str = Field(..., description="Ngày cấp")
    expired_date: str = Field(..., description="Có giá trị đến")
    place_of_issue: DropdownResponse = Field(..., description="Nơi cấp")
    mrz_content: str = Field(None, description="MRZ")  # CCCD
    qr_code_content: str = Field(None, description="Nội dung QR Code")  # CCCD


# III. Phân tích OCR -> 2. Thông tin cơ bản
class CitizenBasicInformationResponse(BaseSchema):
    full_name_vn: str = Field(..., description="Họ và tên")
    gender: DropdownResponse = Field(..., description="Giới tính")
    date_of_birth: str = Field(..., description="Ngày sinh")
    nationality: DropdownResponse = Field(..., description="Quốc tịch")
    province: DropdownResponse = Field(..., description="Quê quán")
    identity_characteristic: str = Field(..., description="Đặc điểm nhận dạng")


# III. Phân tích OCR -> 3. Thông tin địa chỉ
class CitizenOCRResultResponse(BaseSchema):
    identity_document: CitizenCardResponse = Field(..., description="Giấy tờ định danh")
    basic_information: CitizenBasicInformationResponse = Field(..., description="Thông tin cơ bản")
    address_information: AddressInformationResponse = Field(..., description="Thông tin địa chỉ")


class CitizenCardCreateSuccessResponse(BaseSchema):
    cif_id: str = Field(..., description="ID định danh CIF")
    created_at: datetime = Field(..., description="Thời gian tạo")
    created_by: str = Field(..., description="Người tạo")


########################################################################################################################
# Giấy tờ định danh - Hộ chiếu
########################################################################################################################
# I. Thông tin Hộ chiếu
class PassportInformationResponse(BaseSchema):
    identity_image_url: str = Field(..., description="URL hình ảnh Hộ chiếu")
    face_compare_image_url: str = Field(..., description="Hình ảnh chụp khuôn mặt")
    similar_percent: int = Field(..., description="Tỉ lệ so khớp với Hình ảnh chụp khuôn mặt")
    fingerprint: List[FingerPrintResponse] = Field(..., description="Danh sách các vân tay đối chiếu")


# II. Phân tích OCR -> 1. Giấy tờ định danh (Hộ Chiếu)
class PassportDocumentResponse(BaseSchema):
    identity_number: str = Field(..., description="Số GTĐD")
    issued_date: str = Field(..., description="Ngày cấp")
    place_of_issue: DropdownResponse = Field(..., description="Nơi cấp")
    expired_date: str = Field(..., description="Có giá trị đến")
    passport_type: DropdownResponse = Field(..., description="Loại")
    passport_code: DropdownResponse = Field(..., description="Mã số")


# II. Phân tích OCR -> 2. Thông tin cơ bản (Hộ Chiếu)
class PassportBasicInformationResponse(BaseSchema):
    full_name_vn: str = Field(..., description="Họ và tên")
    gender: DropdownResponse = Field(..., description="Giới tính")
    date_of_birth: str = Field(..., description="Ngày sinh")
    nationality: DropdownResponse = Field(..., description="Quốc tịch")
    place_of_birth: DropdownResponse = Field(..., description="Nơi sinh")
    identity_card_number: str = Field(..., description="Số CMND")
    mrz_content: str = Field(None, description="Mã MRZ")


# II. Phân tích OCR (HC)
class PassportOCRResultResponse(BaseSchema):
    identity_document: PassportDocumentResponse = Field(..., description="Giấy tờ định danh")
    basic_information: PassportBasicInformationResponse = Field(..., description="Thông tin cơ bản")


########################################################################################################################
# response detail giấy tờ định danh
########################################################################################################################

class IdentityCardDetailResponse(BaseSchema):
    identity_document_type: DropdownResponse = Field(..., description="Loại giấy tờ định danh")
    frontside_information: FrontSideInformationResponse = Field(..., description="Thông tin mặt trước")
    backside_information: BackSideInformationResponse = Field(..., description="Thông tin mặt sau")
    ocr_result: IdentityCardOCRResultResponse = Field(..., description="Phân tích OCR")


class CitizenCardDetailResponse(BaseSchema):
    identity_document_type: DropdownResponse = Field(..., description="Loại giấy tờ định danh")
    frontside_information: FrontSideInformationResponse = Field(..., description="Thông tin mặt trước")
    backside_information: BackSideInformationResponse = Field(..., description="Thông tin mặt sau")
    ocr_result: CitizenOCRResultResponse = Field(..., description="Phân tích OCR")


class PassportDetailResponse(BaseSchema):
    identity_document_type: DropdownResponse = Field(..., description="Loại giấy tờ định danh")
    passport_information: PassportInformationResponse = Field(..., description="Thông tin hộ chiếu")
    ocr_result: PassportOCRResultResponse = Field(..., description="Phân tích OCR")


########################################################################################################################
# request body save giấy tờ định danh
########################################################################################################################
# II. Thông tin mặt sau CMND, CCCD
class BackSideInformationRequest(BaseSchema):
    identity_image_url: str = Field(..., description="URL hình ảnh mặt sau CMND/CCCD")
    fingerprint: List[FingerPrintRequest] = Field(..., description="Vân tay")


class IdentityCardDocumentRequest(IdentityCardDocumentResponse):
    place_of_issue: DropdownRequest = Field(..., description="Nơi cấp")


class IdentityBasicInformationRequest(IdentityBasicInformationResponse):
    gender: DropdownRequest = Field(..., description="Giới tính")
    nationality: DropdownRequest = Field(..., description="Quốc tịch")
    province: DropdownRequest = Field(..., description="Quê quán")
    ethnic: DropdownRequest = Field(None, description="Dân tộc")
    religion: DropdownRequest = Field(None, description="Tôn giáo")


class AddressRequest(AddressResponse):
    province: DropdownRequest = Field(..., description="Tỉnh/Thành phố")
    district: DropdownRequest = Field(..., description="Quận/Huyện")
    ward: DropdownRequest = Field(..., description="Phường/Xã")


class AddressInformationRequest(BaseSchema):
    resident_address: AddressRequest = Field(..., description="Nơi thường trú")
    contact_address: AddressRequest = Field(..., description="Địa chỉ liên hệ")


class IdentityCardOCRResultRequest(BaseSchema):
    identity_document: IdentityCardDocumentRequest = Field(..., description="Giấy tờ định danh")
    basic_information: IdentityBasicInformationRequest = Field(..., description="Thông tin cơ bản")
    address_information: AddressInformationRequest = Field(..., description="Thông tin địa chỉ")


class IdentityDocumentTypeRequest(BaseSchema):
    code: str = Field(..., description="Mã code")


class IdentityCardDetailRequest(BaseSchema):
    identity_document_type: IdentityDocumentTypeRequest = Field(..., description="Mã loại giấy tờ định danh")
    frontside_information: FrontSideInformationResponse = Field(..., description="Thông tin mặt trước")
    backside_information: BackSideInformationRequest = Field(..., description="Thông tin mặt sau")
    ocr_result: IdentityCardOCRResultRequest = Field(..., description="Phân tích OCR")


class IdentityCardSaveRequest(IdentityCardDetailRequest):
    cif_id: str = Field(None, description="ID định danh CIF")


# CCCD
class CitizenBasicInformationRequest(CitizenBasicInformationResponse):
    gender: DropdownRequest = Field(..., description="Giới tính")
    nationality: DropdownRequest = Field(..., description="Quốc tịch")
    province: DropdownRequest = Field(..., description="Quê quán")
    ethnic: DropdownRequest = Field(..., description="Dân tộc")
    religion: DropdownRequest = Field(..., description="Tôn giáo")


class CitizenCardRequest(CitizenCardResponse):
    place_of_issue: DropdownRequest = Field(..., description="Nơi cấp")


class CitizenCardOCRResultRequest(BaseSchema):
    identity_document: CitizenCardRequest = Field(..., description="Giấy tờ định danh")
    basic_information: CitizenBasicInformationRequest = Field(..., description="Thông tin cơ bản")
    address_information: AddressInformationRequest = Field(..., description="Thông tin địa chỉ")


class CitizenCardDetailRequest(BaseSchema):
    identity_document_type: IdentityDocumentTypeRequest = Field(..., description="Mã loại giấy tờ định danh")
    frontside_information: FrontSideInformationResponse = Field(..., description="Thông tin mặt trước")
    backside_information: BackSideInformationRequest = Field(..., description="Thông tin mặt sau")
    ocr_result: CitizenCardOCRResultRequest = Field(..., description="Phân tích OCR")


class CitizenCardSaveRequest(CitizenCardDetailRequest):
    cif_id: str = Field(None, description="ID định danh CIF")


# HC
class PassportDocumentRequest(PassportDocumentResponse):
    place_of_issue: DropdownRequest = Field(..., description="Nơi cấp")
    passport_type: DropdownRequest = Field(..., description="Loại")
    passport_code: DropdownRequest = Field(..., description="Mã số")


class PassportBasicInformationRequest(PassportBasicInformationResponse):
    gender: DropdownRequest = Field(..., description="Giới tính")
    nationality: DropdownRequest = Field(..., description="Quốc tịch")
    place_of_birth: DropdownRequest = Field(..., description="Nơi sinh")


class PassportOCRResultRequest(BaseSchema):
    identity_document: PassportDocumentRequest = Field(..., description="Giấy tờ định danh")
    basic_information: PassportBasicInformationRequest = Field(..., description="Thông tin cơ bản")


class PassportInformationRequest(BaseSchema):
    fingerprint: List[FingerPrintRequest] = Field(..., description="Vân tay")


class PassportSaveRequest(BaseSchema):
    cif_id: str = Field(None, description="ID định danh CIF")
    identity_document_type: IdentityDocumentTypeRequest = Field(..., description="Mã loại giấy tờ định danh")
    passport_information: PassportInformationRequest = Field(..., description="Thông tin hộ chiếu")
    ocr_result: PassportOCRResultRequest = Field(..., description="Phân tích OCR")


########################################################################################################################
# response save giấy tờ định danh
########################################################################################################################

class IdentityDocumentSaveSuccessResponse(BaseSchema):
    cif_id: str = Field(None, description="ID định danh CIF")
    created_at: datetime = Field(..., description="Thời gian tạo")
    created_by: str = Field(..., description="Người tạo")


EXAMPLE_REQUEST_SAVE_IDENTITY_DOCUMENT = {
    "identity_card": {
        "summary": "CMND",
        "description": "Giấy tờ định danh - Chứng minh nhân dân",
        "value": {
            "identity_document_type": {
                "code": "CMND"
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
                            "id": "1"
                        },
                        "finger_type": {
                            "id": "1"
                        }
                    },
                    {
                        "image_url": "https://example.com/example.jpg",
                        "hand_side": {
                            "id": "1"
                        },
                        "finger_type": {
                            "id": "1"
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
            },
            "cif_id": None
        }
    },
    "citizen_card": {
        "summary": "CCCD",
        "description": "Giấy tờ định danh - Căn cước công dân",
        "value": {
            "identity_document_type": {
                "code": "CCCD"
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
                            "id": "1"
                        },
                        "finger_type": {
                            "id": "1"
                        }
                    },
                    {
                        "image_url": "https://example.com/example.jpg",
                        "hand_side": {
                            "id": "1"
                        },
                        "finger_type": {
                            "id": "1"
                        }
                    },
                    {
                        "image_url": "https://example.com/example.jpg",
                        "hand_side": {
                            "id": "1"
                        },
                        "finger_type": {
                            "id": "1"
                        }
                    },
                    {
                        "image_url": "https://example.com/example.jpg",
                        "hand_side": {
                            "id": "1"
                        },
                        "finger_type": {
                            "id": "1"
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
                        "id": "2"
                    },
                    "expired_date": "07/02/2021",
                    "mrz_content": "IDVNM~079195236~8~079197258639~<< "
                                   "122909199~X~Nu~23092031~X~VNM<<<<<<<<<<<~4Tran~<<~Minh~<~Huyen~<<<….",
                    "qr_code_content": "079087007923||Nguyễn Thái Anh |27061987|Nam|236/11 Lê Thị Hông, Phường 17, "
                                       "Gò Vấp, TPHCM | 21022021 "
                },
                "basic_information": {
                    "full_name_vn": "Nguyễn Phạm Thông",
                    "gender": {
                        "id": "2"
                    },
                    "date_of_birth": "07/02/1994",
                    "nationality": {
                        "id": "1"
                    },
                    "province": {
                        "id": "2"
                    },
                    "identity_characteristic": "Sẹo chấm cách 2.5 so với trán"
                },
                "address_information": {
                    "resident_address": {
                        "province": {
                            "id": "1"
                        },
                        "district": {
                            "id": "1"
                        },
                        "ward": {
                            "id": "1"
                        },
                        "number_and_street": "54/12/25 Đường Long Thới"
                    },
                    "contact_address": {
                        "province": {
                            "id": "1"
                        },
                        "district": {
                            "id": "1"
                        },
                        "ward": {
                            "id": "1"
                        },
                        "number_and_street": "54/12/25 Đường Long Thới"
                    }
                }
            }
        }

    },
    "passport": {
        "summary": "Hộ chiếu",
        "description": "Giấy tờ định danh - Hộ chiếu",
        "value": {
            "identity_document_type": {
                "code": "HC"
            },
            "passport_information": {
                "identity_image_url": "http://example.com/example.jpg",
                "face_compare_image_url": "http://example.com/example.jpg",
                "similar_percent": 94,
                "fingerprint": [
                    {
                        "image_url": "http://example.com/example.jpg",
                        "hand_side": {
                            "id": "1"
                        },
                        "finger_type": {
                            "id": "1"
                        }
                    },
                    {
                        "image_url": "http://example.com/example.jpg",
                        "hand_side": {
                            "id": "1"
                        },
                        "finger_type": {
                            "id": "1",
                            "code": "NGONTRO",
                            "name": "Ngón trỏ"
                        }
                    },
                    {
                        "id": "3",
                        "image_url": "http://example.com/example.jpg",
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
                        "image_url": "http://example.com/example.jpg",
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
    }
}
