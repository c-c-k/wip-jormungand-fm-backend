"""db connection and access functions

TODO: better documentation for db module
TODO: error handling
"""
import contextlib
from pathlib import Path

from sqlalchemy import create_engine, text, Engine
from sqlalchemy.engine import URL

from .config import config
from .logging import get_logger, load_logging_configuration

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
    load_logging_configuration(config.logging.sqlalchemy)
    # for logger_name in ('engine', 'pool', 'dialects', 'orm'):
    #     get_logger(f'sqlalchemy.{logger_name}').setLevel(
    #                 config.logging)


def _init_engine():
    """TODO: Docstring for _init_engine.

    :returns: TODO
    """
    global _engine
    config_sqlalchemy_logging()
    _engine = create_engine(URL.create(**config.database))


def get_engine() -> Engine:
    """TODO: Docstring for get_engine.

    :returns: TODO
    """
    if _engine is None:
        _init_engine()
    return _engine


@contextlib.contextmanager
def get_connection(begin_once: bool = True):
    """Get an sqlalchemy database connection

    transaction context:
        - begin once: implicitly commit at end of context
        - normal: commit only on explicit calls to commit()
    :begin_mode: True (default) for begin once transaction context,
                 False for normal transaction context.
    :returns: A database connection that should usually be used
              for a transaction context
              (i.e. ``with get_engine as conn:...``)
    """
    if begin_once:
        connection = get_connection().begin
    else:
        connection = get_connection().connect
    try:
        with connection as conn:
            yield conn
    except Exception:
        raise
    finally:
        pass
