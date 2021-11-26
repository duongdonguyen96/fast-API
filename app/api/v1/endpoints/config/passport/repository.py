from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.third_parties.oracle.models.master_data.identity import (
    PassportCode, PassportType
)


async def repos_get_passport_type(session: Session) -> ReposReturn:

    passport_types = session.execute(select(PassportType)).scalars().all()
    if not passport_types:
        return ReposReturn(is_error=True, msg="passport_type doesn't have data", loc='config')
    list_passport_type_config = []
    for passport_type in passport_types:
        list_passport_type_config.append({
            "id": passport_type.id,
            "code": passport_type.code,
            "name": passport_type.name
        })

    return ReposReturn(data=list_passport_type_config)


async def repos_get_passport_code(session: Session) -> ReposReturn:

    passport_codes = session.execute(select(PassportCode)).scalars().all()
    if not passport_codes:
        return ReposReturn(is_error=True, msg="passport_code doesn't have data", loc='config')
    list_passport_code_config = []
    for passport_code in passport_codes:
        list_passport_code_config.append({
            "id": passport_code.id,
            "code": passport_code.code,
            "name": passport_code.name
        })

    return ReposReturn(data=list_passport_code_config)
