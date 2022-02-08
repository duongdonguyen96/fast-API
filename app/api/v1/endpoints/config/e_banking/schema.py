from pydantic import Field

from app.api.base.schema import BaseSchema


class EBankingQuestionTypeResponse(BaseSchema):
    type: str = Field(..., min_length=1, description='`Loại`')


class EBankingQuestionResponse(BaseSchema):
    id: str = Field(..., min_length=1, description='`Chuỗi định danh`')
    code: str = Field(..., min_length=1, description='`Mã`')
    content: str = Field(..., min_length=1, description='`Nội dung`')
