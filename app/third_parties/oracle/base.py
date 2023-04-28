from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import VARCHAR, Column, DateTime, text
from sqlalchemy.dialects.oracle import NUMBER
from app.settings.database import DB_CONFIG
from app.utils.functions import now


DATABASE_URL = URL.create(
    drivername="mysql+mysqlconnector",
    username=DB_CONFIG['user_name'],
    password=DB_CONFIG['password'],
    host=DB_CONFIG['host'],
    port=DB_CONFIG['port'],
    database=DB_CONFIG['service_name']
)

engine = create_engine(
    DATABASE_URL,
    pool_size=DB_CONFIG['pool_size'],
    pool_recycle=DB_CONFIG['pool_recycle']
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class CustomBaseModel:
    id = Column(VARCHAR(32), primary_key=True, server_default=text("sys_guid()"), comment='Mã gen tự động')
    update_by = Column(VARCHAR(32), server_default=text("sys_guid()"))
    create_by = Column(VARCHAR(32), server_default=text("sys_guid()"))
    date_create = Column(DateTime, comment='ngày tạo', default=now())
    date_update = Column(DateTime, comment='ngày cập nhật cuối cùng')
    is_active = Column(NUMBER(1,0), default=1, comment='trạng thái hoạt động')
