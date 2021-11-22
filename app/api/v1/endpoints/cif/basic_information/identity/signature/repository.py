from typing import List

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.third_parties.oracle.models.cif.basic_information.identity.model import (
    CustomerIdentity, CustomerIdentityImage
)
from app.third_parties.oracle.models.master_data.identity import ImageType
from app.utils.constant.cif import CIF_ID_TEST, IMAGE_TYPE_SIGNATURE
from app.utils.error_messages import (
    ERROR_CIF_ID_NOT_EXIST, ERROR_IMAGE_TYPE_NOT_EXIST
)
from app.utils.functions import now


async def repos_get_type_id(session: Session) -> ReposReturn:
    query_data = session.execute(
        select(
            ImageType
        ).filter(ImageType.code == IMAGE_TYPE_SIGNATURE)
    ).scalars().first()

    if not query_data:
        return ReposReturn(is_error=True, msg=ERROR_IMAGE_TYPE_NOT_EXIST, loc='image_type')

    return ReposReturn(data=query_data)


async def repos_get_identity_id(cif_id: str, session: Session) -> ReposReturn:
    query_data = session.execute(
        select(
            CustomerIdentity
        ).filter(CustomerIdentity.customer_id == cif_id).order_by(desc(CustomerIdentity.maker_at))
    ).scalars().first()

    if not query_data:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc='cif_id')

    return ReposReturn(data=query_data)


async def repos_save_signature(cif_id: str, list_data_insert: List, session: Session, created_by: str) -> ReposReturn:
    try:
        data_insert = [CustomerIdentityImage(**data_insert) for data_insert in list_data_insert]
        session.bulk_save_objects(data_insert)
        session.commit()
    except Exception as ex:
        return ReposReturn(is_error=True, msg='ERROR_CAN_NOT_CREATE', loc=f'{ex}')

    return ReposReturn(data={
        "cif_id": cif_id,
        "created_at": now(),
        "created_by": created_by
    })


async def repos_get_signature_data(cif_id: str) -> ReposReturn:
    if cif_id != CIF_ID_TEST:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc='cif_id')

    return ReposReturn(data={
        "customer_signatures": [
            {
                "created_date": "2021-06-12",
                "identity_image_transaction_1": "http://example.com/abc.png",
                "identity_image_transaction_2": "http://example.com/abc.png",
                "checked_flag": True
            },
            {
                "created_date": "2021-05-30",
                "identity_image_transaction_1": "http://example.com/abc.png",
                "identity_image_transaction_2": "http://example.com/abc.png",
                "checked_flag": False
            }
        ],
        "compare_signature": {
            "compare_image_url": "http://example.com/abc.png",
            "similar_percent": 94
        }
    })
