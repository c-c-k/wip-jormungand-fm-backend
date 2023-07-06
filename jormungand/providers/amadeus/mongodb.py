import pymongo

from jormungand.core.config import config
from jormungand.core.logging import get_logger

logger = get_logger(__name__)

_client = None
_db = None


def get_client() -> pymongo.MongoClient:
    global _client
    if _client is None:
        _client = pymongo.MongoClient(
                **config["databases.mongodb.client_params"])
    return _client


def get_db() -> pymongo.database.Database:
    global _db, _client
    if _db is None:
        _db = get_client[config["databases.mongodb.database"]]
    return _db
