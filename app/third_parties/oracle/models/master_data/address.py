from sqlalchemy import VARCHAR, CheckConstraint, Column, ForeignKey, Text, text
from sqlalchemy.dialects.oracle import NUMBER
from sqlalchemy.orm import relationship

from app.third_parties.oracle.base import Base


class AddressCountry(Base):
    __tablename__ = 'crm_address_country'
    __table_args__ = (
        CheckConstraint('COUNTRY_GEOGRAPHIC_COORDINATES IS JSON'),
    )

    id = Column('country_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "), comment='ID quốc gia')
    code = Column('country_code', VARCHAR(50), nullable=False, comment='Mã quốc gia')
    name = Column('country_name', VARCHAR(255), nullable=False, comment='Tên quốc gia')
    geographic_coordinates = Column('country_geographic_coordinates', Text, nullable=False,
                                    comment='Tọa độ địa lý quốc gia')
    flag_url = Column('country_flag_url', VARCHAR(500), comment='Đường dẫn tới cờ quốc gia')
    active_flag = Column('country_active_flag', NUMBER(1, 0, False), nullable=False, comment='Trạng thái hoạt động')
    order_no = Column(NUMBER(3, 0, False), comment='Sắp xếp')


class AddressProvince(Base):
    __tablename__ = 'crm_address_province'
    __table_args__ = (
        CheckConstraint('PROVINCE_GEOGRAPHIC_COORDINATES IS JSON'),
    )

    id = Column('province_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='ID tỉnh/thành')
    country_id = Column(ForeignKey('crm_address_country.country_id'), nullable=False, comment='ID quốc gia')
    code = Column('province_code', VARCHAR(50), nullable=False, comment='Mã tỉnh/thành')
    name = Column('province_name', VARCHAR(255), nullable=False, comment='Tên tỉnh/thành')
    geographic_coordinates = Column('province_geographic_coordinates', Text, nullable=False,
                                    comment='Tọa độ địa lý tỉnh/thaành')
    active_flag = Column('province_active_flag', NUMBER(1, 0, False), nullable=False, comment='Trạng thái hoạt động')
    order_no = Column(NUMBER(3, 0, False), comment='Sắp xếp')

    country = relationship('CrmAddressCountry')


class AddressDistrict(Base):
    __tablename__ = 'crm_address_district'
    __table_args__ = (
        CheckConstraint('DISTRICT_GEOGRAPHIC_COORDINATES IS JSON'),
    )

    id = Column('district_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='ID quận/huyện')
    province_id = Column(ForeignKey('crm_address_province.province_id'), nullable=False, comment='ID tỉnh/thành')
    code = Column('district_code', VARCHAR(50), nullable=False, comment='Mã quận/huyện')
    name = Column('district_name', VARCHAR(255), nullable=False, comment='Tên quận/huyện')
    geographic_coordinates = Column('district_geographic_coordinates', Text, nullable=False,
                                    comment='Tọa độ địa lý quận huyện')
    active_flag = Column('district_active_flag', NUMBER(1, 0, False), nullable=False, comment='Trạng thái hoạt động')
    order_no = Column(NUMBER(3, 0, False), comment='Sắp xếp')

    province = relationship('CrmAddressProvince')


class AddressWard(Base):
    __tablename__ = 'crm_address_ward'
    __table_args__ = (
        CheckConstraint('WARD_GEOGRAPHIC_COORDINATES IS JSON'),
    )

    id = Column('ward_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "), comment='ID phường/xã')
    district_id = Column(ForeignKey('crm_address_district.district_id'), nullable=False, comment='ID quận/huyện')
    code = Column('ward_code', VARCHAR(50), nullable=False, comment='Mã phường/xã')
    name = Column('ward_name', VARCHAR(255), nullable=False, comment='Tên phường/xã')
    geographic_coordinates = Column('ward_geographic_coordinates', Text, nullable=False,
                                    comment='Tọa độ địa lý phường/xã')
    active_flag = Column('ward_active_flag', NUMBER(1, 0, False), nullable=False, comment='Trạng thái hoạt động')
    order_no = Column(NUMBER(3, 0, False), comment='Sắp xếp')

    district = relationship('CrmAddressDistrict')


class AddressType(Base):
    __tablename__ = 'crm_address_type'

    id = Column('address_type_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='ID loại địa chỉ')
    code = Column('address_type_code', VARCHAR(50), nullable=False, comment='Mã loại địa chỉ')
    name = Column('address_type_name', VARCHAR(255), nullable=False, comment='Tên loại địa chỉ')
    active_flag = Column('address_type_active_flag', NUMBER(1, 0, False), nullable=False,
                         comment='Trạng thái hoạt động')
    order_no = Column(NUMBER(3, 0, False), comment='Sắp xếp')
