"""db connection and access functions

"""

from sqlalchemy import create_engine

from config import settings
from jormungand.logging_manager import LoggingManager

logger = LoggingManager.get_logger(__name__)

_engine = None


def _init_engine():
    global _engine
    _engine = create_engine(settings['db_uri'])


def get_engine():
    if _engine is None:
        _init_engine()
    return _engine
