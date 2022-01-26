from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.third_parties.oracle.models.master_data.customer import (
    CustomerContactType
)
from app.utils.constant.cif import CUSTOMER_CONTACT_TYPE_GROUP


async def repos_get_customer_contact_type(group: str, session: Session):
    customer_contact_type_infos = session.execute(
        select(CustomerContactType)
        .filter(
            CustomerContactType.group == group
        )
    ).scalars().all()

    if not customer_contact_type_infos:
        return ReposReturn(is_error=True, msg="Customer Contact Type Group must be one of follow string: "
                                              f"{CUSTOMER_CONTACT_TYPE_GROUP}")

    return ReposReturn(data=[{
        "id": customer_contact_type_info.id,
        "code": customer_contact_type_info.id,
        "name": customer_contact_type_info.name
    } for customer_contact_type_info in customer_contact_type_infos])
