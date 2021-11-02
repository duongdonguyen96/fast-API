from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.settings.database import ORACLE_CONFIG

DATABASE_URL = "oracle+cx_oracle://{username}:{password}@{host}:{port}/?service_name={service_name}".format_map({
    'host': ORACLE_CONFIG['host'],
    'port': ORACLE_CONFIG['port'],
    'username': ORACLE_CONFIG['username'],
    'password': ORACLE_CONFIG['password'],
    'service_name': ORACLE_CONFIG['service_name']
})

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
metadata = Base.metadata
