from sqlalchemy import VARCHAR, Column, text
from sqlalchemy.dialects.oracle import NUMBER

from app.third_parties.oracle.models.base import Base


class EBankingNotification(Base):
    __tablename__ = 'crm_eb_notification'
    __table_args__ = {'comment': 'Danh mục tùy chọn thông báo:\n\n  1. Tất toán tài khoản\n  2. Biến động số dư'}

    id = Column('eb_notify_id', VARCHAR(36), primary_key=True, comment='ID chính')
    code = Column('eb_notify_code', VARCHAR(10), nullable=False, comment='Mã code')
    type = Column('eb_notify_type', VARCHAR(10), nullable=False, comment='Loại danh mục')
    name = Column('eb_notify_name', VARCHAR(100), nullable=False, comment='Tên')
    active_flag = Column('eb_notify_active_flag', NUMBER(1, 0, False), comment='Trạng thái')
    order_no = Column(NUMBER(4, 2, True), comment='Sắp xếp')


class EBankingQuestion(Base):
    __tablename__ = 'crm_eb_question'
    __table_args__ = {'comment': 'Danh sách câu hỏi'}

    id = Column('eb_question_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "), comment='ID chính')
    code = Column('eb_question_code', VARCHAR(10), comment='Mã code')
    type = Column('eb_question_type', VARCHAR(10), comment='Loại câu hỏi')
    content = Column('eb_question_content', VARCHAR(100), comment='Nội dung câu hỏi')
    active_flag = Column('eb_active_flag', NUMBER(1, 2, True), comment='Trạng thái')
    order_no = Column('eb_order_no', NUMBER(4, 2, True), comment='Sắp xếp')
