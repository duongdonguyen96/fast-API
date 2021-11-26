from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.third_parties.oracle.models.master_data.others import (
    HrmEmployee, Position, StaffType
)


async def repos_get_staff_type(session: Session) -> ReposReturn:

    staff_types = session.execute(select(StaffType)).scalars().all()
    if not staff_types:
        return ReposReturn(is_error=True, msg="staff_type doesn't have data", loc='config')
    list_staff_type_config = [
        {
            "id": staff_type.id,
            "code": staff_type.code,
            "name": staff_type.name
        } for staff_type in staff_types
    ]

    return ReposReturn(data=list_staff_type_config)


async def repos_get_position(session: Session) -> ReposReturn:

    positions = session.execute(select(Position)).scalars().all()
    if not positions:
        return ReposReturn(is_error=True, msg="position doesn't have data", loc='config')
    list_position_config = [
        {
            "id": position.id,
            "code": position.code,
            "name": position.name
        } for position in positions
    ]

    return ReposReturn(data=list_position_config)


async def repos_get_sale_staff(session: Session) -> ReposReturn:

    sale_staffs = session.execute(select(HrmEmployee)).scalars().all()
    if not sale_staffs:
        return ReposReturn(is_error=True, msg="sale_staff doesn't have data", loc='config')
    list_sale_staff_config = [
        {
            "id": sale_staff.id,
            "fullname_vn": sale_staff.fullname_vn

        } for sale_staff in sale_staffs
    ]

    return ReposReturn(data=list_sale_staff_config)


async def repos_get_indirect_sale_staff(session: Session) -> ReposReturn:

    indirect_sale_staffs = session.execute(select(HrmEmployee)).scalars().all()
    if not indirect_sale_staffs:
        return ReposReturn(is_error=True, msg="sale_staff doesn't have data", loc='config')
    list_inderect_sale_staff_config = [
        {
            "id": indirect_sale_staff.id,
            "fullname_vn": indirect_sale_staff.fullname_vn

        } for indirect_sale_staff in indirect_sale_staffs
    ]

    return ReposReturn(data=list_inderect_sale_staff_config)
