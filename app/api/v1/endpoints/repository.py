from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.third_parties.oracle.base import Base
from app.utils.error_messages import ERROR_ID_NOT_EXIST
from app.utils.functions import dropdown


async def repos_get_model_object_by_id_or_code(model_id: Optional[str], model_code: Optional[str], model: Base,
                                               loc: str, session: Session) -> ReposReturn:
    statement = None

    if model_id:
        statement = select(model).filter(model.id == model_id)

    if model_code:
        statement = select(model).filter(model.code == model_code)

    if hasattr(model, 'active_flag'):
        statement = statement.filter(model.active_flag == 1)

    obj = session.execute(statement).scalar()
    if not obj:
        if not loc:
            loc = f'{str(model.tablename)}_{"id" if model_id else "code"}'

        return ReposReturn(
            is_error=True,
            msg=ERROR_ID_NOT_EXIST,
            loc=loc
        )

    return ReposReturn(data=obj)


async def repos_get_model_objects_by_ids(model_ids: List[str], model: Base, loc: str, session: Session) -> ReposReturn:
    """
    Get model objects by ids
    Chỉ cần truyền vào list id -> hàm sẽ tự chuyển về set(model_ids)
    :param model_ids: danh sách các id cần lấy ra model object
    :param model: model trong DB
    :param loc: vị trí lỗi
    :param session: phiên làm việc với DB bên controller
    :return:
    """
    model_ids = set(model_ids)

    statement = select(model).filter(model.id.in_(model_ids))

    if hasattr(model, 'active_flag'):
        statement = statement.filter(model.active_flag == 1)

    objs = session.execute(statement).scalars().all()
    if len(objs) != len(model_ids):
        return ReposReturn(
            is_error=True,
            msg=ERROR_ID_NOT_EXIST,
            loc=f'{str(model.tablename)}_id' if not loc else loc
        )

    return ReposReturn(data=objs)


async def repos_get_data_model_config(session: Session, model: Base, country_id: Optional[str] = None,
                                      province_id: Optional[str] = None, district_id: Optional[str] = None):
    list_data_engine = select(model)
    if hasattr(model, "country_id"):
        list_data_engine = list_data_engine.filter(model.country_id == country_id)

    if hasattr(model, "district_id"):
        list_data_engine = list_data_engine.filter(model.district_id == district_id)

    if hasattr(model, "province_id"):
        list_data_engine = list_data_engine.filter(model.province_id == province_id)

    if hasattr(model, 'active_flag'):
        list_data_engine = list_data_engine.filter(model.active_flag == 1)

    if hasattr(model, 'order_no'):
        list_data_engine = list_data_engine.order_by(model.order_no)

    list_data = session.execute(list_data_engine).scalars().all()
    if not list_data:
        return ReposReturn(is_error=True, msg="model doesn't have data", loc='config')

    return ReposReturn(data=[
        dropdown(data) for data in list_data
    ])


async def get_model_object_by_customer_id(customer_id: str, model: Base, loc: str, session: Session):
    try:
        obj = session.execute(
            select(
                model
            ).filter(
                model.customer_id == customer_id
            )
        ).scalars().one()
        return ReposReturn(data=obj)
    except Exception:
        return ReposReturn(
            is_error=True,
            msg=ERROR_ID_NOT_EXIST,
            loc=loc,
            detail=f'{str(model.__tablename__)}_id is not exist'
        )
