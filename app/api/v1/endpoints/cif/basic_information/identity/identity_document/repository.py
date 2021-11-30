from typing import Optional

from sqlalchemy import and_, desc, select, update
from sqlalchemy.orm import Session, aliased

from app.api.base.repository import ReposReturn, auto_commit
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
from app.third_parties.oracle.models.cif.form.model import (
    Booking, BookingBusinessForm, BookingCustomer, TransactionDaily
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
    CIF_ID_TEST, CONTACT_ADDRESS_CODE, IDENTITY_DOCUMENT_TYPE_CITIZEN_CARD,
    IDENTITY_DOCUMENT_TYPE_IDENTITY_CARD, IDENTITY_IMAGE_FLAG_BACKSIDE,
    IDENTITY_IMAGE_FLAG_FRONT_SIDE, IMAGE_TYPE_CODE_IDENTITY,
    RESIDENT_ADDRESS_CODE
)
from app.utils.error_messages import ERROR_CIF_ID_NOT_EXIST
from app.utils.functions import dropdown, generate_uuid, now

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


########################################################################################################################
# Lưu lại A. Giấy tờ định danh
########################################################################################################################
@auto_commit
async def repos_save_identity(
        customer_id: Optional[str],
        saving_customer: dict,
        saving_customer_identity: dict,
        saving_customer_individual_info: dict,
        saving_customer_resident_address: dict,
        saving_customer_contact_address: dict,
        save_by: str,
        session: Session
):
    # front_side_information_identity_image_url = identity_document_req.front_side_information.identity_image_url
    # front_side_information_compare_image_url = identity_document_req.front_side_information.face_compare_image_url
    # back_side_information_identity_image_url = identity_document_req.front_side_information.face_compare_image_url

    # TODO: nếu là passport là kiểu khác
    front_side_information_identity_image_url = None
    front_side_information_compare_image_url = None
    back_side_information_identity_image_url = None

    # Tạo mới
    if not customer_id:
        new_transaction_id = generate_uuid()
        new_booking_id = generate_uuid()
        new_customer_id = generate_uuid()
        new_identity_id = generate_uuid()
        new_front_side_identity_image_id = generate_uuid()

        customer_id = new_customer_id

        saving_customer['id'] = new_customer_id

        saving_customer_individual_info['customer_id'] = new_customer_id
        saving_customer_resident_address['customer_id'] = new_customer_id
        saving_customer_contact_address['customer_id'] = new_customer_id

        saving_customer_identity['id'] = new_identity_id
        saving_customer_identity['customer_id'] = new_customer_id

        session.add_all([
            Customer(**saving_customer),
            CustomerIdentity(**saving_customer_identity),
            CustomerIdentityImage(
                id=new_front_side_identity_image_id,
                identity_id=new_identity_id,
                image_type_id=IMAGE_TYPE_CODE_IDENTITY,
                image_url=front_side_information_identity_image_url,
                hand_side_id=None,
                finger_type_id=None,
                vector_data=None,
                active_flag=True,
                maker_id=save_by,
                maker_at=now(),
                updater_id=save_by,
                updater_at=now(),
                identity_image_front_flag=IDENTITY_IMAGE_FLAG_FRONT_SIDE
            ),
            CustomerIndividualInfo(**saving_customer_individual_info),
            CustomerAddress(**saving_customer_resident_address),
            CustomerAddress(**saving_customer_contact_address),
            CustomerCompareImage(
                identity_id=new_identity_id,
                identity_image_id=new_front_side_identity_image_id,
                compare_image_url=front_side_information_compare_image_url,
                similar_percent=00,
                maker_id=save_by,
                maker_at=now()
            ),
            CustomerIdentityImage(
                identity_id=new_identity_id,
                image_type_id=IMAGE_TYPE_CODE_IDENTITY,
                image_url=back_side_information_identity_image_url,
                hand_side_id=None,
                finger_type_id=None,
                vector_data=None,
                active_flag=True,
                maker_id=save_by,
                maker_at=now(),
                updater_id=save_by,
                updater_at=now(),
                identity_image_front_flag=IDENTITY_IMAGE_FLAG_BACKSIDE
            ),

            # Tạo BOOKING, CRM_TRANSACTION_DAILY -> CRM_BOOKING -> BOOKING_CUSTOMER -> BOOKING_BUSSINESS_FORM
            TransactionDaily(
                transaction_id=new_transaction_id,
                data=None,
                description="Tạo CIF -> Thông tin cá nhân -> GTĐD -- Tạo mới",
                updated_at=now()
            ),
            Booking(
                id=new_booking_id,
                transaction_id=new_transaction_id,
                created_at=now(),
                updated_at=now()
            ),
            BookingCustomer(
                booking_id=new_booking_id,
                customer_id=new_customer_id
            ),
            BookingBusinessForm(
                booking_id=new_booking_id,
                business_form_id="BE_TEST",  # TODO
                save_flag=False,
                created_at=now(),
                updated_at=now()
            )
        ])

    # Update
    else:
        # Cập nhật 1 cif_number đã tồn tại
        saving_customer_identity.update({"customer_id": customer_id})
        saving_customer_individual_info.update({"customer_id": customer_id})
        saving_customer_resident_address.update({"customer_id": customer_id})
        saving_customer_contact_address.update({"customer_id": customer_id})

        session.execute(update(Customer).where(
            Customer.id == customer_id
        ).values(**saving_customer))
        # TODO: cần check lại tạo một dòng hay tạo mới nhiều dòng customer_identity
        session.execute(update(CustomerIdentity).where(
            CustomerIdentity.customer_id == customer_id
        ).values(saving_customer_identity))
        session.execute(update(CustomerIndividualInfo).where(
            CustomerIndividualInfo.customer_id == customer_id
        ).values(saving_customer_individual_info))
        session.execute(update(CustomerAddress).where(and_(
            CustomerAddress.customer_id == customer_id,
            CustomerAddress.address_type_id == RESIDENT_ADDRESS_CODE,
        )).values(saving_customer_resident_address))
        session.execute(update(CustomerAddress).where(and_(
            CustomerAddress.customer_id == customer_id,
            CustomerAddress.address_type_id == CONTACT_ADDRESS_CODE,
        )).values(saving_customer_contact_address))

        # TODO cập nhật lại transaction_id trong Booking
        # lưu log trong CRM_TRANSACTION_DAILY
        transaction_id = generate_uuid()
        session.add(
            TransactionDaily(
                transaction_id=transaction_id,
                data=None,
                description="Tạo CIF -> Thông tin cá nhân -> GTĐD -- Cập nhật",
                updated_at=now()
            )
        )

    return ReposReturn(data={
        "cif_id": customer_id
    })
########################################################################################################################
