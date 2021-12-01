from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.third_parties.oracle.models.cif.basic_information.identity.model import (
    CustomerIdentityImage, CustomerSubIdentity
)
from app.third_parties.oracle.models.master_data.identity import (
    CustomerSubIdentityType, PlaceOfIssue
)
from app.utils.constant.cif import CIF_ID_TEST
from app.utils.error_messages import ERROR_CIF_ID_NOT_EXIST
from app.utils.functions import dropdown, now

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


async def repos_get_detail_sub_identity(cif_id: str, session: Session):
    sub_identities = session.execute(
        select(
            CustomerSubIdentity,
            CustomerSubIdentityType,
            PlaceOfIssue,
            CustomerIdentityImage
        )
        .join(CustomerSubIdentityType, CustomerSubIdentity.sub_identity_type_id == CustomerSubIdentityType.id)
        .join(PlaceOfIssue, CustomerSubIdentity.place_of_issue_id == PlaceOfIssue.id)
        .join(CustomerIdentityImage, CustomerSubIdentity.id == CustomerIdentityImage.identity_id)
        .filter(CustomerSubIdentity.customer_id == cif_id)
    ).all()
    data = []
    for sub_identity, sub_identity_type, place_of_issue, customer_identity_image in sub_identities:
        data.append({
            "id": sub_identity.id,
            "name": sub_identity.name,
            "sub_identity_document_type": dropdown(sub_identity_type),
            "sub_identity_document_image_url": customer_identity_image.image_url,
            "ocr_result": {
                "sub_identity_number": sub_identity.number,
                "symbol": sub_identity.symbol,
                "full_name_vn": sub_identity.full_name,
                "date_of_birth": sub_identity.date_of_birth,
                "passport_number": sub_identity.passport_number,
                "place_of_issue": dropdown(place_of_issue),
                "expired_date": sub_identity.sub_identity_expired_date,
                "issued_date": sub_identity.issued_date
            }
        })
    return ReposReturn(data=data)


async def repos_save(cif_id, requests, created_by):
    return ReposReturn(data={
        "cif_id": cif_id,
        "created_at": now(),
        "created_by": created_by
    })


async def repos_get_list_log(cif_id: str) -> ReposReturn:
    if cif_id != CIF_ID_TEST:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc='cif_id')

    return ReposReturn(data=SUB_IDENTITY_LOGS_INFO)
