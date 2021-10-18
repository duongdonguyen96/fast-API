from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.schemas.cif import (
    CustomerClassificationResponse, CustomerEconomicProfessionResponse,
    KYCLevelResponse
)


class CifInformationResponse(BaseSchema):
    self_selected_cif_flag: bool = Field(..., description='Cờ CIF thông thường/ tự chọn. '
                                                          '`False`: thông thường. '
                                                          '`True`: tự chọn')
    cif_number: str = Field(..., description='Số CIF yêu cầu')
    customer_classification: CustomerClassificationResponse = Field(..., description='Đối tượng khách hàng')
    customer_economic_profession: CustomerEconomicProfessionResponse = Field(..., description='Mã ngành KT')
    kyc_level: KYCLevelResponse = Field(..., description='Cấp độ KYC')
