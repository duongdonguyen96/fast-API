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

####################################################################################################
# vùng
####################################################################################################


class ZoneRequest(BaseSchema):
    id: int = Field(..., description='Id vùng')
    name: str = Field(..., description='Tên vùng')


###################################################################################################
# thông tin hậu kiểm của khách hàng
###################################################################################################
class ListPostControlResponse(BaseSchema):
    check_list_id: int = Field(..., description='ID của danh mục kiểm tra')
    check_list_desc: str = Field(..., description='Danh mục kiểm tra')
    answer: str = Field(..., description='Đánh giá')
    note: Optional[str] = Field(..., description='Mô tả')


class PostControlResponse(BaseSchema):
    kss_status: str = Field(..., description="Trạng thái của KSS")
    status: str = Field(..., description='Trạng thái hậu kiểm')
    approve_status: Optional[str] = Field(..., description="Trạng thái phê duyệt")
    post_control: List[ListPostControlResponse] = Field(...)

#############################################################################################
# lịch sử hậu kiểm
#############################################################################################


class HistoryPostCheckResponse(BaseSchema):
    id: int = Field(..., description='ID of History Post-control')
    kss_status: str = Field(..., description='Status post-control description')
    kss_status_old: str = Field(..., description='Status old post-control description')
    create_date_format: str = Field(..., description='Create date')
    approve_status: str = Field(..., description='Trạng thái phê duyệt')
    approve_date_format: str = Field(..., description='Ngày phê duyệt')
    status: str = Field(..., description='Status posst-control')
    status_old: str = Field(..., description='Status old post-control')
    result: str = Field(..., description='Kết quả đánh giá')
    create_user: str = Field(..., description='User create')
    approve_user: str = Field(..., description='User approve')

####################################################################################################
# thống kê theo tháng
####################################################################################################


class StatisticsMonth(BaseSchema):
    month: str = Field(..., description='Thống kê theo tháng')
    total: int = Field(..., description='Thống kê giao dịch của khách hàng')
    success: int = Field(..., description='Tổng hợp giao dịch thành công của khách hàng.')
    refuse: int = Field(..., description='Tổng số giao dịch bị khách hàng từ chối')

####################################################################################################
# Thống kê hồ sơ hậu kiểm
####################################################################################################


class StatisticsProfilesResponse(BaseSchema):
    total: int = Field(..., description="Tổng cộng")
    success: int = Field(..., description="Thành công")
    canceled: int = Field(..., description="Hủy bỏ")
    processing: int = Field(..., description="Chờ hậu kiểm")
    rejected: int = Field(..., description="Cần xác minh")


####################################################################################################
# Thống kê số liệu API POST
####################################################################################################

class StatisticsResponse(BaseSchema):
    time: str = Field(..., description='Thống kê theo thời gian')
    total: int = Field(..., description='Thống kê giao dịch của khách hàng')
    success: int = Field(..., description='Tổng hợp giao dịch thành công của khách hàng.')

####################################################################################################
# create post check
####################################################################################################


class PostCheck(BaseSchema):
    check_list_id: int = Field(..., description='ID của danh mục kiểm tra')
    check_list_desc: str = Field(..., description='Danh mục kiểm tra')
    answer: str = Field(..., description='Đánh giá')
    note: str = Field(..., description='Mô tả')


class CreatePostCheckRequest(BaseSchema):
    customer_id: str = Field(..., description='Id của khách hàng')
    kss_status: str = Field(..., description='Trạng thái hậu kiểm')
    username: str = Field(..., description='User hậu kiểm')
    post_control: List[PostCheck] = Field(...)

####################################################################################################
# phê duyệt hậu kiểm
####################################################################################################


class UpdatePostCheckRequest(BaseSchema):
    customer_id: str = Field(..., description='Id của khách hàng')
    history_post_control_id: int = Field(..., description='ID của lịch sử hậu kiểm')
    username: str = Field(..., description='User hậu kiểm')
