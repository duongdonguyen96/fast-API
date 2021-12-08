from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import cx_Oracle
from app.settings.database import ORACLE_CONFIG

DATABASE_URL = "oracle+cx_oracle://{username}:{password}@{host}:{port}/?service_name={service_name}".format_map({
    'host': ORACLE_CONFIG['host'],
    'port': ORACLE_CONFIG['port'],
    'username': ORACLE_CONFIG['username'],
    'password': ORACLE_CONFIG['password'],
    'service_name': ORACLE_CONFIG['service_name']
})

cx_Oracle.init_oracle_client(lib_dir=r"D:\Users\tait\Downloads\instantclient-basic-windows.x64-19.13.0.0.0dbru\instantclient_19_13",
                             config_dir=r"D:\Users\tait\Downloads\instantclient-basic-windows.x64-19.13.0.0.0dbru\instantclient_19_13")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
metadata = Base.metadata
