from sqlalchemy import and_, desc, select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.third_parties.oracle.models.cif.basic_information.identity.model import (
    CustomerIdentity, CustomerIdentityImage
)
from app.third_parties.oracle.models.cif.basic_information.model import (
    Customer
)
from app.third_parties.oracle.models.master_data.identity import (
    FingerType, HandSide
)
from app.utils.constant.cif import HAND_SIDE_LEFT_CODE
from app.utils.error_messages import (
    ERROR_CAN_NOT_CREATE, ERROR_CIF_ID_NOT_EXIST
)
from app.utils.functions import dropdown, now


async def repos_get_identity_id(cif_id: str, session: Session):
    query_data = session.execute(
        select(
            CustomerIdentity
        ).filter(CustomerIdentity.customer_id == cif_id).order_by(desc(CustomerIdentity.maker_at))
    ).scalars().first()

    if query_data is None:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc="cif_id")

    return ReposReturn(data=query_data)


async def repos_save_fingerprint(cif_id: str, oracle_session: Session, list_data_insert: list,
                                 created_by: str):
    try:
        data_insert = [CustomerIdentityImage(**data_insert) for data_insert in list_data_insert]
        oracle_session.bulk_save_objects(data_insert)
        oracle_session.commit()
    except Exception as ex:
        return ReposReturn(is_error=True, msg=ERROR_CAN_NOT_CREATE, loc=f'{ex}')

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
            CustomerIdentityImage, and_(
                CustomerIdentity.id == CustomerIdentityImage.identity_id,
                CustomerIdentityImage.finger_type_id.isnot(None),
                CustomerIdentityImage.hand_side_id.isnot(None)
            )
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

    for _, _, customer_identity_image, hand_side, finger_print in query_data:
        fingerprint = {
            'image_url': customer_identity_image.image_url,
            'hand_side': dropdown(hand_side),
            'finger_type': dropdown(finger_print)
        }
        if hand_side.code == HAND_SIDE_LEFT_CODE:
            fingerprint_1.append(fingerprint)
        else:
            fingerprint_2.append(fingerprint)

    return ReposReturn(data={
        'fingerprint_1': fingerprint_1,
        'fingerprint_2': fingerprint_2,
    })
