from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.third_parties.oracle.models.master_data.others import HrmEmployee


async def repos_get_sale_staff(session: Session) -> ReposReturn:

    sale_staffs = session.execute(select(HrmEmployee)).scalars().all()
    if not sale_staffs:
        return ReposReturn(is_error=True, msg="sale_staff doesn't have data", loc='config')

    return ReposReturn(data=[
        {
            "id": sale_staff.id,
            "fullname_vn": sale_staff.fullname_vn

        } for sale_staff in sale_staffs
    ])


async def repos_get_indirect_sale_staff(session: Session) -> ReposReturn:

    indirect_sale_staffs = session.execute(select(HrmEmployee)).scalars().all()
    if not indirect_sale_staffs:
        return ReposReturn(is_error=True, msg="sale_staff doesn't have data", loc='config')

    return ReposReturn(data=[
        {
            "id": indirect_sale_staff.id,
            "fullname_vn": indirect_sale_staff.fullname_vn

        } for indirect_sale_staff in indirect_sale_staffs
    ])
