from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.api.v1.endpoints.cif.basic_information.identity.signature.schema import (
    SignaturesRequest
)
from app.third_parties.oracle.models.cif.basic_information.identity.model import (
    CustomerIdentity, CustomerIdentityImage
)
from app.third_parties.oracle.models.cif.basic_information.model import (
    Customer
)
from app.utils.constant.cif import CIF_ID_TEST
from app.utils.error_messages import (
    ERROR_CIF_ID_NOT_EXIST, ERROR_SIGNATURE_IS_NULL
)
from app.utils.functions import datetime_to_date, now


async def repos_save_signature(cif_id: str, signature: SignaturesRequest, created_by: str) -> ReposReturn:
    if cif_id != CIF_ID_TEST:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc='cif_id')

    return ReposReturn(data={
        "cif_id": cif_id,
        "created_at": now(),
        "created_by": created_by
    })


async def repos_get_signature_data(cif_id: str, session: Session) -> ReposReturn:
    query_cif_id = session.execute(select(Customer).filter(Customer.id == cif_id)).scalar()

    if not query_cif_id:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc=f"{cif_id} is exist")

    query_data = session.execute(
        select(
            CustomerIdentity,
            CustomerIdentityImage
        ).join(
            CustomerIdentityImage, and_(
                CustomerIdentity.id == CustomerIdentityImage.identity_id,
                CustomerIdentityImage.finger_type_id.is_(None),
                CustomerIdentityImage.hand_side_id.is_(None),
                CustomerIdentityImage.vector_data.is_(None)
            )
        ).filter(
            CustomerIdentity.customer_id == cif_id
        )
    ).all()

    if not query_data:
        return ReposReturn(is_error=True, msg=ERROR_SIGNATURE_IS_NULL, loc=f"cif_id:{cif_id} -> signature")

    date__signature = {}
    for _, customer_identity_image in query_data:
        date_str = datetime_to_date(customer_identity_image.maker_at)

        if date_str not in date__signature:
            date__signature[date_str] = []

        date__signature[date_str].append(
            {
                'identity_image_id': customer_identity_image.id,
                'image_url': customer_identity_image.image_url,
                'active_flag': customer_identity_image.active_flag
            }
        )

    data_response = [{
        'created_date': data_str,
        'signature': signature
    } for data_str, signature in date__signature.items()]

    return ReposReturn(data=data_response)
