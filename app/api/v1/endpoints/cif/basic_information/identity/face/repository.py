from sqlalchemy import and_, desc, select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.third_parties.oracle.models.cif.basic_information.identity.model import (
    CustomerCompareImage, CustomerIdentity, CustomerIdentityImage
)
from app.third_parties.oracle.models.cif.basic_information.model import (
    Customer
)
from app.utils.error_messages import ERROR_CIF_ID_NOT_EXIST


async def repos_get_list_face(cif_id: str, session: Session) -> ReposReturn:
    query_data = session.execute(
        select(
            Customer,
            CustomerIdentity,
            CustomerIdentityImage,
            CustomerCompareImage
        ).join(
            CustomerIdentity, Customer.id == CustomerIdentity.customer_id
        ).join(
            CustomerIdentityImage, and_(
                CustomerIdentity.id == CustomerIdentityImage.identity_id,
                CustomerIdentityImage.finger_type_id.is_(None),
                CustomerIdentityImage.hand_side_id.is_(None)
            )
        ).join(
            CustomerCompareImage, CustomerIdentityImage.id == CustomerCompareImage.identity_image_id
        ).filter(
            Customer.id == cif_id
        ).order_by(desc(CustomerIdentityImage.maker_at))
    ).all()

    if not query_data:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc="cif_id")

    faces = [
        {
            "maker_at": customer_identity_image.maker_at,
            "identity_image_id": customer_identity_image.id,
            "image_url": customer_identity_image.image_url,
            "created_at": customer_identity_image.maker_at,
            "similar_percent": customer_compare_image.similar_percent
        } for _, _, customer_identity_image, customer_compare_image in query_data
    ]

    return ReposReturn(data=faces)
