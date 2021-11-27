from loguru import logger
from sqlalchemy import delete, select

from app.api.base.repository import ReposReturn
from app.third_parties.oracle.models.cif.basic_information.identity.model import (
    CustomerIdentityImage, CustomerSubIdentity
)
from app.utils.constant.cif import CIF_ID_TEST, IMAGE_TYPE_SUB_IDENTITY
from app.utils.error_messages import ERROR_CIF_ID_NOT_EXIST
from app.utils.functions import generate_uuid, now

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


async def repos_save_sub_identity(customer, requests, saved_by, session):

    sub_identities = session.execute(
        select(
            CustomerSubIdentity
        ).filter(
            CustomerSubIdentity.customer_id == customer.id
        )
    ).scalars().all()

    sub_identity_list = []
    sub_identity_image_list = []
    for sub_identity in requests:
        sub_identity_id = generate_uuid()
        # Tạo giấy tờ định danh phụ
        sub_identity_list.append(CustomerSubIdentity(
            id=sub_identity_id,
            sub_identity_type_id=sub_identity.sub_identity_document_type.id,
            name=sub_identity.name,
            number=sub_identity.ocr_result.sub_identity_number,
            symbol=sub_identity.ocr_result.symbol,
            full_name=sub_identity.ocr_result.full_name_vn,
            date_of_birth=sub_identity.ocr_result.date_of_birth,
            passport_number=sub_identity.ocr_result.passport_number,
            issued_date=sub_identity.ocr_result.issued_date,
            sub_identity_expired_date=sub_identity.ocr_result.expired_date,
            place_of_issue_id=sub_identity.ocr_result.place_of_issue.id,
            customer_id=customer.id,
            maker_at=now(),
            maker_id=saved_by,
            updater_at=now(),
            updater_id=saved_by
        ))

        # Tạo hình ảnh giấy tờ định danh phụ
        sub_identity_image_list.append(CustomerIdentityImage(
            identity_id=sub_identity_id,
            image_type_id=IMAGE_TYPE_SUB_IDENTITY,
            image_url=sub_identity.sub_identity_document_image_url,
            maker_id=saved_by,
            maker_at=now(),
            updater_id=saved_by,
            updater_at=now()
        ))

    session.autoflush = False
    try:
        if not sub_identities:
            session.bulk_save_objects(sub_identity_list)
            session.flush()
            session.bulk_save_objects(sub_identity_image_list)
            session.flush()
        else:
            # Lấy id của GTĐD đã tồn tại trong DB
            sub_identities = session.execute(select(CustomerSubIdentity).filter(
                CustomerSubIdentity.customer_id == customer.id)
            ).scalars().all()
            sub_identity_ids = [sub_identity.id for sub_identity in sub_identities]
            session.execute(delete(CustomerIdentityImage).filter(
                CustomerIdentityImage.identity_id.in_(sub_identity_ids)
            ))
            session.flush()
            session.execute(delete(CustomerSubIdentity).filter(CustomerSubIdentity.customer_id == customer.id))
            session.flush()
            session.bulk_save_objects(sub_identity_list)
            session.flush()
            session.bulk_save_objects(sub_identity_image_list)
            session.flush()
        session.commit()
    except Exception as ex:
        logger.debug(ex)
        return ReposReturn(is_error=True, msg="Save Sub Identity is not success")

    return ReposReturn(data={
        "cif_id": customer.id,
        "created_at": now(),
        "created_by": saved_by
    })


async def repos_get_list_log(cif_id: str) -> ReposReturn:
    if cif_id != CIF_ID_TEST:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc='cif_id')

    return ReposReturn(data=SUB_IDENTITY_LOGS_INFO)
