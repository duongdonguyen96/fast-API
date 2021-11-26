from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.third_parties.oracle.base import Base
from app.utils.error_messages import ERROR_ID_NOT_EXIST


async def repos_get_model_object_by_id(model_id: str, model: Base, loc: str, session: Session) -> ReposReturn:
    statement = select(model).filter(model.id == model_id)

    if hasattr(model, 'active_flag'):
        statement = statement.filter(model.active_flag == 1)

    obj = session.execute(statement).scalar()
    if not obj:
        return ReposReturn(
            is_error=True,
            msg=ERROR_ID_NOT_EXIST,
            loc=f'{str(model.tablename)}_id' if not loc else loc
        )

    return ReposReturn(data=obj)
