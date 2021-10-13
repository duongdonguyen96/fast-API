from pydantic import BaseModel


class Error(BaseModel):
    loc: str = None
    msg: str = None
    detail: str = None
