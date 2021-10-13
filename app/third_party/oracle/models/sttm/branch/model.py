from sqlalchemy import VARCHAR, Column

from app.third_party.oracle.models.utils import Base


class Branch(Base):
    __tablename__ = 'los_sttm_branch'
    __table_args__ = {'comment': 'Danh sách các chi nhánh SCB'}

    branch_code = Column("BRANCH_CODE", VARCHAR(3), primary_key=True)

    branch_name = Column("BRANCH_NAME", VARCHAR(105))

    branch_addr1 = Column("BRANCH_ADDR1", VARCHAR(105))

    branch_addr2 = Column("BRANCH_ADDR2", VARCHAR(105))

    branch_addr3 = Column("BRANCH_ADDR3", VARCHAR(105))

    parent_branch = Column("PARENT_BRANCH", VARCHAR(3))

    regional_office = Column("REGIONAL_OFFICE", VARCHAR(3))

    walkin_customer = Column("WALKIN_CUSTOMER", VARCHAR(9))
