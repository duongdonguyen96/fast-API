import uuid
from typing import List

from loguru import logger
from sqlalchemy import and_, desc, select, update
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import now

from app.api.base.repository import ReposReturn
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
from app.third_parties.oracle.models.master_data.identity import ImageType
from app.third_parties.oracle.models.master_data.others import HrmEmployee
from app.utils.constant.cif import (
    ACTIVED, CIF_ID_TEST, CONTACT_ADDRESS_CODE, IDENTITY_IMAGE_FLAG_BACKSIDE,
    IDENTITY_IMAGE_FLAG_FRONT_SIDE, IMAGE_TYPE_CODE_IDENTITY,
    RESIDENT_ADDRESS_CODE, UNSAVED
)
from app.utils.error_messages import ERROR_CIF_ID_NOT_EXIST


async def repos_get_initializing_customer(cif_id: str, session: Session) -> ReposReturn:
    customer = session.execute(
        select(
            Customer
        ).filter(
            Customer.id == cif_id,
            Customer.complete_flag == 0
        )
    ).scalar()
    if not customer:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc='cif_id')

    return ReposReturn(data=customer)


async def repos_get_hrm_employees(hrm_employee_ids: List[str], session: Session) -> ReposReturn:
    hrm_employees = session.execute(
        select(
            HrmEmployee
        ).filter(
            HrmEmployee.id.in_(hrm_employee_ids)
        )
    ).scalars().all()
    if len(hrm_employees) != len(hrm_employee_ids):
        return ReposReturn(is_error=True, detail="employee is not exist", loc="staff_id")

    return ReposReturn(data=hrm_employees)


async def repos_get_cif_info(cif_id: str) -> ReposReturn:
    if cif_id == CIF_ID_TEST:
        return ReposReturn(data={
            "self_selected_cif_flag": True,
            "cif_number": "123456789",
            "customer_classification": {
                "id": "fd01b796-5ad1-4161-8e2c-2abe41390deb",
                "code": "CN",
                "name": "Cá nhân"
            },
            "customer_economic_profession": {
                "id": "b860d25e-0db2-496b-8bb7-76d6838d191a",
                "code": "KT1",
                "name": "Mã ngành KT"
            },
            "kyc_level": {
                "id": "24152d4a-13c8-4720-a92d-2f2e784af6af",
                "code": "LV1",
                "name": "Level 1"
            }
        }
        )
    else:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc='cif_id')


async def repos_profile_history(cif_id: str) -> ReposReturn:
    if cif_id == CIF_ID_TEST:
        return ReposReturn(data=[
            {

                "created_date": "string",
                "logs":

                    [

                        {
                            "user_id": "string",
                            "full_name": "string",
                            "user_avatar_url": "string",
                            "id": "string",
                            "created_at": "2019-08-24T14:15:22Z",
                            "content": "string"
                        },
                        {
                            "user_id": "string",
                            "full_name": "string",
                            "user_avatar_url": "string",
                            "id": "string",
                            "created_at": "2019-08-24T14:15:22Z",
                            "content": "string"
                        }
                    ]

            },
            {

                "created_date": "string",
                "logs":

                    [

                        {
                            "user_id": "string",
                            "full_name": "string",
                            "user_avatar_url": "string",
                            "id": "string",
                            "created_at": "2019-08-24T14:15:22Z",
                            "content": "string"
                        },
                        {
                            "user_id": "string",
                            "full_name": "string",
                            "user_avatar_url": "string",
                            "id": "string",
                            "created_at": "2019-08-24T14:15:22Z",
                            "content": "string"
                        }
                    ]
            }
        ]
        )
    else:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc='cif_id')


