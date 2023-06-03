"""
TODO: DOC: tests/utils/temp_db.py
"""

import contextlib
from logging import getLogger
from random import randint

from sqlalchemy import create_engine, Engine, text
from sqlalchemy.engine import URL
from sqlalchemy.exc import OperationalError

from jormungand.core.config import config

logger = getLogger(__name__)

_cleanup_db_engine: Engine | None = None


def _init_cleanup_db_engine():
    global _cleanup_db_engine
    _cleanup_db_engine = create_engine(
        URL.create(
            database=config['cleanup_database_name'], **config['test_db']),
        isolation_level='AUTOCOMMIT')


@contextlib.contextmanager
def create_temp_db_engine():
    if _cleanup_db_engine is None:
        _init_cleanup_db_engine()
    with _cleanup_db_engine.begin() as conn:
        create_attempts = 1
        max_create_attempts = 5
        while True:
            try:
                temp_db_name = f"tempdb_{randint(0,65535)}"
                conn.execute(text(f'CREATE DATABASE {temp_db_name};'))
            except OperationalError:
                if create_attempts <= max_create_attempts:
                    logger.error(
                        "failed to create temporary database with name:"
                        f" {temp_db_name} "
                        f", attempt {create_attempts}/{max_create_attempts}"
                    )
                    continue
                logger.error(
                    "failed to create temporary database with name:"
                    f" {temp_db_name} failed {max_create_attempts}"
                    " attempts, aborting!"
                )
                raise
            else:
                break
        engine_ = create_engine(
            URL.create(database=temp_db_name, **config['test_db']),
            echo=False, echo_pool=False)
        yield engine_
        engine_.dispose()
        conn.execute(
                text(f'DROP DATABASE IF EXISTS {temp_db_name} (FORCE);'),
                )
