from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.third_parties.oracle.models.master_data.others import Branch


async def repos_get_branch(session: Session, region_id: Optional[str]) -> ReposReturn:
    branches = session.execute(
        select(
            Branch
        ).filter(
            Branch.active_flag == 1,
            Branch.region_id == region_id)
    ).scalars().all()
    if not branches:
        return ReposReturn(is_error=True, msg="model doesn't have data", loc='config')

    return ReposReturn(data=[
        {
            "id": branch.id,
            "code": branch.code,
            "name": branch.name,
            "address": branch.address
        } for branch in branches
    ])