async def repos_customer_information(cif_id: str) -> ReposReturn:
    if cif_id != CIF_ID_TEST:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc='cif_id')

    return ReposReturn(data={
        "customer_id": "1",
        "status": {
            "id": "1",
            "code": "code",
            "name": "MỞ",
            "active_flag": True
        },
        "cif_number": "2541352",
        "avatar_url": "http://example.com/example.jpg",
        "customer_classification": {
            "id": "1",
            "code": "CANHAN",
            "name": "Cá nhân"
        },
        "full_name": "TRAN MINH HUYEN",
        "gender": {
            "id": "1",
            "code": "NU",
            "name": "Nữ"
        },
        "email": "nhuxuanlenguyen153@gmail.com",
        "mobile_number": "0896524256",
        "identity_number": "079197005869",
        "place_of_issue": {
            "id": "1",
            "code": "HCM",
            "name": "TPHCM"
        },
        "issued_date": "2019-02-02",
        "expired_date": "2032-02-02",
        "date_of_birth": "2002-02-02",
        "nationality": {
            "id": "1",
            "code": "VN",
            "name": "VIỆT NAM"
        },
        "marital_status": {
            "id": "1",
            "code": "DOCTHAN",
            "name": "Độc thân"
        },
        "customer_class": {
            "id": "1",
            "code": "DIAMOND",
            "name": "Diamond"
        },
        "credit_rating": {
            "id": "1",
            "code": "CODE",
            "name": "BBB"
        },
        "address": "144 Nguyễn Thị Minh Khai, Phường Bến Nghé, Quận 1, TPHCM",
        "total_number_of_participant": 3,
        "employees": [
            {
                "id": "1",
                "full_name_vn": "AAAAAA",
                "avatar_url": "http://example.com/example.jpg",
                "user_name": "username",
                "email": "asdfgh@gmail.com",
                "job_title": "chức danh",
                "department_id": "Khối VH&CN"
            },
            {
                "id": "2",
                "full_name_vn": "AAAAAA",
                "avatar_url": "http://example.com/example.jpg",
                "user_name": "username",
                "email": "asdfgh@gmail.com",
                "job_title": "chức danh",
                "department_id": "Khối VH&CN"
            },
            {
                "id": "3",
                "full_name_vn": "AAAAAA",
                "avatar_url": "http://example.com/example.jpg",
                "user_name": "username",
                "email": "asdfgh@gmail.com",
                "job_title": "chức danh",
                "department_id": "Khối VH&CN"
            }
        ]
    })


async def repos_get_last_identity(cif_id: str, session: Session):
    identity = session.execute(
        select(
            CustomerIdentity
        ).filter(CustomerIdentity.customer_id == cif_id).order_by(desc(CustomerIdentity.maker_at))
    ).scalars().first()

    if not identity:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc="cif_id")
    return ReposReturn(data=identity)


async def repos_get_image_type(image_type: str, session: Session) -> ReposReturn:
    image_type = session.execute(
        select(
            ImageType
        ).filter(ImageType.code == image_type)
    ).scalar()

    if not image_type:
        return ReposReturn(is_error=True, msg='ERROR_IMAGE_TYPE_NOT_EXIST', loc='image_type')

    return ReposReturn(data=image_type)


async def repos_update_basic_information_identity(
        customer: Customer,
        customer_identity: dict,
        customer_individual_info: dict,
        customer_resident_address: dict,
        customer_contact_address: dict,
        saving_customer: dict,
        session: Session
):
    try:
        customer_id = customer.id
        customer_identity.update({"customer_id": customer.id})
        customer_individual_info.update({"customer_id": customer.id})
        customer_resident_address.update({"customer_id": customer.id})
        customer_contact_address.update({"customer_id": customer.id})
        session.execute(update(Customer).where(
            Customer.id == customer.id
        ).values(**saving_customer))
        session.execute(update(CustomerIdentity).where(
            CustomerIdentity.customer_id == customer.id
        ).values(customer_identity))
        session.execute(update(CustomerIndividualInfo).where(
            CustomerIndividualInfo.customer_id == customer.id
        ).values(customer_individual_info))
        session.execute(update(CustomerAddress).where(and_(
            CustomerAddress.customer_id == customer.id,
            CustomerAddress.address_type_id == RESIDENT_ADDRESS_CODE,
        )).values(customer_resident_address))
        session.execute(update(CustomerAddress).where(and_(
            CustomerAddress.customer_id == customer.id,
            CustomerAddress.address_type_id == CONTACT_ADDRESS_CODE,
        )).values(customer_contact_address))

        # Tạo BOOKING, CRM_TRANSACTION_DAILY -> CRM_BOOKING -> BOOKING_CUSTOMER -> BOOKING_BUSSINESS_FORM
        transaction_id = str(uuid.uuid4())
        booking_id = str(uuid.uuid4())
        session.add_all([
            TransactionDaily(
                transaction_id=transaction_id,
                data=None,
                description="Tạo CIF -> Thông tin cá nhân -> GTĐD -- Cập nhật",
                updated_at=now()
            ),
            Booking(
                id=booking_id,
                transaction_id=transaction_id,
                created_at=now(),
                updated_at=now()
            ),
            BookingCustomer(
                booking_id=booking_id,
                customer_id=customer_id
            ),
            BookingBusinessForm(
                booking_id=booking_id,
                business_form_id="BE_TEST",  # TODO
                save_flag=UNSAVED,
                created_at=now(),
                updated_at=now()
            )
        ])

        session.commit()
        return customer_id
    except Exception as ex:
        logger.debug(ex)
        session.rollback()
        return ReposReturn(is_error=True, msg="Update customer is not success", loc="cif_number")


