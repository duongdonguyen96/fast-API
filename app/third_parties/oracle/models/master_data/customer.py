from sqlalchemy import VARCHAR, Column, DateTime, ForeignKey, text
from sqlalchemy.dialects.oracle import NUMBER
from sqlalchemy.orm import relationship

from app.third_parties.oracle.base import Base
from app.third_parties.oracle.models.master_data.address import (  # noqa
    AddressCountry
)


class CustomerEconomicProfession(Base):
    __tablename__ = 'crm_cust_economic_profession'

    id = Column('cust_economic_profession_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='ID ngành kinh tế của KHCN')
    code = Column('cust_economic_profession_code', VARCHAR(50), nullable=False, comment='Mã ngành kinh tế của KHCN')
    name = Column('cust_economic_profession_name', VARCHAR(255), nullable=False, comment='Tên ngành kinh tế của KHCN')
    active_flag = Column('cust_economic_profession_active_flag', NUMBER(1, 0, False), nullable=False,
                         comment='Trạng thái hoạt động')
    order_no = Column('order_no', NUMBER(3, 0, False), comment='Sắp xếp')


class CustomerClassification(Base):
    __tablename__ = 'crm_cust_classification'

    id = Column('cust_classification_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='ID phân hạng khách hàng')
    country_id = Column(ForeignKey('crm_address_country.country_id'), nullable=False,
                        comment='ID quốc gia (nhiều ngôn ngữ)')
    code = Column('cust_classification_code', VARCHAR(50), nullable=False, comment='Mã phân hạng khách hàng')
    name = Column('cust_classification_name', VARCHAR(255), nullable=False, comment='Tên phân hạng khách hàng')
    active_flag = Column('cust_classification_active_flag', NUMBER(1, 0, False), nullable=False,
                         comment='Trạng thái hoạt động')
    order_no = Column('order_no', NUMBER(3, 0, False), comment='Sắp xếp')

    country = relationship('AddressCountry')


class CustomerType(Base):
    __tablename__ = 'crm_cust_type'

    id = Column('cust_type_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='ID loại khách hàng')
    code = Column('cust_type_code', VARCHAR(50), nullable=False, comment='Mã loại khách hàng')
    name = Column('cust_type_name', VARCHAR(255), nullable=False, comment='Tên loại khách hàng')
    active_flag = Column('cust_type_active_flag', NUMBER(1, 0, False), nullable=False, comment='Trạng thái hoạt động')
    order_no = Column(NUMBER(3, 0, False), comment='Sắp xếp')


class CustomerCategory(Base):
    __tablename__ = 'crm_cust_category'

    id = Column('cust_category_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='ID đối tượng khách hàng')
    country_id = Column(ForeignKey('crm_address_country.country_id'), nullable=False,
                        comment='ID quốc gia (nhiều ngôn ngữ)')
    code = Column('cust_category_code', VARCHAR(50), nullable=False, comment='Mã đối tượng khách hàng')
    name = Column('cust_category_name', VARCHAR(255), nullable=False, comment='Tên đối tượng khách hàng')
    active_flag = Column('cust_category_active_flag', NUMBER(1, 0, False), nullable=False,
                         comment='Trạng thái hoạt động')
    order_no = Column(NUMBER(3, 0, False), comment='Sắp xếp')

    country = relationship('AddressCountry')


class CustomerStatus(Base):
    __tablename__ = 'crm_customer_status'

    id = Column('cust_status_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='ID trạng thái khách hàng')
    code = Column('cust_status_code', VARCHAR(50), nullable=False, comment='Mã code trạng thái khách hàng')
    name = Column('cust_status_name', VARCHAR(255), nullable=False, comment='Tên trạng thái khách hàng')
    active_flag = Column('cust_status_active_flag', NUMBER(1, 0, False), nullable=False, comment='Trạng thái')
    order_no = Column(NUMBER(3, 0, False), comment='Sắp xếp')
    created_at = Column(DateTime, comment='Thời gian tạo')
    updated_at = Column(DateTime, comment='Thời gian chỉnh sửa')


class CustomerGender(Base):
    __tablename__ = 'crm_cust_gender'

    id = Column('cust_gender_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='ID giới tính')
    country_id = Column(ForeignKey('crm_address_country.country_id'), nullable=False,
                        comment='ID quốc gia (nhiều ngôn ngữ')
    code = Column('cust_gender_code', VARCHAR(50), nullable=False, comment='Mã giới tính')
    name = Column('cust_gender_name', VARCHAR(255), nullable=False, comment='Tên giới tính')
    active_flag = Column('cust_gender_active_flag', NUMBER(1, 0, False), nullable=False, comment='Trạng thái hoạt động')
    order_no = Column(NUMBER(3, 0, False), comment='Sắp xếp')

    country = relationship('AddressCountry')


class CustomerTitle(Base):
    __tablename__ = 'crm_cust_title'

    id = Column('cust_title_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='ID chức danh xưng hô')
    country_id = Column(ForeignKey('crm_address_country.country_id'), nullable=False,
                        comment='ID quốc gia (nhiều ngôn ngữ)')
    code = Column('cust_title_code', VARCHAR(50), nullable=False, comment='Mã chức danh xưng hô')
    name = Column('cust_title_name', VARCHAR(255), nullable=False, comment='Tên chức danh xưng hô')
    active_flag = Column('cust_title_active_flag', NUMBER(1, 3, True), nullable=False, comment='Trạng thái hoạt động')
    order_no = Column(NUMBER(3, 0, False), comment='Sắp xếp')

    country = relationship('AddressCountry')


class CustomerContactType(Base):
    __tablename__ = 'crm_cust_contact_type'
    __table_args__ = {'comment': 'LOẠI LIÊN HỆ'}

    id = Column('cust_contact_type_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='(PK)  Mã loại dữ liệu liên hệ')
    country_id = Column(ForeignKey('crm_address_country.country_id'), comment='(FK)  Mã quốc gia')
    group = Column('cust_contact_type_group', VARCHAR(255))
    name = Column('cust_contact_type_name', VARCHAR(255), comment='Tên loại liên hệ')
    description = Column('cust_contact_type_description', VARCHAR(500), comment='Mô tả loại  liệu liên hệ')

    country = relationship('AddressCountry')


class CustomerRelationshipType(Base):
    __tablename__ = 'crm_cust_relationship_type'
    __table_args__ = {'comment': 'Loại mối quan hệ khách hàng'}

    id = Column('cust_relationship_type_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='(PK) Mã loại mối quan hệ khách hàng')
    country_id = Column(ForeignKey('crm_address_country.country_id'), nullable=False, comment='(FK) Mã quốc gia')
    code = Column('cust_relationship_type_code', VARCHAR(50), nullable=False,
                  comment='Mã code loại mối quan hệ khách hàng')
    name = Column('cust_relationship_type_name', VARCHAR(255), nullable=False,
                  comment='Tên loại mối quan hệ khách hàng')
    active_flag = Column('cust_relationship_type_active_flag', NUMBER(1, 2, True),
                         comment='Trạng thái hoạt động (Có/không)')
    order_no = Column(NUMBER(3, 2, True), comment='Sắp xếp')

    country = relationship('AddressCountry')
