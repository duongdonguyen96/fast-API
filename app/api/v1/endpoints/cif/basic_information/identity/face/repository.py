from sqlalchemy import desc, select

from app.api.base.repository import ReposReturn
from app.third_parties.oracle.models.cif.basic_information.identity.model import (
    CustomerCompareImage, CustomerIdentity, CustomerIdentityImage
)
from app.third_parties.oracle.models.cif.basic_information.model import (
    Customer
)
from app.utils.error_messages import ERROR_CIF_ID_NOT_EXIST
from app.utils.functions import datetime_to_date


async def repos_get_list_face(cif_id: str, session) -> ReposReturn:
    query_data = session.execute(
        select(
            Customer,
            CustomerIdentity,
            CustomerIdentityImage,
            CustomerCompareImage
        ).join(
            CustomerIdentity, Customer.id == CustomerIdentity.customer_id
        ).join(
            CustomerIdentityImage, CustomerIdentity.id == CustomerIdentityImage.identity_id
        ).join(
            CustomerCompareImage, CustomerIdentityImage.id == CustomerCompareImage.identity_image_id
        ).filter(Customer.id == cif_id).order_by(desc(CustomerIdentityImage.maker_at))
    ).all()

    if not query_data:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc="cif_id")

    data_response = []
    data = {}
    for customer, customer_identity, customer_identity_image, customer_compare_image in query_data:

        if data.get('created_date') == datetime_to_date(customer_identity_image.maker_at):
            data['faces'].append({
                "identity_image_id": customer_identity_image.id,
                "image_url": customer_identity_image.image_url,
                "created_at": customer_identity_image.maker_at,
                "similar_percent": customer_compare_image.similar_percent
            })
        else:
            data = {
                "created_date": datetime_to_date(customer_identity_image.maker_at),
                "faces": [
                    {
                        "identity_image_id": customer_identity_image.id,
                        "image_url": customer_identity_image.image_url,
                        "created_at": customer_identity_image.maker_at,
                        "similar_percent": customer_compare_image.similar_percent
                    }
                ]
            }
        if data not in data_response:
            data_response.append(data)

    return ReposReturn(data=data_response)
