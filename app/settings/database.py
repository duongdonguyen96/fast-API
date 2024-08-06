import os

DB_CONFIG = {
    "host": os.getenv("HOST"),
    "port": os.getenv("PORT", 3306),
    "user_name": os.getenv("USER_NAME"),
    "password": os.getenv("PASSWORD"),
    "service_name": os.getenv("SERVICE_NAME"),
    "pool_size": int(os.getenv("POOL_SIZE", 30)),
    "pool_recycle": int(os.getenv("POOL_RECYCLE", 3600))
}
