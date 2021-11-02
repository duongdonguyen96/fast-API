from sqlalchemy import VARCHAR, Column, DateTime, ForeignKey, text
from sqlalchemy.dialects.oracle import NUMBER
from sqlalchemy.orm import relationship

from app.third_parties.oracle.base import Base


class DebitCard(Base):
    __tablename__ = 'CRM_DEBIT_CARD '
    __table_args__ = {'comment': 'THẺ Ghi nợ'}

    id = Column('card_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "), comment='Mã thẻ (PK)')
    customer_id = Column(ForeignKey('crm_customer.customer_id'), comment='Mã khách hàng')
    card_type_id = Column(ForeignKey('crm_card_type.card_type_id'), comment='Mã Đối tượng khách hàng')
    card_issuance_type_id = Column(ForeignKey('crm_card_issuance_type.card_issuance_type_id'),
                                   comment='Mã nơi phát hành Đối tượng khách hàng')
    cust_type_id = Column(ForeignKey('crm_cust_type.cust_type_id'), comment=' Mã loại khách hàng')
    brand_of_card_id = Column(ForeignKey('crm_brand_of_card.brand_of_card_id'),
                              comment='Mã thương hiệu thẻ (Visa, master)')
    card_issuance_fee_id = Column(ForeignKey('crm_card_issuance_fee.card_issuance_fee_id'),
                                  comment='Mã Phí phát hành thẻ')
    card_delivery_address_id = Column(ForeignKey('crm_card_delivery_address.card_delivery_address_id'),
                                      comment='Mã địa chỉ giao nhận thẻv(PK)')
    parent_card_id = Column(ForeignKey('CRM_DEBIT_CARD .card_id'), comment='Mã thẻ cấp cha')
    card_registration_flag = Column(NUMBER(1, 2, True), comment='Trạng thái đk thẻ')
    payment_online_flag = Column(NUMBER(1, 2, True), comment='Trạng thái thanh toán')
    first_name_on_card = Column(VARCHAR(21), comment='Họ in trên thẻ')
    middle_name_on_card = Column(VARCHAR(21), comment='Tên đệm in trên thẻ')
    last_name_on_card = Column(VARCHAR(21), comment='Tên in trên thẻ')
    card_delivery_address_flag = Column(NUMBER(1, 2, True),
                                        comment='Trạng thái địa chỉ giao thẻ (0: giao tại đơn vị SCB, 1: địa chỉ tùy chọn)')
    created_at = Column(DateTime, comment='ngày tạo')
    active_flag = Column(NUMBER(1, 2, True), comment='Trạng thái hoạt động (Có/không)')

    brand_of_card = relationship('CrmBrandOfCard')
    card_delivery_address = relationship('CrmCardDeliveryAddres')
    card_issuance_fee = relationship('CrmCardIssuanceFee')
    card_issuance_type = relationship('CrmCardIssuanceType')
    card_type = relationship('CrmCardType')
    cust_type = relationship('CrmCustType')
    customer = relationship('CrmCustomer')
    parent_card = relationship('CRMDEBITCARD', remote_side=[id])


class CrmCardDeliveryAddres(Base):
    __tablename__ = 'crm_card_delivery_address'
    __table_args__ = {'comment': 'Địa chỉ giao nhận thẻ'}

    card_delivery_address_id = Column(VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                                      comment='Mã địa chỉ giao nhận thẻv(PK)')
    branch_id = Column(ForeignKey('crm_branch.branch_id'), nullable=False, comment='Mã đơn vị (FK)')
    province_id = Column(ForeignKey('crm_address_province.province_id'), nullable=False, comment='Mã tỉnh (FK)')
    district_id = Column(ForeignKey('crm_address_district.district_id'), nullable=False,
                         comment='Mã Thông tin quận huyện (FK)')
    ward_id = Column(ForeignKey('crm_address_ward.ward_id'), nullable=False, comment='Mã Thông tin xã phường (FK)')
    card_delivery_address_address = Column(VARCHAR(500), nullable=False, comment='Địa chỉ')
    card_delivery_address_note = Column(VARCHAR(500), comment='Ghi chú')

    branch = relationship('CrmBranch')
    district = relationship('CrmAddressDistrict')
    province = relationship('CrmAddressProvince')
    ward = relationship('CrmAddressWard')
