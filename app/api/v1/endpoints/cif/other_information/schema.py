from pydantic import Field

from app.api.base.schema import BaseSchema, CreatedUpdatedBaseModel
from app.api.v1.schemas.utils import DropdownRequest, DropdownResponse


class OtherInformationResponse(BaseSchema):
    legal_agreement_flag: bool = Field(..., description="cờ thỏa thuận pháp lý `True`: có , `False`: không ")
    advertising_marketing_flag: bool = Field(
        ...,
        description="Cờ đồng ý nhận SMS, Email tiếp thị quảng cáo từ SCB. "
                    "`True`: có, "
                    "`False`: không."
    )
    sale_staff: DropdownResponse = Field(..., description="Mã nhân viên kinh doanh")
    indirect_sale_staff: DropdownResponse = Field(..., description="Mã nhân viên kinh doanh gián tiếp")


class OtherInformationUpdateRequest(BaseSchema):
    legal_agreement_flag: bool = Field(..., description="cờ thỏa thuận pháp lý `True`: có , `False`: không ")
    advertising_marketing_flag: bool = Field(
        ...,
        description="Cờ đồng ý nhận SMS, Email tiếp thị quảng cáo từ SCB. "
                    "`True`: có, "
                    "`False`: không."
    )
    sale_staff: DropdownRequest = Field(..., description="Mã nhân viên kinh doanh")
    indirect_sale_staff: DropdownRequest = Field(..., description="Mã nhân viên kinh doanh gián tiếp")


class OtherInformationUpdateResponse(CreatedUpdatedBaseModel):
    pass


EXAMPLE_REQUEST_UPDATE_OTHER_INFO = {
    "ex1": {
        "summary": "Example update other information.",
        "description": "Data update other information.",
        "value": {
            "legal_agreement_flag": True,
            "advertising_marketing_flag": False,
            "sale_staff": {"id": "123"},
            "indirect_sale_staff": {"id": "123"}
        }
    }

}

EXAMPLE_RESPONSE_SUCCESS_UPDATE_OTHER_INFO = {
    "ex1": {
        "summary": "Success.",
        "value": {
            "data": {
                "created_at": "2021/10/16 10:46:08",
                "created_by": "system",
                "updated_at": "2021/10/16 10:46:08",
                "updated_by": "system",
            },
            "errors": []
        }
    }
}
