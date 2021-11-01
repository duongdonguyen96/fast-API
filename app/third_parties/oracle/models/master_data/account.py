from sqlalchemy import VARCHAR, Column, text
from sqlalchemy.dialects.oracle import NUMBER

from app.third_parties.oracle.models.base import Base


class AccountClass(Base):
    __tablename__ = 'crm_acc_class'
    __table_args__ = {'comment': 'Loại hình tài khoản'}

    id = Column('acc_class_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='Mã Loại hình tài khoản')
    code = Column('acc_class_code', VARCHAR(50), nullable=False, comment='Mã code Loại hình tài khoản')
    name = Column('acc_class_name', VARCHAR(255), nullable=False, comment='Tên Loại hình tài khoản')


class AccountStructureType(Base):
    __tablename__ = 'crm_acc_structure_type'
    __table_args__ = {'comment': 'Loại kết cấu tài khoản'}

    id = Column('acc_structure_type_', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='Mã loại kết cấu tài khoản')
    parent_id = Column('acc_structure_type_parent_id', VARCHAR(36), comment='Mã cấp cha loại kết cấu tài khoản')
    code = Column('acc_structure_type_code', VARCHAR(50), comment='Mã code loại kết cấu tài khoản')
    name = Column('acc_structure_type_name', VARCHAR(255), comment='Tên loại kết cấu tài khoản')
    value = Column('acc_structure_type_value', VARCHAR(16), comment='Giá trị loại kết cấu tài khoản')
    level = Column('acc_structure_type_level', NUMBER(8, 2, True), comment='Mức độ loại kết cấu tài khoản')
    active_flag = Column('acc_structure_type_active_flag', NUMBER(1, 2, True), comment='Cờ loại kết cấu tài khoản')


class AccountType(Base):
    __tablename__ = 'crm_acc_type'
    __table_args__ = {'comment': 'Loại nhóm sản phẩm (gói) tài khoản'}

    id = Column('acc_type_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='Mã Loại nhóm sản phẩm (gói) tài khoản')
    code = Column('acc_type_code', VARCHAR(50), comment='Mã code Loại nhóm sản phẩm (gói) tài khoản')
    name = Column('acc_type_name', VARCHAR(255), comment='Tên Loại nhóm sản phẩm (gói) tài khoản')
