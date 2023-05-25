"""db connection and access functions

"""
from pathlib import Path

from sqlalchemy import create_engine, text, Engine
from sqlalchemy.engine import URL

from jormungand.core.config import config
from jormungand.core.logging import get_logger

logger = get_logger(__name__)

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
    
