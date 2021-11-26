from sqlalchemy import VARCHAR, Column, DateTime, ForeignKey, text
from sqlalchemy.dialects.oracle import NUMBER
from sqlalchemy.orm import relationship

from app.third_parties.oracle.base import Base
from app.third_parties.oracle.models.master_data.others import (  # noqa
    FatcaCategory
)


class CustomerFatca(Base):
    __tablename__ = 'crm_cust_fatca'

    id = Column('cust_fatca_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='ID FATCA - khách hàng')
    fatca_category_id = Column(ForeignKey('crm_fatca_category.fatca_category_id'), nullable=False,
                               comment='ID danh mục FATCA')
    value = Column('fatca_value', VARCHAR(10), nullable=False, comment='Giá trị chọn FATCA (có/không)')

    customer_id = Column(ForeignKey('crm_customer.customer_id'), nullable=False, comment='Mã khách hàng')

    fatca_category = relationship('FatcaCategory')
    customer = relationship('Customer')


class CustomerFatcaDocument(Base):
    __tablename__ = 'crm_cust_fatca_document'

    id = Column('cust_fatca_doc_id', VARCHAR(36), primary_key=True, unique=True, server_default=text("sys_guid() "),
                comment='ID biểu mẫu đính kèm FATCA')
    customer_fatca_id = Column('cust_fatca_id', ForeignKey('crm_cust_fatca.cust_fatca_id'), nullable=False,
                               comment='ID FATCA - khách hàng')
    document_language_type = Column(VARCHAR(3), nullable=False,
                                    comment='Loại ngôn ngữ biểu mẫu ( Tiếng việt/ Song ngữ)')
    document_name = Column(VARCHAR(255), nullable=False, comment='Tên biểu mẫu')
    document_url = Column(VARCHAR(255), nullable=False, comment='Đường dẫn biểu mẫu')
    document_version = Column(VARCHAR(10), nullable=False, comment='Phiên bản biểu mẫu')
    active_flag = Column(VARCHAR(20), nullable=False, comment='Trạng thái hoạt động')
    created_at = Column(DateTime, nullable=False, comment='Ngày tạo')
    order_no = Column(NUMBER(3, 0, False), comment='Sắp xếp')

    customer_fatca = relationship('CustomerFatca')
