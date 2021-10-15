from dataclasses import dataclass
from typing import Any


@dataclass
class ReposReturn:
    is_error: bool = False
    loc: str = None
    msg: str = None
    detail: str = None
    data: Any = None
