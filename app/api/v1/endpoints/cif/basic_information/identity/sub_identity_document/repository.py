from typing import List

from sqlalchemy import and_, delete, select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn, auto_commit
from app.third_parties.oracle.models.cif.basic_information.identity.model import (
    CustomerIdentityImage, CustomerSubIdentity
)
from app.third_parties.oracle.models.cif.basic_information.model import (
    Customer
)
from app.utils.constant.cif import CIF_ID_TEST, IMAGE_TYPE_CODE_SUB_IDENTITY
from app.utils.error_messages import ERROR_CIF_ID_NOT_EXIST

SUB_IDENTITY_INFO = [
    {
        "id": "1",
        "name": "Giấy tờ định danh phụ 1",
        "sub_identity_document_type": {
            "id": "1",
            "code": "THETAMTRU",
            "name": "Thẻ tạm trú"
        },
        "sub_identity_document_image_url": "http://example.com/example.jpg",
        "ocr_result": {
            "sub_identity_number": "361963424",
            "symbol": "LĐ",
            "full_name_vn": "Nguyễn Văn A",
            "date_of_birth": "1990-08-12",
            "province": {
                "id": "2",
                "code": "HN",
                "name": "Hà Nội"
            },
            "place_of_issue": {
                "id": "2",
                "code": "HCDS",
                "name": "Cục hành chính về trật tự xã hội"
            },
            "expired_date": "2021-02-07",
            "issued_date": "2021-02-07"
        }
    }
]
SUB_IDENTITY_LOGS_INFO = [
    {
        "reference_flag": True,
        "created_date": "2021-02-18",
        "identity_document_type": {
            "id": "1",
            "code": "THETAMTRU1",
            "name": "Thẻ tạm trú 1"
        },
        "identity_images": [
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
            "code": "THETAMTRU2",
            "name": "Thẻ tạm trú 2"
        },
        "identity_images": [
            {
                "image_url": "https://example.com/example.jpg"
            }
        ]
    }
]


async def repos_get_detail(cif_id: str):
    if cif_id != CIF_ID_TEST:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc='cif_id')
    return ReposReturn(data=SUB_IDENTITY_INFO)


@auto_commit
async def repos_save_sub_identity(
        customer: Customer,
        delete_sub_identity_list_ids: List,
        create_sub_identity_list: List,
        create_sub_identity_image_list: List,
        update_sub_identity_list: List,
        update_sub_identity_image_list: List,
        session: Session
):

    # Xóa
    session.execute(delete(CustomerIdentityImage).filter(
        and_(
            CustomerIdentityImage.identity_id.in_(delete_sub_identity_list_ids),
            CustomerIdentityImage.image_type_id == IMAGE_TYPE_CODE_SUB_IDENTITY
        )
    ))
    session.execute(delete(CustomerSubIdentity).filter(
        CustomerSubIdentity.id.in_(delete_sub_identity_list_ids)
    ))

    # Tạo giấy tờ định danh phụ
    session.bulk_save_objects(create_sub_identity_list)
    session.bulk_save_objects(create_sub_identity_image_list)

    # Cập nhật
    session.bulk_save_objects(update_sub_identity_list)
    session.bulk_save_objects(update_sub_identity_image_list)

    return ReposReturn(data={
        "cif_id": customer.id
    })


async def repos_get_list_log(cif_id: str) -> ReposReturn:
    if cif_id != CIF_ID_TEST:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc='cif_id')

    return ReposReturn(data=SUB_IDENTITY_LOGS_INFO)


########################################################################################################################
# Other
########################################################################################################################
async def repos_get_sub_identities(customer_id: str, session: Session):
    sub_identities = session.execute(
        select(
            CustomerSubIdentity
        ).filter(
            CustomerSubIdentity.customer_id == customer_id
        )
    ).scalars()
    return ReposReturn(data=sub_identities)
