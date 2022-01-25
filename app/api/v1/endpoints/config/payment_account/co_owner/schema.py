from typing import List

from pydantic import Field

from app.api.base.schema import BaseSchema


class AgreementOption(BaseSchema):
    id: str = Field(..., description='Id phương thức')
    title: str = Field(..., description="Nội dung phương thức")


class ConfigAgreementResponse(BaseSchema):
    id: str = Field(..., description='Id Thỏa thuận - Ủy quyền')
    content: str = Field(..., description='Nội dung bản thỏa thuận - ủy quyền')
    options: List[AgreementOption] = Field(..., description='Các phương thức đi kèm')
