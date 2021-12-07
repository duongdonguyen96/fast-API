import json
from typing import List, Optional

from sqlalchemy import and_, func, select, update
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.third_parties.oracle.base import Base
from app.third_parties.oracle.models.cif.form.model import (
    Booking, BookingAccount, BookingCustomer, TransactionAll, TransactionDaily
)
from app.utils.error_messages import ERROR_ID_NOT_EXIST
from app.utils.functions import dropdown, generate_uuid, now


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


async def repos_get_optional_model_object_by_code_or_name(
        model: Base, session: Session,
        model_code: Optional[str] = None, model_name: Optional[str] = None
) -> ReposReturn:
    statement = None

    if model_code:
        statement = select(model).filter(model.code == model_code)

    if model_name:
        statement = select(model).filter(func.lower(model.name) == func.lower(model_name))  # TODO: check it

    if not statement:
        return ReposReturn(data=None)

    if hasattr(model, 'active_flag'):
        statement = statement.filter(model.active_flag == 1)

    return ReposReturn(data=session.execute(statement).scalar())


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


async def write_transaction_log_and_update_booking(description: str,
                                                   log_data: json,
                                                   session: Session,
                                                   customer_id: Optional[str] = None,
                                                   account_id: Optional[str] = None,
                                                   transaction_stage_id: str = 'BE_TEST'  # TODO: đợi dữ liệu danh mục
                                                   ) -> Optional[ReposReturn]:
    if customer_id:
        booking = session.execute(
            select(
                Booking
            )
            .join(
                BookingCustomer, and_(
                    Booking.id == BookingCustomer.id,
                    BookingCustomer.customer_id == customer_id
                )
            )
        ).scalar()
    elif account_id:
        booking = session.execute(
            select(
                Booking
            )
            .join(
                BookingAccount, and_(
                    Booking.id == BookingAccount.id,
                    BookingAccount.account_id == account_id
                )
            )
        ).scalar()
    else:
        booking = None

    if not booking:
        return ReposReturn(is_error=True, detail='Can not found booking', loc='cif_id')

    previous_transaction = session.execute(
        select(
            TransactionDaily
        ).filter(transaction_id=booking.transaction_id)
    ).scalar()
    if not previous_transaction:
        # TransactionDaily sau một ngày sẽ bị đẩy vào TransactionAll
        previous_transaction = session.execute(
            select(
                TransactionAll
            ).filter(transaction_id=booking.transaction_id)
        ).scalar()

    if not previous_transaction:
        return ReposReturn(is_error=True, detail='Can not found transaction', loc='cif_id')

    # lưu log trong CRM_TRANSACTION_DAILY
    transaction_id = generate_uuid()
    session.add(
        TransactionDaily(
            transaction_id=transaction_id,
            transaction_stage_id=transaction_stage_id,
            data=log_data,
            transaction_parent_id=booking.transaction_id,
            transaction_root_id=previous_transaction.transaction_root_id,
            description=description,
            created_at=now(),
            updated_at=now()
        )
    )

    # Cập nhật lại transaction_id trong Booking
    session.execute(
        update(
            Booking
        ).filter(
            Booking.id == booking.id
        ).values(
            transaction_id=transaction_id
        )
    )

    return None
