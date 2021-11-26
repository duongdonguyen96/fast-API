from typing import Union

from sqlalchemy import desc, select
from sqlalchemy.orm import Session, aliased

from app.api.base.repository import ReposReturn
from app.api.v1.endpoints.cif.basic_information.identity.identity_document.schema_request import (
    CitizenCardSaveRequest, IdentityCardSaveRequest, PassportSaveRequest
)
from app.api.v1.endpoints.cif.repository import (
    repos_create_basic_information_identity,
    repos_update_basic_information_identity
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
    AddressCountry, AddressDistrict, AddressProvince, AddressType, AddressWard
)
from app.third_parties.oracle.models.master_data.customer import CustomerGender
from app.third_parties.oracle.models.master_data.identity import (
    CustomerIdentityType, FingerType, HandSide, PassportCode, PassportType,
    PlaceOfIssue
)
from app.third_parties.oracle.models.master_data.others import Nation, Religion
from app.utils.constant.cif import (
    ACTIVED, CIF_ID_TEST, CONTACT_ADDRESS_CODE,
    IDENTITY_DOCUMENT_TYPE_CITIZEN_CARD, IDENTITY_DOCUMENT_TYPE_IDENTITY_CARD,
    RESIDENT_ADDRESS_CODE, UNCOMPLETED
)
from app.utils.error_messages import ERROR_CIF_ID_NOT_EXIST
from app.utils.functions import (
    calculate_age, dropdown, now, raise_does_not_exist_string
)
from app.utils.vietnamese_converted import (
    make_short_name, split_name, vietnamese_converted
)

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
async def repos_get_detail_identity(cif_id: str, session: Session) -> ReposReturn:
    place_of_birth = aliased(AddressProvince, name='PlaceOfBirth')

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
            place_of_birth,
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
        .join(place_of_birth, CustomerIndividualInfo.place_of_birth_id == place_of_birth.id)
        .join(AddressProvince, CustomerAddress.address_province_id == AddressProvince.id)
        .join(AddressDistrict, CustomerAddress.address_district_id == AddressDistrict.id)
        .join(AddressWard, CustomerAddress.address_ward_id == AddressWard.id)
        .join(Nation, CustomerIndividualInfo.nation_id == Nation.id)
        .join(Religion, CustomerIndividualInfo.religion_id == Religion.id)
        .outerjoin(PassportType, CustomerIdentity.passport_type_id == PassportType.id)
        .outerjoin(PassportCode, CustomerIdentity.passport_code_id == PassportCode.id)
        .filter(
            Customer.id == cif_id
        )
        .order_by(desc(CustomerIdentityImage.updater_at))
    ).all()

    if not identities:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc='cif_id')

    first_row = identities[0]

    lasted_identity_id = first_row.CustomerIdentity.id  # customer identity id mới nhất
    identity_document_type_id = first_row.CustomerIdentityType.id  # Loại giấy tờ định danh mới nhất

    # vì join với address bị lặp dữ liệu nên cần lọc những fingerprint_ids
    fingerprint_ids = []
    fingerprints = []
    for row in identities:
        if row.CustomerIdentity.id == lasted_identity_id \
                and row.CustomerIdentityImage.hand_side_id \
                and row.CustomerIdentityImage.finger_type_id \
                and row.CustomerIdentityImage.id not in fingerprint_ids:

            fingerprint_ids.append(row.CustomerIdentityImage.id)
            fingerprints.append({
                "image_url": row.CustomerIdentityImage.image_url,
                "hand_side": dropdown(row.HandSide),
                "finger_type": dropdown(row.FingerType)
            })

    response_data = {
        "identity_document_type": dropdown(first_row.CustomerIdentityType),
        "ocr_result": {}
    }

    # CMND, CCCD
    if identity_document_type_id in [IDENTITY_DOCUMENT_TYPE_IDENTITY_CARD, IDENTITY_DOCUMENT_TYPE_CITIZEN_CARD]:
        # Mặt trước
        for row in identities:
            if row.CustomerIdentityImage.identity_image_front_flag == 1:
                response_data["front_side_information"] = {
                    "identity_image_url": row.CustomerIdentityImage.image_url,
                    "face_compare_image_url": row.CustomerCompareImage.compare_image_url,
                    "similar_percent": row.CustomerCompareImage.similar_percent
                }
                break

        # Mặt sau
        for row in identities:
            if row.CustomerIdentityImage.identity_image_front_flag == 0 \
                    and row.CustomerIdentityImage.hand_side_id is None \
                    and row.CustomerIdentityImage.finger_type_id is None:
                response_data["back_side_information"] = {
                    "identity_image_url": row.CustomerIdentityImage.image_url,
                    "fingerprint": fingerprints,
                    "updated_at": row.CustomerIdentityImage.updater_at,
                    "updated_by": row.CustomerIdentityImage.updater_id
                }
                break

        resident_address = None  # noqa
        for row in identities:
            if row.CustomerAddress.address_type_id == RESIDENT_ADDRESS_CODE:
                resident_address = {
                    "province": dropdown(row.AddressProvince),
                    "district": dropdown(row.AddressDistrict),
                    "ward": dropdown(row.AddressWard),
                    "number_and_street": row.CustomerAddress.address
                }
                break

        contact_address = None  # noqa
        for row in identities:
            if row.CustomerAddress.address_type_id == CONTACT_ADDRESS_CODE:
                contact_address = {
                    "province": dropdown(row.AddressProvince),
                    "district": dropdown(row.AddressDistrict),
                    "ward": dropdown(row.AddressWard),
                    "number_and_street": row.CustomerAddress.address
                }
                break

        response_data['ocr_result'].update(**{
            'address_information': {
                'resident_address': resident_address,
                'contact_address': contact_address
            }
        })

        # CMND
        if identity_document_type_id == IDENTITY_DOCUMENT_TYPE_IDENTITY_CARD:
            response_data['ocr_result'].update(**{
                'identity_document': {
                    "identity_number": first_row.CustomerIdentity.identity_num,
                    "issued_date": first_row.CustomerIdentity.issued_date,
                    "place_of_issue": dropdown(first_row.PlaceOfIssue),
                    "expired_date": first_row.CustomerIdentity.expired_date
                },
                'basic_information': {
                    "full_name_vn": first_row.Customer.full_name_vn,
                    "gender": dropdown(first_row.CustomerGender),
                    "date_of_birth": first_row.CustomerIndividualInfo.date_of_birth,
                    "nationality": dropdown(first_row.AddressCountry),
                    "province": dropdown(first_row.PlaceOfBirth),
                    "ethnic": dropdown(first_row.Nation),
                    "religion": dropdown(first_row.Religion),
                    "identity_characteristic": first_row.CustomerIndividualInfo.identifying_characteristics,
                    "father_full_name_vn": first_row.CustomerIndividualInfo.father_full_name,
                    "mother_full_name_vn": first_row.CustomerIndividualInfo.mother_full_name
                }
            })

        # CCCD
        else:
            response_data['ocr_result'].update(**{
                'identity_document': {
                    "identity_number": first_row.CustomerIdentity.identity_num,
                    "issued_date": first_row.CustomerIdentity.issued_date,
                    "expired_date": first_row.CustomerIdentity.expired_date,
                    "place_of_issue": dropdown(first_row.PlaceOfIssue),
                    "mrz_content": first_row.CustomerIdentity.mrz_content,
                    "qr_code_content": first_row.CustomerIdentity.qrcode_content
                },

                'basic_information': {
                    "full_name_vn": first_row.Customer.full_name_vn,
                    "gender": dropdown(first_row.CustomerGender),
                    "date_of_birth": first_row.CustomerIndividualInfo.date_of_birth,
                    "nationality": dropdown(first_row.AddressCountry),
                    "province": dropdown(first_row.PlaceOfBirth),
                    "identity_characteristic": first_row.CustomerIndividualInfo.identifying_characteristics,
                }
            })

    # HO_CHIEU
    else:
        response_data['passport_information'] = {
            "identity_image_url": first_row.CustomerIdentityImage.image_url,
            "face_compare_image_url": first_row.CustomerCompareImage.compare_image_url,
            "similar_percent": first_row.CustomerCompareImage.similar_percent,
            "fingerprint": fingerprints,
        }

        response_data['ocr_result'] = {
            'identity_document': {
                "identity_number": first_row.CustomerIdentity.identity_num,
                "issued_date": first_row.CustomerIdentity.issued_date,
                "place_of_issue": dropdown(first_row.PlaceOfIssue),
                "expired_date": first_row.CustomerIdentity.expired_date,
                "passport_type": dropdown(first_row.PassportType),
                "passport_code": dropdown(first_row.PassportCode)
            },
            'basic_information': {
                "full_name_vn": first_row.Customer.full_name_vn,
                "gender": dropdown(first_row.CustomerGender),
                "date_of_birth": first_row.CustomerIndividualInfo.date_of_birth,
                "nationality": dropdown(first_row.AddressCountry),
                "place_of_birth": dropdown(first_row.AddressProvince),
                "identity_card_number": first_row.CustomerIdentity.identity_number_in_passport,
                "mrz_content": first_row.CustomerIdentity.mrz_content
            }
        }

    return ReposReturn(data=response_data)

########################################################################################################################


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
    front_side_information_identity_image_url = identity_document_req.front_side_information.identity_image_url
    front_side_information_compare_image_url = identity_document_req.front_side_information.face_compare_image_url
    back_side_information_identity_image_url = identity_document_req.front_side_information.face_compare_image_url
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
    under_15_year_old_flag = True if calculate_age(date_of_birth) < 15 else False
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
        customer_id = await repos_create_basic_information_identity(
            cif_number,
            saving_customer,
            customer_individual_info,
            customer_resident_address,
            customer_contact_address,
            customer_identity,
            front_side_information_identity_image_url,
            front_side_information_compare_image_url,
            back_side_information_identity_image_url,
            save_by,
            session
        )

    return ReposReturn(data={
        "cif_id": customer_id
    })
