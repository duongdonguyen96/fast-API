from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.settings.database import ORACLE_CONFIG

DATABASE_URL = "oracle+cx_oracle://{username}:{password}@{host}:{port}/?service_name={service_name}".format_map({
    'host': ORACLE_CONFIG['host'],
    'port': ORACLE_CONFIG['port'],
    'username': ORACLE_CONFIG['username'],
    'password': ORACLE_CONFIG['password'],
    'service_name': ORACLE_CONFIG['service_name']
})

engine = create_engine(
    DATABASE_URL,
    poolclass=NullPool
)
Session = sessionmaker(
    engine,
    expire_on_commit=False
)


def oracle_session():
    """Provide a transactional scope around a series of operations."""
    with Session() as session:
        try:
            logger.info("Start session Oracle")
            yield session
        except Exception as ex:
            logger.exception(f"Oracle ex: {ex}")
            session.rollback()
            logger.exception(f"Oracle rollback: {ex}")
        finally:
            logger.info("Oracle close")
            session.close()
