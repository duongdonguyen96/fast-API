from typing import Optional

from pydantic import Field

from app.api.base.schema import BaseSchema


class AccountStructureTypeRequest(BaseSchema):
    level: int = Field(..., description="Cấp độ kiểu kiến trúc tài khoản", ge=1, le=3)
    parent_id: Optional[str] = Field(None, description="Mã cấp cha loại kết cấu tài khoản")
