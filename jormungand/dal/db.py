"""db connection and access functions

"""
from pathlib import Path

from sqlalchemy import create_engine, text, Engine
from sqlalchemy.engine import URL

from jormungand.utils.config import config
from jormungand.logging_manager import LoggingManager

logger = LoggingManager.get_logger(__name__)

_CURRENT_DIR = Path(__file__).parent

_engine: Engine | None = None


def _init_engine():
    global _engine
    _engine = create_engine(
            URL.create(**config['database']),
            echo=config.get('db_echo', False))


def get_db_engine() -> Engine:
    if _engine is None:
        _init_engine()
    return _engine

def init_db():
    with get_db_engine().connect() as conn:
        with _CURRENT_DIR.joinpath('schema.sql').open() as f:
            query = text(f.read())
            conn.execute(query)
        with _CURRENT_DIR.joinpath('stored_procedures.sql').open() as f:
            query = text(f.read())
            conn.execute(query)
        conn.commit()
    
