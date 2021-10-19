from typing import List, Tuple

from app.api.base.schema import Error
from app.settings.service import SERVICE
from app.utils.error_messages import (
    FILE_IS_NULL, FILE_TOO_LARGE, TOO_MANY_FILE
)

MAX_FILE_SIZE = SERVICE["file-upload"]["file_size_max"]
FILE_LIMIT = SERVICE["file-upload"]["file_limit"]


def file_validator(file: bytes) -> Tuple[bool, List[Error]]:
    errors: List[Error] = list()

    file_size = len(file)
    if file_size == 0:
        errors.append(Error(msg=FILE_IS_NULL))

    if file_size > MAX_FILE_SIZE:
        errors.append(Error(msg=FILE_TOO_LARGE))

    if errors:
        return False, errors
    else:
        return True, errors


def files_validator(files: List[bytes]) -> Tuple[bool, List[Error]]:
    errors: List[Error] = list()

    if len(files) == 0:
        errors.append(Error(msg=FILE_IS_NULL))

    if len(files) > FILE_LIMIT:
        errors.append(Error(msg=TOO_MANY_FILE))

    for file in files:
        is_valid, file_errors = file_validator(file)
        if not is_valid:
            errors += file_errors

    if errors:
        return False, errors
    else:
        return True, errors
