from sqlalchemy import VARCHAR, Column, DateTime, ForeignKey, Table, text
from sqlalchemy.dialects.oracle import NUMBER
from sqlalchemy.orm import relationship

from app.third_parties.oracle.models.base import Base, metadata


class EBankingReceiverNotificationRelationship(Base):
    __tablename__ = 'crm_eb_receiver_noti_relationship'
    __table_args__ = {'comment': 'Mối quan hệ thông tin nhận thông báo: Bố mẹ,vợ chồng,...'}

    id = Column('reg_receiver_noti_relationship_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='Mã Mối quan hệ thông tin nhận thông báo: Bố mẹ,vợ chồng,...')
    eb_reg_balance_casa_id = Column(VARCHAR(36), nullable=False,
                                    comment='Mã Đăng ký Biến động số dư các loại tài khoản Thanh toán')
    relationship_type_id = Column(VARCHAR(36), nullable=False, comment='Mã Quan hệ khách hàng')
    mobile_number = Column('mobile_num', VARCHAR(10), nullable=False, comment='Số Điện thoại')
    full_name = Column(VARCHAR(100), nullable=False, comment='Tên đầy đủ')


t_crm_eb_reg_balance_fd_noti = Table(
    'crm_eb_reg_balance_fd_noti', metadata,
    Column('eb_notify_id', ForeignKey('crm_eb_notification.eb_notify_id'), comment='Mã Danh mục tùy chọn thông báo'),
    Column('customer_id', ForeignKey('crm_eb_reg_balance_fd_option.customer_id')),
    comment='Tùy chọn thông báo - Tài khoản tiết kiệm'
)


class EBankingRegisterBalanceFdOption(Base):
    __tablename__ = 'crm_eb_reg_balance_fd_option'
    __table_args__ = {'comment': 'Hình thức thông báo: OTT, SMS'}

    customer_id = Column(VARCHAR(36), primary_key=True, comment='Mã khách hàng')
    customer_contact_type_id = Column('cust_contact_type_id', VARCHAR(36), nullable=False, comment='Mã LOẠI LIÊN HỆ')
    created_at = Column(DateTime, nullable=False, comment='Ngày tạo')
    updated_at = Column(DateTime, comment='Ngày cập nhật')

    eb_notification = relationship('CrmEbNotification', secondary='crm_eb_reg_balance_fd_noti')


t_crm_eb_info_authen = Table(
    'crm_eb_info_authen', metadata,
    Column('eb_info_id', ForeignKey('crm_ebanking_info.eb_info_id'),
           comment='Liên kết thông tin tài khoản ib với hình thức xác thực'),
    Column('method_authen_id', ForeignKey('crm_method_authen.method_authen_id'),
           comment='Danh mục Hình thức xác thực Vân tay Khuôn mặt SMS SOFT TOKEN HARD TOKEN'),
    comment='Liên kết thông tin tài khoản ib với hình thức xác thực'
)


class EBankingRegisterBalanceFd(Base):
    __tablename__ = 'crm_eb_reg_balance_fd'
    __table_args__ = {'comment': 'Đăng ký Biến động số dư các loại tài khoản Tiết kiệm'}

    id = Column('reg_balance_fd_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='Mã Đăng ký Biến động số dư các loại tài khoản Tiết kiệm')
    td_account_id = Column(ForeignKey('crm_td_account.td_account_id'), comment='Mã Tài khoản Tiết kiệm')
    customer_id = Column(ForeignKey('crm_eb_reg_balance_fd_option.customer_id'))

    customer = relationship('CrmEbRegBalanceFdOption')
    td_account = relationship('CrmTdAccount')


class EBankingInfo(Base):
    __tablename__ = 'crm_ebanking_info'
    __table_args__ = {'comment': 'Thông tin e-banking'}

    id = Column('eb_info_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='Mã Thông tin e-banking')
    customer_id = Column(VARCHAR(36), comment='Mã khách hàng')
    method_active_password_id = Column('eb_method_active_pw_id', VARCHAR(36),
                                       comment='Hình thức nhận mật khẩu kích hoạt lần đầu')
    account_name = Column('eb_account_name', VARCHAR(100), comment='Tên đăng nhập')
    note = Column('eb_note', VARCHAR(1000), comment='Ghi chú nội dungg')
    ib_mb_flag = Column(NUMBER(1, 0, False), comment='Cờ có đăng ký Mobile -  Internet banking hay không')
    method_payment_fee_flag = Column('eb_method_payment_fee_flag', NUMBER(1, 0, False),
                                     comment='Cờ thanh toán phí tiền mặt - chuyển khoản')
    reset_password_flag = Column('eb_reset_password_flag', NUMBER(1, 0, False), comment='Cờ tùy chọn reset password')
    active_account_flag = Column('eb_active_account_flag', NUMBER(1, 0, False),
                                 comment='Cờ tùy chọn trạng thái kích hoạt ebanking')
    account_payment_fee = Column('eb_account_payment_fee', VARCHAR(50), comment='Số tài khoản thanh toán phí')

    method_authentication = relationship('CrmMethodAuthen', secondary='crm_eb_info_authen')


class EBankingRegisterBalance(Base):
    __tablename__ = 'crm_eb_reg_balance'
    __table_args__ = {'comment': '(Đăng ký Biến động số dư các loại tài khoản Thanh toán/ Tiết kiệm)'}

    id = Column('eb_reg_balance_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='Mã Đăng ký Biến động số dư các loại tài khoản ')
    account_id = Column(VARCHAR(36), comment='Số tài khoản ')
    eb_reg_account_type = Column(VARCHAR(50), comment='Loại tài khoản ( tài khoản tiết kiệm, tài khoản thanh tóan, ..)')
    customer_id = Column(ForeignKey('crm_customer.customer_id'), comment='Mã khách hàng')
    name = Column('eb_reg_balance_name', VARCHAR(100), comment='Tên Đăng ký Biến động số dư các loại tài khoản ')
    mobile_number = Column('mobile_num', VARCHAR(10), comment='Số điện thoại')
    full_name = Column(VARCHAR(100), comment='Tên đầy đủ')

    customer = relationship('CrmCustomer')


class EBankingRegisterBalanceNotification(Base):
    __tablename__ = 'crm_eb_reg_balance_noti'
    __table_args__ = {'comment': 'Tùy chọn thông báo - Tài khoản thanh toán/TKTK'}

    id = Column('eb_reg_balance_casa_noti_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "))
    eb_reg_account_type = Column(VARCHAR(50), nullable=False,
                                 comment='Loại tài khoản ( tài khoản tiết kiệm, tài khoản thanh tóan, ..)')
    customer_id = Column(ForeignKey('crm_customer.customer_id'), nullable=False, comment='Mã khách hàng')
    eb_notify_id = Column(ForeignKey('crm_eb_notification.eb_notify_id'), nullable=False,
                          comment='Mã Danh mục tùy chọn thông báo')

    customer = relationship('CrmCustomer')
    eb_notify = relationship('CrmEbNotification')


class EBankingRegisterBalanceOption(Base):
    __tablename__ = 'crm_eb_reg_balance_option'
    __table_args__ = {'comment': '(Hình thức thông báo: OTT, SMS của TKTT/TKTK)'}

    id = Column('eb_reg_balance_option_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "))
    customer_id = Column(ForeignKey('crm_customer.customer_id'), nullable=False, comment='Mã khách hàng')
    customer_contact_type_id = Column(ForeignKey('crm_cust_contact_type.cust_contact_type_id'), nullable=False,
                                      comment='Mã loại xác thực ( ott/sms/token,..)')
    eb_reg_account_type = Column(VARCHAR(50), nullable=False,
                                 comment='Loại tài khoản ( tài khoản tiết kiệm, tài khoản thanh tóan, ..)')
    created_at = Column(DateTime, nullable=False, comment='Ngày tạo')
    updated_at = Column(DateTime, comment='Ngày cập nhật')

    customer_contact_type = relationship('CrmCustContactType')
    customer = relationship('CrmCustomer')


class EBankingResetPassword(Base):
    __tablename__ = 'crm_ebanking_reset_pass'
    __table_args__ = {'comment': 'Cấp lại mật khẩu e-banking'}

    id = Column('eb_reset_pass_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='Mã Cấp lại mật khẩu e-banking')
    eb_info_id = Column(ForeignKey('crm_ebanking_info.eb_info_id'), comment='Mã Thông tin e-banking')
    eb_method_new_pass_id = Column(VARCHAR(36), comment='Mã Id  tạo pass mới ')
    upload_file_url = Column(VARCHAR(1000), comment='đường dẫn url')
    conclusion_flag = Column(NUMBER(1, 0, False), comment='Trạng thái thực hiện yêu cầu')
    conclusion_note = Column(VARCHAR(1000), comment='Ghi chú')

    eb_info = relationship('CrmEbankingInfo')


class TdAccount(Base):
    __tablename__ = 'crm_td_account'
    __table_args__ = {'comment': 'Tài khoản Tiết kiệm'}

    id = Column('td_account_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='Mã Tài khoản Tiết kiệm')
    customer_id = Column(VARCHAR(36), comment='Mã khách hàng')
    td_account_num = Column(VARCHAR(16), comment='Số tài khoản tiết kiệm,')
    currency_id = Column(VARCHAR(36), comment='Danh mục loại tiền')
    acc_type_id = Column(VARCHAR(36), comment='Loại nhóm sản phẩm (gói) tài khoản')
    acc_class_id = Column(VARCHAR(36), comment='Loại hình tài khoản')
    maker_id = Column(VARCHAR(36), comment='người thực hiện')
    maker_at = Column(DateTime, comment='ngày thực hiện')
    checker_id = Column(VARCHAR(36), comment='người phê duyệt')
    checker_at = Column(DateTime, comment='ngày phê duyệt')
    approve_status = Column(VARCHAR(3), comment='trạng phái phê duyệt')
    acc_active_flag = Column(NUMBER(1, 0, False), comment='trạng thái hoạt động')
    updated_at = Column(DateTime, comment='ngày cập nhật')
