import uuid
from datetime import date, datetime
from typing import Callable, Dict

from loguru import logger
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.settings.config import (
    DATE_INPUT_OUTPUT_FORMAT, DATETIME_INPUT_OUTPUT_FORMAT
)
from app.third_parties.oracle.base import Base


def dropdown(data) -> dict:
    return {
        'id': data.id,
        'code': data.code,
        'name': data.name,
    }


def today():
    """
    get today
    :return: date
    """
    return date.today()


def now():
    return datetime.now()


def datetime_to_string(_time: datetime, _format=DATETIME_INPUT_OUTPUT_FORMAT) -> str:
    if _time:
        return _time.strftime(_format)
    return ''


def string_to_datetime(string: str, default=None, _format=DATETIME_INPUT_OUTPUT_FORMAT) -> datetime:
    try:
        return datetime.strptime(string, _format)
    except (ValueError, TypeError):
        return default


def date_to_string(_date: date, _format=DATE_INPUT_OUTPUT_FORMAT) -> str:
    if _date:
        return _date.strftime(_format)
    return ''


def string_to_date(string: str, default=None, _format=DATE_INPUT_OUTPUT_FORMAT) -> datetime:
    try:
        return datetime.strptime(string, _format)
    except (ValueError, TypeError):
        return default


def date_to_datetime(date_input: date, default=None) -> datetime:
    try:
        return datetime.combine(date_input, datetime.min.time())
    except (ValueError, TypeError):
        return default


def datetime_to_date(datetime_input: datetime, default=None) -> date:
    try:
        return datetime_input.date()
    except (ValueError, TypeError):
        return default


def end_time_of_day(datetime_input: datetime, default=None) -> datetime:
    try:
        return datetime_input.replace(hour=23, minute=59, second=59)
    except (ValueError, TypeError):
        return default


def generate_uuid() -> str:
    """
    :return: str
    """
    return uuid.uuid4().hex.upper()


def set_id_after_inserted(schema, db_model):
    """
    Cần set uuid từ model vừa insert dưới db SQL lên schema của object tương ứng với đối tượng đó để insert vào mongdb
    :param schema:
    :param db_model:
    :return:
    """
    schema.set_uuid(db_model.uuid)


def travel_dict(d: dict, process_func: Callable):
    process_func(d)
    if isinstance(d, Dict):
        for key, value in d.items():
            if type(value) is dict:
                travel_dict(value, process_func)
            elif isinstance(value, (list, set, tuple,)):
                for item in value:
                    travel_dict(item, process_func)
            else:
                process_func((key, value))
    return d


def process_generate_uuid(d):
    if isinstance(d, dict) and ("uuid" in d) and (d["uuid"] is None):
        d.update({"uuid": generate_uuid()})


def check_exist_by_id(model_id: str, model: Base, session: Session):
    try:
        session.execute(
            select(model).filter(model.id == model_id)
        ).one()
        return False
    except Exception as ex:
        logger.debug(ex)
        return True


def check_exist_list_by_id(check_list: list, session: Session):
    list_error = []
    for model_id, model, message in check_list:
        is_error = check_exist_by_id(model_id, model, session)
        if is_error:
            list_error.append(message)
    return list_error


def check_not_null(check_list):
    list_error = []
    for model_id, _, message in check_list:
        # print(model_id)
        if not model_id:
            list_error.append(message)
    return list_error
