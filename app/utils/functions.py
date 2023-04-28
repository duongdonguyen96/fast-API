import uuid
from datetime import date, datetime, timedelta


from app.settings.config import (
    DATE_INPUT_OUTPUT_FORMAT, DATETIME_INPUT_OUTPUT_FORMAT
)

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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


def date_to_string(_date: date, default='', _format=DATE_INPUT_OUTPUT_FORMAT) -> str:
    if _date:
        return _date.strftime(_format)
    return default


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


def date_string_to_other_date_string_format(
        date_input: str,
        from_format: str,
        to_format: str = DATE_INPUT_OUTPUT_FORMAT,
        default=''
):
    _date = string_to_date(date_input, _format=from_format)
    if not _date:
        return default

    return date_to_string(_date, _format=to_format, default=default)


def generate_uuid() -> str:
    """
    :return: str
    """
    return uuid.uuid4().hex.upper()


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
