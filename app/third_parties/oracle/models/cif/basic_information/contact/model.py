from sqlalchemy import VARCHAR, Column, DateTime, ForeignKey, text
from sqlalchemy.dialects.oracle import NUMBER
from sqlalchemy.orm import relationship

from app.third_parties.oracle.base import Base


class CrmCustContactTypeDatum(Base):
    __tablename__ = 'crm_cust_contact_type_data'
    __table_args__ = {'comment': 'CHI TIẾT THÔNG TIN LOẠI LIÊN HỆ'}

    cust_contact_type_id = Column(ForeignKey('crm_cust_contact_type.cust_contact_type_id'), primary_key=True)
    customer_id = Column(ForeignKey('crm_customer.customer_id'), nullable=False, comment='Mã khách hàng')
    cust_contact_type_created_at = Column(DateTime, comment='Ngày tạo')
    active_flag = Column(NUMBER(1, 2, True), comment='Sắp xếp')
    order_no = Column(NUMBER(4, 2, True), comment='(FK) Mã chi tiết liện hệTrạng thái hoạt động (Có/không)')

    customer = relationship('CrmCustomer')


class CrmCustCompanyInfo(Base):
    __tablename__ = 'crm_cust_company_info'
    __table_args__ = {'comment': 'Thông tin riêng Khách hàng Doanh nghiệp'}

    customer_id = Column(ForeignKey('crm_customer.customer_id'), primary_key=True, server_default=text("sys_guid() "),
                         comment='Mã khách hàng')
    open_date = Column(DateTime, comment='Ngày mở')
    employees_num = Column(NUMBER(8, 2, True), comment='Mã Danh mục Loại nhân viên giới thiệu')


class CustomerAddress(Base):
    __tablename__ = 'crm_cust_address'

    id = Column('address_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='ID địa chỉ khách hàng')
    customer_id = Column(ForeignKey('crm_customer.customer_id'), nullable=False, comment='Mã khách hàng')
    address_type_id = Column(ForeignKey('crm_address_type.address_type_id'), nullable=False, comment='Loại địa chỉ')
    address_country_id = Column(ForeignKey('crm_address_country.country_id'), nullable=False, comment='ID quốc gia')
    address_province_id = Column(ForeignKey('crm_address_province.province_id'), nullable=False,
                                 comment='ID tỉnh/thành')
    address_district_id = Column(ForeignKey('crm_address_district.district_id'), nullable=False,
                                 comment='ID quận/huyện')
    address_ward_id = Column(ForeignKey('crm_address_ward.ward_id'), nullable=False, comment='ID phường/xã')
    address = Column(VARCHAR(255), nullable=False, comment='Địa chỉ đầy đủ khách hàng (Địa chỉ 1)')
    zip_code = Column(VARCHAR(10), nullable=False, comment='Mã bưu chính')
    latitude = Column(VARCHAR(60), comment='Vĩ độ')
    longitude = Column(VARCHAR(60), comment='Kinh độ')
    address_primary_flag = Column(NUMBER(1, 0, False), nullable=False, comment='Cờ địa chỉ chính')
    address_domestic_flag = Column(NUMBER(1, 0, False), nullable=False, comment='Cờ check địa chỉ trong/ngoài nước')
    address_2 = Column(VARCHAR(255), nullable=False, comment='Địa chỉ 2')
    address_same_permanent_flag = Column(NUMBER(1, 0, False), server_default=text("""\
0
"""), comment='Cờ giống địa chỉ thường trú')

    address_country = relationship('CrmAddressCountry')
    address_district = relationship('CrmAddressDistrict')
    address_province = relationship('CrmAddressProvince')
    address_type = relationship('CrmAddressType')
    address_ward = relationship('CrmAddressWard')
    customer = relationship('CrmCustomer')


class CustomerProfessional(Base):
    __tablename__ = 'crm_cust_professional'
    __table_args__ = {'comment': 'Thông tin nghề nghiệp - cơ quan'}

    id = Column('cust_professional_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='Mã nghề nghiệp khách hàng')
    career_id = Column(ForeignKey('crm_career.career_id'), comment='Mã ngành nghề')
    position_id = Column(ForeignKey('crm_position.position_id'), comment='Mã chức vụ')
    average_income_amount_id = Column(ForeignKey('crm_average_income_amount.average_income_amount_id'),
                                      comment='Thu nhập bình quân 3 tháng gần nhất')
    company_name = Column(VARCHAR(255), comment='Tên cơ quan')
    company_phone = Column(VARCHAR(12), comment='Số điện thoại cơ quan')
    company_address = Column(VARCHAR(255), comment='Địa chỉ cơ quan')

    average_income_amount = relationship('CrmAverageIncomeAmount')
    career = relationship('CrmCareer')
    position = relationship('CrmPosition')
