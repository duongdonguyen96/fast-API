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
from app.utils.functions import datetime_to_date


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

    date__faces = {}
    for _, _, customer_identity_image, customer_compare_image in query_data:
        date_str = datetime_to_date(customer_identity_image.maker_at)
        if date_str not in date__faces:
            date__faces[date_str] = []

        date__faces[date_str].append(
            {
                "identity_image_id": customer_identity_image.id,
                "image_url": customer_identity_image.image_url,
                "created_at": customer_identity_image.maker_at,
                "similar_percent": customer_compare_image.similar_percent
            }
        )

    data_response = [{
        'created_date': data_str,
        'faces': faces
    } for data_str, faces in date__faces.items()]

    return ReposReturn(data=data_response)
