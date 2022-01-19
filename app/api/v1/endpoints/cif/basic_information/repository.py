from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.settings.event import service_soa
from app.third_parties.oracle.models.cif.basic_information.guardian_and_relationship.model import (
    CustomerPersonalRelationship
)


async def repos_get_customer_detail(
        cif_number: str
):
    is_success, customer_detail = await service_soa.retrieve_customer_ref_data_mgmt(cif_number=cif_number)

    if not is_success:
        return ReposReturn(is_error=True, msg=customer_detail["message"])

    return ReposReturn(data=customer_detail)


async def repos_get_customer_personal_relationships(
        session: Session,
        relationship_type: int,
        cif_id: str
):
    return session.execute(
        select(
            CustomerPersonalRelationship
        ).filter(
            CustomerPersonalRelationship.type == relationship_type,
            CustomerPersonalRelationship.customer_id == cif_id
        )).scalars().all()
