from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.third_parties.oracle.models.master_data.identity import (
    CustomerIdentityType, CustomerSubIdentityType
)


async def repos_get_identity_document(session: Session) -> ReposReturn:

    identity_types = session.execute(select(CustomerIdentityType)).scalars().all()
    if not identity_types:
        return ReposReturn(is_error=True, msg="identity_type doesn't have data", loc='config')
    list_identity_type_config = [
        {
            "id": identity_type.id,
            "code": identity_type.code,
            "name": identity_type.name
        } for identity_type in identity_types
    ]

    return ReposReturn(data=list_identity_type_config)


async def repos_get_sub_identity_document(session: Session) -> ReposReturn:

    sub_identity_types = session.execute(select(CustomerSubIdentityType)).scalars().all()
    if not sub_identity_types:
        return ReposReturn(is_error=True, msg="sub_identity_type doesn't have data", loc='config')
    list_sub_identity_type_config = [
        {
            "id": sub_identity_type.id,
            "code": sub_identity_type.code,
            "name": sub_identity_type.name
        } for sub_identity_type in sub_identity_types
    ]

    return ReposReturn(data=list_sub_identity_type_config)
