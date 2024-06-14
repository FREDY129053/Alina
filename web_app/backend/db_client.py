from pymongo import MongoClient

import config_db

client = MongoClient(
    f"mongodb://{config_db.MONGO_HOST}:{config_db.MONGO_PORT}"
)
db = client[config_db.MONGO_DB]