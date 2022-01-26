from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.third_parties.oracle.models.master_data.customer import (
    CustomerContactType
)


async def repos_get_customer_contact_type(session: Session):
    customer_contact_type_infos = session.execute(select(CustomerContactType)).scalars().all()

    return ReposReturn(data=[{
        "id": customer_contact_type_info.id,
        "code": customer_contact_type_info.name,
        "name": customer_contact_type_info.description
    } for customer_contact_type_info in customer_contact_type_infos])
