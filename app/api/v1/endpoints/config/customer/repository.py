from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.third_parties.oracle.models.master_data.customer import (
    CustomerContactType, CustomerType
)


async def repos_get_customer_type(session: Session) -> ReposReturn:

    customer_types = session.execute(select(CustomerType)).scalars().all()
    if not customer_types:
        return ReposReturn(is_error=True, msg="customer_type doesn't have data", loc='config')
    list_customer_type_config = [
        {
            "id": customer_type.id,
            "code": customer_type.code,
            "name": customer_type.name
        } for customer_type in customer_types
    ]

    return ReposReturn(data=list_customer_type_config)


async def repos_get_customer_contact_type(session: Session) -> ReposReturn:

    customer_contact_types = session.execute(select(CustomerContactType)).scalars().all()
    if not customer_contact_types:
        return ReposReturn(is_error=True, msg="customer_contact_type doesn't have data", loc='config')
    list_customer_contact_type_config = [
        {
            "id": customer_contact_type.id,
            "code": customer_contact_type.code,
            "name": customer_contact_type.name
        } for customer_contact_type in customer_contact_types
    ]

    return ReposReturn(data=list_customer_contact_type_config)
