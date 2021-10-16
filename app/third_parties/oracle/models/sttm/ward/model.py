from sqlalchemy import CHAR, CLOB, VARCHAR, Column, DateTime, Float
from sqlalchemy.dialects.oracle import NUMBER

from app.third_parties.oracle.models.utils import Base


class Ward(Base):
    __tablename__ = 'los_sttm_ward'

    ward_code = Column("WARD_CODE", VARCHAR(6), primary_key=True)

    description = Column("DESCRIPTION", VARCHAR(105))

    province_code = Column("PROVINCE_CODE", VARCHAR(6))

    district_code = Column("DISTRICT_CODE", VARCHAR(6))

    area = Column("AREA", VARCHAR(40))

    zip_code = Column("ZIP_CODE", VARCHAR(40))

    record_stat = Column("RECORD_STAT", CHAR(1))

    auth_stat = Column("AUTH_STAT", CHAR(1))

    once_auth = Column("ONCE_AUTH", CHAR(1))

    mod_no = Column("MOD_NO", NUMBER(4, 0, False))

    maker_id = Column("MAKER_ID", VARCHAR(12))

    maker_dt_stamp = Column("MAKER_DT_STAMP", DateTime)

    checker_id = Column("CHECKER_ID", VARCHAR(12))

    checker_dt_stamp = Column("CHECKER_DT_STAMP", DateTime)

    geojson = Column('GEOJSON', CLOB)

    geom_area = Column('GEOM_AREA', Float)
