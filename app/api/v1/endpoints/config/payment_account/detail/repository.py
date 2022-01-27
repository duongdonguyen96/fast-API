from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.third_parties.oracle.models.master_data.account import (
    AccountStructureType
)


async def repos_get_account_structure_type(level: int, session: Session):
    account_structure_type_infos = session.execute(
        select(
            AccountStructureType
        ).filter(
            AccountStructureType.level == level
        )
    ).scalars().all()

    return ReposReturn(data=[{
        "id": account_structure_type_info.id,
        "code": account_structure_type_info.code,
        "name": account_structure_type_info.name,
    } for account_structure_type_info in account_structure_type_infos])
