from typing import List

from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.third_parties.oracle.models.cif.basic_information.identity.model import (
    CustomerIdentity, CustomerIdentityImage
)
from app.third_parties.oracle.models.master_data.identity import (
    FingerType, HandSide
)
from app.utils.constant.cif import HAND_SIDE_LEFT_CODE
from app.utils.error_messages import ERROR_CIF_ID_NOT_EXIST
from app.utils.functions import dropdown, now


async def repos_get_hand_sides(hand_side_ids: List[str], session: Session):
    crm_hand_sides = session.execute(
        select(
            HandSide
        ).filter(HandSide.code.in_(hand_side_ids))
    ).scalars().all()

    if len(crm_hand_sides) != len(hand_side_ids):
        return ReposReturn(is_error=True, detail="hand side is not exist", loc="hand_side id")

    return ReposReturn(data=crm_hand_sides)


async def repos_get_finger_types(finger_type_ids: List[str], session: Session):
    crm_finger_types = session.execute(
        select(
            FingerType
        ).filter(FingerType.code.in_(finger_type_ids))
    ).scalars().all()

    if len(crm_finger_types) != len(finger_type_ids):
        return ReposReturn(is_error=True, detail="finger type is not exist", loc="finger_type id")

    return ReposReturn(data=crm_finger_types)


async def repos_save_fingerprint(
        cif_id: str,
        session: Session,
        list_data_insert: list,
        created_by: str
) -> ReposReturn:

    data_insert = [CustomerIdentityImage(**data_insert) for data_insert in list_data_insert]
    session.bulk_save_objects(data_insert)
    session.commit()

    return ReposReturn(data={
        "cif_id": cif_id,
        "created_at": now(),
        "created_by": created_by
    })


async def repos_get_data_finger(cif_id: str, session: Session) -> ReposReturn:
    query_data = session.execute(
        select(
            CustomerIdentityImage,
            HandSide,
            FingerType
        ).join(
            CustomerIdentity, and_(
                CustomerIdentityImage.identity_id == CustomerIdentity.id,
                CustomerIdentity.customer_id == cif_id
            )
        ).join(
            HandSide, CustomerIdentityImage.hand_side_id == HandSide.id
        ).join(
            FingerType, CustomerIdentityImage.finger_type_id == FingerType.id
        ).filter(
            CustomerIdentityImage.finger_type_id.isnot(None),
            CustomerIdentityImage.hand_side_id.isnot(None)
        ).order_by(CustomerIdentityImage.finger_type_id)
    ).all()

    if not query_data:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc="cif_id")

    fingerprint_1 = []
    fingerprint_2 = []

    for customer_identity_image, hand_side, finger_print in query_data:
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
