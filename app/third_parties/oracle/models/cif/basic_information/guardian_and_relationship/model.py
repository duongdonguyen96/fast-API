from sqlalchemy import VARCHAR, Column, ForeignKey, text
from sqlalchemy.dialects.oracle import NUMBER
from sqlalchemy.orm import relationship

from app.third_parties.oracle.base import Base
from app.third_parties.oracle.models.cif.basic_information.model import (  # noqa
    Customer
)
from app.third_parties.oracle.models.master_data.customer import (  # noqa
    CustomerRelationshipType
)


class CustomerPersonalRelationship(Base):
    __tablename__ = 'crm_cust_personal_relationship'
    __table_args__ = {'comment': 'Người giám hộ và Mối quan hệ khách hàng'}

    id = Column('cust_personal_relationship_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='Mã quan hệ khách hàng cá nhân')
    customer_id = Column(ForeignKey('crm_customer.customer_id'), nullable=False, comment='Mã khách hàng')
    customer_relationship_type_id = Column(ForeignKey('crm_cust_relationship_type.cust_relationship_type_id'),
                                           nullable=False, comment='Mã loại mối quan hệ khách hàng')
    type = Column('cust_personal_relationship_type', NUMBER(1, 2, True), nullable=False,
                  comment='Loại quan hệ khách hàng cá nhân (0: Người giám hộ, 1: Mối quan hệ khách hàng)')
    customer_personal_relationship_cif_number = Column('cust_personal_relationship_cif_num', VARCHAR(9),
                                                       comment='Số cif của Người giám hộ hoặc Mối quan hệ khách hàng')
    customer_relationship_id = Column('cust_relationship_id', VARCHAR(36), comment='Mã Khách hàng có mối quan hệ')

    customer_relationship_type = relationship('CustomerRelationshipType')
    customer = relationship('Customer')
