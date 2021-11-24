from typing import Union

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.api.v1.endpoints.cif.basic_information.identity.identity_document.schema_request import (
    CitizenCardSaveRequest, IdentityCardSaveRequest, PassportSaveRequest
)
from app.third_parties.oracle.models.cif.basic_information.contact.model import (
    CustomerAddress
)
from app.third_parties.oracle.models.cif.basic_information.identity.model import (
    CustomerCompareImage, CustomerIdentity, CustomerIdentityImage
)
from app.third_parties.oracle.models.cif.basic_information.model import (
    Customer
)
from app.third_parties.oracle.models.cif.basic_information.personal.model import (
    CustomerIndividualInfo
)
from app.third_parties.oracle.models.master_data.address import (
    AddressCountry, AddressDistrict, AddressProvince, AddressWard
)
from app.third_parties.oracle.models.master_data.customer import CustomerGender
from app.third_parties.oracle.models.master_data.identity import (
    CustomerIdentityType, FingerType, HandSide, PassportCode, PassportType,
    PlaceOfIssue
)
from app.third_parties.oracle.models.master_data.others import Nation, Religion
from app.utils.constant.cif import (
    CIF_ID_TEST, CONTACT_ADDRESS_CODE, IDENTITY_DOCUMENT_TYPE,
    IDENTITY_DOCUMENT_TYPE_PASSPORT, RESIDENT_ADDRESS_CODE
)
from app.utils.error_messages import (
    ERROR_CIF_ID_NOT_EXIST, ERROR_IDENTITY_DOCUMENT_NOT_EXIST
)
from app.utils.functions import dropdown, now

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


########################################################################################################################
# Chi tiết A. Giấy tờ định danh
########################################################################################################################
async def repos_get_detail_identity(cif_id: str, identity_document_type_id: str, session: Session) -> ReposReturn:
    identities = session.execute(
        select(
            Customer,
            CustomerIdentity,
            CustomerIndividualInfo,
            CustomerAddress,
            CustomerIdentityImage,
            CustomerIdentityType,
            CustomerCompareImage,
            HandSide,
            FingerType,
            PlaceOfIssue,
            CustomerGender,
            AddressCountry,
            AddressProvince,
            AddressDistrict,
            AddressWard,
            Nation,
            Religion,
            PassportType,
            PassportCode
        )
        .join(CustomerIdentity, Customer.id == CustomerIdentity.customer_id)
        .join(CustomerIndividualInfo, Customer.id == CustomerIndividualInfo.customer_id)
        .join(CustomerAddress, Customer.id == CustomerAddress.customer_id)
        .outerjoin(CustomerIdentityImage, CustomerIdentity.id == CustomerIdentityImage.identity_id)
        .outerjoin(CustomerCompareImage, CustomerIdentityImage.id == CustomerCompareImage.identity_image_id)
        .outerjoin(CustomerIdentityType, CustomerIdentity.identity_type_id == CustomerIdentityType.id)

        .outerjoin(HandSide, CustomerIdentityImage.hand_side_id == HandSide.id)
        .outerjoin(FingerType, CustomerIdentityImage.finger_type_id == FingerType.id)
        .join(PlaceOfIssue, CustomerIdentity.place_of_issue_id == PlaceOfIssue.id)
        .join(CustomerGender, CustomerIndividualInfo.gender_id == CustomerGender.id)
        .join(AddressCountry, CustomerIndividualInfo.country_of_birth_id == AddressCountry.id)
        .join(AddressProvince, CustomerIndividualInfo.place_of_birth_id == AddressProvince.id)
        .join(AddressDistrict, CustomerAddress.address_district_id == AddressDistrict.id)
        .join(AddressWard, CustomerAddress.address_ward_id == AddressWard.id)
        .join(Nation, CustomerIndividualInfo.nation_id == Nation.id)
        .join(Religion, CustomerIndividualInfo.religion_id == Religion.id)
        .outerjoin(PassportType, CustomerIdentity.passport_type_id == PassportType.id)
        .outerjoin(PassportCode, CustomerIdentity.passport_code_id == PassportCode.id)
        .filter(
            Customer.id == cif_id,
            CustomerIdentity.identity_type_id == identity_document_type_id
        )
        .order_by(desc(CustomerIdentityImage.updater_at))
    ).all()

    if not identities:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc='cif_id')

    identity_info = await repos_get_identity_info(identities, identity_document_type_id)

    return ReposReturn(data=identity_info)


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
########################################################################################################################


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
