from typing import List, Optional

from pydantic import Field

from app.api.base.schema import BaseSchema


class ListKSS(BaseSchema):
    customer_id: Optional[str] = Field(..., description="Id customer")
    transaction_id: Optional[str] = Field(..., description="Mã giao dịch")
    full_name: Optional[str] = Field(..., description="Họ và tên")
    cif: Optional[str] = Field(..., description="Số Cif")
    phone_number: Optional[str] = Field(..., description="Số điện thoại")
    document_id: Optional[str] = Field(..., description="Số CMND/căn cước công dân/hộ chiếu")
    document_type: Optional[int] = Field(..., description="Loại giấy tờ giao dịch: "
                                                          "0: Hộ chiếu, "
                                                          "1: CMND cũ (9 số), "
                                                          "2: CMND mới (12 số), "
                                                          "3: CCCD cũ, "
                                                          "4: CCCD mới (gắn chíp)")
    status: Optional[str] = Field(..., description="Trạng thái")
    trans_date: Optional[str] = Field(..., description="Trạng thái giao dịch")
    ekyc_step: Optional[str] = Field(..., description="Nghiệp vụ")
    kss_status: Optional[str] = Field(..., description="Trạng thái kiểm soát sau")
    date_kss: Optional[str] = Field(..., description="Ngày kiểm soát sau")
    user_kss: Optional[str] = Field(..., description="Người kiểm soát sau")
    approve_status: Optional[str] = Field(..., description="Trạng thái phê duyệt")
    date_approve: Optional[str] = Field(..., description="Ngày phê duyệt")
    user_approve: Optional[str] = Field(..., description="Người thái phê duyệt")


class KSSResponse(BaseSchema):
    detail: List[ListKSS] = Field(..., description='Dữ liệu danh sách kiểm soát sau')
    total_page: int = Field(..., description='Tổng page')
    total_record: int = Field(..., description='Tổng record')
    page: int = Field(..., description='Số page')


class QueryParamsKSSRequest(BaseSchema):
    tran_type_id: str = Field(None, description="Theo loại giao dịch")
    transaction_id: str = Field(None, description='Theo mã giao dịch')
    approve_status: str = Field(None, description='Theo trạng thái phê duyệt')
    branch_id: str = Field(None, description='Theo đơn vị')
    step_status: str = Field(None, description='Theo trạng thái giao dịch')
    zone_id: str = Field(None, description='Theo vùng')
    start_date: str = Field(None, description='Từ ngày')
    end_date: str = Field(None, description='Đến ngày')
    page_num: int = Field(None, description='Số trang')
    record_per_page: int = Field(None, description='Số record')

####################################################################################################
# Branch
####################################################################################################


class BranchResponse(BaseSchema):
    zone_id: int = Field(..., description='Zone id')
    code: str = Field(..., description='code')
    name: str = Field(..., description='name')
