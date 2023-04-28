import os

DB_CONFIG = {
    "host": os.getenv("HOST"),
    "port": os.getenv("PORT"),
    "user_name": os.getenv("USER_NAME"),
    "password": os.getenv("PASSWORD"),
    "service_name": os.getenv("SERVICE_NAME"),
    # 'pool_size': os.getenv("POOL_SIZE"),
    # 'pool_recycle': os.getenv("POOL_RECYCLE")
}
