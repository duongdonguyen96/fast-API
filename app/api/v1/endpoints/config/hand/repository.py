from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.third_parties.oracle.models.master_data.identity import (
    FingerType, HandSide
)


async def repos_get_hand_side(session: Session) -> ReposReturn:

    hand_sides = session.execute(select(HandSide)).scalars().all()
    if not hand_sides:
        return ReposReturn(is_error=True, msg="hand_side doesn't have data", loc='config')
    list_return_hand_side_config = []
    for hand_side in hand_sides:
        list_return_hand_side_config.append({
            "id": hand_side.id,
            "code": hand_side.code,
            "name": hand_side.name
        })

    return ReposReturn(data=list_return_hand_side_config)


async def repos_get_finger_printer(session: Session) -> ReposReturn:
    finger_types = session.execute(select(FingerType)).scalars().all()
    if not finger_types:
        return ReposReturn(is_error=True, msg="finger_type doesn't have data", loc='config')
    list_return_finger_type_config = []
    for finger_type in finger_types:
        list_return_finger_type_config.append({
            "id": finger_type.id,
            "code": finger_type.code,
            "name": finger_type.name
        })

    return ReposReturn(data=list_return_finger_type_config)
