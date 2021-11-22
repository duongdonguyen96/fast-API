from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.third_parties.oracle.models.cif.basic_information.model import Customer
from app.utils.constant.cif import CIF_ID_TEST
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
