from sqlalchemy import and_, desc, select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.third_parties.oracle.models.cif.basic_information.identity.model import (
    CustomerCompareImage, CustomerIdentity
)
from app.third_parties.oracle.models.cif.basic_information.model import (
    Customer
)
from app.utils.error_messages import ERROR_CIF_ID_NOT_EXIST


async def repos_get_list_face(cif_id: str, session: Session) -> ReposReturn:
    query_data = session.execute(
        select(
            CustomerCompareImage
        ).join(
            CustomerIdentity, CustomerCompareImage.identity_id == CustomerIdentity.id
        ).join(
            Customer, and_(
                CustomerIdentity.customer_id == Customer.id,
                Customer.id == cif_id
            )
        ).order_by(desc(CustomerCompareImage.maker_at))
    ).scalars().all()

    if not query_data:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc="cif_id")

    faces = [
        {
            "maker_at": customer_compare_image.maker_at,
            "identity_image_id": customer_compare_image.id,
            "image_url": customer_compare_image.compare_image_url,
            "created_at": customer_compare_image.maker_at,
            "similar_percent": customer_compare_image.similar_percent
        } for customer_compare_image in query_data
    ]

    return ReposReturn(data=faces)
