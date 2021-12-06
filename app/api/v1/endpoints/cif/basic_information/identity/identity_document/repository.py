import json
from typing import List, Optional

from sqlalchemy import and_, desc, select, update
from sqlalchemy.orm import Session, aliased

from app.api.base.repository import ReposReturn, auto_commit
from app.api.v1.endpoints.repository import (
    repos_get_model_object_by_id_or_code,
    repos_get_optional_model_object_by_code_or_name,
    write_transaction_log_and_update_booking
)
from app.settings.event import service_ekyc, service_file
from app.third_parties.oracle.models.cif.basic_information.contact.model import (
    CustomerAddress
)
from app.third_parties.oracle.models.cif.basic_information.identity.model import (
    CustomerCompareImage, CustomerIdentity, CustomerIdentityImage,
    CustomerIdentityImageTransaction
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
    CONTACT_ADDRESS_CODE, EKYC_IDENTITY_TYPE_FRONT_SIDE_IDENTITY_CARD,
    IDENTITY_DOCUMENT_TYPE_CITIZEN_CARD, IDENTITY_DOCUMENT_TYPE_IDENTITY_CARD,
    IDENTITY_DOCUMENT_TYPE_PASSPORT, RESIDENT_ADDRESS_CODE
)
from app.utils.error_messages import ERROR_CALL_SERVICE, ERROR_CIF_ID_NOT_EXIST
from app.utils.functions import (
    date_string_to_other_date_string_format, date_to_string, dropdown,
    generate_uuid, now
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


async def repos_get_identity_log_list(
        cif_id: str,
        session: Session
) -> ReposReturn:
    identity_image_transactions = session.execute(
        select(
            CustomerIdentityImageTransaction,
        )
        .join(CustomerIdentityImage, CustomerIdentityImageTransaction.identity_image_id == CustomerIdentityImage.id)
        .join(CustomerIdentity, and_(
            CustomerIdentityImage.identity_id == CustomerIdentity.id,
            CustomerIdentity.customer_id == cif_id
        ))
        .order_by(desc(CustomerIdentityImageTransaction.maker_at))
    ).scalars().all()

    identity_log_infos = []
    if not identity_image_transactions:
        return ReposReturn(data=identity_log_infos)

    date__identity_images = {}

    for identity_image_transaction in identity_image_transactions:
        maker_at = date_to_string(identity_image_transaction.maker_at)

        if maker_at not in identity_log_infos:
            date__identity_images[maker_at] = []

        date__identity_images[maker_at].append({
            "image_url": identity_image_transaction.image_url
        })

    identity_log_infos = [{
        "reference_flag": False,
        "created_date": created_date,
        "identity_images": identity_images
    } for created_date, identity_images in date__identity_images.items()]

    identity_log_infos[0]["reference_flag"] = True

    return ReposReturn(data=identity_log_infos)


########################################################################################################################
# Lưu lại A. Giấy tờ định danh
########################################################################################################################
@auto_commit
async def repos_save_identity(
        identity_document_type_id: str,
        customer_id: Optional[str],
        identity_id: Optional[str],
        saving_customer: dict,
        saving_customer_identity: dict,
        saving_customer_individual_info: dict,
        saving_customer_resident_address: Optional[dict],  # CMND, CCCD mới có
        saving_customer_contact_address: Optional[dict],  # CMND, CCCD mới có
        saving_customer_compare_image: dict,
        saving_customer_identity_images: List[dict],
        log_data: json,
        session: Session
):

    new_first_identity_image_id = generate_uuid()  # ID ảnh mặt trước hoặc ảnh hộ chiếu
    new_second_identity_image_id = generate_uuid()  # ID ảnh mặt sau

    # Tạo mới
    if not customer_id:
        new_customer_id = generate_uuid()
        new_identity_id = generate_uuid()

        customer_id = new_customer_id  # Lấy id sau khi create thành công
        # create new Customer
        saving_customer['id'] = new_customer_id
        session.add(
            Customer(**saving_customer)
        )

        # create new CustomerIndividualInfo
        saving_customer_individual_info['customer_id'] = new_customer_id
        session.add(
            CustomerIndividualInfo(**saving_customer_individual_info)
        )

        # create new CustomerIdentity
        saving_customer_identity['id'] = new_identity_id
        saving_customer_identity['customer_id'] = new_customer_id
        session.add(
            CustomerIdentity(**saving_customer_identity)
        )
        await create_customer_identity_image_and_customer_compare_image(
            identity_id=new_identity_id,
            new_first_identity_image_id=new_first_identity_image_id,
            new_second_identity_image_id=new_second_identity_image_id,
            saving_customer_identity_images=saving_customer_identity_images,
            saving_customer_compare_image=saving_customer_compare_image,
            session=session
        )

        if identity_document_type_id != IDENTITY_DOCUMENT_TYPE_PASSPORT:
            # create new CustomerAddress for resident address
            saving_customer_resident_address['customer_id'] = new_customer_id
            session.add(
                CustomerAddress(**saving_customer_resident_address)
            )

            # create new CustomerAddress for contact address
            saving_customer_contact_address['customer_id'] = new_customer_id
            session.add(
                CustomerAddress(**saving_customer_contact_address)
            )

        new_transaction_id = generate_uuid()
        new_booking_id = generate_uuid()

        # create booking & log
        session.add_all([
            # Tạo BOOKING, CRM_TRANSACTION_DAILY -> CRM_BOOKING -> BOOKING_CUSTOMER -> BOOKING_BUSSINESS_FORM
            TransactionDaily(
                transaction_id=new_transaction_id,
                transaction_stage_id='BE_TEST',  # TODO
                data=log_data,
                transaction_root_id=new_transaction_id,
                description="Tạo CIF -> Thông tin cá nhân -> GTĐD -- Tạo mới",
                created_at=now(),
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

    # TODO: Lưu Log lịch sử thay đổi GTDD

    # Update
    else:
        # Cập nhật 1 cif_number đã tồn tại
        saving_customer_identity.update({
            "id": identity_id,
            "customer_id": customer_id
        })
        saving_customer_individual_info.update({"customer_id": customer_id})

        session.execute(update(Customer).filter(
            Customer.id == customer_id
        ).values(**saving_customer))

        session.execute(update(CustomerIdentity).filter(
            CustomerIdentity.customer_id == customer_id
        ).values(saving_customer_identity))

        session.execute(update(CustomerIndividualInfo).filter(
            CustomerIndividualInfo.customer_id == customer_id
        ).values(saving_customer_individual_info))

        # Passport thì không có địa chỉ
        if identity_document_type_id != IDENTITY_DOCUMENT_TYPE_PASSPORT:
            saving_customer_resident_address.update({"customer_id": customer_id})
            saving_customer_contact_address.update({"customer_id": customer_id})

            session.execute(update(CustomerAddress).filter(and_(
                CustomerAddress.customer_id == customer_id,
                CustomerAddress.address_type_id == RESIDENT_ADDRESS_CODE,
            )).values(saving_customer_resident_address))
            session.execute(update(CustomerAddress).filter(and_(
                CustomerAddress.customer_id == customer_id,
                CustomerAddress.address_type_id == CONTACT_ADDRESS_CODE,
            )).values(saving_customer_contact_address))

        # ảnh chụp giấy tờ
        saving_customer_compare_image['identity_id'] = identity_id

        for saving_customer_identity_image in saving_customer_identity_images:
            saving_customer_identity_image['identity_id'] = identity_id

        await create_customer_identity_image_and_customer_compare_image(
            identity_id=identity_id,
            new_first_identity_image_id=new_first_identity_image_id,
            new_second_identity_image_id=new_second_identity_image_id,
            saving_customer_identity_images=saving_customer_identity_images,
            saving_customer_compare_image=saving_customer_compare_image,
            session=session
        )

        await write_transaction_log_and_update_booking(
            description="Tạo CIF -> Thông tin cá nhân -> GTĐD -- Cập nhật",
            log_data=log_data,
            session=session,
            customer_id=customer_id
        )

    # TODO: Lưu Log lịch sử thay đổi GTDD

    return ReposReturn(data={
        "cif_id": customer_id
    })
########################################################################################################################


########################################################################################################################
# Repo khác
########################################################################################################################
async def repos_get_identity_information(customer_id: str, session: Session):
    identities = session.execute(
        select(
            Customer,
            CustomerIdentity,
            CustomerIndividualInfo,
            CustomerAddress
        )
        .join(CustomerIdentity, Customer.id == CustomerIdentity.customer_id)
        .join(CustomerIndividualInfo, Customer.id == CustomerIndividualInfo.customer_id)
        .join(CustomerAddress, Customer.id == CustomerAddress.customer_id)
        .filter(Customer.id == customer_id)
    ).all()

    if not identities:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc="cif_id")

    customer, customer_identity, customer_individual_info, _ = identities[0]
    customer_resident_address: Optional[CustomerAddress] = None
    customer_contact_address: Optional[CustomerAddress] = None
    for _, _, _, customer_address in identities:
        if customer_address.address_type_id == RESIDENT_ADDRESS_CODE:
            customer_resident_address = customer_address
        if customer_address.address_type_id == CONTACT_ADDRESS_CODE:
            customer_contact_address = customer_address

    return ReposReturn(data=(
        customer, customer_identity, customer_individual_info, customer_resident_address, customer_contact_address
    ))


async def create_customer_identity_image_and_customer_compare_image(
    identity_id,
    new_first_identity_image_id,
    new_second_identity_image_id,
    saving_customer_identity_images,
    saving_customer_compare_image,
    session: Session
):
    # create new CustomerIdentityImage ảnh mặt trước hoặc hộ chiếu
    saving_customer_identity_images[0]['id'] = new_first_identity_image_id
    saving_customer_identity_images[0]['identity_id'] = identity_id
    session.add(
        CustomerIdentityImage(**saving_customer_identity_images[0])
    )
    # create new CustomerIdentityImage ảnh mặt sau
    if len(saving_customer_identity_images) > 1:
        saving_customer_identity_images[1]['id'] = new_second_identity_image_id
        saving_customer_identity_images[1]['identity_id'] = identity_id
        session.add(
            CustomerIdentityImage(**saving_customer_identity_images[1])
        )
    # create new CustomerCompareImage
    saving_customer_compare_image['identity_id'] = identity_id
    saving_customer_compare_image['identity_image_id'] = new_first_identity_image_id
    session.add(
        CustomerCompareImage(**saving_customer_compare_image)
    )

    return None


########################################################################################################################
# Gọi qua eKYC để OCR giấy tờ định danh
########################################################################################################################
async def repos_upload_identity_document_and_ocr(
        identity_type: int,
        image_file: bytes,
        image_file_name: str,
        session: Session
):
    is_success, ocr_response = await service_ekyc.ocr_identity_document(
        file=image_file,
        filename=image_file_name,
        identity_type=identity_type
    )
    if not is_success:
        return ReposReturn(is_error=True, msg=ERROR_CALL_SERVICE, detail=ocr_response.get('message'))

    file_response = await service_file.upload_file(file=image_file, name=image_file_name)
    if not file_response:
        return ReposReturn(is_error=True, msg=ERROR_CALL_SERVICE, detail='Call to service file failed')

    if identity_type == EKYC_IDENTITY_TYPE_FRONT_SIDE_IDENTITY_CARD:
        response_data = await mapping_ekyc_front_side_identity_card_ocr_data(
            image_url=file_response['file_url'],
            ocr_data=ocr_response.get('data', {}),
            session=session
        )
    else:
        response_data = await mapping_ekyc_passport_ocr_data(
            image_url=file_response['file_url'],
            ocr_data=ocr_response.get('data', {}),
            session=session
        )

    return ReposReturn(data=response_data)


async def mapping_ekyc_front_side_identity_card_ocr_data(image_url: str, ocr_data: dict, session: Session):
    vietnamese_nationality = await repos_get_model_object_by_id_or_code(
        model_id=None,
        model_code='VN',  # TODO: tạo constant,
        model=AddressCountry,
        loc='nationality:VN',
        session=session
    )

    try:
        # TODO: tách tỉnh ra query. Hỏi thăm bên eKYC xem có case đặc biệt không
        place_of_origin = ocr_data.get('place_of_origin', ', ').split(', ')[-1]
    except ValueError:
        place_of_origin = None

    optional_place_of_origin = await repos_get_optional_model_object_by_code_or_name(
        model_name=place_of_origin,
        model=AddressProvince,
        session=session
    )

    try:
        number_and_street, ward, district, province = ocr_data.get('place_of_residence', ', , , ').split(', ')
    except ValueError:
        number_and_street = ward = district = province = ''

    optional_province = await repos_get_optional_model_object_by_code_or_name(
        model_name=province,
        model=AddressProvince,
        session=session
    )
    optional_district = await repos_get_optional_model_object_by_code_or_name(
        model_name=district,
        model=AddressDistrict,
        session=session
    )
    optional_ward = await repos_get_optional_model_object_by_code_or_name(
        model_name=ward,
        model=AddressWard,
        session=session
    )

    resident_address = {
        "province": dropdown(optional_province) if optional_province else None,
        "district": dropdown(optional_district) if optional_district else None,
        "ward": dropdown(optional_ward) if optional_ward else None,
        "number_and_street": number_and_street
    }

    front_side_identity_card_info = {
        "front_side_information": {
            "identity_image_url": image_url
        },
        "ocr_result": {
            "identity_document": {
                "identity_number": ocr_data.get('document_id'),
                "expired_date": ''  # TODO: có thể CMND 12 số có
            },
            "basic_information": {
                "full_name_vn": ocr_data.get('full_name'),
                "date_of_birth": date_string_to_other_date_string_format(ocr_data.get('date_of_birth'),
                                                                         from_format='%d-%m-%Y'),
                "nationality": dropdown(vietnamese_nationality),
                "province": dropdown(optional_place_of_origin) if optional_place_of_origin else None,
            },
            "address_information": {
                "resident_address": resident_address,
                "contact_address": resident_address
            }
        }
    }

    return front_side_identity_card_info


async def mapping_ekyc_passport_ocr_data(image_url: str, ocr_data: dict, session: Session):
    optional_place_of_issue = await repos_get_optional_model_object_by_code_or_name(
        model_name=ocr_data.get('place_of_issue'),
        model=PlaceOfIssue,
        session=session
    )

    optional_passport_code = await repos_get_optional_model_object_by_code_or_name(
        model_name=ocr_data.get('passport_code'),
        model=PassportCode,
        session=session
    )

    optional_gender = await repos_get_optional_model_object_by_code_or_name(
        model_code='NU' if ocr_data.get('gender') == 'F' else 'NAM',  # TODO: tự tạo constant
        model=CustomerGender,
        session=session
    )

    optional_nationality = await repos_get_optional_model_object_by_code_or_name(
        model_name=ocr_data.get('nationality', '/').split('/')[0],  # Việt Nam/Vietnamese
        model=AddressCountry,
        session=session
    )

    optional_place_of_birth = await repos_get_optional_model_object_by_code_or_name(
        model_name=ocr_data.get('place_of_origin'),  # Việt Nam/Vietnamese
        model=AddressProvince,
        session=session
    )

    passport_info = {
        "passport_information": {
            "identity_image_url": image_url
        },
        "ocr_result": {
            "identity_document":
                {
                    "identity_number": ocr_data.get('document_id'),
                    "issued_date": date_string_to_other_date_string_format(ocr_data.get('date_of_issue'),
                                                                           from_format='%d/%m/%Y'),
                    "place_of_issue": dropdown(optional_place_of_issue) if optional_place_of_issue else None,
                    "expired_date": date_string_to_other_date_string_format(ocr_data.get('date_of_expiry'),
                                                                            from_format='%d/%m/%Y'),
                    "passport_type": {  # TODO: chỗ này bên Ekyc chưa thấy trả vể
                        "id": "string",
                        "code": "string",
                        "name": "string"
                    },
                    "passport_code": dropdown(optional_passport_code) if optional_passport_code else None,
                },
            "basic_information":
                {
                    "full_name_vn": ocr_data.get('full_name'),
                    "gender": dropdown(optional_gender) if optional_gender else None,
                    "date_of_birth": date_string_to_other_date_string_format(ocr_data.get('date_of_birth'),
                                                                             from_format='%d/%m/%Y'),
                    "nationality": dropdown(optional_nationality) if optional_nationality else None,
                    "place_of_birth": dropdown(optional_place_of_birth) if optional_place_of_birth else None,
                    "identity_card_number": ocr_data.get('id_card_number'),
                    "mrz_content": f"{ocr_data.get('mrz_1', '')}\n{ocr_data.get('mrz_2', '')}"
                }
        }
    }

    return passport_info
