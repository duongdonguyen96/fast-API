from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.api.v1.endpoints.cif.basic_information.identity.fingerprint.schema import (
    TwoFingerPrintRequest
)
from app.third_parties.oracle.models.cif.basic_information.identity.model import (
    CustomerIdentity, CustomerIdentityImage
)
from app.third_parties.oracle.models.cif.basic_information.model import (
    Customer
)
from app.third_parties.oracle.models.master_data.identity import (
    FingerType, HandSide
)
from app.utils.constant.cif import CIF_ID_TEST
from app.utils.error_messages import ERROR_CIF_ID_NOT_EXIST
from app.utils.functions import now


async def repos_save_fingerprint(cif_id: str, finger_request: TwoFingerPrintRequest, created_by: str):
    if cif_id != CIF_ID_TEST:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc='cif_id')
    return ReposReturn(data={
        "cif_id": cif_id,
        "created_at": now(),
        "created_by": created_by
    })


async def repos_get_data_finger(cif_id: str, session: Session) -> ReposReturn:

    query_data = session.execute(
        select(
            Customer,
            CustomerIdentity,
            CustomerIdentityImage,
            HandSide,
            FingerType
        ).join(
            CustomerIdentity, Customer.id == CustomerIdentity.customer_id
        ).join(
            CustomerIdentityImage, CustomerIdentity.id == CustomerIdentityImage.identity_id
        ).join(
            HandSide, CustomerIdentityImage.hand_side_id == HandSide.id
        ).join(
            FingerType, CustomerIdentityImage.finger_type_id == FingerType.id
        ).filter(Customer.id == cif_id).order_by(CustomerIdentityImage.finger_type_id)
    ).all()

    if not query_data:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc="cif_id")

    fingerprint_1 = []
    fingerprint_2 = []
    data_response = {
        'fingerprint_1': fingerprint_1,
        'fingerprint_2': fingerprint_2,
    }

    for _, _, customer_identity_image, hand_side, finger_print in query_data:
        if hand_side.id == "1":
            fingerprint_1.append(
                {
                    'image_url': customer_identity_image.image_url,
                    'hand_side': {
                        'id': hand_side.id,
                        'code': hand_side.code,
                        'name': hand_side.name
                    },
                    'finger_type': {
                        'id': finger_print.id,
                        'code': finger_print.code,
                        'name': finger_print.name
                    }
                }
            )
        else:
            fingerprint_2.append(
                {
                    'image_url': customer_identity_image.image_url,
                    'hand_side': {
                        'id': hand_side.id,
                        'code': hand_side.code,
                        'name': hand_side.name
                    },
                    'finger_type': {
                        'id': finger_print.id,
                        'code': finger_print.code,
                        'name': finger_print.name
                    }
                }
            )

    return ReposReturn(data=data_response)
