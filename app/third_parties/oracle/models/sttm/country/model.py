from sqlalchemy import VARCHAR, Column

from app.third_parties.oracle.models.utils import Base


class Country(Base):
    __tablename__ = 'los_sttm_country'

    country_code = Column("COUNTRY_CODE", VARCHAR(3), primary_key=True)

    description = Column("DESCRIPTION", VARCHAR(105))