async def repos_create_basic_information_identity(
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
):
    self_selected_cif_flag = 0

    if not cif_number:
        self_selected_cif_flag = 1

    # Tạo thông tin KH
    saving_customer.update({
        "cif_number": cif_number,
        "self_selected_cif_flag": self_selected_cif_flag
    })
    new_customer = Customer(**saving_customer)

    try:
        session.begin_nested()
        session.add(new_customer)
        session.commit()
        session.refresh(new_customer)
        customer_id = new_customer.id

        customer_individual_info.update({"customer_id": customer_id})
        customer_resident_address.update({"customer_id": customer_id})
        customer_contact_address.update({"customer_id": customer_id})

        customer_identity.update({"customer_id": customer_id})
        new_identity = CustomerIdentity(**customer_identity)
        session.add(new_identity)
        session.commit()
        session.refresh(new_identity)
        identity_id = new_identity.id

        new_front_side_identity_image = CustomerIdentityImage(**{
            "identity_id": identity_id,
            "image_type_id": IMAGE_TYPE_CODE_IDENTITY,
            "image_url": front_side_information_identity_image_url,
            "hand_side_id": None,
            "finger_type_id": None,
            "vector_data": None,
            "active_flag": ACTIVED,
            "maker_id": save_by,
            "maker_at": now(),
            "updater_id": save_by,
            "updater_at": now(),
            "identity_image_front_flag": IDENTITY_IMAGE_FLAG_FRONT_SIDE
        })
        session.add(new_front_side_identity_image)
        session.commit()
        session.refresh(new_front_side_identity_image)
        front_side_identity_image_id = new_front_side_identity_image.id
        front_side_identity_compare_image = {
            "identity_id": identity_id,
            "identity_image_id": front_side_identity_image_id,
            "compare_image_url": front_side_information_compare_image_url,
            "similar_percent": 00,
            "maker_id": save_by,
            "maker_at": now()
        }
        back_side_information_identity = {
            "identity_id": identity_id,
            "image_type_id": IMAGE_TYPE_CODE_IDENTITY,
            "image_url": back_side_information_identity_image_url,
            "hand_side_id": None,
            "finger_type_id": None,
            "vector_data": None,
            "active_flag": ACTIVED,
            "maker_id": save_by,
            "maker_at": now(),
            "updater_id": save_by,
            "updater_at": now(),
            "identity_image_front_flag": IDENTITY_IMAGE_FLAG_BACKSIDE
        }
        session.add_all([
            CustomerIndividualInfo(**customer_individual_info),
            CustomerAddress(**customer_resident_address),
            CustomerAddress(**customer_contact_address),
            CustomerCompareImage(**front_side_identity_compare_image),
            CustomerIdentityImage(**back_side_information_identity)
        ])

        # Tạo BOOKING, CRM_TRANSACTION_DAILY -> CRM_BOOKING -> BOOKING_CUSTOMER -> BOOKING_BUSSINESS_FORM
        transaction_id = str(uuid.uuid4())
        booking_id = str(uuid.uuid4())

        session.add_all([
            TransactionDaily(
                transaction_id=transaction_id,
                data=None,
                description="Tạo CIF -> Thông tin cá nhân -> GTĐD -- Tạo mới",
                updated_at=now()
            ),
            Booking(
                id=booking_id,
                transaction_id=transaction_id,
                created_at=now(),
                updated_at=now()
            ),
            BookingCustomer(
                booking_id=booking_id,
                customer_id=customer_id
            ),
            BookingBusinessForm(
                booking_id=booking_id,
                business_form_id="BE_TEST",  # TODO
                save_flag=UNSAVED,
                created_at=now(),
                updated_at=now()
            )
        ])
        session.commit()
        return customer_id
    except Exception as ex:
        logger.debug(ex)
        session.rollback()
        return ReposReturn(is_error=True, msg="Create new customer is not success", loc="cif_number")
