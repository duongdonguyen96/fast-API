import uuid
from datetime import date, datetime
from typing import Callable, Dict, List, Set, Tuple, Union


def today():
    """
    get today
    :return: date
    """
    return date.today()


def get_current_date():
    return datetime.now()


def generate_uuid() -> str:
    """
    :return: str
    """
    return str(uuid.uuid4())


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
