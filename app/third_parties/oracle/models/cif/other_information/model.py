from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.third_parties.oracle.models.base import Base


# class CrmCustEmployee(CrmStaffType):
class CrmCustEmployee(Base):
    __tablename__ = 'crm_cust_employee'
    __table_args__ = {'comment': 'Nhân viên - khách hàng'}

    staff_type_id = Column(ForeignKey('crm_staff_type.staff_type_id'), primary_key=True, comment='Mã Danh mục Loại nhân viên giới thiệu')
    employee_id = Column(ForeignKey('hrm_employee.id'), nullable=False, comment='Mã nhân viên')
    customer_id = Column(ForeignKey('crm_customer.customer_id'), nullable=False, comment='Mã khách hàng')
    created_at = Column(DateTime, comment='Ngày tạo')
    updated_at = Column(DateTime, comment='Ngày cập nhật')

    customer = relationship('CrmCustomer')
    employee = relationship('HrmEmployee')
