from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.third_parties.oracle.models.master_data.account import (
    AccountClass, AccountType
)


async def repos_get_account_type(session: Session) -> ReposReturn:
    account_types = session.execute(select(AccountType)).scalars().all()
    if not account_types:
        return ReposReturn(is_error=True, msg="account_type doesn't have data", loc='config')
    list_account_type_config = []
    for account_type in account_types:
        list_account_type_config.append({
            "id": account_type.id,
            "code": account_type.code,
            "name": account_type.name
        })

    return ReposReturn(data=list_account_type_config)


async def repos_get_account_class(session: Session) -> ReposReturn:
    account_classes = session.execute(select(AccountClass)).scalars().all()
    if not account_classes:
        return ReposReturn(is_error=True, msg="account_class doesn't have data", loc='config')
    list_account_class_config = []
    for account_class in account_classes:
        list_account_class_config.append({
            "id": account_class.id,
            "code": account_class.code,
            "name": account_class.name
        })

    return ReposReturn(data=list_account_class_config)


#  ################################################ cần xem lại ###########################################

# async def repos_get_account_structure_type(session: Session) -> ReposReturn:
#     account_structure_types = session.execute(select(AccountClass)).scalars().all()
#     if not account_structure_types:
#         return ReposReturn(is_error=True, msg="account_class doesn't have data", loc='config')
#     list_account_structure_type_config = []
#     for account_structure_type in account_structure_types:
#         list_account_structure_type_config.append({
#             "id": account_structure_type.id,
#             "code": account_structure_type.code,
#             "name": account_structure_type.name
#         })
#
#     return ReposReturn(data=list_account_structure_type_config)
#  ################################################ cần xem lại ###########################################
