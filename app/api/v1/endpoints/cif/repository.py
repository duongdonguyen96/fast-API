from typing import List

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.third_parties.oracle.models.cif.basic_information.identity.model import (
    CustomerIdentity
)
from app.third_parties.oracle.models.cif.basic_information.model import (
    Customer
)
from app.third_parties.oracle.models.master_data.customer import (
    CustomerClassification, CustomerEconomicProfession
)
from app.third_parties.oracle.models.master_data.identity import ImageType
from app.third_parties.oracle.models.master_data.others import KYCLevel
from app.utils.constant.cif import CIF_ID_TEST
from app.utils.error_messages import (
    ERROR_CIF_ID_NOT_EXIST, ERROR_CIF_NUMBER_EXIST, ERROR_CIF_NUMBER_NOT_EXIST
)
from app.utils.functions import dropdown


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


async def repos_get_cif_info(cif_id: str, session: Session) -> ReposReturn:
    customer_info = session.execute(
        select(
            Customer.cif_number,
            Customer.self_selected_cif_flag,
            CustomerClassification,
            CustomerEconomicProfession,
            CustomerEconomicProfession
        )
        .join(CustomerClassification, Customer.customer_classification_id == CustomerClassification.id)
        .join(CustomerEconomicProfession, Customer.customer_economic_profession_id == CustomerEconomicProfession.id)
        .join(KYCLevel, Customer.kyc_level_id == KYCLevel.id)
        .filter(
            Customer.id == cif_id,
            Customer.active_flag == 1
        )
    ).first()
    if not customer_info:
        return ReposReturn(
            is_error=True,
            msg=ERROR_CIF_ID_NOT_EXIST,
            loc='cif_id'
        )
    cif_number, self_selected_cif_flag, customer_classification, customer_economic_profession, kyc_level = customer_info
    return ReposReturn(data={
        "self_selected_cif_flag": self_selected_cif_flag,
        "cif_number": cif_number,
        "customer_classification": dropdown(customer_classification),
        "customer_economic_profession": dropdown(customer_economic_profession),
        "kyc_level": dropdown(kyc_level)
    })


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


async def repos_get_customer_identity(cif_id: str, session: Session):
    identity = session.execute(
        select(
            CustomerIdentity
        ).filter(CustomerIdentity.customer_id == cif_id).order_by(desc(CustomerIdentity.maker_at))
    ).scalars().first()

    if not identity:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc="cif_id")
    return ReposReturn(data=identity)


# TODO: replace with self.get_model_object_by_code
async def repos_get_image_type(image_type: str, session: Session) -> ReposReturn:
    image_type = session.execute(
        select(
            ImageType
        ).filter(ImageType.code == image_type)
    ).scalar()

    if not image_type:
        return ReposReturn(is_error=True, msg='ERROR_IMAGE_TYPE_NOT_EXIST', loc='image_type')

    return ReposReturn(data=image_type)


async def repos_check_not_exist_cif_number(cif_number: str, session: Session) -> ReposReturn:
    # TODO: call to core
    cif_number = session.execute(
        select(
            Customer.cif_number
        ).filter(Customer.cif_number == cif_number)
    ).scalars().first()

    if cif_number:
        return ReposReturn(is_error=True, msg=ERROR_CIF_NUMBER_EXIST, loc="cif_number")

    return ReposReturn(data='Cif number is not exist')


async def repos_get_customers_by_cif_numbers(
        cif_numbers: List[str],
        session: Session
) -> ReposReturn:
    customers = session.execute(
        select(
            Customer
        ).filter(Customer.cif_number.in_(cif_numbers))
    ).scalars().all()

    if not customers or len(cif_numbers) != len(customers):
        return ReposReturn(
            is_error=True,
            msg=ERROR_CIF_NUMBER_NOT_EXIST,
            loc="cif_number"
        )

    return ReposReturn(data=customers)
