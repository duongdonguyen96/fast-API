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
    FingerType, PassportType, PassportCode
from app.third_parties.oracle.models.master_data.others import Nation, Religion
from app.utils.constant.cif import (
    CIF_ID_TEST, IDENTITY_DOCUMENT_TYPE, IDENTITY_DOCUMENT_TYPE_CITIZEN_CARD,
    IDENTITY_DOCUMENT_TYPE_IDENTITY_CARD, RESIDENT_ADDRESS_CODE, CONTACT_ADDRESS_CODE, IDENTITY_FRONT_SIDE,
    IDENTITY_BACK_SIDE
)
from app.utils.error_messages import (
    ERROR_CIF_ID_NOT_EXIST, ERROR_IDENTITY_DOCUMENT_NOT_EXIST, MESSAGE_STATUS
)
from app.utils.functions import now, raise_does_not_exist_string, dropdown

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


async def repos_get_detail(
        cif_id: str, identity_document_type_id: str, oracle_session: Session, current_user
) -> ReposReturn:
    if identity_document_type_id not in IDENTITY_DOCUMENT_TYPE:
        return ReposReturn(is_error=True, msg=f"{MESSAGE_STATUS[ERROR_IDENTITY_DOCUMENT_NOT_EXIST]} in "
                                              f"{IDENTITY_DOCUMENT_TYPE}", loc='identity_document_type_id')

    # Loại giấy tờ định danh
    # Phân tích OCR -> Giấy tờ định danh
    try:
        customer_identity_type, ocr_customer_identity, ocr_place_of_issue, ocr_passport_type, ocr_passport_code = \
        oracle_session.execute(
            select(
                CustomerIdentityType,
                CustomerIdentity,
                PlaceOfIssue,
                PassportType,
                PassportCode
            )
            .join(CustomerIdentity, CustomerIdentity.identity_type_id == CustomerIdentityType.id)
            .join(PlaceOfIssue, PlaceOfIssue.id == CustomerIdentity.place_of_issue_id)
            .outerjoin(PassportType, PassportType.id == CustomerIdentity.passport_type_id)
            .outerjoin(PassportCode, PassportCode.id == CustomerIdentity.passport_code_id)
            .filter(CustomerIdentity.customer_id == cif_id, CustomerIdentityType.id == identity_document_type_id)
        ).one()
    except Exception as ex:
        return ReposReturn(is_error=True, msg=f"Customer Identity Type does not exist in {identity_document_type_id=} "
                                              f"and {cif_id=}", loc='identity_document_type_id, cif_id')

    # Phân tích OCR -> Thông tin cơ bản
    try:
        ocr_basic_info_customer, ocr_basic_info_customer_individual_info, ocr_basic_info_customer_gender, \
        ocr_basic_info_customer_country, ocr_basic_info_customer_province, ocr_basic_info_customer_religion, \
        ocr_basic_info_customer_nation, _ = oracle_session.execute(
            select(
                Customer,
                CustomerIndividualInfo,
                CustomerGender,
                AddressCountry,
                AddressProvince,
                Religion,
                Nation,
                CustomerIdentity
            )
            .join(CustomerIndividualInfo, CustomerIndividualInfo.customer_id == Customer.id)
            .join(CustomerGender, CustomerGender.id == CustomerIndividualInfo.gender_id)
            .join(AddressCountry, AddressCountry.id == CustomerIndividualInfo.country_of_birth_id)
            .join(AddressProvince, AddressProvince.id == CustomerIndividualInfo.place_of_birth_id)
            .join(Religion, Religion.id == CustomerIndividualInfo.religion_id)
            .join(Nation, Nation.id == CustomerIndividualInfo.nation_id)
            .filter(
                Customer.id == cif_id,
                CustomerIdentity.identity_type_id == identity_document_type_id
            )
        ).first()
    except Exception as ex:
        return ReposReturn(is_error=True, msg=raise_does_not_exist_string("Basic Information"),
                           loc='ocr_result -> basic_information')

    # Phân tích OCR -> Địa chi thường trú
    try:
        customer_resident_address, customer_resident_address_province, \
        customer_resident_address_district, customer_resident_address_ward = oracle_session.execute(
            select(
                CustomerAddress,
                AddressProvince,
                AddressDistrict,
                AddressWard
            )
            .join(AddressProvince, AddressProvince.id == CustomerAddress.address_province_id)
            .join(AddressDistrict, AddressDistrict.id == CustomerAddress.address_district_id)
            .join(AddressWard, AddressWard.id == CustomerAddress.address_ward_id)
            .join(AddressType, and_(
                AddressType.id == CustomerAddress.address_type_id,
                AddressType.code == RESIDENT_ADDRESS_CODE
            ))
            .filter(
                Customer.id == cif_id,
                CustomerIdentity.identity_type_id == identity_document_type_id
            )
        ).first()
    except Exception as ex:
        return ReposReturn(is_error=True, msg=raise_does_not_exist_string("Resident Address"),
                           loc='ocr_result -> resident_address')

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
            .filter(
                Customer.id == cif_id,
                CustomerIdentity.identity_type_id == identity_document_type_id
            )
        ).first()
    except Exception as ex:
        return ReposReturn(is_error=True, msg=raise_does_not_exist_string("Contact Address"),
                           loc='ocr_result -> contact_address')

    fingerprint_list = []

    if identity_document_type_id == IDENTITY_DOCUMENT_TYPE_IDENTITY_CARD or \
            identity_document_type_id == IDENTITY_DOCUMENT_TYPE_CITIZEN_CARD:
        # Thông tin mặt trước
        # Thông tin mặt sau
        try:
            identity_informations = oracle_session.execute(
                select(
                    CustomerIdentityImage,
                    HandSide,
                    FingerType,
                    CustomerCompareImage
                )
                .join(CustomerIdentity, and_(
                    CustomerIdentity.id == CustomerIdentityImage.identity_id,
                    CustomerIdentity.customer_id == cif_id
                ))
                .outerjoin(CustomerCompareImage, CustomerCompareImage.identity_image_id == CustomerIdentityImage.id)
                .outerjoin(HandSide, HandSide.id == CustomerIdentityImage.hand_side_id)
                .outerjoin(FingerType, FingerType.id == CustomerIdentityImage.finger_type_id)
                .filter(
                    CustomerIdentity.customer_id == cif_id,
                    CustomerIdentityImage.identity_type_id == identity_document_type_id
                )
            ).all()
        except Exception as ex:
            return ReposReturn(is_error=True, msg=raise_does_not_exist_string("Back Side Information"), loc='back_side_information')

        # Set up giá trị mặc nhiên
        identity_info_front_side_information = {
            "identity_image_url": "",
            "face_compare_image_url": "",
            "similar_percent": 00
        }
        identity_info_backside_information = {
            "identity_image_url": "",
            "fingerprint": fingerprint_list,
            "updated_at": now(),
            "updated_by": ""
        }
        for customer_identity_image, hand_side, finger_type, front_side_customer_compare_image in identity_informations:
            if customer_identity_image.identity_image_front_flag:
                identity_info_front_side_information['identity_image_url'] = customer_identity_image.image_url
                identity_info_front_side_information['face_compare_image_url'] = front_side_customer_compare_image.compare_image_url
                identity_info_front_side_information['similar_percent'] = front_side_customer_compare_image.similar_percent
            else:
                if customer_identity_image.hand_side_id is None and \
                        customer_identity_image.finger_type_id is None:
                    identity_info_backside_information['identity_image_url'] = customer_identity_image.image_url
                    identity_info_backside_information['updated_at'] = customer_identity_image.updater_at
                    identity_info_backside_information['updated_by'] = customer_identity_image.updater_id

                else:
                    fingerprint_list.append({
                        "image_url": customer_identity_image.image_url,
                        "hand_side": dropdown(hand_side),
                        "finger_type": dropdown(finger_type)
                    })

        if identity_document_type_id == IDENTITY_DOCUMENT_TYPE_IDENTITY_CARD:
            identity_info = {
                "identity_document_type": dropdown(customer_identity_type),
                "frontside_information": identity_info_front_side_information,
                "backside_information": identity_info_backside_information,
                "ocr_result": {
                    "identity_document": {
                        "identity_number": ocr_customer_identity.identity_num,
                        "issued_date": ocr_customer_identity.issued_date,
                        "place_of_issue": dropdown(ocr_place_of_issue),
                        "expired_date": ocr_customer_identity.expired_date
                    },
                    "basic_information": {
                        "full_name_vn": ocr_basic_info_customer.full_name_vn,
                        "gender": dropdown(ocr_basic_info_customer_gender),
                        "date_of_birth": ocr_basic_info_customer_individual_info.date_of_birth,
                        "nationality": dropdown(ocr_basic_info_customer_country),
                        "province": dropdown(ocr_basic_info_customer_province),
                        "ethnic": dropdown(ocr_basic_info_customer_nation),
                        "religion": dropdown(ocr_basic_info_customer_religion),
                        "identity_characteristic": ocr_basic_info_customer_individual_info.identifying_characteristics,
                        "father_full_name_vn": ocr_basic_info_customer_individual_info.father_full_name,
                        "mother_full_name_vn": ocr_basic_info_customer_individual_info.mother_full_name
                    },
                    "address_information": {
                        "resident_address": {
                            "province": dropdown(customer_resident_address_province),
                            "district": dropdown(customer_resident_address_district),
                            "ward": dropdown(customer_resident_address_ward),
                            "number_and_street": customer_resident_address.address
                        },
                        "contact_address": {
                            "province": dropdown(customer_contact_address_province),
                            "district": dropdown(customer_contact_address_district),
                            "ward": dropdown(customer_contact_address_ward),
                            "number_and_street": customer_contact_address.address
                        }
                    }
                }
            }
            return ReposReturn(data=identity_info)

        elif identity_document_type_id == IDENTITY_DOCUMENT_TYPE_CITIZEN_CARD:
            citizen_card_info = {
                "identity_document_type": dropdown(customer_identity_type),
                "frontside_information": identity_info_front_side_information,
                "backside_information": identity_info_backside_information,
                "ocr_result": {
                    "identity_document": {
                        "identity_number": ocr_customer_identity.identity_num,
                        "issued_date": ocr_customer_identity.issued_date,
                        "place_of_issue": dropdown(ocr_place_of_issue),
                        "expired_date": ocr_customer_identity.expired_date,
                        "mrz_content": ocr_customer_identity.mrz_content,
                        "qr_code_content": ocr_customer_identity.qrcode_content
                    },
                    "basic_information": {
                        "full_name_vn": ocr_basic_info_customer.full_name_vn,
                        "gender": dropdown(ocr_basic_info_customer_gender),
                        "date_of_birth": ocr_basic_info_customer_individual_info.date_of_birth,
                        "nationality": dropdown(ocr_basic_info_customer_country),
                        "province": dropdown(ocr_basic_info_customer_province),
                        "identity_characteristic": "Sẹo chấm cách 2.5 so với trán"
                    },
                    "address_information": {
                        "resident_address": {
                            "province": dropdown(customer_resident_address_province),
                            "district": dropdown(customer_resident_address_district),
                            "ward": dropdown(customer_resident_address_ward),
                            "number_and_street": customer_resident_address.address
                        },
                        "contact_address": {
                            "province": dropdown(customer_contact_address_province),
                            "district": dropdown(customer_contact_address_district),
                            "ward": dropdown(customer_contact_address_ward),
                            "number_and_street": customer_contact_address.address
                        }
                    }
                }
            }
            return ReposReturn(data=citizen_card_info)
    else:
        # Thông tin hộ chiếu
        try:
            passport_images = oracle_session.execute(
                select(
                    CustomerIdentity,
                    CustomerIdentityImage,
                    CustomerCompareImage,
                    HandSide,
                    FingerType
                )
                .join(CustomerIdentityImage, and_(
                    CustomerIdentityImage.identity_id ==CustomerIdentity.id,
                    CustomerIdentityImage.identity_image_front_flag.is_(None),
                ))
                .outerjoin(CustomerCompareImage, and_(
                    CustomerCompareImage.identity_image_id == CustomerIdentityImage.id
                ))
                .outerjoin(HandSide, HandSide.id == CustomerIdentityImage.hand_side_id)
                .outerjoin(FingerType, FingerType.id == CustomerIdentityImage.finger_type_id)
                .filter(
                    CustomerIdentity.customer_id == cif_id,
                    CustomerIdentity.identity_type_id == identity_document_type_id,
                )
                .order_by(desc(CustomerIdentityImage.updater_at))
            ).all()
        except Exception as ex:
            return ReposReturn(is_error=True, msg=raise_does_not_exist_string("Passport Information"), loc='passport_information')

        passport_information_image_url = ""
        passport_information_compare_image_url = ""
        passport_information_similar_percent = 00
        for _, customer_identity_passport_image, customer_passport_compare_image, \
            hand_side, finger_type in passport_images:

            # Nếu CÓ thông tin vân tay, bàn tay -> Hình ảnh vân tay hộ chiếu
            if hand_side and finger_type:
                fingerprint_list.append({
                    "image_url": customer_identity_passport_image.image_url,
                    "hand_side": dropdown(hand_side),
                    "finger_type": dropdown(finger_type)
                })
            # Nếu KHÔNG có thông tin vân tay, bàn tay -> Hình ảnh hộ chiếu/ Hình ảnh đối chiếu
            else:
                passport_information_image_url = customer_identity_passport_image.image_url
                passport_information_compare_image_url = customer_passport_compare_image.compare_image_url
                passport_information_similar_percent = customer_passport_compare_image.similar_percent

        passport_info = {
            "identity_document_type": dropdown(customer_identity_type),
            "passport_information": {
                "identity_image_url": passport_information_image_url,
                "face_compare_image_url": passport_information_compare_image_url,
                "similar_percent": passport_information_similar_percent,
                "fingerprint": fingerprint_list
            },
            "ocr_result": {
                "identity_document": {
                    "identity_number": ocr_customer_identity.identity_num,
                    "issued_date": ocr_customer_identity.issued_date,
                    "place_of_issue": dropdown(ocr_place_of_issue),
                    "expired_date": ocr_customer_identity.expired_date,
                    "passport_type": dropdown(ocr_passport_type),
                    "passport_code": dropdown(ocr_passport_code)
                },
                "basic_information": {
                    "full_name_vn": ocr_basic_info_customer.full_name_vn,
                    "gender": dropdown(ocr_basic_info_customer_gender),
                    "date_of_birth": ocr_basic_info_customer_individual_info.date_of_birth,
                    "nationality": dropdown(ocr_basic_info_customer_country),
                    "place_of_birth": dropdown(ocr_basic_info_customer_province),
                    "identity_card_number": ocr_customer_identity.identity_number_in_passport,
                    "mrz_content": ocr_customer_identity.mrz_content
                }
            }
        }
        return ReposReturn(data=passport_info)


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
