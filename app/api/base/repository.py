from dataclasses import dataclass
from typing import Any


@dataclass
class ReposReturn:
    is_error: bool = False
    loc: str = ''
    msg: str = ''
    detail: str = ''
    data: Any = None
