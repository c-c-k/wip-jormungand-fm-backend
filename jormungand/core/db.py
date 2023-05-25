"""db connection and access functions

"""
from pathlib import Path

from sqlalchemy import create_engine, text, Engine
from sqlalchemy.engine import URL

from .config import config
from .logging import get_logger

logger = get_logger(__name__)

_CURRENT_DIR = Path(__file__).parent

_engine: Engine | None = None


def config_sqlalchemy_logging():
    """Configures sqlalchemy logging

    Mostly this just sets the log-level for the sqlalchemy loggers.
    for details see:
    https://docs.sqlalchemy.org/en/20/core/engines.html#dbengine-logging
    :returns: None
    """
    for logger_name in ('engine', 'pool', 'dialects', 'orm'):
        get_logger(f'sqlalchemy.{logger_name}').setLevel(
                    config.logging[f'sqlalchemy.{logger_name}'])


def _init_engine():
    """TODO: Docstring for _init_engine.

    :returns: TODO
    """
    global _engine
    config_sqlalchemy_logging()
    _engine = create_engine(URL.create(**config.database))


def get_db_engine() -> Engine:
    if _engine is None:
        _init_engine()
    return _engine

def init_db():
    with get_db_engine().connect() as conn:
        with _CURRENT_DIR.joinpath('./sql/schema.sql').open() as f:
            query = text(f.read())
            conn.execute(query)
        with _CURRENT_DIR.joinpath('./sql/stored_procedures.sql').open() as f:
            query = text(f.read())
            conn.execute(query)
        conn.commit()
    
