import motor.motor_asyncio

from app.settings.database import MONGO_CONFIG

DATABASE_URL = 'mongodb://{username}:{password}@{host}:{port}/{database}'.format_map(
    {
        'host': MONGO_CONFIG['host'],
        'port': MONGO_CONFIG['port'],
        'username': MONGO_CONFIG['username'],
        'password': MONGO_CONFIG['password'],
        'database': MONGO_CONFIG['database'],
    }
)
mongo_connect = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URL)
mongo_db = mongo_connect[MONGO_CONFIG['database']]
