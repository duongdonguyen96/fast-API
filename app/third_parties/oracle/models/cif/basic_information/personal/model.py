from sqlalchemy import VARCHAR, Column, DateTime, ForeignKey
from sqlalchemy.dialects.oracle import NUMBER
from sqlalchemy.orm import relationship

from app.third_parties.oracle.base import Base
from app.third_parties.oracle.models.cif.basic_information.fatca.model import (  # noqa
    CustomerFatca
)
from app.third_parties.oracle.models.master_data.address import (  # noqa
    AddressCountry, AddressProvince
)
from app.third_parties.oracle.models.master_data.customer import (  # noqa
    CustomerGender, CustomerTitle
)
from app.third_parties.oracle.models.master_data.others import (  # noqa
    MaritalStatus, Nation, Religion, ResidentStatus
)


class CustomerIndividualInfo(Base):
    __tablename__ = 'crm_cust_individual_info'

    customer_id = Column(ForeignKey('crm_customer.customer_id'), primary_key=True, comment='Mã khách hàng')
    gender_id = Column(ForeignKey('crm_cust_gender.cust_gender_id'), nullable=False, comment='Mã giới tính')
    title_id = Column(ForeignKey('crm_cust_title.cust_title_id'), nullable=False,
                      comment='Mã Danh xưng khách hàng (ông, bà, ...)')
    place_of_birth_id = Column(ForeignKey('crm_address_province.province_id'), nullable=False,
                               comment='Mã nơi sinh (theo tỉnh/thành)')
    country_of_birth_id = Column(ForeignKey('crm_address_country.country_id'), nullable=False,
                                 comment='Mã quốc gia sinh')
    resident_status_id = Column(ForeignKey('crm_resident_status.resident_status_id'), nullable=False,
                                comment='Mã tình trạng cư trú')
    customer_fatca_id = Column(ForeignKey('crm_cust_fatca.cust_fatca_id'), nullable=False,
                               comment='Mã MAPPING KH - FATCA')
    religion_id = Column(ForeignKey('crm_religion.religion_id'), nullable=False, comment='Mã tôn giáo')
    nation_id = Column(ForeignKey('crm_nation.nation_id'), nullable=False, comment='Mã dân tộc')
    marital_status_id = Column(ForeignKey('crm_marital_status.marital_status_id'), nullable=False,
                               comment='Mã tình trạng hôn nhân')
    date_of_birth = Column(DateTime, nullable=False, comment='Ngày sinh')
    under_15_year_old_flag = Column(NUMBER(1, 0, False), nullable=False, comment='Trạng thái dưới 15 tuổi')
    guardian_flag = Column(NUMBER(1, 0, False), nullable=False, comment='Cờ có người giám hộ không')
    identifying_characteristics = Column(VARCHAR(1000), comment='Đặc điểm nhận dạng')
    father_full_name = Column(VARCHAR(100), comment='Họ tên Cha')
    mother_full_name = Column(VARCHAR(100), comment='Họ tên Mẹ')

    country_of_birth = relationship('AddressCountry')
    customer_fatca = relationship('CustomerFatca')
    customer_gender = relationship('CustomerGender')
    marital_status = relationship('MaritalStatus')
    nation = relationship('Nation')
    place_of_birth = relationship('AddressProvince')
    religion = relationship('Religion')
    resident_status = relationship('ResidentStatus')
    customer_title = relationship('CustomerTitle')
